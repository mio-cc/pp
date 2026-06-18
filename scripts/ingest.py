#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语 / 卷分阶段注入接口 —— AI 供稿的唯一推荐入口。

为什么用它
    手改 data/raw/terms_seed.csv 极易出错：列错位、含逗号字段未转义、漏填必填、
    definition 复读术语名、越级自造顶层分类、term_uid 重复。本工具在「写入之前」做
        ① 格式校验（JSON Schema：schema/term.schema.json、schema/volume.schema.json）
        ② 业务规则校验（顶层分类∈config、UID 格式/唯一、同卷中文名唯一、定义非复读非占位）
        ③ 查重检测（新增项与库内近似项比对）
    三关全过才写入、重建、再校验。其他模型只需按模版产出 JSON，不必接触 CSV。

用法
    python scripts/ingest.py check      <terms.json>    # 只校验术语，不写库（建议先跑）
    python scripts/ingest.py add-terms  <terms.json>    # 校验通过 → 追加 CSV → 重建 → 校验
    python scripts/ingest.py add-volume <volume.json>   # 校验通过 → 写 config/volumes.json → 重建

三种填充场景都走 add-terms（区别只在 category 怎么写）
    · 给「已有分支」加原子术语：category 写到已存在的叶子路径，例 "曝光控制 / 快门速度"。
    · 给「已有卷」加新分支：category 写一条更深的新路径，首段仍须是该卷在 config 里的顶层分类。
    · 加「全新卷」：先 add-volume 注册卷与其顶层分类，再 add-terms 填该卷术语。

terms.json：术语对象数组，见 docs/templates/term.template.json（多值用数组，不要写分号；
            term_uid 可留空，工具按该卷现有最大号 +1 自动分配）。
volume.json：单个卷对象，见 docs/templates/volume.template.json。
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "volumes.json"
CSV_PATH = ROOT / "data" / "raw" / "terms_seed.csv"
TERM_SCHEMA = ROOT / "schema" / "term.schema.json"
VOLUME_SCHEMA = ROOT / "schema" / "volume.schema.json"

CSV_FIELDS = ["term_uid", "zh_term", "en_term", "aliases", "volume_code", "category",
              "definition_long", "visual_effect", "prompt_usage", "use_cases",
              "related_terms", "confused_with", "tags", "source_refs", "status", "version"]
ARRAY_FIELDS = ["aliases", "use_cases", "related_terms", "confused_with", "tags"]
PLACEHOLDER_PAT = re.compile(r"待补充|TODO|TBD|简短定义|占位")
NEAR_DUP_RATIO = 0.86


def fail(msg: str) -> None:
    print(f"\n✗ {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"找不到文件：{path}")
    except json.JSONDecodeError as e:
        fail(f"JSON 解析失败 {path}：第 {e.lineno} 行 {e.msg}")


def get_validator(schema_path: Path):
    try:
        import jsonschema
    except ImportError:
        fail("缺少依赖 jsonschema。请先运行：pip install jsonschema --break-system-packages")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return jsonschema.Draft7Validator(schema)


def read_csv_rows() -> list[dict]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(s: str) -> str:
    return re.sub(r"[。.；;，,、\s]+$", "", (s or "").strip())


def run(cmd: list[str]) -> int:
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(ROOT)).returncode


# ---------------------------------------------------------------- terms
def validate_terms(objs, config, existing):
    """返回 (errors, warnings, prepared_rows)。errors 非空则禁止写入。"""
    if not isinstance(objs, list):
        fail("terms.json 顶层必须是数组 [ ... ]，每个元素是一条术语对象。")
    declared = {v["code"]: set(v.get("categories", [])) for v in config["volumes"]}
    valid_codes = set(declared)
    validator = get_validator(TERM_SCHEMA)

    errors, warnings, prepared = [], [], []
    seen_uid = set(existing["uids"])
    seen_zh = {k: set(v) for k, v in existing["zh_by_vol"].items()}
    next_no = dict(existing["max_no"])  # volume -> 当前最大序号

    for i, obj in enumerate(objs):
        tag = f"[第{i+1}条 {obj.get('zh_term','?') if isinstance(obj, dict) else '?'}]"
        # ① 格式
        schema_errs = sorted(validator.iter_errors(obj), key=lambda e: e.path)
        if schema_errs:
            for e in schema_errs:
                loc = ".".join(str(p) for p in e.path) or "(根)"
                errors.append(f"{tag} 字段 {loc}：{e.message}")
            continue
        vol = obj["volume_code"]
        # ② 业务
        if vol not in valid_codes:
            errors.append(f"{tag} volume_code={vol} 未在 config/volumes.json 注册。先 add-volume 或改用已有卷。")
            continue
        segs = [s.strip() for s in obj["category"].split(" / ")]
        if any(not s for s in segs):
            errors.append(f"{tag} category 含空段：{obj['category']!r}。用 ' / ' 分隔，不能有空层。")
        top = segs[0]
        if top not in declared[vol]:
            errors.append(f"{tag} 顶层分类 {top!r} 不在 {vol} 的 config 声明里。"
                          f"该卷允许的顶层：{sorted(declared[vol])}。要么改用其一，要么先在 config 增补。")
        if norm(obj["definition_long"]) == norm(obj["zh_term"]):
            errors.append(f"{tag} definition_long 不能复读术语名，必须是真实解释。")
        if PLACEHOLDER_PAT.search(obj["definition_long"]):
            errors.append(f"{tag} definition_long 含占位词（待补充/TODO 等），必须写真实定义。")
        # UID
        uid = (obj.get("term_uid") or "").strip()
        if uid:
            if uid in seen_uid:
                errors.append(f"{tag} term_uid={uid} 已存在或在本批重复。留空可自动分配。")
            elif uid[:3] != vol:
                errors.append(f"{tag} term_uid 前缀 {uid[:3]} 与 volume_code {vol} 不一致。")
            else:
                seen_uid.add(uid)
                try:
                    next_no[vol] = max(next_no.get(vol, 0), int(uid[5:]))
                except ValueError:
                    pass
        # 同卷中文名唯一
        zh = obj["zh_term"].strip()
        volzh = seen_zh.setdefault(vol, set())
        if zh in volzh:
            errors.append(f"{tag} 同卷已存在中文名 {zh!r}（term 不可重复）。")
        else:
            # ③ 近似查重（警告）
            for ex in volzh:
                if SequenceMatcher(None, zh, ex).ratio() >= NEAR_DUP_RATIO:
                    warnings.append(f"{tag} 中文名 {zh!r} 与已有 {ex!r} 高度相似，确认不是重复再加。")
                    break
            volzh.add(zh)
        prepared.append(obj)

    # 自动分配空 UID
    for obj in prepared:
        if not (obj.get("term_uid") or "").strip():
            vol = obj["volume_code"]
            next_no[vol] = next_no.get(vol, 0) + 1
            obj["term_uid"] = f"{vol}_T{next_no[vol]:04d}"
    return errors, warnings, prepared


def to_csv_row(obj) -> dict:
    row = {}
    for f in CSV_FIELDS:
        v = obj.get(f, "")
        if f in ARRAY_FIELDS:
            row[f] = ";".join(x.strip() for x in (v or []) if x.strip())
        else:
            row[f] = (v if v not in (None,) else "")
    if not row.get("source_refs"):
        row["source_refs"] = "整理"
    if not row.get("status"):
        row["status"] = "published"
    if not row.get("version"):
        row["version"] = "V1.0"
    return row


def existing_index(rows):
    uids, zh_by_vol, max_no = set(), {}, {}
    for r in rows:
        uid = (r.get("term_uid") or "").strip()
        vol = (r.get("volume_code") or "").strip()
        if uid:
            uids.add(uid)
            if uid[:3] == vol:
                try:
                    max_no[vol] = max(max_no.get(vol, 0), int(uid[5:]))
                except ValueError:
                    pass
        zh_by_vol.setdefault(vol, set()).add((r.get("zh_term") or "").strip())
    return {"uids": uids, "zh_by_vol": zh_by_vol, "max_no": max_no}


def cmd_terms(path, write):
    config = load_json(CONFIG_PATH)
    objs = load_json(path)
    rows = read_csv_rows()
    errors, warnings, prepared = validate_terms(objs, config, existing_index(rows))

    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"\n✗ 校验未通过，{len(errors)} 个错误，未写入任何数据：")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"\n✓ 校验通过：{len(prepared)} 条术语合规" + (f"（{len(warnings)} 条警告，见上）" if warnings else ""))
    for o in prepared:
        print(f"    {o['term_uid']}  {o['zh_term']} / {o['en_term']}  ←  {o['volume_code']} · {o['category']}")
    if not write:
        print("\n（check 模式：未写入。确认无误后改用 add-terms 入库。）")
        return

    new_rows = rows + [to_csv_row(o) for o in prepared]
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(new_rows)
    print(f"\n✓ 已写入 CSV（{len(rows)} → {len(new_rows)} 行）。重建中…")
    if run([sys.executable, "-B", "scripts/rebuild.py"]) != 0:
        fail("重建失败，请检查。")
    if run([sys.executable, "-B", "scripts/validate_kb.py"]) != 0:
        fail("重建后校验未通过，请检查。")
    print("\n✓ 完成：术语已入库并通过校验。")


# ---------------------------------------------------------------- volume
def cmd_volume(path):
    config = load_json(CONFIG_PATH)
    obj = load_json(path)
    validator = get_validator(VOLUME_SCHEMA)
    errs = sorted(validator.iter_errors(obj), key=lambda e: e.path)
    if errs:
        print("✗ 卷对象格式校验未通过：")
        for e in errs:
            loc = ".".join(str(p) for p in e.path) or "(根)"
            print(f"  - 字段 {loc}：{e.message}")
        sys.exit(1)
    codes = {v["code"] for v in config["volumes"]}
    seqs = {v["sequence"] for v in config["volumes"]}
    if obj["code"] in codes:
        fail(f"卷代码 {obj['code']} 已存在，请用未占用的（现有：{sorted(codes)}）。")
    if obj["sequence"] in seqs:
        fail(f"sequence={obj['sequence']} 已被占用（现有：{sorted(seqs)}）。")
    config["volumes"].append(obj)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 已注册新卷 {obj['code']} {obj['title']}，顶层分类：{obj['categories']}")
    print("  重建中…")
    if run([sys.executable, "-B", "scripts/rebuild.py"]) != 0:
        fail("重建失败。")
    print("✓ 完成：新卷已注册。现在可以用 add-terms 给它填术语了。")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in {"check", "add-terms", "add-volume"}:
        print(__doc__)
        sys.exit(0 if len(sys.argv) <= 1 else 2)
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == "check":
        cmd_terms(path, write=False)
    elif cmd == "add-terms":
        cmd_terms(path, write=True)
    elif cmd == "add-volume":
        cmd_volume(path)


if __name__ == "__main__":
    main()

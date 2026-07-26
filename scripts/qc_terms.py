#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""填充质量抽检（只读，不写库、不改代码）。

对应 docs/fill-discipline.md 第三节「质量门槛」与第四节「定时检测」。
按章程门槛扫描 SQLite 主库，输出达标率与不达标 term_uid 清单，用于：
  - 每 5 批 / 每切一卷时定时检测新增术语质量；
  - 定位存量注水条目，交由 update-terms 回填修正。

用法：
    python scripts/qc_terms.py            # 全量扫描
    python scripts/qc_terms.py --since V04_T0111   # 只统计该 uid 及之后新增的
    python scripts/qc_terms.py --vol V04   # 只看某卷

门槛（与章程一致）：
    definition_long ≥ 40 字
    visual_effect   ≥ 15 字
    prompt_usage    ≥ 15 字
    en_term         须为正常英文（非中文、≥2 字）
    definition      非套话
    volume_code     须在 config/volumes.json 注册
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
CFG = ROOT / "config" / "volumes.json"

DEF_MIN = 40
VE_MIN = 15
PU_MIN = 15
VAGUE = re.compile(
    r"^(这是|常用于|一种|指代|指).{0,6}(术语|高频|常见|概念|词)$"
    r"|(适用于|用于).{0,4}(场景|各种|多种|情况)$"
    r"|(视觉效果?好|画面效果好|提升画质)$"
)


def L(s) -> str:
    return (s or "").strip()


def parse_uid(uid):
    """V04_T0111 -> ('V04', 111)；解析失败返回 (None, -1)。"""
    m = re.match(r"^(V\d{2})_T(\d{4})$", uid or "")
    if not m:
        return None, -1
    return m.group(1), int(m.group(2))


def load_rows(vol_filter=None, since_uid=None):
    if not DB.exists():
        raise SystemExit(f"✗ 主库不存在：{DB}")
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    sql = (
        "SELECT t.term_uid, t.zh_term, t.en_term, t.definition_long, "
        "t.visual_effect, t.prompt_usage, v.code AS vol "
        "FROM terms t JOIN volumes v ON v.id = t.volume_id"
    )
    if vol_filter:
        sql += " WHERE v.code = ?"
        rows = conn.execute(sql, (vol_filter,)).fetchall()
    else:
        rows = conn.execute(sql).fetchall()
    conn.close()
    # since_uid 按「同卷 + 数字序号下界」精确过滤（term_uid 是字符串，不能直接字符串比较）
    if since_uid:
        s_vol, s_no = parse_uid(since_uid)
        if s_vol is None:
            raise SystemExit(f"✗ --since 格式应为 V04_T0111，收到：{since_uid}")

        def seq_of(uid):
            m = re.match(r"^V\d{2}_T(\d{4})$", uid or "")
            return int(m.group(1)) if m else -1

        rows = [r for r in rows if r["vol"] == s_vol and seq_of(r["term_uid"]) >= s_no]
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description="填充质量抽检（只读）")
    ap.add_argument("--vol", help="只看某卷，如 V04")
    ap.add_argument("--since", help="只统计该 term_uid 及之后新增的，如 V04_T0111")
    args = ap.parse_args()

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    valid_codes = {v["code"] for v in cfg["volumes"]}

    rows = load_rows(vol_filter=args.vol, since_uid=args.since)
    n = len(rows)

    bad_def = []
    bad_def30 = []
    bad_ve = []
    bad_pu = []
    bad_en = []
    vague_def = []
    bad_vol = []
    for r in rows:
        d = L(r["definition_long"])
        e = L(r["en_term"])
        v = L(r["visual_effect"])
        p = L(r["prompt_usage"])
        uid, zh = r["term_uid"], r["zh_term"]
        if len(d) < DEF_MIN:
            bad_def.append((uid, zh, len(d)))
        if len(d) < 30:
            bad_def30.append((uid, zh, len(d)))
        if len(v) < VE_MIN:
            bad_ve.append((uid, zh, len(v)))
        if len(p) < PU_MIN:
            bad_pu.append((uid, zh, len(p)))
        if len(e) < 2 or re.search(r"[一-鿿]", e):
            bad_en.append((uid, zh, e[:20]))
        if VAGUE.search(d):
            vague_def.append((uid, zh, d[:30]))
        if r["vol"] not in valid_codes:
            bad_vol.append((uid, r["vol"]))

    scope = f"（vol={args.vol}）" if args.vol else (f"（since={args.since}）" if args.since else "（全量）")
    print(f"术语数{scope}: {n}")
    print(f"合法卷数(config): {len(valid_codes)}")
    print()
    print("=== 达标率（按 docs/fill-discipline.md 门槛）===")
    print(f"  definition_long ≥40字 : {n-len(bad_def)}/{n}  ({100*(n-len(bad_def))/max(n,1):.1f}%)")
    print(f"  definition_long ≥30字 : {n-len(bad_def30)}/{n}  ({100*(n-len(bad_def30))/max(n,1):.1f}%)")
    print(f"  visual_effect   ≥15字 : {n-len(bad_ve)}/{n}  ({100*(n-len(bad_ve))/max(n,1):.1f}%)")
    print(f"  prompt_usage    ≥15字 : {n-len(bad_pu)}/{n}  ({100*(n-len(bad_pu))/max(n,1):.1f}%)")
    print(f"  en_term 正常          : {n-len(bad_en)}/{n}  ({100*(n-len(bad_en))/max(n,1):.1f}%)")
    print(f"  definition 非套话      : {n-len(vague_def)}/{n}  ({100*(n-len(vague_def))/max(n,1):.1f}%)")
    print(f"  volume_code 合法       : {n-len(bad_vol)}/{n}")
    print()

    def grp(title, lst, show=30):
        print(f"--- {title}: {len(lst)} 条（前 {show}）---")
        for uid, zh, *rest in lst[:show]:
            extra = f"  [{rest[0]}]" if rest else ""
            print(f"    {uid}  {zh}{extra}")
        if len(lst) > show:
            print(f"    … 其余 {len(lst)-show} 条")
        print()

    grp("definition <40字", bad_def)
    grp("visual_effect <15字", bad_ve)
    grp("prompt_usage <15字", bad_pu)
    grp("en_term 异常(含中文/过短)", bad_en)
    grp("definition 套话", vague_def)
    grp("volume_code 不合法", bad_vol)


if __name__ == "__main__":
    main()

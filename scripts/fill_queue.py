"""填充工单 —— 找出最缺内容的卷与空分支，生成可直接交给 AI 的供稿工单。

用法：
    python scripts/fill_queue.py                     # 优先级榜（人看）
    python scripts/fill_queue.py --json              # 机器可读队列
    python scripts/fill_queue.py --order V36 --count 30
        # 生成 V36 的供稿工单（含契约要点/顶层白名单/现有词避重表），
        # 把输出直接投喂给 AI，AI 产出 terms.json 后走
        # POST /api/ingest/check → python scripts/ingest.py add-terms 入库。

优先级 = 卷缺口比例（1 - 现有/目标）；卷内空分类排最前。
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
CONFIG = ROOT / "config" / "volumes.json"


def load() -> tuple[list[dict], dict]:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    vols = conn.execute(
        """
        SELECT v.code, v.title, v.target_terms, v.purpose, COUNT(t.id) AS current
        FROM volumes v LEFT JOIN terms t ON t.volume_id = v.id
        GROUP BY v.id ORDER BY v.sequence_no
        """
    ).fetchall()
    cats = conn.execute(
        """
        SELECT v.code AS vcode, c.name, COUNT(t.id) AS n
        FROM categories c JOIN volumes v ON v.id = c.volume_id
        LEFT JOIN terms t ON t.category_id = c.id
        GROUP BY c.id ORDER BY v.sequence_no, c.sort_order
        """
    ).fetchall()
    conn.close()
    cats_by_vol: dict[str, list] = {}
    for r in cats:
        cats_by_vol.setdefault(r["vcode"], []).append({"path": r["name"], "count": r["n"]})
    queue = []
    for v in vols:
        target = v["target_terms"] or 0
        gap = max(0, target - v["current"])
        vcats = cats_by_vol.get(v["code"], [])
        queue.append({
            "code": v["code"], "title": v["title"], "purpose": v["purpose"] or "",
            "current": v["current"], "target": target, "gap": gap,
            "gap_ratio": round(gap / target, 3) if target else 0.0,
            "empty_branches": [c["path"] for c in vcats if c["count"] == 0],
            "thin_branches": [c for c in vcats if 0 < c["count"] < 8],
        })
    queue.sort(key=lambda x: (-x["gap_ratio"], -x["gap"]))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    return queue, config


def print_board(queue: list[dict]) -> None:
    print(f"{'卷':<5} {'标题':<14} {'现有/目标':>11} {'缺口':>6}  空分类")
    for q in queue:
        empties = "、".join(q["empty_branches"][:4]) + ("…" if len(q["empty_branches"]) > 4 else "")
        print(f"{q['code']:<5} {q['title']:<14} {q['current']:>5}/{q['target']:<5} {q['gap']:>6}  {empties or '-'}")


def make_order(queue: list[dict], config: dict, code: str, count: int, branch: str | None) -> str:
    q = next((x for x in queue if x["code"] == code), None)
    if not q:
        sys.exit(f"未知卷 {code}")
    cfg_vol = next((v for v in config["volumes"] if v["code"] == code), {})
    tops = cfg_vol.get("categories", [])

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    existing = conn.execute(
        """
        SELECT t.zh_term, c.name AS category FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE v.code = ? ORDER BY c.name, t.term_uid
        """,
        (code,),
    ).fetchall()
    conn.close()

    target_desc = f"分支 {branch!r}" if branch else (
        "空分类（按下面列表依次填）" if q["empty_branches"] else "薄弱分支加深"
    )
    lines = [
        f"# 供稿工单 — {code} {q['title']}",
        "",
        f"卷用途：{q['purpose']}",
        f"进度：{q['current']} / {q['target']}（缺口 {q['gap']}）。本单目标：新增 {count} 条。",
        f"填充目标：{target_desc}",
        "",
        "## 顶层分类白名单（category 首段必须取自这里）",
        "、".join(tops) or "（config 未声明）",
        "",
        "## 空分类（优先填这些；可在其下自由加更深分支）",
        "\n".join("- " + b for b in q["empty_branches"]) or "（无）",
        "",
        "## 已有术语（避免重复；同卷 zh_term 必须唯一）",
        "\n".join(f"- {r['zh_term']}  ←  {r['category']}" for r in existing[:400]) or "（本卷为空）",
        "",
        "## 供稿要求（契约摘要，完整规则见 GET /api/contract）",
        "1. 输出 JSON 数组，每条含：zh_term、en_term、volume_code、category、definition_long、",
        "   visual_effect、prompt_usage、use_cases[]、tags[]、status='published'、version='V1.0'；",
        "   可选 aliases[]、related_terms[]、confused_with[]。term_uid 留空由系统分配。",
        "2. 名字即提示词：zh_term/en_term 必须原子、具体、可直接粘进绘图工具；",
        "   笼统词（如“发型”“颜色”）是分支名不是术语。",
        f"3. category 用 ' / ' 分隔、深度不限，首段 ∈ 上述白名单，volume_code='{code}'。",
        "4. definition_long 100–200 字真实解释，禁止复读名字、禁止占位词。",
        "5. 同一最深分支下的术语互为可选项（互斥），如同为发型的不同具体款式。",
        "",
        "## 提交流程",
        "生成 terms.json → POST /api/ingest/check 在线校验（含语义近重警告）→",
        "python scripts/ingest.py add-terms terms.json 入库。",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="输出机器可读队列")
    ap.add_argument("--order", metavar="VXX", help="生成指定卷的供稿工单")
    ap.add_argument("--branch", help="限定工单目标分支路径")
    ap.add_argument("--count", type=int, default=30, help="工单目标条数")
    args = ap.parse_args()

    if not DB.exists():
        sys.exit("主库不存在，先运行 python scripts/build_kb.py")
    queue, config = load()

    if args.order:
        print(make_order(queue, config, args.order, args.count, args.branch))
    elif args.json:
        print(json.dumps(queue, ensure_ascii=False, indent=2))
    else:
        print_board(queue)


if __name__ == "__main__":
    main()

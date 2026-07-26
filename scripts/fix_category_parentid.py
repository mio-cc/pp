"""
幂等 parent_id 递归建链脚本
==========================
将 categories 表里形如 "顶层 / 中间 / ... / 叶子" 的扁平命名行拆成多级父子链：

  · 顶层（无 " / "）：来自 config 注册，parent_id=NULL，是树的根
  · 中间层（路径某前缀，例 "A / B"）：若不存在则按稳定 slug 插入，
    parent_id 指向上一层；若已存在则只补 parent_id（幂等）
  · 叶子（完整路径行）：把原有扁平行的 parent_id 链到倒数第二层

支持任意层数。幂等安全：仅处理 parent_id IS NULL 的命名行；
中间节点用 (volume_id, name) 复用，避免重复插入；slug 形如
"vNN-mid-{slugify(中间路径)}-{序号}" 全卷唯一。

直接改 SQLite 主库（唯一可接受的特例：name 已落库但 parent_id 未连线）。

用法：
    python scripts/fix_category_parentid.py            # 执行建链
    python scripts/fix_category_parentid.py --dry-run  # 只打印不改库
"""
from __future__ import annotations
import argparse
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
BACKUP = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite.bak-fix-parentid"


def slugify(value: str) -> str:
    """与 build_kb.slugify 保持一致的轻量实现，确保 slug 稳定可复算。"""
    import re
    v = value.strip().lower()
    v = re.sub(r"\s+", "-", v)
    v = re.sub(r"[^a-z0-9\-_.]+", "", v)
    v = v.strip("-_.")
    return v or "mid"


def top_lookup(conn: sqlite3.Connection) -> dict[tuple[int, str], int]:
    """(volume_id, top_name) -> top_id  仅顶层（不含 ' / '）"""
    rows = conn.execute(
        "SELECT id, volume_id, name FROM categories WHERE name NOT LIKE '% / %'"
    ).fetchall()
    return {(vid, name): cid for cid, vid, name in rows}


def next_sort(conn: sqlite3.Connection, vid: int) -> int:
    row = conn.execute(
        "SELECT COALESCE(MAX(sort_order), 0) FROM categories WHERE volume_id=?", (vid,)
    ).fetchone()
    return int(row[0] or 0) + 1


def fix(dry_run: bool) -> int:
    if not DB.exists():
        print(f"[ERR] 主库不存在: {DB}")
        return 2
    if not dry_run:
        shutil.copy2(DB, BACKUP)
        print(f"[BACKUP] {BACKUP}")

    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        tops = top_lookup(conn)
        sub_rows = conn.execute(
            "SELECT id, volume_id, name FROM categories "
            "WHERE name LIKE '% / %' AND parent_id IS NULL "
            "ORDER BY volume_id, sort_order, id"
        ).fetchall()
        missing: list[tuple[int, int, str]] = []
        chained = 0           # 已链 parent_id 的扁平叶子数
        mid_inserted = 0      # 新插入的中间层节点数
        mid_reused = 0        # 复用已存在的中间层节点次数
        mid_slug_collisions = 0

        conn.execute("BEGIN")
        for cid, vid, name in sub_rows:
            segs = [s.strip() for s in name.split(" / ")]
            if len(segs) < 2:
                continue  # 防御：含 / 但首段/末段为空理论上被 ingest 拦截
            top_id = tops.get((vid, segs[0]))
            if top_id is None:
                missing.append((cid, vid, name))
                continue

            cur_parent_id = top_id
            path = segs[0]
            # i = 1..N-1：最后一段是叶子（本行），其余段是中间层
            for i in range(1, len(segs)):
                path = f"{path} / {segs[i]}"
                if i == len(segs) - 1:
                    # 叶子段：直接链本扁平行
                    conn.execute(
                        "UPDATE categories SET parent_id=? WHERE id=? AND parent_id IS NULL",
                        (cur_parent_id, cid),
                    )
                    chained += 1
                else:
                    # 中间层段：复用或插入
                    mid = conn.execute(
                        "SELECT id FROM categories WHERE volume_id=? AND name=?",
                        (vid, path),
                    ).fetchone()
                    if mid is None:
                        slug = f"v{vid}-mid-{slugify(path)}"
                        # slug 唯一约束可能冲突（同卷多中间层 slugify 后撞名）→ 兜底加序号
                        dup = conn.execute(
                            "SELECT 1 FROM categories WHERE volume_id=? AND slug=?",
                            (vid, slug),
                        ).fetchone()
                        if dup:
                            slug = f"{slug}-{next_sort(conn, vid):02d}"
                            mid_slug_collisions += 1
                        cur = conn.execute(
                            "INSERT INTO categories(volume_id, name, slug, parent_id, sort_order) "
                            "VALUES(?,?,?,?,?)",
                            (vid, path, slug, cur_parent_id, next_sort(conn, vid)),
                        )
                        cur_parent_id = cur.lastrowid
                        mid_inserted += 1
                    else:
                        # 已存在 → 仅在 parent_id 仍空时补链，保持幂等
                        conn.execute(
                            "UPDATE categories SET parent_id=? WHERE id=? AND parent_id IS NULL",
                            (cur_parent_id, mid[0]),
                        )
                        cur_parent_id = mid[0]
                        mid_reused += 1

        if dry_run:
            conn.execute("ROLLBACK")
            print(f"[DRY] 将链 {chained} 条扁平叶子；"
                  f"插入 {mid_inserted} 条中间层节点；复用 {mid_reused} 次；"
                  f"slug 冲突兜底 {mid_slug_collisions} 次")
        else:
            conn.execute("COMMIT")
            print(f"[OK] 已链 {chained} 条扁平叶子 parent_id；"
                  f"新建 {mid_inserted} 条中间层节点；复用 {mid_reused} 次；"
                  f"slug 冲突兜底 {mid_slug_collisions} 次")
        if missing:
            print(f"[WARN] {len(missing)} 条找不到匹配顶层(跳过):")
            for cid, vid, name in missing[:20]:
                print(f"   id={cid} vol={vid} name={name}")
            if len(missing) > 20:
                print(f"   ...及另外 {len(missing) - 20} 条")
        conn.close()
        return 0 if (chained or dry_run) else 1
    except Exception as e:
        conn.execute("ROLLBACK")
        conn.close()
        if not dry_run:
            shutil.copy2(BACKUP, DB)  # 失败时还原主库
            print(f"[ROLLBACK] 已还原主库：{e}")
        else:
            print(f"[ERR] dry-run 失败：{e}")
        return 3


def main() -> int:
    ap = argparse.ArgumentParser(description="递归建链 categories.parent_id（任意层数）")
    ap.add_argument("--dry-run", action="store_true", help="只打印不写库")
    args = ap.parse_args()
    return fix(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
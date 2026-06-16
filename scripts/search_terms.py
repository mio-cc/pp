from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"


def like_query(conn: sqlite3.Connection, query: str, limit: int) -> list[sqlite3.Row]:
    pattern = f"%{query}%"
    return conn.execute(
        """
        SELECT DISTINCT
            t.term_uid,
            t.zh_term,
            t.en_term,
            v.code AS volume_code,
            v.title AS volume_title,
            c.name AS category,
            t.definition_short
        FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        LEFT JOIN term_aliases a ON a.term_id = t.id
        LEFT JOIN term_chunks tc ON tc.term_id = t.id
        WHERE
            t.zh_term LIKE ?
            OR t.en_term LIKE ?
            OR a.alias LIKE ?
            OR t.definition_short LIKE ?
            OR t.definition_long LIKE ?
            OR t.prompt_usage LIKE ?
            OR tc.content LIKE ?
        ORDER BY v.sequence_no, t.term_uid
        LIMIT ?
        """,
        (pattern, pattern, pattern, pattern, pattern, pattern, pattern, limit),
    ).fetchall()


def fts_query(conn: sqlite3.Connection, query: str, limit: int) -> list[str]:
    # FTS5 is strongest for Latin tokens here. Chinese substring recall is covered by LIKE.
    try:
        rows = conn.execute(
            """
            SELECT term_uid
            FROM terms_fts
            WHERE terms_fts MATCH ?
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
    except sqlite3.Error:
        return []
    return [row[0] for row in rows]


def rows_by_uids(conn: sqlite3.Connection, uids: list[str]) -> list[sqlite3.Row]:
    if not uids:
        return []
    placeholders = ",".join("?" for _ in uids)
    rows = conn.execute(
        f"""
        SELECT
            t.term_uid,
            t.zh_term,
            t.en_term,
            v.code AS volume_code,
            v.title AS volume_title,
            c.name AS category,
            t.definition_short
        FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.term_uid IN ({placeholders})
        """,
        uids,
    ).fetchall()
    by_uid = {row["term_uid"]: row for row in rows}
    return [by_uid[uid] for uid in uids if uid in by_uid]


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python scripts/search_terms.py "关键词" [limit]')
        return 2
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        print("Run: python scripts/build_kb.py")
        return 1

    query = sys.argv[1].strip()
    limit = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows: list[sqlite3.Row] = []
        seen: set[str] = set()
        for row in rows_by_uids(conn, fts_query(conn, query, limit)):
            rows.append(row)
            seen.add(row["term_uid"])
        for row in like_query(conn, query, limit):
            if row["term_uid"] not in seen:
                rows.append(row)
                seen.add(row["term_uid"])
            if len(rows) >= limit:
                break
    finally:
        conn.close()

    if not rows:
        print(f"No terms found for: {query}")
        return 0

    for index, row in enumerate(rows, start=1):
        english = f" / {row['en_term']}" if row["en_term"] else ""
        print(f"{index}. [{row['term_uid']}] {row['zh_term']}{english}")
        print(f"   {row['volume_code']} {row['volume_title']} > {row['category'] or '未分类'}")
        print(f"   {row['definition_short']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


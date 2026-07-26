"""构建术语向量表 —— 写入主库 term_vectors 与 vector_meta。

用法：
    python scripts/build_vectors.py

在 rebuild 之后运行（或由 rebuild.py 自动调用）。零依赖，2 千条 <1s，
10 万条约 1 分钟；再大规模时换 sqlite-vec/FAISS，接口不变。
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import textvec

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"


def main() -> None:
    if not DB.exists():
        print("✗ 主库不存在，先运行 python scripts/build_kb.py", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT t.id, t.term_uid, t.zh_term, t.en_term, t.definition_long,
               COALESCE((SELECT GROUP_CONCAT(alias, ' ') FROM term_aliases a WHERE a.term_id = t.id), '') AS aliases
        FROM terms t
        """
    ).fetchall()

    all_counts = []
    for r in rows:
        text = textvec.term_text(r["zh_term"], r["en_term"] or "", r["definition_long"] or "", r["aliases"])
        all_counts.append(textvec.raw_counts(text))
    idf = textvec.build_idf(all_counts)

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS term_vectors (
            term_id INTEGER PRIMARY KEY REFERENCES terms(id) ON DELETE CASCADE,
            vec BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS vector_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        DELETE FROM term_vectors;
        """
    )
    for r, counts in zip(rows, all_counts):
        vec = textvec.finalize(counts, idf)
        conn.execute("INSERT INTO term_vectors(term_id, vec) VALUES (?, ?)", (r["id"], textvec.pack(vec)))
    conn.execute(
        "INSERT OR REPLACE INTO vector_meta(key, value) VALUES ('idf', ?), ('dim', ?), ('count', ?)",
        (json.dumps(idf), str(textvec.DIM), str(len(rows))),
    )
    conn.commit()
    conn.close()
    print(f"✓ 已写入 {len(rows)} 条术语向量（dim={textvec.DIM}，含 IDF）→ term_vectors")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import json
import re
import shutil
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "volumes.json"
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
EXPORT_DIR = ROOT / "data" / "exports"
WEB_EXPORT_DIR = EXPORT_DIR / "web"
GENERATED_TERMS_DIR = ROOT / "generated" / "terms"
SCHEMA_FILES = [
    ROOT / "schema" / "001_initial_schema.sql",
    ROOT / "schema" / "002_search_indexes.sql",
]

LIST_SEPARATOR = ";"
VALID_STATUSES = {"draft", "review", "published", "deprecated"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def split_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(LIST_SEPARATOR) if item.strip()]


def slugify(value: str, fallback: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9\-_.]+", "", value)
    value = value.strip("-_.")
    return value or fallback


def safe_filename(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\r\n\t]+', "_", value)
    value = re.sub(r"\s+", "_", value.strip())
    return value[:120] or "untitled"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _clear_dir_contents(directory: Path) -> None:
    """清空目录内容但保留目录本身。
    某些受限挂载环境（如工作区 mount）禁止 rmdir，删整个目录会报 PermissionError，
    因此逐项删除内容、保留目录，确保跨环境都能重建。"""
    if not directory.exists():
        return
    for child in directory.iterdir():
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
            if child.exists():  # rmtree 被禁止时，回退为清空子目录内容
                _clear_dir_contents(child)
        else:
            try:
                child.unlink()
            except OSError:
                pass


def reset_outputs() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    WEB_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_TERMS_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    _clear_dir_contents(GENERATED_TERMS_DIR)


def init_schema(conn: sqlite3.Connection) -> None:
    for schema_file in SCHEMA_FILES:
        conn.executescript(schema_file.read_text(encoding="utf-8"))


def sync_volumes(conn: sqlite3.Connection, config: dict) -> dict[str, int]:
    volume_ids: dict[str, int] = {}
    for volume in config["volumes"]:
        cur = conn.execute(
            """
            INSERT INTO volumes (code, title, sequence_no, target_terms, purpose, status)
            VALUES (?, ?, ?, ?, ?, 'active')
            """,
            (
                volume["code"],
                volume["title"],
                volume["sequence"],
                volume["target_terms"],
                volume.get("purpose", ""),
            ),
        )
        volume_id = int(cur.lastrowid)
        volume_ids[volume["code"]] = volume_id

        for index, category in enumerate(volume.get("categories", []), start=1):
            slug = f"{volume['code'].lower()}-c{index:02d}-{slugify(category, f'category-{index:02d}')}"
            conn.execute(
                """
                INSERT INTO categories (volume_id, name, slug, sort_order)
                VALUES (?, ?, ?, ?)
                """,
                (volume_id, category, slug, index),
            )

    for edge in config.get("cross_volume_edges", []):
        source_id = volume_ids[edge["source"]]
        target_id = volume_ids[edge["target"]]
        conn.execute(
            """
            INSERT INTO volume_relations (
                source_volume_id, target_volume_id, relation_type, rationale
            )
            VALUES (?, ?, ?, ?)
            """,
            (source_id, target_id, edge["type"], edge.get("rationale", "")),
        )

    return volume_ids


def category_lookup(conn: sqlite3.Connection) -> dict[tuple[str, str], int]:
    rows = conn.execute(
        """
        SELECT v.code, c.name, c.id
        FROM categories c
        JOIN volumes v ON v.id = c.volume_id
        """
    ).fetchall()
    return {(row[0], row[1]): int(row[2]) for row in rows}


def ensure_category(
    conn: sqlite3.Connection,
    lookup: dict[tuple[str, str], int],
    volume_code: str,
    volume_id: int,
    category: str,
) -> int:
    key = (volume_code, category)
    if key in lookup:
        return lookup[key]

    count = conn.execute(
        "SELECT COUNT(*) FROM categories WHERE volume_id = ?", (volume_id,)
    ).fetchone()[0]
    sort_order = int(count) + 1
    slug = f"{volume_code.lower()}-c{sort_order:02d}-{slugify(category, f'category-{sort_order:02d}')}"
    cur = conn.execute(
        """
        INSERT INTO categories (volume_id, name, slug, sort_order)
        VALUES (?, ?, ?, ?)
        """,
        (volume_id, category, slug, sort_order),
    )
    lookup[key] = int(cur.lastrowid)
    return lookup[key]


def insert_tags(conn: sqlite3.Connection, term_id: int, tags: list[str]) -> None:
    for tag in tags:
        conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
        tag_id = conn.execute("SELECT id FROM tags WHERE name = ?", (tag,)).fetchone()[0]
        conn.execute(
            "INSERT OR IGNORE INTO term_tags (term_id, tag_id) VALUES (?, ?)",
            (term_id, tag_id),
        )


def insert_aliases(conn: sqlite3.Connection, term_id: int, aliases: list[str]) -> None:
    for alias in aliases:
        conn.execute(
            """
            INSERT OR IGNORE INTO term_aliases (term_id, alias, language)
            VALUES (?, ?, 'mixed')
            """,
            (term_id, alias),
        )


def insert_label_relations(
    conn: sqlite3.Connection,
    term_id: int,
    relation_type: str,
    labels: list[str],
) -> None:
    for label in labels:
        conn.execute(
            """
            INSERT INTO term_relations (
                source_term_id, relation_type, target_label
            )
            VALUES (?, ?, ?)
            """,
            (term_id, relation_type, label),
        )


def build_chunk_content(row: dict, aliases: list[str], tags: list[str]) -> str:
    lines = [
        f"中文术语：{row['zh_term']}",
        f"英文术语：{row.get('en_term', '')}",
        f"别名：{'; '.join(aliases)}",
        f"卷册：{row['volume_code']}",
        f"分类：{row['category']}",
        f"一句话定义：{row.get('definition_short', '')}",
        f"详细解释：{row.get('definition_long', '')}",
        f"视觉表现：{row.get('visual_effect', '')}",
        f"Prompt 用法：{row.get('prompt_usage', '')}",
        f"正向提示词：{row.get('positive_prompt', '')}",
        f"负向提示词：{row.get('negative_prompt', '')}",
        f"适用场景：{row.get('use_cases', '')}",
        f"标签：{'; '.join(tags)}",
    ]
    return "\n".join(line for line in lines if not line.endswith("："))


def insert_chunks(
    conn: sqlite3.Connection,
    term_id: int,
    term_uid: str,
    row: dict,
    aliases: list[str],
    tags: list[str],
) -> None:
    full_content = build_chunk_content(row, aliases, tags)
    prompt_content = "\n".join(
        [
            f"术语：{row['zh_term']} / {row.get('en_term', '')}",
            f"Prompt 用法：{row.get('prompt_usage', '')}",
            f"正向提示词：{row.get('positive_prompt', '')}",
            f"负向提示词：{row.get('negative_prompt', '')}",
        ]
    )
    chunks = [
        ("full", full_content),
        ("prompt", prompt_content),
    ]
    for chunk_type, content in chunks:
        chunk_uid = f"{term_uid}_{chunk_type}"
        conn.execute(
            """
            INSERT INTO term_chunks (
                chunk_uid, term_id, chunk_type, content, token_hint
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (chunk_uid, term_id, chunk_type, content, max(1, len(content) // 2)),
        )


def import_csv_files(conn: sqlite3.Connection, volume_ids: dict[str, int]) -> tuple[int, int]:
    lookup = category_lookup(conn)
    rows_seen = 0
    rows_imported = 0
    run_id = str(uuid.uuid4())
    started_at = utc_now()
    source_paths = []

    for csv_path in sorted(RAW_DIR.glob("*.csv")):
        source_paths.append(str(csv_path.relative_to(ROOT)))
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows_seen += 1
                row = {key: (value or "").strip() for key, value in row.items()}
                if not row.get("term_uid") or not row.get("zh_term"):
                    continue
                volume_code = row["volume_code"]
                if volume_code not in volume_ids:
                    raise ValueError(f"Unknown volume_code {volume_code!r} in {csv_path}")
                status = row.get("status") or "draft"
                if status not in VALID_STATUSES:
                    raise ValueError(f"Invalid status {status!r} for {row['term_uid']}")

                volume_id = volume_ids[volume_code]
                category_id = ensure_category(
                    conn,
                    lookup,
                    volume_code,
                    volume_id,
                    row.get("category") or "未分类",
                )
                cur = conn.execute(
                    """
                    INSERT INTO terms (
                        term_uid, zh_term, en_term, volume_id, category_id,
                        definition_short, definition_long, visual_effect,
                        prompt_usage, positive_prompt, negative_prompt,
                        use_cases, source_refs, notes, status, version
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row["term_uid"],
                        row["zh_term"],
                        row.get("en_term", ""),
                        volume_id,
                        category_id,
                        row.get("definition_short", ""),
                        row.get("definition_long", ""),
                        row.get("visual_effect", ""),
                        row.get("prompt_usage", ""),
                        row.get("positive_prompt", ""),
                        row.get("negative_prompt", ""),
                        row.get("use_cases", ""),
                        row.get("source_refs", ""),
                        row.get("notes", ""),
                        status,
                        row.get("version") or "V1.0",
                    ),
                )
                term_id = int(cur.lastrowid)
                aliases = split_list(row.get("aliases"))
                tags = split_list(row.get("tags"))
                insert_aliases(conn, term_id, aliases)
                insert_tags(conn, term_id, tags)
                insert_label_relations(
                    conn, term_id, "related", split_list(row.get("related_terms"))
                )
                insert_label_relations(
                    conn, term_id, "confused_with", split_list(row.get("confused_with"))
                )
                insert_chunks(conn, term_id, row["term_uid"], row, aliases, tags)
                rows_imported += 1

    conn.execute(
        """
        INSERT INTO import_runs (
            run_id, source_path, rows_seen, rows_imported, started_at, finished_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            "; ".join(source_paths),
            rows_seen,
            rows_imported,
            started_at,
            utc_now(),
        ),
    )
    return rows_seen, rows_imported


def rebuild_fts(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM terms_fts")
    rows = conn.execute(
        """
        SELECT
            t.id,
            t.term_uid,
            t.zh_term,
            t.en_term,
            COALESCE(GROUP_CONCAT(a.alias, '; '), '') AS aliases,
            COALESCE(t.definition_short, '') || char(10) ||
            COALESCE(t.definition_long, '') || char(10) ||
            COALESCE(t.visual_effect, '') || char(10) ||
            COALESCE(t.prompt_usage, '') || char(10) ||
            COALESCE(t.positive_prompt, '') || char(10) ||
            COALESCE(t.negative_prompt, '') || char(10) ||
            COALESCE(t.use_cases, '') AS body
        FROM terms t
        LEFT JOIN term_aliases a ON a.term_id = t.id
        GROUP BY t.id
        """
    ).fetchall()
    for row in rows:
        conn.execute(
            """
            INSERT INTO terms_fts (term_uid, zh_term, en_term, aliases, body)
            VALUES (?, ?, ?, ?, ?)
            """,
            (row[1], row[2], row[3], row[4], row[5]),
        )


def export_rag_jsonl(conn: sqlite3.Connection) -> int:
    output_path = EXPORT_DIR / "terms_for_rag.jsonl"
    rows = conn.execute(
        """
        SELECT
            tc.chunk_uid,
            t.term_uid,
            t.zh_term,
            t.en_term,
            v.code AS volume_code,
            v.title AS volume_title,
            c.name AS category,
            tc.chunk_type,
            tc.content,
            t.status,
            t.version
        FROM term_chunks tc
        JOIN terms t ON t.id = tc.term_id
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        ORDER BY v.sequence_no, t.term_uid, tc.chunk_type
        """
    ).fetchall()
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            payload = {
                "chunk_uid": row[0],
                "term_uid": row[1],
                "zh_term": row[2],
                "en_term": row[3],
                "volume_code": row[4],
                "volume_title": row[5],
                "category": row[6],
                "chunk_type": row[7],
                "content": row[8],
                "status": row[9],
                "version": row[10],
            }
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return len(rows)


def export_volume_summary(conn: sqlite3.Connection) -> None:
    output_path = EXPORT_DIR / "volumes_summary.csv"
    rows = conn.execute(
        """
        SELECT
            v.code,
            v.title,
            v.target_terms,
            COUNT(t.id) AS current_terms,
            ROUND(COUNT(t.id) * 100.0 / v.target_terms, 2) AS completion_percent
        FROM volumes v
        LEFT JOIN terms t ON t.volume_id = v.id
        GROUP BY v.id
        ORDER BY v.sequence_no
        """
    ).fetchall()
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["volume_code", "title", "target_terms", "current_terms", "completion_percent"])
        writer.writerows(rows)


def export_terms_catalog(conn: sqlite3.Connection) -> None:
    output_path = EXPORT_DIR / "terms_catalog.csv"
    rows = conn.execute(
        """
        SELECT
            t.term_uid,
            t.zh_term,
            t.en_term,
            v.code,
            v.title,
            c.name,
            t.definition_short,
            t.status,
            t.version
        FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        ORDER BY v.sequence_no, t.term_uid
        """
    ).fetchall()
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "term_uid",
                "zh_term",
                "en_term",
                "volume_code",
                "volume_title",
                "category",
                "definition_short",
                "status",
                "version",
            ]
        )
        writer.writerows(rows)


def export_web_json(conn: sqlite3.Connection) -> int:
    """导出前端离线模式所需的静态 JSON，结构与 FastAPI 返回保持同构。"""
    conn.row_factory = sqlite3.Row

    # 术语全字段（含别名、标签、相关/易混淆术语聚合）
    term_rows = conn.execute(
        """
        SELECT
            t.term_uid,
            t.zh_term,
            t.en_term,
            v.code AS volume_code,
            v.title AS volume_title,
            v.sequence_no AS volume_sequence,
            c.name AS category,
            t.definition_short,
            t.definition_long,
            t.visual_effect,
            t.prompt_usage,
            t.positive_prompt,
            t.negative_prompt,
            t.use_cases,
            t.source_refs,
            t.status,
            t.version,
            COALESCE((SELECT GROUP_CONCAT(alias, ';') FROM term_aliases WHERE term_id = t.id), '') AS aliases,
            COALESCE((
                SELECT GROUP_CONCAT(tags.name, ';')
                FROM term_tags JOIN tags ON tags.id = term_tags.tag_id
                WHERE term_tags.term_id = t.id
            ), '') AS tags,
            COALESCE((
                SELECT GROUP_CONCAT(target_label, ';')
                FROM term_relations
                WHERE source_term_id = t.id AND relation_type = 'related'
            ), '') AS related_terms,
            COALESCE((
                SELECT GROUP_CONCAT(target_label, ';')
                FROM term_relations
                WHERE source_term_id = t.id AND relation_type = 'confused_with'
            ), '') AS confused_with
        FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        ORDER BY v.sequence_no, t.term_uid
        """
    ).fetchall()

    terms = []
    for row in term_rows:
        terms.append(
            {
                "term_uid": row["term_uid"],
                "zh_term": row["zh_term"],
                "en_term": row["en_term"] or "",
                "volume_code": row["volume_code"],
                "volume_title": row["volume_title"],
                "category": row["category"] or "",
                "definition_short": row["definition_short"] or "",
                "definition_long": row["definition_long"] or "",
                "visual_effect": row["visual_effect"] or "",
                "prompt_usage": row["prompt_usage"] or "",
                "positive_prompt": row["positive_prompt"] or "",
                "negative_prompt": row["negative_prompt"] or "",
                "use_cases": split_list(row["use_cases"]),
                "aliases": split_list(row["aliases"]),
                "tags": split_list(row["tags"]),
                "related_terms": split_list(row["related_terms"]),
                "confused_with": split_list(row["confused_with"]),
                "source_refs": row["source_refs"] or "",
                "status": row["status"],
                "version": row["version"],
            }
        )

    # 卷册（含目标量、当前量、分类列表）
    volume_rows = conn.execute(
        """
        SELECT v.code, v.title, v.sequence_no, v.target_terms, v.purpose,
               COUNT(t.id) AS current_terms
        FROM volumes v
        LEFT JOIN terms t ON t.volume_id = v.id
        GROUP BY v.id
        ORDER BY v.sequence_no
        """
    ).fetchall()
    volumes = []
    for vr in volume_rows:
        cats = conn.execute(
            """
            SELECT c.name, COUNT(t.id) AS term_count
            FROM categories c
            LEFT JOIN terms t ON t.category_id = c.id
            WHERE c.volume_id = (SELECT id FROM volumes WHERE code = ?)
            GROUP BY c.id
            ORDER BY c.sort_order
            """,
            (vr["code"],),
        ).fetchall()
        target = vr["target_terms"] or 0
        current = vr["current_terms"] or 0
        volumes.append(
            {
                "code": vr["code"],
                "title": vr["title"],
                "sequence": vr["sequence_no"],
                "target_terms": target,
                "current_terms": current,
                "completion_percent": round(current * 100.0 / target, 2) if target else 0.0,
                "purpose": vr["purpose"] or "",
                "categories": [{"name": c["name"], "term_count": c["term_count"]} for c in cats],
            }
        )

    # 标签云
    tag_rows = conn.execute(
        """
        SELECT tags.name, COUNT(term_tags.term_id) AS term_count
        FROM tags
        LEFT JOIN term_tags ON term_tags.tag_id = tags.id
        GROUP BY tags.id
        ORDER BY term_count DESC, tags.name
        """
    ).fetchall()
    tags = [{"name": r["name"], "term_count": r["term_count"]} for r in tag_rows]

    # 状态分布
    status_rows = conn.execute(
        "SELECT status, COUNT(*) AS c FROM terms GROUP BY status"
    ).fetchall()
    status_counts = {r["status"]: r["c"] for r in status_rows}

    total_terms = len(terms)
    target_total = sum(v["target_terms"] for v in volumes)
    meta = {
        "project": "AI视觉设计与提示词工程百科",
        "version": "V1.0",
        "generated_at": utc_now(),
        "total_terms": total_terms,
        "target_total": target_total,
        "completion_percent": round(total_terms * 100.0 / target_total, 2) if target_total else 0.0,
        "status_counts": status_counts,
        "volumes": volumes,
        "tags": tags,
    }

    (WEB_EXPORT_DIR / "terms.json").write_text(
        json.dumps({"total": total_terms, "items": terms}, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    (WEB_EXPORT_DIR / "volumes.json").write_text(
        json.dumps({"items": volumes}, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    (WEB_EXPORT_DIR / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    return total_terms


def term_markdown(row: sqlite3.Row) -> str:
    aliases = split_list(row["aliases"])
    tags = split_list(row["tags"])
    related_terms = split_list(row["related_terms"])
    confused_with = split_list(row["confused_with"])

    def list_block(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- 暂无"

    return f"""---
term_uid: {row["term_uid"]}
zh_term: {row["zh_term"]}
en_term: {row["en_term"] or ""}
aliases: {json.dumps(aliases, ensure_ascii=False)}
volume_code: {row["volume_code"]}
volume_title: {row["volume_title"]}
category: {row["category"] or ""}
status: {row["status"]}
version: {row["version"]}
---

# {row["zh_term"]}{f' / {row["en_term"]}' if row["en_term"] else ''}

## 一句话定义

{row["definition_short"] or "待补充。"}

## 详细解释

{row["definition_long"] or "待补充。"}

## 视觉表现

{row["visual_effect"] or "待补充。"}

## Prompt 用法

```text
{row["prompt_usage"] or "待补充。"}
```

### 正向提示词

```text
{row["positive_prompt"] or "待补充。"}
```

### 负向提示词

```text
{row["negative_prompt"] or "待补充。"}
```

## 适用场景

{list_block(split_list(row["use_cases"]))}

## 相关术语

{list_block(related_terms)}

## 易混淆术语

{list_block(confused_with)}

## 标签

{list_block(tags)}

## 来源与备注

{row["source_refs"] or "待补充。"}
"""


def export_markdown(conn: sqlite3.Connection) -> int:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT
            t.term_uid,
            t.zh_term,
            t.en_term,
            v.code AS volume_code,
            v.title AS volume_title,
            c.name AS category,
            t.definition_short,
            t.definition_long,
            t.visual_effect,
            t.prompt_usage,
            t.positive_prompt,
            t.negative_prompt,
            t.use_cases,
            t.source_refs,
            t.status,
            t.version,
            COALESCE((SELECT GROUP_CONCAT(alias, ';') FROM term_aliases WHERE term_id = t.id), '') AS aliases,
            COALESCE((
                SELECT GROUP_CONCAT(tags.name, ';')
                FROM term_tags
                JOIN tags ON tags.id = term_tags.tag_id
                WHERE term_tags.term_id = t.id
            ), '') AS tags,
            COALESCE((
                SELECT GROUP_CONCAT(target_label, ';')
                FROM term_relations
                WHERE source_term_id = t.id AND relation_type = 'related'
            ), '') AS related_terms,
            COALESCE((
                SELECT GROUP_CONCAT(target_label, ';')
                FROM term_relations
                WHERE source_term_id = t.id AND relation_type = 'confused_with'
            ), '') AS confused_with
        FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
        ORDER BY v.sequence_no, t.term_uid
        """
    ).fetchall()
    for row in rows:
        volume_dir = GENERATED_TERMS_DIR / f"{row['volume_code']}_{safe_filename(row['volume_title'])}"
        volume_dir.mkdir(parents=True, exist_ok=True)
        filename = safe_filename(f"{row['term_uid']}_{row['zh_term']}") + ".md"
        (volume_dir / filename).write_text(term_markdown(row), encoding="utf-8", newline="\n")
    return len(rows)


def main() -> None:
    reset_outputs()
    config = load_config()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        init_schema(conn)
        volume_ids = sync_volumes(conn, config)
        rows_seen, rows_imported = import_csv_files(conn, volume_ids)
        rebuild_fts(conn)
        rag_chunks = export_rag_jsonl(conn)
        export_volume_summary(conn)
        export_terms_catalog(conn)
        web_terms = export_web_json(conn)
        markdown_count = export_markdown(conn)
        conn.commit()
    finally:
        conn.close()

    print(f"Built knowledge base: {DB_PATH.relative_to(ROOT)}")
    print(f"CSV rows seen: {rows_seen}")
    print(f"Terms imported: {rows_imported}")
    print(f"Markdown pages: {markdown_count}")
    print(f"RAG chunks: {rag_chunks}")
    print(f"Web JSON terms: {web_terms} -> {WEB_EXPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "volumes.json"
DB_PATH = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"


def print_section(title: str) -> None:
    print(f"\n== {title} ==")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    target_total = sum(volume["target_terms"] for volume in config["volumes"])
    if target_total != config["project"]["target_total_terms"]:
        errors.append(
            f"Volume target total {target_total} does not match project target "
            f"{config['project']['target_total_terms']}."
        )

    if not DB_PATH.exists():
        errors.append(f"Database not found: {DB_PATH}")
        print_section("Errors")
        for error in errors:
            print(f"- {error}")
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        term_count = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
        volume_count = conn.execute("SELECT COUNT(*) FROM volumes").fetchone()[0]

        duplicate_terms = conn.execute(
            """
            SELECT v.code, t.zh_term, COUNT(*) AS count
            FROM terms t
            JOIN volumes v ON v.id = t.volume_id
            GROUP BY v.code, t.zh_term
            HAVING COUNT(*) > 1
            """
        ).fetchall()
        for volume_code, zh_term, count in duplicate_terms:
            errors.append(f"Duplicate zh_term in {volume_code}: {zh_term} ({count} rows)")

        missing_required = conn.execute(
            """
            SELECT term_uid, zh_term
            FROM terms
            WHERE
                TRIM(COALESCE(term_uid, '')) = ''
                OR TRIM(COALESCE(zh_term, '')) = ''
                OR TRIM(COALESCE(definition_short, '')) = ''
            """
        ).fetchall()
        for term_uid, zh_term in missing_required:
            errors.append(f"Missing required field: {term_uid or '[no uid]'} {zh_term or '[no zh_term]'}")

        no_category = conn.execute(
            """
            SELECT term_uid, zh_term
            FROM terms
            WHERE category_id IS NULL
            """
        ).fetchall()
        for term_uid, zh_term in no_category:
            warnings.append(f"No category assigned: {term_uid} {zh_term}")

        unresolved_relations = conn.execute(
            """
            SELECT COUNT(*)
            FROM term_relations
            WHERE target_term_id IS NULL AND target_label IS NOT NULL
            """
        ).fetchone()[0]
        if unresolved_relations:
            warnings.append(
                f"{unresolved_relations} term relations are label-only. "
                "This is acceptable during drafting; resolve to term IDs later."
            )

        low_definition = conn.execute(
            """
            SELECT term_uid, zh_term
            FROM terms
            WHERE LENGTH(COALESCE(definition_short, '')) < 8
            """
        ).fetchall()
        for term_uid, zh_term in low_definition:
            warnings.append(f"Very short definition: {term_uid} {zh_term}")

        echo_definition = conn.execute(
            """
            SELECT term_uid, zh_term, definition_short
            FROM terms
            WHERE
                RTRIM(TRIM(COALESCE(definition_short, '')), '。.；;，, ')
                = RTRIM(TRIM(COALESCE(zh_term, '')), '。.；;，, ')
            """
        ).fetchall()
        for term_uid, zh_term, definition_short in echo_definition:
            errors.append(
                f"definition_short repeats zh_term: {term_uid} {zh_term} -> {definition_short}"
            )

        placeholder_definition = conn.execute(
            """
            SELECT term_uid, zh_term, definition_short
            FROM terms
            WHERE
                definition_short LIKE '%简短定义%'
                OR definition_short LIKE '%待补充%'
                OR definition_short LIKE '%TODO%'
                OR definition_short LIKE '%TBD%'
            """
        ).fetchall()
        for term_uid, zh_term, definition_short in placeholder_definition:
            errors.append(
                f"definition_short is placeholder text: {term_uid} {zh_term} -> {definition_short}"
            )

        print_section("Summary")
        print(f"Volumes: {volume_count}")
        print(f"Terms: {term_count}")
        print(f"Target terms: {target_total}")
        print(f"Current completion: {term_count / target_total:.2%}")

        print_section("Volume Progress")
        rows = conn.execute(
            """
            SELECT
                v.code,
                v.title,
                v.target_terms,
                COUNT(t.id) AS current_terms
            FROM volumes v
            LEFT JOIN terms t ON t.volume_id = v.id
            GROUP BY v.id
            ORDER BY v.sequence_no
            """
        ).fetchall()
        for code, title, target, current in rows:
            print(f"{code} {title}: {current}/{target}")

    finally:
        conn.close()

    if warnings:
        print_section("Warnings")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print_section("Errors")
        for error in errors:
            print(f"- {error}")
        return 1

    print_section("Result")
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

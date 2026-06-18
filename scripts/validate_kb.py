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
        declared = {v["code"]: set(v.get("categories", [])) for v in config["volumes"]}

        # 同卷中文名唯一
        for volume_code, zh_term, count in conn.execute(
            """
            SELECT v.code, t.zh_term, COUNT(*) AS count
            FROM terms t JOIN volumes v ON v.id = t.volume_id
            GROUP BY v.code, t.zh_term HAVING COUNT(*) > 1
            """
        ).fetchall():
            errors.append(f"Duplicate zh_term in {volume_code}: {zh_term} ({count} rows)")

        # 硬必填非空（最小 1 字）：term_uid / zh_term / en_term / definition_long / version
        for col in ("term_uid", "zh_term", "en_term", "definition_long", "version"):
            for (term_uid,) in conn.execute(
                f"SELECT term_uid FROM terms WHERE TRIM(COALESCE({col}, '')) = ''"
            ).fetchall():
                errors.append(f"Missing required field {col}: {term_uid or '[no uid]'}")

        # 未挂分类（警告）
        for term_uid, zh_term in conn.execute(
            "SELECT term_uid, zh_term FROM terms WHERE category_id IS NULL"
        ).fetchall():
            warnings.append(f"No category assigned: {term_uid} {zh_term}")

        # label-only 关系（警告）
        unresolved = conn.execute(
            "SELECT COUNT(*) FROM term_relations WHERE target_term_id IS NULL AND target_label IS NOT NULL"
        ).fetchone()[0]
        if unresolved:
            warnings.append(
                f"{unresolved} term relations are label-only. Acceptable during drafting; resolve later."
            )

        # definition_long 不得复读术语名（错误）
        for term_uid, zh_term, dl in conn.execute(
            """
            SELECT term_uid, zh_term, definition_long FROM terms
            WHERE RTRIM(TRIM(COALESCE(definition_long, '')), '。.；;，, ')
                = RTRIM(TRIM(COALESCE(zh_term, '')), '。.；;，, ')
            """
        ).fetchall():
            errors.append(f"definition_long repeats zh_term: {term_uid} {zh_term} -> {dl}")

        # definition_long 不得是占位文本（错误）
        for term_uid, zh_term, dl in conn.execute(
            """
            SELECT term_uid, zh_term, definition_long FROM terms
            WHERE definition_long LIKE '%简短定义%' OR definition_long LIKE '%待补充%'
               OR definition_long LIKE '%TODO%' OR definition_long LIKE '%TBD%'
            """
        ).fetchall():
            errors.append(f"definition_long is placeholder text: {term_uid} {zh_term} -> {dl}")

        # term_uid 格式 V##_T####
        for (term_uid,) in conn.execute(
            "SELECT term_uid FROM terms WHERE term_uid NOT GLOB 'V[0-9][0-9]_T[0-9][0-9][0-9][0-9]'"
        ).fetchall():
            errors.append(f"term_uid format invalid: {term_uid}")

        # term_uid 前缀须与所属卷一致
        for term_uid, code in conn.execute(
            "SELECT t.term_uid, v.code FROM terms t JOIN volumes v ON v.id = t.volume_id "
            "WHERE substr(t.term_uid, 1, 3) != v.code"
        ).fetchall():
            errors.append(f"term_uid prefix does not match volume: {term_uid} (volume {code})")

        # 顶层分类须 ∈ config 声明
        for term_uid, code, name in conn.execute(
            "SELECT t.term_uid, v.code, c.name FROM terms t "
            "JOIN volumes v ON v.id = t.volume_id JOIN categories c ON c.id = t.category_id"
        ).fetchall():
            top = (name or "").split(" / ")[0].strip()
            if declared.get(code) and top not in declared[code]:
                errors.append(f"top category not declared in config: {term_uid} {code} -> {top}")

        # status 取值合法
        valid_status = {"draft", "review", "published", "deprecated"}
        for (status,) in conn.execute("SELECT DISTINCT status FROM terms").fetchall():
            if status not in valid_status:
                errors.append(f"invalid status value: {status}")

        # 每条术语至少一个 tag
        n = conn.execute(
            "SELECT COUNT(*) FROM terms t WHERE NOT EXISTS"
            "(SELECT 1 FROM term_tags tt WHERE tt.term_id = t.id)"
        ).fetchone()[0]
        if n:
            errors.append(f"{n} terms have no tags")

        # 卡片展示字段空（警告：存量豁免；新增经 ingest 硬卡）
        for col in ("visual_effect", "prompt_usage", "use_cases"):
            n = conn.execute(
                f"SELECT COUNT(*) FROM terms WHERE TRIM(COALESCE({col}, '')) = ''"
            ).fetchone()[0]
            if n:
                warnings.append(f"{n} terms have empty {col} (card-displayed; backfill recommended)")

        print_section("Summary")
        print(f"Volumes: {volume_count}")
        print(f"Terms: {term_count}")
        print(f"Target terms: {target_total}")
        print(f"Current completion: {term_count / target_total:.2%}")

        print_section("Volume Progress")
        for code, title, target, current in conn.execute(
            """
            SELECT v.code, v.title, v.target_terms, COUNT(t.id) AS current_terms
            FROM volumes v LEFT JOIN terms t ON t.volume_id = v.id
            GROUP BY v.id ORDER BY v.sequence_no
            """
        ).fetchall():
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

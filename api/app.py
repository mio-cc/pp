"""
AI视觉设计与提示词工程百科 —— 只读 API 服务层（FastAPI）

设计原则：
- 以只读模式打开 SQLite 主库，物理上无法改坏数据。
- 返回结构与 build_kb.py 导出的 data/exports/web/*.json 保持同构。
- 仅提供查询，不开放写入；写入仍走「改 CSV → build」的可追溯流程。

启动：
    pip install -r api/requirements.txt
    python -m uvicorn api.app:app --reload --port 8000
文档：
    http://localhost:8000/docs
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Literal, Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
WEB_DIR = ROOT / "web"
CATEGORY_SEPARATOR = " / "

VALID_SORTS = {
    "uid": "t.term_uid",
    "zh": "t.zh_term",
    "volume": "v.sequence_no, t.term_uid",
    "status": "t.status, t.term_uid",
}

app = FastAPI(
    title="AI视觉设计与提示词工程百科 API",
    description="只读知识库接口：术语筛选、全文搜索、卷册/分类/标签元数据、提示词导出。",
    version="2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def get_conn() -> sqlite3.Connection:
    """以只读模式连接主库。"""
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="数据库不存在，请先运行 python scripts/build_kb.py",
        )
    uri = f"file:{DB_PATH.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# 启动时探测一次 trigram FTS 是否存在（中文子串检索走索引的关键）。
_TRIGRAM_READY: Optional[bool] = None


def trigram_ready(conn: sqlite3.Connection) -> bool:
    global _TRIGRAM_READY
    if _TRIGRAM_READY is None:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='terms_fts_tri'"
        ).fetchone()
        _TRIGRAM_READY = row is not None
    return _TRIGRAM_READY


def fts_match_uids(conn: sqlite3.Connection, q: str, limit: int) -> list[str]:
    """用 trigram FTS 取候选 term_uid（≥3字才有效，已索引，避免全表 LIKE 扫描）。
    把查询作为带引号短语传入，trigram 会做子串匹配。"""
    if len(q) < 3 or not trigram_ready(conn):
        return []
    phrase = '"' + q.replace('"', '""') + '"'
    try:
        rows = conn.execute(
            "SELECT term_uid FROM terms_fts_tri WHERE terms_fts_tri MATCH ? LIMIT ?",
            (phrase, limit),
        ).fetchall()
        return [r[0] for r in rows]
    except sqlite3.Error:
        return []


def split_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


class TermUidListPayload(BaseModel):
    term_uids: list[str] = Field(default_factory=list, description="术语 UID 列表")


class CombinePromptsPayload(TermUidListPayload):
    language: Literal["en", "cn", "both"] = "en"
    format: Literal["comma", "newline", "weighted"] = "comma"


def extract_term_uids(payload: list[str] | TermUidListPayload) -> list[str]:
    raw_uids = payload if isinstance(payload, list) else payload.term_uids
    return [uid.strip() for uid in raw_uids if uid and uid.strip()]


def normalize_category_path(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    parts = [part.strip() for part in value.replace("\\", "/").split("/") if part.strip()]
    if not parts:
        return None
    return CATEGORY_SEPARATOR.join(parts)


def add_category_filters(
    where: list[str],
    params: list,
    category: Optional[str] = None,
    category_prefix: Optional[str] = None,
) -> None:
    normalized_category = normalize_category_path(category)
    if normalized_category:
        where.append("c.name = ?")
        params.append(normalized_category)

    normalized_prefix = normalize_category_path(category_prefix)
    if normalized_prefix:
        where.append("(c.name = ? OR c.name LIKE ?)")
        params.extend([normalized_prefix, f"{normalized_prefix}{CATEGORY_SEPARATOR}%"])


def order_rows_by_uids(
    rows: list[sqlite3.Row], requested_uids: list[str]
) -> tuple[list[sqlite3.Row], list[str]]:
    by_uid = {row["term_uid"]: row for row in rows}
    ordered = [by_uid[uid] for uid in requested_uids if uid in by_uid]
    missing = [uid for uid in requested_uids if uid not in by_uid]
    return ordered, missing


def serialize_term(row: sqlite3.Row, full: bool = False) -> dict:
    data = {
        "term_uid": row["term_uid"],
        "zh_term": row["zh_term"],
        "en_term": row["en_term"] or "",
        "volume_code": row["volume_code"],
        "volume_title": row["volume_title"],
        "category": row["category"] or "",
        "definition_short": row["definition_short"] or "",
        "positive_prompt": row["positive_prompt"] or "",
        "negative_prompt": row["negative_prompt"] or "",
        "positive_prompt_cn": (row["positive_prompt_cn"] or "") if "positive_prompt_cn" in row.keys() else "",
        "negative_prompt_cn": (row["negative_prompt_cn"] or "") if "negative_prompt_cn" in row.keys() else "",
        "tags": split_list(row["tags"] if "tags" in row.keys() else ""),
        "status": row["status"],
    }
    if full:
        data.update(
            {
                "definition_long": row["definition_long"] or "",
                "visual_effect": row["visual_effect"] or "",
                "prompt_usage": row["prompt_usage"] or "",
                "use_cases": split_list(row["use_cases"]),
                "aliases": split_list(row["aliases"]),
                "related_terms": split_list(row["related_terms"]),
                "confused_with": split_list(row["confused_with"]),
                "source_refs": row["source_refs"] or "",
                "version": row["version"],
            }
        )
    return data


_CN_READY = None


def cn_ready(conn: sqlite3.Connection) -> bool:
    """检测 terms 是否有双语列；旧库(未跑 schema 004)缺列时优雅降级，避免 500。"""
    global _CN_READY
    if _CN_READY is None:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(terms)").fetchall()]
        _CN_READY = "positive_prompt_cn" in cols
    return _CN_READY


def _cn_select(conn: sqlite3.Connection) -> str:
    return ("t.positive_prompt_cn, t.negative_prompt_cn" if cn_ready(conn)
            else "'' AS positive_prompt_cn, '' AS negative_prompt_cn")


def term_base_select(conn: sqlite3.Connection) -> str:
    return f"""
    SELECT
        t.id, t.term_uid, t.zh_term, t.en_term,
        v.code AS volume_code, v.title AS volume_title, v.sequence_no,
        c.name AS category,
        t.definition_short, t.positive_prompt, t.negative_prompt,
        {_cn_select(conn)}, t.status,
        COALESCE((SELECT GROUP_CONCAT(tags.name, ';')
                  FROM term_tags JOIN tags ON tags.id = term_tags.tag_id
                  WHERE term_tags.term_id = t.id), '') AS tags
    FROM terms t
    JOIN volumes v ON v.id = t.volume_id
    LEFT JOIN categories c ON c.id = t.category_id
"""


def term_detail_select(conn: sqlite3.Connection) -> str:
    return f"""
        SELECT
            t.id, t.term_uid, t.zh_term, t.en_term,
            v.code AS volume_code, v.title AS volume_title,
            c.name AS category,
            t.definition_short, t.definition_long, t.visual_effect,
            t.prompt_usage, t.positive_prompt, t.negative_prompt,
            {_cn_select(conn)},
            t.use_cases, t.source_refs, t.status, t.version,
            COALESCE((SELECT GROUP_CONCAT(alias, ';') FROM term_aliases WHERE term_id = t.id), '') AS aliases,
            COALESCE((SELECT GROUP_CONCAT(tags.name, ';') FROM term_tags
                      JOIN tags ON tags.id = term_tags.tag_id WHERE term_tags.term_id = t.id), '') AS tags,
            COALESCE((SELECT GROUP_CONCAT(target_label, ';') FROM term_relations
                      WHERE source_term_id = t.id AND relation_type = 'related'), '') AS related_terms,
            COALESCE((SELECT GROUP_CONCAT(target_label, ';') FROM term_relations
                      WHERE source_term_id = t.id AND relation_type = 'confused_with'), '') AS confused_with
        FROM terms t
        JOIN volumes v ON v.id = t.volume_id
        LEFT JOIN categories c ON c.id = t.category_id
    """


@app.get("/api/health")
def health() -> dict:
    if not DB_PATH.exists():
        return {"status": "no_db", "detail": "运行 python scripts/build_kb.py 生成主库"}
    conn = get_conn()
    try:
        n = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    finally:
        conn.close()
    return {"status": "ok", "terms": n, "version": "2.0"}


@app.get("/api/meta")
def meta() -> dict:
    """一次性返回卷册、标签、统计，供前端初始化下拉框。"""
    conn = get_conn()
    try:
        volumes = _volumes(conn)
        tag_rows = conn.execute(
            """
            SELECT tags.name, COUNT(term_tags.term_id) AS c
            FROM tags LEFT JOIN term_tags ON term_tags.tag_id = tags.id
            GROUP BY tags.id ORDER BY c DESC, tags.name
            """
        ).fetchall()
        status_rows = conn.execute(
            "SELECT status, COUNT(*) AS c FROM terms GROUP BY status"
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
        target_total = sum(v["target_terms"] for v in volumes)
    finally:
        conn.close()
    return {
        "project": "AI视觉设计与提示词工程百科",
        "version": "V1.0",
        "total_terms": total,
        "target_total": target_total,
        "completion_percent": round(total * 100.0 / target_total, 2) if target_total else 0.0,
        "status_counts": {r["status"]: r["c"] for r in status_rows},
        "volumes": volumes,
        "tags": [{"name": r["name"], "term_count": r["c"]} for r in tag_rows],
    }


def _volumes(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        """
        SELECT v.code, v.title, v.sequence_no, v.target_terms, v.purpose,
               COUNT(t.id) AS current_terms
        FROM volumes v LEFT JOIN terms t ON t.volume_id = v.id
        GROUP BY v.id ORDER BY v.sequence_no
        """
    ).fetchall()
    # 一次性取所有分类计数，按卷分组（避免每卷一条查询的 N+1）。
    cat_rows = conn.execute(
        """
        SELECT v.code AS vcode, c.name, c.sort_order, COUNT(t.id) AS c
        FROM categories c
        JOIN volumes v ON v.id = c.volume_id
        LEFT JOIN terms t ON t.category_id = c.id
        GROUP BY c.id ORDER BY v.sequence_no, c.sort_order
        """
    ).fetchall()
    cats_by_vol: dict[str, list] = {}
    for cr in cat_rows:
        cats_by_vol.setdefault(cr["vcode"], []).append(
            {"name": cr["name"], "term_count": cr["c"]}
        )
    out = []
    for r in rows:
        target = r["target_terms"] or 0
        current = r["current_terms"] or 0
        out.append(
            {
                "code": r["code"],
                "title": r["title"],
                "sequence": r["sequence_no"],
                "target_terms": target,
                "current_terms": current,
                "completion_percent": round(current * 100.0 / target, 2) if target else 0.0,
                "purpose": r["purpose"] or "",
                "categories": cats_by_vol.get(r["code"], []),
            }
        )
    return out


@app.get("/api/volumes")
def volumes() -> dict:
    conn = get_conn()
    try:
        return {"items": _volumes(conn)}
    finally:
        conn.close()


@app.get("/api/volumes/{code}/categories")
def volume_categories(code: str) -> dict:
    conn = get_conn()
    try:
        vol = conn.execute("SELECT id FROM volumes WHERE code = ?", (code,)).fetchone()
        if not vol:
            raise HTTPException(status_code=404, detail=f"未找到卷册 {code}")
        rows = conn.execute(
            """
            SELECT c.name, COUNT(t.id) AS c
            FROM categories c LEFT JOIN terms t ON t.category_id = c.id
            WHERE c.volume_id = ? GROUP BY c.id ORDER BY c.sort_order
            """,
            (vol["id"],),
        ).fetchall()
        return {"volume_code": code, "items": [{"name": r["name"], "term_count": r["c"]} for r in rows]}
    finally:
        conn.close()


@app.get("/api/tags")
def tags() -> dict:
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT tags.name, COUNT(term_tags.term_id) AS c
            FROM tags LEFT JOIN term_tags ON term_tags.tag_id = tags.id
            GROUP BY tags.id ORDER BY c DESC, tags.name
            """
        ).fetchall()
        return {"items": [{"name": r["name"], "term_count": r["c"]} for r in rows]}
    finally:
        conn.close()


@app.get("/api/terms")
def list_terms(
    q: Optional[str] = Query(None, description="关键词，匹配中英文名/别名/定义"),
    volume: Optional[str] = Query(None, description="卷册 code，如 V08"),
    category: Optional[str] = Query(None, description="分类名（精确匹配）"),
    category_prefix: Optional[str] = Query(None, description="分类路径前缀（层级筛选），如「代表性风格/」"),
    tag: Optional[str] = Query(None, description="单个标签名"),
    tags: Optional[str] = Query(None, description="多个标签名，用逗号分隔，如「色彩,艺术」"),
    tag_logic: str = Query("AND", description="多标签逻辑：AND/OR"),
    status: Optional[str] = Query(None, description="draft/review/published/deprecated"),
    sort: str = Query("volume", description="排序：uid/zh/volume/status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
) -> dict:
    conn = get_conn()
    try:
        where = []
        params: list = []
        if volume:
            where.append("v.code = ?")
            params.append(volume)
        if category:
            where.append("c.name = ?")
            params.append(category)
        if category_prefix:
            where.append("c.name LIKE ?")
            params.append(f"{category_prefix}%")
        if status:
            where.append("t.status = ?")
            params.append(status)
        if tag:
            where.append(
                "t.id IN (SELECT term_tags.term_id FROM term_tags "
                "JOIN tags ON tags.id = term_tags.tag_id WHERE tags.name = ?)"
            )
            params.append(tag)
        if tags:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            if tag_list:
                if tag_logic == "OR":
                    placeholders = ",".join("?" for _ in tag_list)
                    where.append(
                        f"t.id IN (SELECT DISTINCT term_tags.term_id FROM term_tags "
                        f"JOIN tags ON tags.id = term_tags.tag_id WHERE tags.name IN ({placeholders}))"
                    )
                    params.extend(tag_list)
                else:  # AND
                    for tag_name in tag_list:
                        where.append(
                            "t.id IN (SELECT term_tags.term_id FROM term_tags "
                            "JOIN tags ON tags.id = term_tags.tag_id WHERE tags.name = ?)"
                        )
                        params.append(tag_name)
            params.append(tag)
        if q:
            # ≥3字：用 trigram FTS 取候选 id，命中后用 IN 过滤（走索引，避免全表扫描）。
            # <3字或无 trigram：退回 LIKE（短查询数据量影响小）。
            uids = fts_match_uids(conn, q, 5000)
            if uids:
                placeholders = ",".join("?" for _ in uids)
                where.append(
                    f"t.term_uid IN ({placeholders})"
                )
                params.extend(uids)
            else:
                like = f"%{q}%"
                where.append(
                    "(t.zh_term LIKE ? OR t.en_term LIKE ? OR t.definition_short LIKE ? "
                    "OR t.id IN (SELECT term_id FROM term_aliases WHERE alias LIKE ?))"
                )
                params.extend([like, like, like, like])

        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        total = conn.execute(
            f"SELECT COUNT(*) FROM terms t JOIN volumes v ON v.id = t.volume_id "
            f"LEFT JOIN categories c ON c.id = t.category_id{where_sql}",
            params,
        ).fetchone()[0]

        order_sql = VALID_SORTS.get(sort, VALID_SORTS["volume"])
        offset = (page - 1) * page_size
        rows = conn.execute(
            f"{term_base_select(conn)}{where_sql} ORDER BY {order_sql} LIMIT ? OFFSET ?",
            params + [page_size, offset],
        ).fetchall()

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size if page_size else 0,
            "items": [serialize_term(r) for r in rows],
        }
    finally:
        conn.close()


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(20, ge=1, le=100)) -> dict:
    """全文搜索：
    - ≥3字：trigram FTS 子串检索（已索引，十万级也快），覆盖中英文/别名/正文。
    - <3字或无 trigram：LIKE 兜底（短查询数据量影响小）。
    """
    conn = get_conn()
    try:
        uids = fts_match_uids(conn, q, limit)
        if uids:
            ph = ",".join("?" for _ in uids)
            rows = conn.execute(
                f"{term_base_select(conn)} WHERE t.term_uid IN ({ph})", uids
            ).fetchall()
            by_uid = {r["term_uid"]: r for r in rows}
            items = [serialize_term(by_uid[u]) for u in uids if u in by_uid]
            return {"query": q, "count": len(items), "items": items, "engine": "trigram"}

        # 短查询 / 无 trigram：LIKE 兜底
        like = f"%{q}%"
        rows = conn.execute(
            f"""{term_base_select(conn)}
            LEFT JOIN term_aliases a ON a.term_id = t.id
            WHERE t.zh_term LIKE ? OR t.en_term LIKE ? OR a.alias LIKE ?
               OR t.definition_short LIKE ? OR t.definition_long LIKE ? OR t.prompt_usage LIKE ?
            GROUP BY t.id ORDER BY v.sequence_no, t.term_uid LIMIT ?
            """,
            (like, like, like, like, like, like, limit),
        ).fetchall()
        items = [serialize_term(r) for r in rows]
        return {"query": q, "count": len(items), "items": items, "engine": "like"}
    finally:
        conn.close()


@app.get("/api/stats")
def stats() -> dict:
    conn = get_conn()
    try:
        volumes = _volumes(conn)
        total = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
        target_total = sum(v["target_terms"] for v in volumes)
        status_rows = conn.execute(
            "SELECT status, COUNT(*) AS c FROM terms GROUP BY status"
        ).fetchall()
        return {
            "total_terms": total,
            "target_total": target_total,
            "completion_percent": round(total * 100.0 / target_total, 2) if target_total else 0.0,
            "status_counts": {r["status"]: r["c"] for r in status_rows},
            "volumes": volumes,
        }
    finally:
        conn.close()


@app.get("/api/export/prompts")
def export_prompts(
    volume: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    format: str = Query("json", pattern="^(json|text)$"),
):
    """按筛选导出纯提示词清单，给提示词工程批量取用。"""
    conn = get_conn()
    try:
        where = ["t.positive_prompt IS NOT NULL AND t.positive_prompt != ''"]
        params: list = []
        if volume:
            where.append("v.code = ?")
            params.append(volume)
        if tag:
            where.append(
                "t.id IN (SELECT term_tags.term_id FROM term_tags "
                "JOIN tags ON tags.id = term_tags.tag_id WHERE tags.name = ?)"
            )
            params.append(tag)
        where_sql = " WHERE " + " AND ".join(where)
        rows = conn.execute(
            f"""
            SELECT t.term_uid, t.zh_term, t.en_term, v.code AS volume_code,
                   t.positive_prompt, t.negative_prompt
            FROM terms t JOIN volumes v ON v.id = t.volume_id{where_sql}
            ORDER BY v.sequence_no, t.term_uid
            """,
            params,
        ).fetchall()
    finally:
        conn.close()

    if format == "text":
        lines = []
        for r in rows:
            lines.append(f"# {r['zh_term']} / {r['en_term']} [{r['term_uid']}]")
            lines.append(f"+ {r['positive_prompt']}")
            if r["negative_prompt"]:
                lines.append(f"- {r['negative_prompt']}")
            lines.append("")
        return PlainTextResponse("\n".join(lines))

    return JSONResponse(
        {
            "count": len(rows),
            "items": [
                {
                    "term_uid": r["term_uid"],
                    "zh_term": r["zh_term"],
                    "en_term": r["en_term"] or "",
                    "volume_code": r["volume_code"],
                    "positive_prompt": r["positive_prompt"] or "",
                    "negative_prompt": r["negative_prompt"] or "",
                }
                for r in rows
            ],
        }
    )


@app.post("/api/terms/batch")
def batch_terms(payload: list[str] | TermUidListPayload = Body(...)) -> dict:
    """批量获取多个术语的完整详情。

    Body: ["V06_T0211", "V02_T0120", "V08_T0127"]
    """
    term_uids = extract_term_uids(payload)
    if not term_uids:
        return {"count": 0, "requested_count": 0, "missing_term_uids": [], "items": []}
    if len(term_uids) > 50:
        raise HTTPException(status_code=400, detail="批量查询最多50条")

    conn = get_conn()
    try:
        placeholders = ",".join("?" for _ in term_uids)
        rows = conn.execute(
            f"{term_detail_select(conn)} WHERE t.term_uid IN ({placeholders})",
            term_uids,
        ).fetchall()
        ordered_rows, missing_term_uids = order_rows_by_uids(rows, term_uids)
        return {
            "count": len(ordered_rows),
            "requested_count": len(term_uids),
            "missing_term_uids": missing_term_uids,
            "items": [serialize_term(r, full=True) for r in ordered_rows],
        }
    finally:
        conn.close()


@app.get("/api/terms/random")
def random_terms(
    count: int = Query(5, ge=1, le=20, description="返回数量"),
    volume: Optional[str] = Query(None, description="限定卷册"),
    category: Optional[str] = Query(None, description="限定分类"),
    category_prefix: Optional[str] = Query(None, description="限定分类路径前缀"),
    tag: Optional[str] = Query(None, description="限定标签"),
) -> dict:
    """随机返回术语，用于探索发现。"""
    conn = get_conn()
    try:
        where = []
        params: list = []
        if volume:
            where.append("v.code = ?")
            params.append(volume)
        add_category_filters(where, params, category, category_prefix)
        if tag:
            where.append(
                "t.id IN (SELECT term_tags.term_id FROM term_tags "
                "JOIN tags ON tags.id = term_tags.tag_id WHERE tags.name = ?)"
            )
            params.append(tag)

        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        total = conn.execute(
            f"SELECT COUNT(*) FROM terms t JOIN volumes v ON v.id = t.volume_id "
            f"LEFT JOIN categories c ON c.id = t.category_id{where_sql}",
            params,
        ).fetchone()[0]
        rows = conn.execute(
            f"{term_base_select(conn)}{where_sql} ORDER BY RANDOM() LIMIT ?",
            params + [count],
        ).fetchall()
        return {"count": len(rows), "available": total, "items": [serialize_term(r) for r in rows]}
    finally:
        conn.close()


@app.post("/api/prompts/combine")
def combine_prompts(payload: CombinePromptsPayload) -> dict:
    """合并多个术语的提示词。

    Args:
        term_uids: 术语UID列表
        language: en/cn/both
        format: comma（逗号分隔）/ newline（换行）/ weighted（带权重）
    """
    term_uids = extract_term_uids(payload)
    language = payload.language
    format = payload.format
    if not term_uids:
        return {
            "combined": "",
            "combined_en": "",
            "combined_cn": "",
            "language": language,
            "format": format,
            "count": 0,
            "requested_count": 0,
            "missing_term_uids": [],
            "terms": [],
        }
    if len(term_uids) > 30:
        raise HTTPException(status_code=400, detail="合并提示词最多30条")

    conn = get_conn()
    try:
        placeholders = ",".join("?" for _ in term_uids)
        rows = conn.execute(
            f"""
            SELECT t.term_uid, t.zh_term, t.positive_prompt,
                   {_cn_select(conn).split(',')[0]} AS positive_prompt_cn
            FROM terms t
            WHERE t.term_uid IN ({placeholders})
            """,
            term_uids,
        ).fetchall()
        ordered_rows, missing_term_uids = order_rows_by_uids(rows, term_uids)

        terms_data = []
        prompts_en = []
        prompts_cn = []

        for r in ordered_rows:
            terms_data.append({
                "term_uid": r["term_uid"],
                "zh_term": r["zh_term"],
                "positive_prompt": r["positive_prompt"] or "",
                "positive_prompt_cn": r["positive_prompt_cn"] or "",
            })
            if r["positive_prompt"]:
                prompts_en.append(r["positive_prompt"])
            if r["positive_prompt_cn"]:
                prompts_cn.append(r["positive_prompt_cn"])

        # 组合提示词
        if format == "comma":
            sep = ", "
        elif format == "newline":
            sep = "\n"
        else:  # weighted
            sep = ", "
            prompts_en = [f"({p}:1.1)" for p in prompts_en]
            prompts_cn = [f"({p}:1.1)" for p in prompts_cn]

        combined_en = sep.join(prompts_en)
        combined_cn = sep.join(prompts_cn)
        combined = ""
        if language == "en":
            combined = combined_en
        elif language == "cn":
            combined = combined_cn
        else:  # both
            if combined_en and combined_cn:
                combined = combined_en + "\n" + combined_cn
            else:
                combined = combined_en or combined_cn

        return {
            "combined": combined,
            "combined_en": combined_en,
            "combined_cn": combined_cn,
            "language": language,
            "format": format,
            "count": len(terms_data),
            "requested_count": len(term_uids),
            "missing_term_uids": missing_term_uids,
            "terms": terms_data,
        }
    finally:
        conn.close()


@app.get("/api/terms/{term_uid}")
def term_detail(term_uid: str) -> dict:
    conn = get_conn()
    try:
        row = conn.execute(
            f"{term_detail_select(conn)} WHERE t.term_uid = ?",
            (term_uid,),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"未找到术语 {term_uid}")
        return serialize_term(row, full=True)
    finally:
        conn.close()


@app.get("/api/terms/{term_uid}/related")
def related_terms(term_uid: str, limit: int = Query(5, ge=1, le=10)) -> dict:
    """获取相关术语（基于同分类、同标签智能推荐）。"""
    conn = get_conn()
    try:
        # 先获取当前术语的分类和标签
        current = conn.execute(
            f"{term_base_select(conn)} WHERE t.term_uid = ?",
            (term_uid,),
        ).fetchone()
        if not current:
            raise HTTPException(status_code=404, detail=f"未找到术语 {term_uid}")

        # 获取相关术语：相同分类优先，然后相同标签
        rows = conn.execute(
            f"""
            {term_base_select(conn)}
            WHERE t.term_uid != ?
            ORDER BY
                CASE WHEN c.name = ? THEN 0 ELSE 1 END,
                (SELECT COUNT(*) FROM term_tags WHERE term_tags.term_id = t.id
                 AND term_tags.tag_id IN (
                     SELECT tags.id FROM tags JOIN term_tags ON tags.id = term_tags.tag_id
                     WHERE term_tags.term_id = (SELECT id FROM terms WHERE term_uid = ?)
                 )) DESC,
                v.sequence_no, t.term_uid
            LIMIT ?
            """,
            (term_uid, current["category"], term_uid, limit),
        ).fetchall()

        return {"count": len(rows), "items": [serialize_term(r) for r in rows]}
    finally:
        conn.close()


@app.get("/api/terms/compare")
def compare_terms(a: str, b: str) -> dict:
    """对比两个术语的异同。"""
    conn = get_conn()
    try:
        row_a = conn.execute(
            f"{term_detail_select(conn)} WHERE t.term_uid = ?",
            (a,),
        ).fetchone()
        row_b = conn.execute(
            f"{term_detail_select(conn)} WHERE t.term_uid = ?",
            (b,),
        ).fetchone()

        if not row_a:
            raise HTTPException(status_code=404, detail=f"未找到术语 {a}")
        if not row_b:
            raise HTTPException(status_code=404, detail=f"未找到术语 {b}")

        term_a = serialize_term(row_a, full=True)
        term_b = serialize_term(row_b, full=True)

        # 计算异同
        same_volume = term_a["volume_code"] == term_b["volume_code"]
        same_category = term_a["category"] == term_b["category"]
        same_tags = set(term_a["tags"]) & set(term_b["tags"])

        return {
            "term_a": term_a,
            "term_b": term_b,
            "comparison": {
                "same_volume": same_volume,
                "same_category": same_category,
                "common_tags": list(same_tags),
                "tag_count_a": len(term_a["tags"]),
                "tag_count_b": len(term_b["tags"]),
            }
        }
    finally:
        conn.close()


@app.get("/api/volumes/{code}/categories/tree")
def category_tree(code: str) -> dict:
    """获取分类的树状结构。"""
    conn = get_conn()
    try:
        vol = conn.execute("SELECT id FROM volumes WHERE code = ?", (code,)).fetchone()
        if not vol:
            raise HTTPException(status_code=404, detail=f"未找到卷册 {code}")

        rows = conn.execute(
            """
            SELECT c.name, COUNT(t.id) AS count
            FROM categories c
            LEFT JOIN terms t ON t.category_id = c.id
            WHERE c.volume_id = ?
            GROUP BY c.id
            ORDER BY c.sort_order
            """,
            (vol["id"],),
        ).fetchall()

        # 构建树状结构
        tree = {}
        for r in rows:
            path = r["name"].split(" / ")
            current = tree
            for i, part in enumerate(path):
                if part not in current:
                    current[part] = {"_count": 0, "_children": {}}
                # 如果是叶子节点或中间节点，累加计数
                if i == len(path) - 1:
                    current[part]["_count"] = r["count"]
                current = current[part]["_children"]

        return {"volume_code": code, "tree": tree}
    finally:
        conn.close()


@app.get("/api/search/advanced")
def advanced_search(
    zh_term: Optional[str] = Query(None),
    en_term: Optional[str] = Query(None),
    definition_short: Optional[str] = Query(None),
    positive_prompt: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    volume: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> dict:
    """高级搜索（指定字段搜索）。"""
    conn = get_conn()
    try:
        where = []
        params = []

        if zh_term:
            where.append("t.zh_term LIKE ?")
            params.append(f"%{zh_term}%")
        if en_term:
            where.append("t.en_term LIKE ?")
            params.append(f"%{en_term}%")
        if definition_short:
            where.append("t.definition_short LIKE ?")
            params.append(f"%{definition_short}%")
        if positive_prompt:
            where.append("t.positive_prompt LIKE ?")
            params.append(f"%{positive_prompt}%")
        if category:
            where.append("c.name LIKE ?")
            params.append(f"%{category}%")
        if volume:
            where.append("v.code = ?")
            params.append(volume)

        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        rows = conn.execute(
            f"{term_base_select(conn)}{where_sql} ORDER BY v.sequence_no, t.term_uid LIMIT ?",
            params + [limit],
        ).fetchall()

        return {"count": len(rows), "items": [serialize_term(r) for r in rows]}
    finally:
        conn.close()


@app.get("/")
def root() -> dict:
    return {
        "name": "AI视觉设计与提示词工程百科 API",
        "version": "2.1",
        "docs": "/docs",
        "web": "/app/" if (WEB_DIR / "index.html").exists() else None,
        "endpoints": [
            "/api/health", "/api/meta", "/api/volumes", "/api/tags",
            "/api/terms", "/api/terms/{term_uid}", "/api/terms/batch",
            "/api/terms/random", "/api/terms/{term_uid}/related",
            "/api/terms/compare", "/api/search", "/api/search/advanced",
            "/api/stats", "/api/export/prompts", "/api/prompts/combine",
            "/api/volumes/{code}/categories", "/api/volumes/{code}/categories/tree",
        ],
    }


# 把前端单页同源挂到 /app/ —— 浏览器打开 http://localhost:8000/app/ 即 API 模式。
if (WEB_DIR / "index.html").exists():
    from fastapi.staticfiles import StaticFiles

    app.mount("/app", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

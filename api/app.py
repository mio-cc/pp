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
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
WEB_DIR = ROOT / "web"

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
    allow_methods=["GET"],
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


TERM_BASE_SELECT = """
    SELECT
        t.id, t.term_uid, t.zh_term, t.en_term,
        v.code AS volume_code, v.title AS volume_title, v.sequence_no,
        c.name AS category,
        t.definition_short, t.positive_prompt, t.negative_prompt,
        t.positive_prompt_cn, t.negative_prompt_cn, t.status,
        COALESCE((SELECT GROUP_CONCAT(tags.name, ';')
                  FROM term_tags JOIN tags ON tags.id = term_tags.tag_id
                  WHERE term_tags.term_id = t.id), '') AS tags
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
    category: Optional[str] = Query(None, description="分类名"),
    tag: Optional[str] = Query(None, description="标签名"),
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
        if status:
            where.append("t.status = ?")
            params.append(status)
        if tag:
            where.append(
                "t.id IN (SELECT term_tags.term_id FROM term_tags "
                "JOIN tags ON tags.id = term_tags.tag_id WHERE tags.name = ?)"
            )
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
            f"{TERM_BASE_SELECT}{where_sql} ORDER BY {order_sql} LIMIT ? OFFSET ?",
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


@app.get("/api/terms/{term_uid}")
def term_detail(term_uid: str) -> dict:
    conn = get_conn()
    try:
        row = conn.execute(
            """
            SELECT
                t.id, t.term_uid, t.zh_term, t.en_term,
                v.code AS volume_code, v.title AS volume_title,
                c.name AS category,
                t.definition_short, t.definition_long, t.visual_effect,
                t.prompt_usage, t.positive_prompt, t.negative_prompt,
                t.positive_prompt_cn, t.negative_prompt_cn,
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
            WHERE t.term_uid = ?
            """,
            (term_uid,),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"未找到术语 {term_uid}")
        return serialize_term(row, full=True)
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
                f"{TERM_BASE_SELECT} WHERE t.term_uid IN ({ph})", uids
            ).fetchall()
            by_uid = {r["term_uid"]: r for r in rows}
            items = [serialize_term(by_uid[u]) for u in uids if u in by_uid]
            return {"query": q, "count": len(items), "items": items, "engine": "trigram"}

        # 短查询 / 无 trigram：LIKE 兜底
        like = f"%{q}%"
        rows = conn.execute(
            f"""{TERM_BASE_SELECT}
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


@app.get("/")
def root() -> dict:
    return {
        "name": "AI视觉设计与提示词工程百科 API",
        "docs": "/docs",
        "web": "/app/" if (WEB_DIR / "index.html").exists() else None,
        "endpoints": [
            "/api/health", "/api/meta", "/api/volumes", "/api/tags",
            "/api/terms", "/api/terms/{term_uid}", "/api/search",
            "/api/stats", "/api/export/prompts",
        ],
    }


# 把前端单页同源挂到 /app/ —— 浏览器打开 http://localhost:8000/app/ 即 API 模式。
if (WEB_DIR / "index.html").exists():
    from fastapi.staticfiles import StaticFiles

    app.mount("/app", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

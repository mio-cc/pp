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

import array
import importlib.util
import json
import sqlite3
from pathlib import Path
from typing import Literal, Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
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
    version="2.1",
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
    # 平台方言：generic 通用；sd → 权重写作 (term:1.1)；mj → 权重写作 term::1.1
    dialect: Literal["generic", "sd", "mj"] = "generic"
    # 追加在结果末尾的平台参数（原样拼接），如 " --ar 16:9 --v 6"
    suffix: str = ""


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


def term_base_select(conn: sqlite3.Connection) -> str:
    return f"""
    SELECT
        t.id, t.term_uid, t.zh_term, t.en_term,
        v.code AS volume_code, v.title AS volume_title, v.sequence_no,
        c.name AS category,
        t.status,
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
            t.definition_long, t.visual_effect, t.prompt_usage,
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


@app.get("/api/health", summary="健康检查")
def health() -> dict:
    if not DB_PATH.exists():
        return {"status": "no_db", "detail": "运行 python scripts/build_kb.py 生成主库"}
    conn = get_conn()
    try:
        n = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    finally:
        conn.close()
    return {"status": "ok", "terms": n, "version": "2.1"}


@app.get("/api/meta", summary="元数据（卷册/标签/统计）")
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


@app.get("/api/volumes", summary="卷册列表")
def volumes() -> dict:
    conn = get_conn()
    try:
        return {"items": _volumes(conn)}
    finally:
        conn.close()


@app.get("/api/volumes/{code}/categories", summary="卷册分类列表")
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


@app.get("/api/tags", summary="标签云")
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


@app.get("/api/terms", summary="术语列表（筛选+分页）")
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
        # 分类过滤统一走带 " / " 边界的前缀匹配，避免「布光」误中「布光与用光」
        add_category_filters(where, params, category, category_prefix)
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
                    "(t.zh_term LIKE ? OR t.en_term LIKE ? OR t.definition_long LIKE ? "
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


@app.get("/api/tree", summary="全库骨架（卷+分类路径+计数）")
def tree() -> dict:
    """全库骨架一次拉取：卷 + 全部分类路径 + 计数（无正文，约几十 KB）。

    前端首屏与 AI 探索共用：AI 供稿前先看这里找空分支（term_count=0）与未达标的卷。
    """
    conn = get_conn()
    try:
        vol_rows = conn.execute(
            """
            SELECT v.code, v.title, v.sequence_no, v.target_terms, v.purpose,
                   COUNT(t.id) AS current_terms
            FROM volumes v LEFT JOIN terms t ON t.volume_id = v.id
            GROUP BY v.id ORDER BY v.sequence_no
            """
        ).fetchall()
        cat_rows = conn.execute(
            """
            SELECT v.code AS vcode, c.name, COUNT(t.id) AS n
            FROM categories c
            JOIN volumes v ON v.id = c.volume_id
            LEFT JOIN terms t ON t.category_id = c.id
            GROUP BY c.id ORDER BY v.sequence_no, c.sort_order
            """
        ).fetchall()
    finally:
        conn.close()
    cats_by_vol: dict[str, list] = {}
    for r in cat_rows:
        cats_by_vol.setdefault(r["vcode"], []).append(
            {"path": r["name"], "term_count": r["n"]}
        )
    return {
        "separator": CATEGORY_SEPARATOR,
        "volumes": [
            {
                "code": r["code"],
                "title": r["title"],
                "target_terms": r["target_terms"] or 0,
                "current_terms": r["current_terms"] or 0,
                "purpose": r["purpose"] or "",
                "categories": cats_by_vol.get(r["code"], []),
            }
            for r in vol_rows
        ],
    }


@app.get("/api/contract", summary="供稿契约（Schema+顶层白名单+流程）")
def contract() -> dict:
    """机器可读供稿契约：term JSON Schema + 各卷顶层分类白名单 + 提交流程。

    AI 供稿前 GET 一次即可自查全部规则，不再依赖读仓库文件。
    """
    schema_path = ROOT / "schema" / "term.schema.json"
    config_path = ROOT / "config" / "volumes.json"
    if not schema_path.exists() or not config_path.exists():
        raise HTTPException(status_code=503, detail="schema/term.schema.json 或 config/volumes.json 缺失")
    term_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return {
        "term_schema": term_schema,
        "volumes": [
            {
                "code": v["code"],
                "title": v["title"],
                "target_terms": v.get("target_terms", 0),
                "allowed_top_categories": v.get("categories", []),
            }
            for v in config.get("volumes", [])
        ],
        "category_rule": (
            "category 为完整分类路径，用 ' / ' 分隔，深度不限；"
            "首段必须在该卷 allowed_top_categories 内，其后自由分支；"
            "术语挂在路径末端，名字本身即提示词（zh_term=中文提示词，en_term=英文提示词）。"
        ),
        "workflow": [
            "1. GET /api/tree 查看结构，找空分支（term_count=0）或未达标的卷",
            "2. GET /api/contract 获取本契约与字段规则",
            "3. 生成 terms.json（对象数组，多值字段用数组）",
            "4. POST /api/ingest/check 在线 dry-run 校验，报错则修",
            "5. python scripts/ingest.py add-terms terms.json 写入（唯一落库通道）",
        ],
    }


_SCRIPT_MODS: dict = {}


def _script(name: str):
    """按需加载 scripts/{name}.py（顶层仅常量与函数定义，加载安全）。"""
    if name not in _SCRIPT_MODS:
        spec = importlib.util.spec_from_file_location(f"kb_{name}", ROOT / "scripts" / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _SCRIPT_MODS[name] = mod
    return _SCRIPT_MODS[name]


def _ingest_module():
    return _script("ingest")


# ---------------------------------------------------------------- 向量层
# term_vectors 由 scripts/build_vectors.py 生成（哈希字符 n-gram TF-IDF，零依赖）。
# 2 千条内存 ~5MB、查询 <200ms；十万级时换 sqlite-vec/numpy，本接口不变。
_VEC: dict = {"stamp": None, "ids": [], "vecs": [], "idf": None}


def _vectors(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='term_vectors'"
    ).fetchone()
    if not row:
        raise HTTPException(status_code=503, detail="向量表不存在，请运行 python scripts/build_vectors.py")
    stamp = conn.execute("SELECT COUNT(*) FROM term_vectors").fetchone()[0]
    if _VEC["stamp"] != stamp:
        idf_row = conn.execute("SELECT value FROM vector_meta WHERE key='idf'").fetchone()
        rows = conn.execute("SELECT term_id, vec FROM term_vectors").fetchall()
        _VEC.update(
            stamp=stamp,
            ids=[r[0] for r in rows],
            vecs=[array.array("f", r[1]) for r in rows],
            idf=json.loads(idf_row[0]) if idf_row else None,
        )
    return _VEC


def _query_vec(text: str, idf) -> list[float]:
    tv = _script("textvec")
    return tv.finalize(tv.raw_counts(text), idf)


def _top_similar(conn: sqlite3.Connection, qvec, limit: int, exclude_id: int | None = None):
    vec_state = _vectors(conn)
    scored = []
    for tid, v in zip(vec_state["ids"], vec_state["vecs"]):
        if tid == exclude_id:
            continue
        s = 0.0
        for a, b in zip(qvec, v):
            s += a * b
        if s > 0.05:
            scored.append((s, tid))
    scored.sort(reverse=True)
    return scored[:limit]


def _rows_by_ids(conn: sqlite3.Connection, ids: list[int]) -> dict:
    if not ids:
        return {}
    ph = ",".join("?" for _ in ids)
    rows = conn.execute(f"{term_base_select(conn)} WHERE t.id IN ({ph})", ids).fetchall()
    return {r["id"]: r for r in rows}


@app.get("/api/search/semantic", summary="语义模糊检索")
def search_semantic(q: str = Query(..., min_length=1), limit: int = Query(20, ge=1, le=100)) -> dict:
    """模糊/语义检索：字符 n-gram 向量余弦，比 LIKE 更能容忍换词与描述式查询。

    与 /api/search（字面精确）互补，前端可双路合并。
    """
    conn = get_conn()
    try:
        vec_state = _vectors(conn)
        qvec = _query_vec(q, vec_state["idf"])
        top = _top_similar(conn, qvec, limit)
        by_id = _rows_by_ids(conn, [tid for _, tid in top])
        items = []
        for score, tid in top:
            if tid in by_id:
                item = serialize_term(by_id[tid])
                item["score"] = round(score, 4)
                items.append(item)
        return {"query": q, "count": len(items), "items": items, "engine": "ngram-tfidf"}
    finally:
        conn.close()


@app.get("/api/terms/{term_uid}/similar", summary="相似术语（向量）")
def similar_terms(term_uid: str, limit: int = Query(10, ge=1, le=50)) -> dict:
    """基于向量的相似术语（查重视角：分数≥0.6 通常是近重复候选）。"""
    conn = get_conn()
    try:
        row = conn.execute("SELECT id FROM terms WHERE term_uid = ?", (term_uid,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"未找到术语 {term_uid}")
        vec_row = conn.execute(
            "SELECT vec FROM term_vectors WHERE term_id = ?", (row["id"],)
        ).fetchone()
        if not vec_row:
            raise HTTPException(status_code=503, detail="该术语无向量，请重跑 build_vectors.py")
        _vectors(conn)  # 确保缓存加载
        qvec = array.array("f", vec_row[0])
        top = _top_similar(conn, qvec, limit, exclude_id=row["id"])
        by_id = _rows_by_ids(conn, [tid for _, tid in top])
        items = []
        for score, tid in top:
            if tid in by_id:
                item = serialize_term(by_id[tid])
                item["score"] = round(score, 4)
                items.append(item)
        return {"term_uid": term_uid, "count": len(items), "items": items}
    finally:
        conn.close()


@app.get("/api/terms/{term_uid}/graph", summary="术语关系图谱（1跳）")
def term_graph(term_uid: str) -> dict:
    """术语 1 跳关系图：related / confused_with 的出边与入边。

    build_kb 已把可解析的中文名绑定为真实 target_term_id；
    未解析的以 label 节点返回（前端可按名搜索跳转）。
    """
    conn = get_conn()
    try:
        row = conn.execute(
            f"{term_base_select(conn)} WHERE t.term_uid = ?", (term_uid,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"未找到术语 {term_uid}")
        center_id = row["id"]
        edges_rows = conn.execute(
            """
            SELECT r.source_term_id, r.target_term_id, r.target_label, r.relation_type,
                   ts.term_uid AS source_uid, tt.term_uid AS target_uid
            FROM term_relations r
            JOIN terms ts ON ts.id = r.source_term_id
            LEFT JOIN terms tt ON tt.id = r.target_term_id
            WHERE r.source_term_id = ? OR r.target_term_id = ?
            """,
            (center_id, center_id),
        ).fetchall()
        node_ids = {center_id}
        edges = []
        label_nodes = []
        for e in edges_rows:
            if e["target_term_id"]:
                node_ids.add(e["source_term_id"])
                node_ids.add(e["target_term_id"])
                edges.append({
                    "source": e["source_uid"], "target": e["target_uid"],
                    "type": e["relation_type"], "resolved": True,
                })
            elif e["source_term_id"] == center_id:
                label_nodes.append(e["target_label"])
                edges.append({
                    "source": e["source_uid"], "target_label": e["target_label"],
                    "type": e["relation_type"], "resolved": False,
                })
        by_id = _rows_by_ids(conn, list(node_ids))
        return {
            "center": term_uid,
            "nodes": [serialize_term(r) for r in by_id.values()],
            "label_nodes": sorted(set(label_nodes)),
            "edges": edges,
        }
    finally:
        conn.close()


@app.post("/api/ingest/check", summary="术语在线校验（dry-run 不写入）")
def ingest_check(payload: list[dict] = Body(...)) -> dict:
    """只读 dry-run 校验：复用 scripts/ingest.py 的全部规则，不写入任何数据。

    Body: 术语对象数组（同 ingest.py check 的输入）。
    写入仍只能走本地 `python scripts/ingest.py add-terms`，API 保持只读边界。
    """
    if not payload:
        raise HTTPException(status_code=400, detail="请求体必须是非空数组，每个元素是一条术语对象")
    if len(payload) > 500:
        raise HTTPException(status_code=400, detail="单次最多校验 500 条")
    ing = _ingest_module()
    config = json.loads((ROOT / "config" / "volumes.json").read_text(encoding="utf-8"))
    rows = ing.read_csv_rows()
    errors, warnings, prepared = ing.validate_terms(payload, config, ing.existing_index(rows))

    # 语义近重（向量余弦）：字符级 SequenceMatcher 抓不到的「换词重复」在这里补上。
    # 仅警告不阻断；向量表缺失时静默跳过。
    semantic_dups = []
    try:
        conn = get_conn()
        try:
            vec_state = _vectors(conn)
            tv = _script("textvec")
            for obj in prepared:
                qvec = tv.finalize(
                    tv.raw_counts(tv.term_text(
                        obj.get("zh_term", ""), obj.get("en_term", ""), obj.get("definition_long", "")
                    )),
                    vec_state["idf"],
                )
                top = _top_similar(conn, qvec, 3)
                hits = [(s, tid) for s, tid in top if s >= 0.55]
                if hits:
                    by_id = _rows_by_ids(conn, [tid for _, tid in hits])
                    for s, tid in hits:
                        if tid in by_id:
                            semantic_dups.append({
                                "zh_term": obj.get("zh_term", ""),
                                "similar_to": by_id[tid]["zh_term"],
                                "term_uid": by_id[tid]["term_uid"],
                                "score": round(s, 3),
                            })
        finally:
            conn.close()
    except HTTPException:
        pass  # 向量表未构建：跳过语义查重

    return {
        "ok": not errors,
        "checked": len(payload),
        "errors": errors,
        "warnings": warnings,
        "semantic_dups": semantic_dups,
        "prepared_count": len(prepared),
        "assigned_uids": [o.get("term_uid", "") for o in prepared],
        "note": "dry-run：未写入任何数据。UID 为预演分配，实际以 ingest.py add-terms 入库结果为准。"
                "semantic_dups 为向量近重警告（≥0.55），请人工确认是否重复。",
    }


@app.get("/api/search", summary="全文搜索")
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
               OR t.definition_long LIKE ? OR t.prompt_usage LIKE ?
            GROUP BY t.id ORDER BY v.sequence_no, t.term_uid LIMIT ?
            """,
            (like, like, like, like, like, limit),
        ).fetchall()
        items = [serialize_term(r) for r in rows]
        return {"query": q, "count": len(items), "items": items, "engine": "like"}
    finally:
        conn.close()


@app.get("/api/stats", summary="全局统计")
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


@app.get("/api/export/prompts", summary="导出纯提示词清单")
def export_prompts(
    volume: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    format: str = Query("json", pattern="^(json|text)$"),
):
    """按筛选导出纯提示词清单，给提示词工程批量取用。"""
    conn = get_conn()
    try:
        where = ["t.en_term IS NOT NULL AND t.en_term != ''"]
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
            SELECT t.term_uid, t.zh_term, t.en_term, v.code AS volume_code
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
            lines.append(f"+ {r['en_term']}")
            lines.append(f"+ {r['zh_term']}")
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
                    "prompt_en": r["en_term"] or "",
                    "prompt_cn": r["zh_term"],
                }
                for r in rows
            ],
        }
    )


@app.post("/api/terms/batch", summary="批量获取术语详情")
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


@app.get("/api/terms/random", summary="随机术语")
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


@app.post("/api/prompts/combine", summary="组合提示词（SD/MJ方言）")
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
            SELECT t.term_uid, t.zh_term, t.en_term
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
            en = r["en_term"] or r["zh_term"]
            cn = r["zh_term"]
            terms_data.append({
                "term_uid": r["term_uid"],
                "zh_term": r["zh_term"],
                "prompt_en": en,
                "prompt_cn": cn,
            })
            if en:
                prompts_en.append(en)
            if cn:
                prompts_cn.append(cn)

        # 组合提示词（weighted 的写法随平台方言变化）
        if format == "comma":
            sep = ", "
        elif format == "newline":
            sep = "\n"
        else:  # weighted
            sep = ", "
            if payload.dialect == "mj":
                prompts_en = [f"{p}::1.1" for p in prompts_en]
                prompts_cn = [f"{p}::1.1" for p in prompts_cn]
            else:  # generic / sd 均用 SD 风格括号权重
                prompts_en = [f"({p}:1.1)" for p in prompts_en]
                prompts_cn = [f"({p}:1.1)" for p in prompts_cn]

        combined_en = sep.join(prompts_en)
        combined_cn = sep.join(prompts_cn)
        if payload.suffix:
            combined_en = (combined_en + " " + payload.suffix.strip()).strip()
            combined_cn = (combined_cn + " " + payload.suffix.strip()).strip()
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
            "dialect": payload.dialect,
            "count": len(terms_data),
            "requested_count": len(term_uids),
            "missing_term_uids": missing_term_uids,
            "terms": terms_data,
        }
    finally:
        conn.close()


@app.get("/api/terms/compare", summary="对比两个术语")
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


@app.get("/api/terms/{term_uid}", summary="术语详情")
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


@app.get("/api/terms/{term_uid}/related", summary="相关术语推荐")
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


@app.get("/api/volumes/{code}/categories/tree", summary="卷内分类树")
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


@app.get("/api/search/advanced", summary="高级搜索（按字段）")
def advanced_search(
    zh_term: Optional[str] = Query(None),
    en_term: Optional[str] = Query(None),
    definition: Optional[str] = Query(None),
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
        if definition:
            where.append("t.definition_long LIKE ?")
            params.append(f"%{definition}%")
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


@app.get("/", include_in_schema=False)
def root():
    """根路径直达前端页面；无前端产物时回退到 API 索引。"""
    if (WEB_DIR / "index.html").exists():
        return RedirectResponse(url="/app/", status_code=307)
    return api_index()


@app.get("/api", summary="API 端点索引")
def api_index() -> dict:
    return {
        "name": "AI视觉设计与提示词工程百科 API",
        "version": "2.1",
        "docs": "/docs",
        "web": "/app/" if (WEB_DIR / "index.html").exists() else None,
        "endpoints": [
            "/api/health", "/api/meta", "/api/tree", "/api/contract",
            "/api/volumes", "/api/tags",
            "/api/terms", "/api/terms/{term_uid}", "/api/terms/batch",
            "/api/terms/random", "/api/terms/{term_uid}/related",
            "/api/terms/compare", "/api/search", "/api/search/advanced",
            "/api/search/semantic", "/api/terms/{term_uid}/similar",
            "/api/terms/{term_uid}/graph",
            "/api/stats", "/api/export/prompts", "/api/prompts/combine",
            "/api/ingest/check",
            "/api/volumes/{code}/categories", "/api/volumes/{code}/categories/tree",
        ],
    }


# 把前端单页同源挂到 /app/ —— 浏览器打开 http://localhost:8000/app/ 即 API 模式。
if (WEB_DIR / "index.html").exists():
    from fastapi.staticfiles import StaticFiles

    app.mount("/app", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

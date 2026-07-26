"""视觉术语库 MCP Server —— 把知识库暴露为 AI 可直接调用的工具。

任何支持 MCP 的客户端（Claude Code / Claude Desktop 等）接入后，AI 即可：
- 读库选词：search_terms / get_term / get_tree / similar_terms
- 组合提示词：combine_prompts（含 SD/MJ 方言）
- 供稿自查：get_contract / check_terms / fill_queue（写入仍走本地 ingest.py，保持只读边界）

注册（项目根 .mcp.json 已配置）：
    { "mcpServers": { "visual-terms-kb": {
        "command": "./.venv/Scripts/python.exe", "args": ["scripts/mcp_server.py"] } } }

直读 SQLite（只读 URI），无需先启动 FastAPI。
"""
from __future__ import annotations

import array
import json
import sqlite3
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import textvec  # noqa: E402

mcp = FastMCP("visual-terms-kb")


def conn_ro() -> sqlite3.Connection:
    c = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def brief(r: sqlite3.Row) -> dict:
    return {
        "term_uid": r["term_uid"], "zh_term": r["zh_term"], "en_term": r["en_term"] or "",
        "volume_code": r["volume_code"], "category": r["category"] or "",
    }


BASE_SELECT = """
    SELECT t.id, t.term_uid, t.zh_term, t.en_term, v.code AS volume_code, c.name AS category
    FROM terms t JOIN volumes v ON v.id = t.volume_id
    LEFT JOIN categories c ON c.id = t.category_id
"""


@mcp.tool()
def search_terms(query: str, limit: int = 10, semantic: bool = False) -> list[dict]:
    """搜索术语。semantic=False 为字面匹配（名称/别名/释义 LIKE）；
    semantic=True 为向量模糊匹配（容忍换词，返回 score）。"""
    c = conn_ro()
    try:
        if not semantic:
            like = f"%{query}%"
            rows = c.execute(
                BASE_SELECT + """
                WHERE t.zh_term LIKE ? OR t.en_term LIKE ? OR t.definition_long LIKE ?
                   OR t.id IN (SELECT term_id FROM term_aliases WHERE alias LIKE ?)
                ORDER BY v.sequence_no, t.term_uid LIMIT ?
                """,
                (like, like, like, like, limit),
            ).fetchall()
            return [brief(r) for r in rows]
        idf_row = c.execute("SELECT value FROM vector_meta WHERE key='idf'").fetchone()
        if not idf_row:
            return [{"error": "向量表未构建，请运行 python scripts/build_vectors.py"}]
        idf = json.loads(idf_row[0])
        qvec = textvec.finalize(textvec.raw_counts(query), idf)
        scored = []
        for tid, blob in c.execute("SELECT term_id, vec FROM term_vectors"):
            v = array.array("f", blob)
            s = sum(a * b for a, b in zip(qvec, v))
            if s > 0.05:
                scored.append((s, tid))
        scored.sort(reverse=True)
        ids = [tid for _, tid in scored[:limit]]
        if not ids:
            return []
        ph = ",".join("?" for _ in ids)
        rows = {r["id"]: r for r in c.execute(BASE_SELECT + f" WHERE t.id IN ({ph})", ids)}
        return [dict(brief(rows[tid]), score=round(s, 3)) for s, tid in scored[:limit] if tid in rows]
    finally:
        c.close()


@mcp.tool()
def get_term(term_uid: str) -> dict:
    """按 UID 取术语完整详情（释义/视觉表现/用法/场景/标签/关联）。"""
    c = conn_ro()
    try:
        r = c.execute(
            BASE_SELECT + ", t.definition_long, t.visual_effect, t.prompt_usage, t.use_cases, t.status"
            " WHERE t.term_uid = ?", (term_uid,)
        ).fetchone()
        if not r:
            return {"error": f"未找到 {term_uid}"}
        rel = c.execute(
            "SELECT relation_type, COALESCE((SELECT term_uid FROM terms WHERE id=target_term_id), '') AS uid,"
            " target_label FROM term_relations WHERE source_term_id = ?", (r["id"],)
        ).fetchall()
        return {
            **brief(r),
            "definition_long": r["definition_long"] or "",
            "visual_effect": r["visual_effect"] or "",
            "prompt_usage": r["prompt_usage"] or "",
            "use_cases": [x for x in (r["use_cases"] or "").split(";") if x],
            "status": r["status"],
            "relations": [{"type": x["relation_type"], "term_uid": x["uid"], "label": x["target_label"]} for x in rel],
        }
    finally:
        c.close()


@mcp.tool()
def get_tree(volume: str = "") -> dict:
    """全库骨架：卷 + 分类路径 + 计数。volume 传 V01 等可只看一卷。
    AI 供稿前用它找空分支（term_count=0）。"""
    c = conn_ro()
    try:
        where, params = ("WHERE v.code = ?", [volume]) if volume else ("", [])
        vols = c.execute(
            f"SELECT v.code, v.title, v.target_terms, COUNT(t.id) AS current FROM volumes v "
            f"LEFT JOIN terms t ON t.volume_id=v.id {where} GROUP BY v.id ORDER BY v.sequence_no", params
        ).fetchall()
        cats = c.execute(
            f"SELECT v.code AS vcode, c.name, COUNT(t.id) AS n FROM categories c "
            f"JOIN volumes v ON v.id=c.volume_id LEFT JOIN terms t ON t.category_id=c.id "
            f"{where} GROUP BY c.id ORDER BY v.sequence_no, c.sort_order", params
        ).fetchall()
        by_vol: dict[str, list] = {}
        for r in cats:
            by_vol.setdefault(r["vcode"], []).append({"path": r["name"], "term_count": r["n"]})
        return {"volumes": [
            {"code": v["code"], "title": v["title"], "target": v["target_terms"],
             "current": v["current"], "categories": by_vol.get(v["code"], [])}
            for v in vols
        ]}
    finally:
        c.close()


@mcp.tool()
def similar_terms(term_uid: str, limit: int = 8) -> list[dict]:
    """向量相似术语（选词联想 / 查重视角，score≥0.6 多为近重复）。"""
    c = conn_ro()
    try:
        r = c.execute("SELECT id FROM terms WHERE term_uid = ?", (term_uid,)).fetchone()
        if not r:
            return [{"error": f"未找到 {term_uid}"}]
        row = c.execute("SELECT vec FROM term_vectors WHERE term_id = ?", (r["id"],)).fetchone()
        if not row:
            return [{"error": "无向量，请重跑 build_vectors.py"}]
        qvec = array.array("f", row[0])
        scored = []
        for tid, blob in c.execute("SELECT term_id, vec FROM term_vectors WHERE term_id != ?", (r["id"],)):
            v = array.array("f", blob)
            s = sum(a * b for a, b in zip(qvec, v))
            scored.append((s, tid))
        scored.sort(reverse=True)
        ids = [tid for _, tid in scored[:limit]]
        ph = ",".join("?" for _ in ids)
        rows = {x["id"]: x for x in c.execute(BASE_SELECT + f" WHERE t.id IN ({ph})", ids)}
        return [dict(brief(rows[tid]), score=round(s, 3)) for s, tid in scored[:limit] if tid in rows]
    finally:
        c.close()


@mcp.tool()
def combine_prompts(term_uids: list[str], language: str = "en", weighted: bool = False,
                    dialect: str = "generic", suffix: str = "") -> dict:
    """按 UID 顺序组合提示词。language: en/cn/both；weighted 加权重；
    dialect: generic/sd → (term:1.1)，mj → term::1.1；suffix 原样追加（如 '--ar 16:9'）。"""
    c = conn_ro()
    try:
        ph = ",".join("?" for _ in term_uids)
        rows = {r["term_uid"]: r for r in c.execute(
            f"SELECT term_uid, zh_term, en_term FROM terms WHERE term_uid IN ({ph})", term_uids)}
        missing = [u for u in term_uids if u not in rows]
        ens, cns = [], []
        for u in term_uids:
            if u not in rows:
                continue
            r = rows[u]
            en, cn = r["en_term"] or r["zh_term"], r["zh_term"]
            if weighted:
                en = f"{en}::1.1" if dialect == "mj" else f"({en}:1.1)"
                cn = f"{cn}::1.1" if dialect == "mj" else f"({cn}:1.1)"
            ens.append(en)
            cns.append(cn)
        en_s, cn_s = ", ".join(ens), ", ".join(cns)
        if suffix:
            en_s = (en_s + " " + suffix.strip()).strip()
            cn_s = (cn_s + " " + suffix.strip()).strip()
        combined = en_s if language == "en" else cn_s if language == "cn" else (en_s + "\n" + cn_s)
        return {"combined": combined, "combined_en": en_s, "combined_cn": cn_s, "missing": missing}
    finally:
        c.close()


@mcp.tool()
def get_contract() -> dict:
    """供稿契约：term JSON Schema + 各卷顶层分类白名单 + 提交流程。"""
    schema = json.loads((ROOT / "schema" / "term.schema.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "config" / "volumes.json").read_text(encoding="utf-8"))
    return {
        "term_schema": schema,
        "volumes": [{"code": v["code"], "title": v["title"],
                     "allowed_top_categories": v.get("categories", [])} for v in config["volumes"]],
        "workflow": "get_tree 找空分支 → 生成 terms 数组 → check_terms 校验 → "
                    "本地 python scripts/ingest.py add-terms terms.json 入库（MCP 不提供写入）",
    }


@mcp.tool()
def check_terms(terms: list[dict]) -> dict:
    """术语数组 dry-run 校验（Schema/白名单/查重/占位检测），不写入任何数据。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("kb_ingest", ROOT / "scripts" / "ingest.py")
    ing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ing)
    config = json.loads((ROOT / "config" / "volumes.json").read_text(encoding="utf-8"))
    errors, warnings, prepared = ing.validate_terms(terms, config, ing.existing_index(ing.read_csv_rows()))
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "assigned_uids": [o.get("term_uid", "") for o in prepared]}


@mcp.tool()
def fill_queue(volume: str = "", count: int = 30) -> str:
    """填充优先级。不传 volume 返回缺口榜（JSON）；传卷号返回该卷供稿工单全文。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("kb_fillq", ROOT / "scripts" / "fill_queue.py")
    fq = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fq)
    queue, config = fq.load()
    if not volume:
        return json.dumps(queue[:15], ensure_ascii=False, indent=1)
    return fq.make_order(queue, config, volume, count, None)


if __name__ == "__main__":
    mcp.run()

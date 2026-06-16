# 工作流

## 采集

1. 先在 `data/raw/terms_seed.csv` 中添加术语。
2. 每个分卷可以后续拆成独立 CSV，例如 `data/raw/V01_photography.csv`。
3. 同义词、标签、相关术语统一用半角分号 `;` 分隔。

## 构建

```powershell
python scripts/build_kb.py
```

构建脚本会执行：

- 初始化 SQLite schema。
- 从 `config/volumes.json` 同步卷册、分类和跨卷关系。
- 从 CSV 导入术语。
- 拆分术语文本块，生成 RAG/向量库预处理 JSONL。
- 输出 Markdown 术语页和卷册统计。

## 校验

```powershell
python scripts/validate_kb.py
```

校验脚本检查：

- 卷册目标总量是否为 10,000。
- `term_uid` 是否唯一。
- 必填字段是否为空。
- 同一卷内是否有重复中文术语。
- 是否存在没有定义或没有分类的条目。

## 检索

```powershell
python scripts/search_terms.py "赛博朋克"
```

本地检索优先使用 SQLite FTS5；如果当前 SQLite 不支持 FTS5，会自动退回到普通 `LIKE` 查询。

## 向量库接入

`data/exports/terms_for_rag.jsonl` 是向量库入口。每一行是一个可 embedding 的文本块，包含：

- `chunk_uid`
- `term_uid`
- `zh_term`
- `en_term`
- `volume_code`
- `volume_title`
- `category`
- `chunk_type`
- `content`

推荐做法：用 SQLite/CSV 维护权威数据，用 Qdrant、Chroma、FAISS 或其他向量库保存 embedding 索引。


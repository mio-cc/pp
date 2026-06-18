# 数据契约 — terms_seed.csv（v2 · 16 列）

> 核心理念：**原子化术语的名字本身就是提示词**——`zh_term`=中文提示词，`en_term`=英文提示词。
> 因此不再有 `positive_prompt` / `definition_short` 等列（v2 已从 21 列精简为 16 列）。

唯一采集入口：`data/raw/terms_seed.csv`（UTF-8 BOM）。**强烈建议不要手改 CSV**，改用接口：
`python scripts/ingest.py add-terms terms.json`（见 `docs/templates/` 与 `docs/ai-contributor-guide.md`）。
若必须手改：改完跑 `python scripts/rebuild.py` 重建，再 `python scripts/validate_kb.py` 校验。

## 字段（16 列，顺序固定）

| # | 字段 | 必填 | 卡片展示 | 说明 |
|---|------|------|----------|------|
| 1 | term_uid | 是 | 是(副标题) | `V{XX}_T{NNNN}`，卷内唯一递增 |
| 2 | zh_term | 是 | 是(标题=中文提示词) | 中文名，原子最小单位 |
| 3 | en_term | 是 | 是(副标题=英文提示词) | 英文名 |
| 4 | aliases | 否 | 否(仅搜索) | 别名，`;` 分隔 |
| 5 | volume_code | 是 | 是(路径) | 卷册代码 V01–V15 |
| 6 | category | 是 | 是(路径) | 分类路径，` / ` 分隔，深度不限 |
| 7 | definition_long | 是 | 是 | 详细解释（建议 100–200 字，硬下限 1 字） |
| 8 | visual_effect | 是 | 是 | 视觉表现 |
| 9 | prompt_usage | 是 | 是 | 提示词用法 |
| 10 | use_cases | 是 | 是 | 适用场景，`;` 分隔 |
| 11 | related_terms | 否 | 否 | 相关术语（中文名），`;` 分隔 |
| 12 | confused_with | 否 | 否 | 易混淆术语，`;` 分隔 |
| 13 | tags | 是 | 是 | 标签，`;` 分隔 |
| 14 | source_refs | 否 | 否 | 来源 |
| 15 | status | 是 | 否 | draft/review/published/deprecated |
| 16 | version | 是 | 否 | 版本号 |

## 核心约束

- **名字即提示词**：不要再写正向/负向提示词列（已删）。术语名要足够原子、具体，本身可直接当提示词粘贴。
- **分类即路径，深度不限**：`category` = `顶层分类 / 子类 / … / 叶子`。顶层段**必须**是 `config/volumes.json` 中该卷声明的分类；其后自由分支；末端是原子叶子。
- **术语原子化**：每条是可直接复制、无歧义的最小概念。笼统词（焦距/颜色/色温）必须沿路径分支拆细。
- **同叶子互斥**：同一最深路径下的术语互为可选项（仅前端视觉提示，API 不做冲突检测）。
- **definition_long 必须是真定义**：不得等于 `zh_term`、不得写占位（待补充/TODO/简短定义）。
- **同卷 zh_term 唯一、term_uid 全局唯一**。

## 权威源与校验

SQLite 主库是唯一权威源；Markdown / JSONL / 前端 JSON / API 都是导出物。写入只走「ingest 接口（或改 CSV）→ rebuild」可追溯流程，API 只读。
`scripts/validate_kb.py` 会强校验：必填非空、term_uid 格式/前缀/唯一、同卷 zh 唯一、顶层分类∈config、status 取值、definition_long 非复读非占位、每条≥1 tag。visual_effect/prompt_usage/use_cases 暂为警告（存量豁免，新增经 ingest 硬卡）。

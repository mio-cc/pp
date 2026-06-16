# 数据契约

## Dataset

- Name: AI视觉设计与提示词工程百科术语库
- Owner/team: 个人知识库项目
- Source system: `data/raw/terms_seed.csv` 与后续分卷 CSV
- Consumers: SQLite 查询、Markdown 百科页、RAG/向量库、未来 DOCX/PDF/EPUB 导出

## 主键与粒度

- 粒度：一行代表一个术语条目。
- 主键：`term_uid`，建议格式为 `V01_T0001`。
- 术语可以跨卷关联，但每条术语必须有一个主归属卷 `volume_code`。

## 核心字段

| 字段 | 类型 | 必填 | 语义 |
| --- | --- | --- | --- |
| `term_uid` | text | 是 | 稳定 ID，不随中文名变化 |
| `zh_term` | text | 是 | 中文术语 |
| `en_term` | text | 否 | 英文术语或行业通用表达 |
| `aliases` | text | 否 | 别名，用 `;` 分隔 |
| `volume_code` | text | 是 | 所属卷册，如 `V02` |
| `category` | text | 是 | 卷内一级分类 |
| `definition_short` | text | 是 | 一句话解释 |
| `definition_long` | text | 否 | 百科型长解释 |
| `visual_effect` | text | 否 | 在画面中的视觉表现 |
| `prompt_usage` | text | 否 | 适合放入提示词的表达 |
| `positive_prompt` | text | 否 | 正向提示词示例 |
| `negative_prompt` | text | 否 | 负向提示词或规避项 |
| `use_cases` | text | 否 | 适用场景，用 `;` 分隔 |
| `related_terms` | text | 否 | 相关术语，用 `;` 分隔 |
| `confused_with` | text | 否 | 易混淆术语，用 `;` 分隔 |
| `tags` | text | 否 | 标签，用 `;` 分隔 |
| `source_refs` | text | 否 | 来源、书籍、课程或内部整理说明 |
| `status` | text | 是 | `draft`、`review`、`published`、`deprecated` |
| `version` | text | 是 | 如 `V1.0` |

## 质量规则

- `term_uid` 必须唯一。
- `zh_term + volume_code` 不建议重复。
- `volume_code` 必须存在于 `config/volumes.json`。
- `definition_short` 建议不为空。
- `status` 只能取 `draft/review/published/deprecated`。
- 别名、标签、相关术语统一用半角分号 `;` 分隔。

## 变更管理

- 新增字段先更新本文件，再更新 `schema/` 和 `scripts/`。
- 批量导入前保留原始 CSV。
- 生成物可重建，权威内容应回写到 `data/raw/` 或数据库导出流程中。


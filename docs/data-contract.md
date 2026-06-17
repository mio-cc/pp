# 数据契约 — terms_seed.csv

唯一采集入口：`data/raw/terms_seed.csv`（UTF-8 BOM，多值用英文分号 `;`）。
改完跑 `python scripts/build_kb.py` 重建，再用 `python scripts/validate_kb.py` 校验。

## 字段（21 列，顺序固定）

| # | 字段 | 必填 | 说明 |
|---|------|------|------|
| 1 | term_uid | 是 | `V{XX}_T{NNNN}`，卷内递增 |
| 2 | zh_term | 是 | 中文名（原子、具体） |
| 3 | en_term | 是 | 英文名 |
| 4 | aliases | 否 | 别名，`;` 分隔 |
| 5 | volume_code | 是 | 卷册代码 V01–V15 |
| 6 | category | 是 | **分类路径**，` / ` 分隔，深度不限（分支到原子层） |
| 7 | definition_short | 是 | 真实一句话定义，解释术语含义/作用/视觉特征；禁止复读术语名或写占位 |
| 8 | definition_long | 是 | 详细解释 |
| 9 | visual_effect | 是 | 视觉表现 |
| 10 | prompt_usage | 是 | 提示词用法 |
| 11 | positive_prompt | 是 | 正向提示词（英文） |
| 12 | negative_prompt | 否 | 负向提示词（英文） |
| 13 | positive_prompt_cn | 是 | 正向提示词（中文，与英文对应） |
| 14 | negative_prompt_cn | 否 | 负向提示词（中文，与英文对应） |
| 15 | use_cases | 是 | 适用场景，`;` 分隔 |
| 16 | related_terms | 否 | 相关术语（中文名），`;` 分隔 |
| 17 | confused_with | 否 | 易混淆术语 |
| 18 | tags | 是 | 标签，`;` 分隔 |
| 19 | source_refs | 否 | 来源 |
| 20 | status | 是 | draft/review/published/deprecated |
| 21 | version | 是 | 版本号 |

## 核心约束

- **分类即路径，深度不限**：`category` = `顶层分类 / 子类 / … / 叶子`。顶层段须是 config/volumes.json 中该卷的分类；
  其后自由分支。系统按 ` / ` 递归建树。
- **术语原子化**：每条术语是可直接复制、无歧义的最小概念。笼统词必须沿路径分支拆细
  （如 `… / 镜头畸变` → 桶形畸变 / 枕形畸变；`… / 定焦镜头` → 35mm / 50mm / 85mm）。
- **同叶子互斥**：同一最深路径下的术语互为可选项；前端篮中并存会标红（仅视觉提示，不阻断复制；API 不做冲突检测）。
- **提示词中英双语并存、与术语对应**：只用 positive(英) + positive_prompt_cn(中)，一一对应到术语本身；**不用负向**，negative 两列留空、前端不展示。
- **短定义必须是真定义**：`definition_short` 不得等于 `zh_term`，不得写 `术语名 + 。`、`术语名的简短定义。`、`待补充`、`TODO` 等占位文本。
- 含英文逗号的提示词字段在 CSV 中必须用双引号包裹；列表字段用 `;` 分隔。

## 权威源

SQLite 主库是唯一权威源；Markdown / JSONL / 前端 JSON / API 都是导出物。写入只走「改 CSV → build」可追溯流程，API 只读。

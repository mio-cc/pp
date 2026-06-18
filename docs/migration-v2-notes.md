# v2 迁移说明：关键约束 / 风险点 / 潜在 bug

记录「名字即提示词 + 16 列 + 接口化」迁移（21→16 列）的约束、已处理风险与待观察项。

## 一、关键约束（已由 validate_kb + ingest 强制）

- **结构固定 16 列**，名字即提示词：不存在 positive_prompt/definition_short/negative 列。
- term_uid 必须 `V##_T####`、卷内唯一递增、前缀与卷一致；**全局唯一**。
- 同卷 `zh_term` 唯一。
- `category` 顶层段必须 ∈ `config/volumes.json` 该卷声明；路径用 ` / `，无空层。
- `definition_long` 必填、**不得复读 zh_term**、不得占位（待补充/TODO/TBD/简短定义）。
- `status` ∈ {draft,review,published,deprecated}；每条术语 ≥1 个 tag。
- ingest 额外硬卡：必填非空、多值必须是数组、term_uid 空则自动分配、新增查重（同名拒绝/近似警告）。
- 软约束（warning，存量豁免、新增经 ingest 硬卡）：visual_effect / prompt_usage / use_cases 非空。

## 二、风险点筛查（迁移中发现并已处理）

1. **数据丢失风险**：1545 条术语只有 definition_short、definition_long 为空；直接删 short 会丢定义。
   → 已做 `definition_long = long 非空 ? long : short` 合并迁移，definition_long 空值=0，零丢失。
2. **受限挂载禁止删除**：build_kb 的 `unlink()` 在 mount 上报 PermissionError；就地截断后 sqlite 增量写又报 `disk I/O error`。
   → 新增 `scripts/rebuild.py`：临时目录(tmpfs)全新构建 → 整体 `copyfile` 回写 → 清 -wal/-shm/-journal sidecar。manage.sh build 已改指向它。
3. **大文件编辑截断**：用 Edit/Write 工具改 build_kb.py/app.py 会被 mount 同步截断（已实际踩坑，build_kb 一度截断在 849 行）。
   → 所有大文件改动改用 bash heredoc 整文写 + `ast.parse` 校验 + 残留字段断言。
4. **前端原生依赖不匹配**：node_modules 为宿主 OS 安装，rollup 缺 linux 原生二进制，vite build 失败。
   → 安装 `@rollup/rollup-linux-x64-gnu`（glibc 2.35），构建通过；产物自检无 positive_prompt。
5. **vite emptyOutDir 需删除权限**：已开启该文件夹删除权限，旧 web/assets 清理正常。
6. **列表 vs 详情字段差异**：`/api/terms` 列表不返回长字段；卡片在 **API 模式** 经新增的 `kb.termDetail()` 拉 `/api/terms/{uid}` 补全；**离线模式** 的 web JSON 已含全部 16 字段，卡片直接可用。

## 三、潜在 bug / 待观察

1. **名字即提示词的质量依赖**：弃用了旧 positive_prompt 里更丰富的关键词（如 "85mm lens, portrait, creamy bokeh"），改用 en_term/zh_term 当提示词。若个别术语名不足以独立成提示词，建议把关键信息并入术语名或 definition。当前 1611 条 en_term 均非空，质量建议抽查。
2. **存量空字段**：visual_effect/prompt_usage/use_cases 各 1545 条为空（warning）。卡片对空字段用 `v-if` 隐藏，不会显示空块；建议后续用 ingest 逐卷回填。
3. **ingest 写入后重建失败的中间态**：add-terms 先写 CSV 再 rebuild；若 rebuild 因环境失败，CSV 已写入但库未更新。ingest 会报错提示；可重跑 `python scripts/rebuild.py` 或从 git 还原 CSV。
4. **运行期依赖 jsonschema**：ingest 用 jsonschema(3.2.0, Draft7) 做格式校验；缺失时会提示 `pip install jsonschema --break-system-packages`。API/build/validate 不依赖它。
5. **近似查重阈值**：difflib 比率 0.86，可能漏报或误报，仅警告不阻断，靠人工确认。
6. **term_uid 自动分配**：按该卷 CSV 现有最大号 +1，不回填空洞；跨批多次 add-terms 安全。
7. **legacy 脚本**：`scripts/legacy/` 下旧生成器仍按 21 列写法，**勿运行**，否则引回废弃列；新增一律走 ingest。

## 四、最终验证结果

validate_kb 通过(0 error)；11/11 接口 200；terms=1611；ingest check/add-terms/add-volume 三场景通过；前端 vite 构建产物无旧字段；manage.sh build 指向 rebuild.py。

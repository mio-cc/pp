# 填充纪律与质检规程（Fill Discipline & QC）

> 本文件是本项目术语补全工作的**唯一章程**。任何 AI 模型按本章程产出 JSON，
> 经 `scripts/ingest.py` 校验入库。目标是：在补齐 20,700 条目标的同时，
> **边界清晰、格式统一、质量不注水**。
>
> 本文件为文档，非代码。不修改任何 `.py` / `.vue` / `.json`（config 仅经 `add-volume` 接口改）。

---

## 〇、总原则

1. **只走接口，不改代码**：写入唯一入口是 `python scripts/ingest.py`。
   禁止手改 `data/raw/terms_seed.csv`、禁止改任何源码、禁止经 API 写库（API 只读）。
2. **原子写入、先检后填**：每批先 `check` 确认全过，再 `add-terms`。
   任一错整批不写，无需人工回滚（接口自带 CSV/主库回滚）。
3. **质量优先于数量**：达标率优先于填条数。宁可少填，不可注水。
4. **可溯源**：每批 JSON 经接口写入后，主库与 exports 由 `rebuild` 自动回写。

---

## 一、边界（什么能填、什么不能）

### 1.1 三层结构

| 层 | 创建方式 | 接口 | 说明 |
|----|---------|------|------|
| **卷（体系）** | 先 `add-volume 新卷.json` 注册卷 + 顶层分类 | `ingest.py add-volume` | 直接写 `config/volumes.json` |
| **中间层（分类路径）** | 术语 JSON 的 `category` 字段写整条路径 | `add-terms`（随术语） | build 时整条路径当 1 个节点入 `categories` 表；中间分支无需预注册，写更深路径自动建 |
| **原子术语** | 一条 JSON 对象，`zh_term` = 路径末端的叶子 | `add-terms` | 入库 `terms` 表，挂到对应 `category_id` |

### 1.2 硬边界（接口强制，违反即整批拒绝）

- `volume_code` 必须已在 `config/volumes.json` 注册（当前 **V01–V38 共 38 卷**，文档旧表 V01–V15 已过时，以 config 为准）。
- `category` 用 ` / `（空格-斜杠-空格）分隔：
  - **首段（顶层）必须 ∈ 该卷 config 声明的 `categories`**；
  - 不得有空层；不得用逗号；深度不限。
- `term_uid` 留空自动分配（按该卷最大号+1）；手填须 `V##__T####` 且前缀与卷一致。
- 同卷 `zh_term` 完全相同 → 拒绝；高度相似（>0.86）→ 警告。
- `status` ∈ `draft / review / published / deprecated`。
- `definition_long` 不得复读 `zh_term`、不得含 `待补充/TODO/TBD/简短定义`。
- 每个术语至少 1 个 `tag`、至少 1 个 `use_cases`。

### 1.3 结构性边界（需自行判断，接口不卡）

- **原子化**：笼统词（焦距 / 颜色 / 色温 / 镜头畸变）是**分支名不是术语**。
  术语必须是可直接复制、无歧义的最小概念（如 `85mm人像`、`深红色`、`暖色温3200K`）。
- **互斥靠结构**：互斥取值放进同一最深分类下（35mm/50mm/85mm 同在 `…/定焦镜头`），天然互为可选项。
- **不重复造轮子**：新增前先扫该卷已有 `zh_term`，避免与既有术语实质近义。

---

## 二、格式（每条术语 16 字段规范）

### 2.1 必填（11 个，非空）

`zh_term`（中文提示词）· `en_term`（英文提示词）· `volume_code` · `category`
· `definition_long` · `visual_effect` · `prompt_usage` · `use_cases[]`
· `tags[]` · `status` · `version`

### 2.2 选填

`term_uid`（留空）· `aliases[]` · `related_terms[]` · `confused_with[]` · `source_refs`（默认「整理」）

### 2.3 多值字段一律写**数组**，接口自动转 CSV 的 `;`

`aliases / use_cases / related_terms / confused_with / tags` —— **不要写分号字符串**。

### 2.4 命名即提示词

`zh_term` = 中文提示词，`en_term` = 英文提示词，二者本身应可直接粘进
Stable Diffusion / Midjourney / DALL·E。

---

## 三、质量门槛（接口不卡，本章程强制）

> 实测：存量 2043 条中约 59% 的 `definition_long` 不足 30 字（历史注水）。
> 本章程对**新增**术语执行以下门槛，杜绝继续注水。

| 字段 | 门槛 | 禁止 |
|------|------|------|
| `definition_long` | **≥40 字**；讲清「是什么 / 原理或由来 / 对画面的影响 / 典型用法」 | 禁止复读名字、禁止套话（「这是XX高频术语。」「适用于各种场景。」）、禁止占位 |
| `visual_effect` | **≥15 字**；必须描述「画面长什么样」 | 禁止写成用途、禁止空泛（「视觉效果很好」） |
| `prompt_usage` | **≥15 字**；必须说明「提示词里怎么用、强调什么、配合哪些词/参数」 | 禁止与 definition 重复、禁止空泛 |
| `en_term` | 须为**像真能粘进生图工具的英文表述**，对应 `zh_term` | 禁止机翻乱码、禁止拼音硬凑、禁止留空 |
| `use_cases` / `tags` | 至少 1 项，且与术语语义贴合 | 禁止堆无关标签凑数 |

**自检清单（每条提交前逐条过）：**
- [ ] `zh_term` 是原子最小单位，不是笼统分支词？
- [ ] `category` 首段 ∈ 该卷 config 声明？
- [ ] `definition_long` ≥40 字且非套话、非复读？
- [ ] `visual_effect` / `prompt_usage` ≥15 字且各司其职？
- [ ] `en_term` 是真英文提示词、非机翻？
- [ ] 同卷无 `zh_term` 实质重复？

---

## 四、定时检测（QC 节奏）

1. **每批**：先 `check` 后 `add-terms`，看校验输出逐条过。
2. **每满 5 批 或 每切一卷**：跑一次质检脚本 `scripts/qc_terms.py`（只读，不改代码/不改库），统计：
   - `definition_long` <40 字占比、<30 字占比；
   - `visual_effect` / `prompt_usage` <15 字条数；
   - `en_term` 异常（<2 字 / 含中文字符）条数；
   - `definition` 套话条数；
   - `volume_code` 未注册条数。
   列出不达标 `term_uid`，用 `update-terms` 回填修正（不改代码）。
   - 全量：`python scripts/qc_terms.py`
   - 某卷：`python scripts/qc_terms.py --vol V04`
   - 本会话新增精确范围：`python scripts/qc_terms.py --since V04_T0111`
3. **进度监控**：每次 `add-terms` 后看 `validate_kb.py` 的 Volume Progress，
   确保按「缺口从大到小」推进，最终 38 卷全部接近 `target_terms`。

---

## 五、标准工作流（每批）

```bash
# 0. 设 UTF-8 输出（避开 GBK 控制台 ✓/⚠ 编码坑）
export PYTHONIOENCODING=utf-8      # Windows: set PYTHONIOENCODING=utf-8

# 1. 选该卷一个分支，生成 20–40 条 JSON（数组，多值用数组）
# 2. 先校验，不写库
python scripts/ingest.py check  批次.json
# 3. 全过后再入库（自动：写CSV → rebuild → 再校验 → 失败回滚）
python scripts/ingest.py add-terms 批次.json
# 4. 看 validate_kb.py 的 Volume Progress 确认进度
python scripts/validate_kb.py
```

---

## 六、优先级策略

- **顺序**：按缺口从大到小 —— V04 → V08 → V36 → V02 → V37 → V12 → V14 → V10 → V17 → V16 → … 填满 38 卷。
- **批次**：每批 20–40 条（原子写入，整批回滚，批太大出错成本高、太小效率低）。
- **零卷优先**：V27–V38 共 12 卷当前为 0 条，按缺口排到时集中做起来。

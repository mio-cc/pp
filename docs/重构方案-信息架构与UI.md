# 重构方案 — 信息架构与 UI（2026-07）

> 目标：把「体系 → 分类 → 子分支 → 术语」的上下层级做实做稳；UI 去掉 AI 味（渐变、毛玻璃、悬浮动画、胶囊卡片），换成克制的工具风；结构上易扩展、易于 AI 自主填写、易于程序化 API 调用。
> 配套样例：`docs/重构样例-UI.html`（自包含，双击即看，即目标形态）。

---

## 一、现状诊断（基于通读全部代码得出）

**做得对、要保留的：**
- SQLite 唯一权威源 + 只读 API + 「ingest → rebuild」可追溯写入链路，架构分层清晰。
- `category` 为不限深度的路径（` / ` 分隔），顶层白名单在 `config/volumes.json`——这个模型本身就是可扩展的，不需要推翻。
- trigram FTS + 分页 + 分卷懒加载导出，十万级容量设计成立。
- `ingest.py check/add-terms/add-volume/update-terms` 已经是 AI 友好的写入接口。

**要修的问题：**

| # | 问题 | 位置 |
|---|------|------|
| 1 | `frontend/src/components/` 四个组件（SideTree/TermGrid/DetailDrawer/PromptDock）**无任何引用，是死代码**；实际全部逻辑挤在 483 行的 `App.vue` 里 | frontend/src |
| 2 | UI 有明显 AI 味：body 双径向渐变背景、`backdrop-filter` 毛玻璃、hover `translateY` 悬浮、胶囊圆角卡片、弹性 toast、悬浮 dock、装饰性 Unicode 图标（◆ ⌘ ∅） | style.css、App.vue |
| 3 | 侧栏树靠**拉全卷术语后前端建树**（`loadVolumeTerms` 翻页拉完整卷），与「懒加载」设计相悖；服务端已有 `/api/volumes/{code}/categories/tree` 却没用 | useKB.js |
| 4 | `/api/terms` 的 `category_prefix` 用 `LIKE 'prefix%'` 无边界，`布光` 会误中 `布光与用光`；而 `/api/terms/random` 的同名参数有 ` / ` 边界——**两处行为不一致** | api/app.py:371 vs 124 |
| 5 | 无 URL 路由：当前视图不可分享、不可回退、AI/爬虫无法直达某分类或术语 | App.vue |
| 6 | `style.css` 残留 `.arco-btn-primary` 覆写（Arco 已移除）；README 架构图仍写「Vue 3 + Arco」 | style.css、README |

---

## 二、信息架构：层级不定深，只定三种角色

数据模型不动（仍是 volume + category 路径 + term）。**不固定层数**——层级深度由内容自然决定，可以是 `卷 / 分类 / 术语` 两段路径，也可以是 `卷 / 分类 / a / b / c / 术语` 任意深。定形的不是层数，而是路径上每个节点的**角色**，全库只有三种：

```
卷      volume         V01–V38，config/volumes.json 注册，AI 通过 add-volume 扩展
分支    category 路径   首段须在该卷 config 白名单内（ingest 强校验），
                       其后自由分支、深度不限，写更深路径即自动建层
术语    term           原子叶子，名字即提示词，永远挂在某条路径末端
```

规则（已有约定，正式定形为契约）：
- **节点单一职责**：一个路径节点要么继续分支、要么直接挂术语，不混放。
- **同叶互斥**：同一最深路径下的术语互为可选项（UI 冲突提示的依据）。
- **扩展即写路径**：加术语 → 挂到叶子；嫌某层太粗 → 直接写更深的路径，层就长出来了；加专业方向 → config 增顶层分类；加领域 → add-volume。不存在「层数上限」这种需要改代码的扩展。
- **UI/API 必须深度无关**：树递归渲染、面包屑按段生成、`category_prefix` 按路径前缀过滤——任何组件不得假设固定层数（样例 HTML 已按此实现，`镜头与光学 / 焦距 / 定焦镜头` 三段与 `曝光控制 / 光圈` 两段同一套代码渲染）。

---

## 三、UI 重构（核心交付，见样例 HTML）

### 3.1 设计原则（反 AI 味清单）

| 禁止 | 替代 |
|------|------|
| 渐变（背景/文字/边框） | 纯色纸面 `#f7f7f5` + 白面板 |
| 毛玻璃 backdrop-filter | 实心面板 + 1px 分隔线 |
| hover 位移/缩放/弹性动画 | 仅背景色变化，无位移 |
| 圆角胶囊卡片瀑布 | **表格行**呈现术语（术语库本质是词典，词典是表不是卡片墙） |
| 大圆角 + 多层阴影 | 圆角 0–2px，全局禁 box-shadow |
| 装饰图标/emoji | 纯文字 + 少量语义色块（状态点） |
| 多彩标签 | 单一强调色，只用于「当前选中/可点击/主按钮」 |

### 3.2 视觉基调

- **色**：纸白 + 墨黑两级灰 + 唯一强调色**印章红 `#9a3b26`**（选它而非蓝色：符合中文词典气质，且和常见 AI 生成页的蓝紫系拉开距离）。状态色仅三枚小方块：published 绿 / review 黄 / draft 灰。
- **字**：UI 与正文用系统无衬线；**词头（术语中文名）用衬线**（宋体系），一眼词典感；英文提示词、UID、计数一律等宽字体——数据感靠等宽，不靠装饰。
- **层级表达全部交给排版**：缩进、字号、字重、1px 线，不用色块和阴影表层级。

### 3.3 布局（三栏一底，全部常驻，无悬浮层）

```
┌──────────────────────────────────────────────────────┐
│ 顶栏：库名 · 统计 · 搜索 · 模式标识            48px │
├──────────┬──────────────────────────┬────────────────┤
│ 树        │ 面包屑（路径本体，段段可点）│ 术语详情        │
│ L0/L1/L2 │ 子分支链接行              │ （词典条目式，   │
│ 缩进+计数 │ 术语表格：中文│英文│UID│状态│  常驻右栏，     │
│          │                          │  不再抽屉弹出）  │
├──────────┴──────────────────────────┴────────────────┤
│ 提示词栏：已选词 · EN/中/中英 · 复制           44px │
└──────────────────────────────────────────────────────┘
```

关键决策：
- **详情从「悬浮抽屉」改为常驻右栏**——词典的查-比-选是并行动作，不该互相遮挡；也消灭了一个浮层。
- **提示词篮从悬浮 dock 改为底部通栏**——它是工作台不是气泡。
- **面包屑就是分类路径本身**（`V01 摄影体系 / 曝光控制 / 光圈`），所见即数据，人和 AI 读到的是同一条 category。

### 3.4 前端工程落地

1. `App.vue` 拆为 5 个真实使用的组件：`TreeNav / Breadcrumb / TermTable / TermDetail / PromptBar`；删除现有 4 个死组件。
2. 树的结构改用 `/api/volumes/{code}/categories/tree`（结构与计数），术语只在点到叶子时按 `category` 精确拉取——不再全卷拉取建树。
3. 加 hash 路由：`#/V01`、`#/V01/曝光控制/光圈`、`#/term/V01_T0001`。可分享、可回退，AI 可以直接构造 URL 直达。
4. `style.css` 重写为设计令牌（样例 HTML 的 `:root` 即令牌清单），删除渐变与 arco 残留。

---

## 四、API 补强（面向 AI 与程序调用）

只读边界不动，补三个端点、修一处不一致：

1. **修** `/api/terms` 的 `category_prefix`：与 random 对齐为 `(c.name = ? OR c.name LIKE ? || ' / %')`，消除「布光」误中「布光与用光」。
2. **增 `GET /api/tree`**：一次返回全库骨架（38 卷 × 全部分类路径 × 计数，无正文，约几十 KB）。前端首屏、AI 探索共用，替代逐卷点开。
3. **增 `GET /api/contract`**：返回 `schema/term.schema.json` + 每卷允许的顶层分类 + ingest 流程说明。AI 供稿前 `GET /api/contract` 一次即可自查规则，不再依赖读仓库文件。
4. **增 `POST /api/ingest/check`**：纯校验 dry-run（复用 `ingest.py` 校验逻辑，不写库，不破只读原则）。AI 生成 JSON 后先在线校验，全过再由人执行 `add-terms`。

## 五、AI 自主填写链路（定形为标准回路）

```
GET /api/tree          看结构，找空分支（count=0 或目标未达的卷）
GET /api/contract      拿字段规则 + 该卷顶层白名单
生成 terms.json         （数组，字段照契约）
POST /api/ingest/check 在线校验，报错则修
python scripts/ingest.py add-terms terms.json   写入（唯一落库通道，人触发）
python scripts/rebuild.py                        重建导出物
```

这个回路里 AI 需要的一切都是机器可读的（tree/contract/check 全是 JSON），且写入永远走同一条可追溯通道。

## 六、实施顺序

| 阶段 | 内容 | 改动面 | 状态 |
|------|------|--------|------|
| P0 | 样例 HTML 定稿，确认视觉方向（黑白灰 · 融合布局） | docs/ | ✅ 完成 |
| P1 | 前端重构：设计令牌 + 拆 8 组件 + 删 4 个死代码组件 + Lucide 图标 | frontend/ | ✅ 完成 |
| P2 | API：修 category_prefix 边界，增 tree / contract / ingest.check | api/app.py | ✅ 完成 |
| P3 | hash 路由与深链（`#/V01/曝光控制/光圈/@V01_T0001`，可分享可回退） | frontend/ | ✅ 完成 |
| P4 | 文档同步（README 架构与端点表、API 指南 v2.2、AI 供稿指南在线回路） | docs/ | ✅ 完成 |

实施说明：P1 保留了「拉全卷建树」的数据流（API/离线双模式同构），未切换到 tree 接口渲染侧栏——tree 端点已就绪，前端切换留作后续优化项。

---

## 七、拓展实施记录（2026-07）

| 方向 | 落地内容 | 状态 |
|------|----------|------|
| 填充流水线 | `scripts/fill_queue.py` 缺口榜 + 供稿工单生成；已示范填充 V36 发型 24 条（2236→2260） | ✅ |
| 语义查重 | `scripts/textvec.py` + `build_vectors.py`（哈希 n-gram TF-IDF，rebuild 自动构建）；`/api/ingest/check` 返回 `semantic_dups`，实测拦截换名重复 | ✅ |
| MCP Server | `scripts/mcp_server.py` + `.mcp.json`，8 工具直读 SQLite；MCP 客户端打开项目即用 | ✅ |
| 语义检索 | `/api/search/semantic`、`/api/terms/{uid}/similar`；纯语义联想偏弱，升级路径=换真实 embedding，接口不变 | ✅ |
| 平台方言 | combine 支持 `dialect=sd/mj` + `suffix`；前端底栏方言切换 | ✅ |
| 槽位工作台 | 提示词栏按 主体→风格→光影→构图→参数 槽位排序标注；`#/basket/uid,…` 分享链接一键还原整篮 | ✅ |
| 关系图谱 | build_kb 解析 related/confused 为真实边（916/1002）；`/api/terms/{uid}/graph`；前端图谱视图留作后续 | ✅ API 层 |
| 术语配图 | 暂缓：应在词条量过半后按卷分批做（需统一底图的生成流水线），schema 届时加 `image_ref` | ⏸ 规划 |

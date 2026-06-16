# AI视觉设计与提示词工程百科 V1.0

这是一个面向约 10,000 条专业术语的结构化知识库项目。主数据源采用 SQLite，人工采集入口采用 CSV，自动导出 Markdown 与 RAG/向量库预处理 JSONL，并向上提供只读 API 服务与 Vue 3 前端页面。架构按「按需懒加载」设计，可承载数万到数十万术语。

## 项目结构

```text
config/                  卷册拓扑、分类和跨卷关系
schema/                  SQLite 表结构与搜索索引（含 trigram 中文检索）
data/raw/                人工维护的采集模板与种子词表
data/kb/                 自动生成的 SQLite 主库
data/exports/            自动生成的 RAG JSONL、卷册统计等
data/exports/web/        自动生成的前端静态 JSON（index + 分卷，离线懒加载）
docs/                    数据契约、工作流、卷册拓扑、升级架构说明
docs/templates/          术语条目模板
generated/terms/         自动生成的 Markdown 术语页
scripts/                 构建、校验、搜索、启动脚本
api/                     FastAPI 只读服务层（懒加载分页 + trigram 搜索）
frontend/                Vue 3 + Vite（轻量，无重型 UI 库） 前端源码
web/                     前端构建产物（FastAPI 挂到 /app/，已随仓库预构建）
```

## 面向十万级数据的设计

在保持轻量（无重型中间件）的同时，按「按需懒加载」原则设计：

- **SQLite + 索引**：对 `volume_id / category_id / status` 建复合索引，百万行级查询仍是毫秒级。
- **trigram 全文检索**：trigram 分词的 FTS 表让中文子串检索（≥3 字）走索引，避免 `LIKE '%词%'` 全表扫描；1-2 字短查询自动回退 LIKE。
- **API 分页**：`/api/terms` 服务端分页，前端从不一次性拉全量。
- **前端懒加载**：首屏只加载 `index.json`（卷 + 分类 + 计数，无正文），点到哪卷/哪分类才拉哪部分；大分类分页渲染。
- **分卷静态导出**：离线模式下 `data/exports/web/volumes/{卷}.json` 按卷加载，无需巨型 JSON。

## 架构分层

```text
采集层  data/raw/*.csv
  │  build_kb.py
数据层  SQLite 主库 + FTS5/trigram 全文索引（唯一权威源）
  │            ├──> API 服务层  api/app.py（FastAPI，只读，分页 + trigram 搜索）
  │            └──> 前端静态 JSON  data/exports/web/（index.json + volumes/*.json）
表现层  Vue 3 + Arco（frontend/ 源码 → web/ 构建产物，双模式：连 API / 离线 JSON）
```

详见 `docs/upgrade-architecture.md`。

## 前端（Vue 3 + Vite（轻量，无重型 UI 库））

```bash
# 开发模式（需 Node.js 18+）
cd frontend
npm install
npm run dev          # http://localhost:5173，/api 自动代理到本地 8000

# 构建（产物输出到 ../web，供 FastAPI 在 /app/ 托管）
npm run build
# 或在项目根目录： ./manage.sh frontend
```

仓库已附带预构建的 `web/`，**服务器无需安装 Node** 即可直接运行（只需 Python）。

## 快速开始

```powershell
# 1. 构建主库、导出物与前端静态数据
python scripts/build_kb.py

# 2. 校验数据质量
python scripts/validate_kb.py

# 3. 命令行检索
python scripts/search_terms.py "低调照明"
```

## 启动 API 与前端

```powershell
# 安装 API 依赖（仅 fastapi + uvicorn，与零依赖的采集脚本隔离）
pip install -r api/requirements.txt

# 启动服务（含前端）
python scripts/run_api.py --port 8000
#   或： python -m uvicorn api.app:app --reload --port 8000

# 访问：
#   前端页面     http://localhost:8000/app/
#   API 交互文档 http://localhost:8000/docs
#   术语接口     http://localhost:8000/api/terms?volume=V08&q=控制
```

不想启动服务时，可直接双击 `web/index.html`，它会自动回退到「离线模式」读取 `data/exports/web/*.json`。

## API 端点

| 路径 | 用途 |
| --- | --- |
| `/api/health` | 健康检查 |
| `/api/meta` | 卷册/标签/统计元数据（前端初始化用） |
| `/api/volumes`、`/api/volumes/{code}/categories` | 卷册与分类 |
| `/api/tags` | 标签云 |
| `/api/terms` | 术语列表（筛选 `q/volume/category/tag/status` + 分页 + 排序） |
| `/api/terms/{term_uid}` | 术语详情 |
| `/api/search` | 全文搜索（FTS5 + LIKE 兜底） |
| `/api/stats` | 全局统计 |
| `/api/export/prompts` | 按筛选导出纯提示词清单（`format=json\|text`） |

## Linux 一键运维

```bash
chmod +x manage.sh

./manage.sh setup       # 一键环境配置（创建 venv + 安装依赖 + 构建知识库）
./manage.sh start       # 启动 API 服务（默认 8000 端口）
./manage.sh stop        # 停止服务
./manage.sh restart     # 重启
./manage.sh status      # 查看运行状态
./manage.sh build       # 重新构建知识库
./manage.sh frontend    # 重新构建前端（需 Node.js 18+；仓库已附带预构建产物）
./manage.sh validate    # 校验数据质量
./manage.sh search 景深  # 命令行搜索
./manage.sh update      # Git 拉取更新 + 重建 + 重启
./manage.sh logs        # 查看日志
```

## AI 贡献术语

本项目支持通过 AI 模型批量填充术语。详见 `docs/ai-contributor-guide.md`。

简要流程：读取 CSV 格式 → 按 term_uid 编号规则追加新行 → 运行 build_kb.py 构建。

## 推荐编辑方式

1. 在 `data/raw/terms_seed.csv` 中继续添加术语。
2. 每次添加后运行 `python scripts/build_kb.py`。
3. 用 `python scripts/validate_kb.py` 检查重复、缺字段、卷册目标量。
4. 用 `python scripts/search_terms.py "关键词"` 或 API 做检索验证。

## 数据原则

- SQLite 是权威数据源，向量库只作为检索索引。
- CSV 是采集入口，不直接作为长期知识库。
- API 只读：写入仍走「改 CSV → build」的可追溯流程。
- Markdown、JSONL、前端 JSON、未来的 DOCX/PDF/EPUB 都是导出物。
- 每条术语尽量同时服务“百科解释”和“AI 视觉提示词使用”。


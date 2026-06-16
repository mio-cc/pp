# AI视觉设计与提示词工程百科 V1.0

这是一个面向约 10,000 条专业术语的结构化知识库项目。主数据源采用 SQLite，人工采集入口采用 CSV，自动导出 Markdown 与 RAG/向量库预处理 JSONL，并向上提供只读 API 服务与零构建前端页面。

## 项目结构

```text
config/                  卷册拓扑、分类和跨卷关系
schema/                  SQLite 表结构与搜索索引
data/raw/                人工维护的采集模板与种子词表
data/kb/                 自动生成的 SQLite 主库
data/exports/            自动生成的 RAG JSONL、卷册统计等
data/exports/web/        自动生成的前端静态 JSON（离线模式数据源）
docs/                    数据契约、工作流、卷册拓扑、升级架构说明
docs/templates/          术语条目模板
generated/terms/         自动生成的 Markdown 术语页
scripts/                 构建、校验、搜索、启动脚本
api/                     FastAPI 只读服务层
web/                     零构建前端单页（双模式）
```

## 三层架构

```text
采集层  data/raw/*.csv
  │  build_kb.py
数据层  SQLite 主库 + FTS5 全文索引（唯一权威源）
  │            ├──> API 服务层  api/app.py（FastAPI，只读）
  │            └──> 前端静态 JSON  data/exports/web/*.json
表现层  web/index.html（双模式：连 API 动态查询 / 无 API 时读静态 JSON 离线浏览）
```

详见 `docs/upgrade-architecture.md`。

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
./manage.sh validate    # 校验数据质量
./manage.sh search 景深  # 命令行搜索
./manage.sh update      # Git 拉取更新 + 重建 + 重启
./manage.sh logs        # 查看日志
```

## AI 贡献术语

本项目支持通过 AI 模型批量填充术语。详见 `docs/ai-contributor-guide.
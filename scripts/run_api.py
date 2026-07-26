"""便捷启动脚本：python scripts/run_api.py [--port 8000]
等价于 python -m uvicorn api.app:app --reload --port 8000
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="启动百科 API 服务")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="开发模式自动重载")
    args = parser.parse_args()

    try:
        import uvicorn
    except ImportError:
        print("缺少依赖，请先运行： pip install -r api/requirements.txt")
        return 1

    db = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
    if not db.exists():
        print("提示：主库还不存在，建议先运行 python scripts/build_kb.py")

    sys.path.insert(0, str(ROOT))
    print(f"API 文档:  http://{args.host}:{args.port}/docs")
    print(f"前端页面:  http://{args.host}:{args.port}/app/")
    uvicorn.run("api.app:app", host=args.host, port=args.port, reload=args.reload)
    return 0


if __name__ == "__main__":
    sys.exit(main())

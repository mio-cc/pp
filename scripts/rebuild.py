#!/usr/bin/env python3
"""受限挂载环境下安全重建主库。

为什么需要它：工作区是受限 mount，禁止删除文件，且 sqlite 在「就地截断后增量写入」时会报
disk I/O error。可靠做法是：在系统临时目录(tmpfs)里全新构建，再把构建好的完整文件整体拷回
（覆盖写允许、删除/就地增量不允许）。

用法：python scripts/rebuild.py
等价于「干净地」跑一次 build_kb，并把 sqlite 主库与 data/exports 产物回写到工作区。
"""
from __future__ import annotations
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "kb"
        (tmp / "data").mkdir(parents=True)
        for d in ("config", "schema", "scripts"):
            shutil.copytree(ROOT / d, tmp / d)
        shutil.copytree(ROOT / "data" / "raw", tmp / "data" / "raw")

        proc = subprocess.run(
            [sys.executable, "-B", "scripts/build_kb.py"], cwd=str(tmp)
        )
        if proc.returncode != 0:
            print("❌ build_kb 失败，未回写。", file=sys.stderr)
            return proc.returncode

        # 回写主库（整体覆盖写）
        db_src = tmp / "data" / "kb" / "visual_prompt_terms.sqlite"
        db_dst = ROOT / "data" / "kb" / "visual_prompt_terms.sqlite"
        db_dst.parent.mkdir(parents=True, exist_ok=True)
        # 先清掉旧库与 sidecar（-wal/-shm/-journal），避免与新库冲突报 disk I/O error
        for suffix in ("", "-wal", "-shm", "-journal"):
            fp = Path(str(db_dst) + suffix)
            if fp.exists():
                try:
                    fp.unlink()
                except OSError:
                    pass
        shutil.copyfile(db_src, db_dst)

        # 回写 exports（逐文件覆盖，不删旧）
        exp_src = tmp / "data" / "exports"
        if exp_src.exists():
            for p in exp_src.rglob("*"):
                if p.is_file():
                    dst = ROOT / "data" / "exports" / p.relative_to(exp_src)
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(p, dst)

    print("✅ 重建完成并已回写主库与 exports。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

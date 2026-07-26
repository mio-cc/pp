"""轻量文本向量化 —— 哈希字符 n-gram TF-IDF（零依赖，纯 Python）。

用途：
- 语义近重查重（ingest check、/api/ingest/check 的 semantic_dups 警告）
- 模糊检索（/api/search/semantic、/api/terms/{uid}/similar）

设计取舍：
- 不依赖任何模型/网络，离线可复现；中文短文本上字符 2-gram 的
  余弦相似已足够做「近重复检测」与「比 LIKE 更模糊的召回」。
- 维度哈希用 md5（稳定，跨进程一致；Python 内建 hash 有随机盐不可用）。
- 若未来接入真实 embedding（API 或本地模型），只需替换 vectorize()
  并 rebuild 向量表，调用方（API/脚本）不变。
"""
from __future__ import annotations

import hashlib
import math
import re
import struct

DIM = 512
_CLEAN = re.compile(r"[\s。．.,，、；;：:！!？?（）()\[\]【】\"'“”‘’/\\|+_-]+")


def _ngrams(text: str) -> list[str]:
    t = _CLEAN.sub("", (text or "").lower())
    if not t:
        return []
    if len(t) == 1:
        return [t]
    return [t[i:i + 2] for i in range(len(t) - 1)]


def _slot(gram: str) -> int:
    return int.from_bytes(hashlib.md5(gram.encode("utf-8")).digest()[:4], "big") % DIM


def term_text(zh: str, en: str = "", definition: str = "", extra: str = "") -> str:
    """入向量的文本口径：名称权重最高（重复三遍），其次英文与释义。"""
    return ((zh or "") + " ") * 3 + (en or "") + " " + (definition or "") + " " + (extra or "")


def raw_counts(text: str) -> dict[int, float]:
    counts: dict[int, float] = {}
    for g in _ngrams(text):
        s = _slot(g)
        counts[s] = counts.get(s, 0.0) + 1.0
    return counts


def finalize(counts: dict[int, float], idf: list[float] | None = None) -> list[float]:
    """sublinear TF（1+ln）×可选 IDF，再 L2 归一。返回 DIM 维稠密向量。"""
    vec = [0.0] * DIM
    for s, c in counts.items():
        w = 1.0 + math.log(c)
        if idf is not None:
            w *= idf[s]
        vec[s] = w
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec


def build_idf(all_counts: list[dict[int, float]]) -> list[float]:
    n = max(1, len(all_counts))
    df = [0] * DIM
    for counts in all_counts:
        for s in counts:
            df[s] += 1
    return [math.log((1 + n) / (1 + d)) + 1.0 for d in df]


def pack(vec: list[float]) -> bytes:
    return struct.pack(f"<{DIM}f", *vec)


def unpack(blob: bytes) -> list[float]:
    return list(struct.unpack(f"<{DIM}f", blob))


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))  # 已归一，点积即余弦

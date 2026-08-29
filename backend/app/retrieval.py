"""BM25 + lightweight TF-IDF retrieval over regulatory modules. No embedding API."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from app.models import RegulatoryModule

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-']+")
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "by", "with",
    "must", "shall", "should", "their", "that", "this", "from", "be", "is",
    "are", "as", "at", "not", "no", "its", "it", "into", "than", "via",
}


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1]


def module_corpus_text(mod: RegulatoryModule) -> str:
    kws = " ".join(mod.keywords or [])
    checks = " ".join(mod.evidence_checklist or [])
    return f"{mod.obligation} {kws} {kws} {checks} {mod.category} {mod.locator_article}"


@dataclass
class RetrievedModule:
    module: RegulatoryModule
    score: float
    bm25: float
    tfidf: float


def _tfidf_scores(query_tokens: list[str], docs: list[list[str]]) -> list[float]:
    if not docs:
        return []
    n = len(docs)
    df: dict[str, int] = {}
    for doc in docs:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1
    idf = {t: math.log((n + 1) / (c + 0.5)) + 1.0 for t, c in df.items()}
    q_tf: dict[str, int] = {}
    for t in query_tokens:
        q_tf[t] = q_tf.get(t, 0) + 1
    q_norm_sq = 0.0
    q_w: dict[str, float] = {}
    for t, tf in q_tf.items():
        w = (1 + math.log(tf)) * idf.get(t, 0.0)
        q_w[t] = w
        q_norm_sq += w * w
    q_norm = math.sqrt(q_norm_sq) or 1.0
    scores: list[float] = []
    for doc in docs:
        tf: dict[str, int] = {}
        for t in doc:
            tf[t] = tf.get(t, 0) + 1
        dot = 0.0
        d_norm_sq = 0.0
        for t, c in tf.items():
            w = (1 + math.log(c)) * idf.get(t, 0.0)
            d_norm_sq += w * w
            if t in q_w:
                dot += w * q_w[t]
        d_norm = math.sqrt(d_norm_sq) or 1.0
        scores.append(dot / (q_norm * d_norm))
    return scores


def retrieve(
    modules: list[RegulatoryModule],
    query_text: str,
    frameworks: list[str] | None = None,
    top_k: int = 16,
) -> list[RetrievedModule]:
    pool = modules
    if frameworks:
        wanted = {f.lower() for f in frameworks}
        pool = [m for m in modules if m.framework_id.lower() in wanted]
    if not pool:
        return []

    docs = [tokenize(module_corpus_text(m)) for m in pool]
    query_tokens = tokenize(query_text)
    if not query_tokens:
        query_tokens = ["custody", "licence", "disclosure"]

    bm25 = BM25Okapi(docs)
    bm_raw = list(bm25.get_scores(query_tokens))
    tf_raw = _tfidf_scores(query_tokens, docs)

    def _norm(vals: list[float]) -> list[float]:
        lo, hi = min(vals), max(vals)
        if hi - lo < 1e-9:
            return [0.5 for _ in vals]
        return [(v - lo) / (hi - lo) for v in vals]

    bm_n = _norm(bm_raw)
    tf_n = _norm(tf_raw)
    ranked: list[RetrievedModule] = []
    for mod, b, t, bn, tn in zip(pool, bm_raw, tf_raw, bm_n, tf_n):
        score = 0.65 * bn + 0.35 * tn
        ranked.append(RetrievedModule(module=mod, score=score, bm25=float(b), tfidf=float(t)))
    ranked.sort(key=lambda r: r.score, reverse=True)
    return ranked[:top_k]

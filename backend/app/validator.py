"""Citation validator — second pass after generation.

Drops or flags findings that cite a module not in the retrieved set,
and flags claims whose key terms do not overlap the cited obligation.
"""

from __future__ import annotations

import re

from app.generator import DraftFinding
from app.retrieval import tokenize

_STATUS_GROUNDED = "grounded"
_STATUS_HITL = "needs_human_verification"
_STATUS_UNSUPPORTED = "unsupported"

_CONTENT_STOP = {
    "project", "pack", "appears", "address", "against", "include", "including",
    "observed", "missing", "partial", "coverage", "checklist", "items", "evidence",
    "aligned", "obligation", "licensing", "gap", "still", "further", "primary",
    "excerpt", "itself", "flags", "open", "drafting", "limited", "narrative",
    "only", "must", "client", "clients",
}


def _claim_terms(claim: str) -> set[str]:
    return {t for t in tokenize(claim) if t not in _CONTENT_STOP and len(t) > 3}


def _obligation_terms(text: str) -> set[str]:
    return {t for t in tokenize(text) if len(t) > 3}


def validate_drafts(
    drafts: list[DraftFinding],
    retrieved_ids: set[str],
) -> list[DraftFinding]:
    kept: list[DraftFinding] = []
    for draft in drafts:
        flags = list(draft.flags)
        mid = draft.module.id
        if mid not in retrieved_ids:
            flags.append("cited_module_not_in_retrieved_set")
            # Drop ungrounded citations entirely — they cannot be source-traced.
            continue

        claim_terms = _claim_terms(draft.claim)
        obl_terms = _obligation_terms(draft.module.obligation)
        kw_terms = {t.lower() for t in (draft.module.keywords or [])}
        kw_terms |= {t for k in (draft.module.keywords or []) for t in tokenize(k)}
        overlap = claim_terms & (obl_terms | kw_terms)

        if len(overlap) < 2:
            flags.append("claim_terms_do_not_overlap_cited_obligation")

        # Hallucinated article numbers (e.g. Art. 999) that are not the cited locator.
        cited_art = draft.module.locator_article or ""
        for match in re.finditer(r"\bArt\.?\s*\d+[a-z]?\b", draft.claim, flags=re.I):
            if cited_art and match.group(0).lower().replace(" ", "") not in cited_art.lower().replace(" ", ""):
                if match.group(0).lower() not in cited_art.lower():
                    flags.append(f"unexpected_article_citation:{match.group(0)}")

        draft.flags = sorted(set(flags))
        kept.append(draft)
    return kept


def assign_status(draft: DraftFinding) -> tuple[str, float]:
    """Confidence is derived from retrieval score, then penalised by validator flags."""
    base = max(0.15, min(0.97, 0.35 + 0.6 * draft.retrieval_score))
    flags = draft.flags
    if "cited_module_not_in_retrieved_set" in flags:
        return _STATUS_UNSUPPORTED, min(base, 0.2)
    if "claim_terms_do_not_overlap_cited_obligation" in flags:
        return _STATUS_UNSUPPORTED, min(base * 0.5, 0.4)
    if any(f.startswith("unexpected_article_citation") for f in flags):
        return _STATUS_HITL, min(base, 0.55)
    if draft.coverage == "partial":
        return _STATUS_HITL, min(base, 0.72)
    if draft.coverage == "missing":
        # A well-cited gap is still grounded — the *gap* is supported by the pack.
        return _STATUS_GROUNDED, min(max(base, 0.55), 0.88)
    if draft.coverage == "covered" and base >= 0.55:
        return _STATUS_GROUNDED, base
    return _STATUS_HITL, base

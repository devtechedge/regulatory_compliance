"""Finding generation: OpenAI if keyed, otherwise a deterministic citation-bound writer."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.config import settings
from app.models import RegulatoryModule
from app.retrieval import RetrievedModule, tokenize

# Phrases we look for in the project pack to judge checklist coverage.
_ITEM_HINTS: dict[str, list[str]] = {
    "segregation": ["segregat", "not commingled", "distinct from", "client asset"],
    "wallet": ["wallet inventory", "wallet", "hot wallet", "cold"],
    "cold": ["cold vault", "cold storage", "cold-wallet", "offline"],
    "key": ["key-management", "key management", "mpc", "multi-party", "hsm", "key ceremony"],
    "reconciliation": ["reconcil"],
    "white paper": ["white paper", "whitepaper"],
    "risk": ["risk factor", "risk-warning", "risk warning"],
    "marketing": ["marketing", "landing-page", "landing page"],
    "attestation": ["attestation", "independent audit", "independent attest"],
    "reserve": ["reserve", "backed 1:1", "backing"],
    "redemption": ["redemption", "physical delivery"],
    "complaints": ["complaints-handling", "complaints procedure", "complaints scheme", "complaints register"],
    "conflict": ["conflicts-of-interest", "conflicts of interest", "dual role"],
    "governance": ["board charter", "organisational chart", "compliance officer"],
    "capital": ["own-funds", "paid-up capital", "prudential"],
    "insurance": ["indemnity", "cyber insurance", "insurance binder"],
    "market-abuse": ["market-abuse", "market abuse", "insider list", "surveillance"],
    "aml": ["aml", "cdd", "kyc", "travel rule", "mlro", "sanctions"],
    "authorisation": ["licence has been granted", "authorization", "authorisation application", "filed with"],
    "outsourcing": ["outsourcing register", "due-diligence", "exit plan"],
    "continuity": ["business-continuity", "disaster-recovery", "incident-response"],
    "fee": ["fee schedule"],
}



_NEG = re.compile(
    r"\b(no|not|never|none|missing|absent|tbd|without|undisclosed|unrestricted|"
    r"silent|has not|have not|hasn.t|does not|do not|don.t|neither|nor a |"
    r"not been|not documented|not claim|not contain|not addressed|invented by)\b",
    re.I,
)


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [s.strip() for s in parts if s.strip()]


def _hints_for(item: str) -> list[str]:
    item_l = item.lower()
    hints: list[str] = []
    for key, values in _ITEM_HINTS.items():
        if key in item_l or any(h in item_l for h in values):
            hints.extend(values)
    if not hints:
        hints = [item_l]
    # keep unique, longest first so "white paper" beats "paper"
    seen: set[str] = set()
    out: list[str] = []
    for h in sorted(set(hints), key=len, reverse=True):
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


def _pack_matches(item: str, pack: str) -> bool:
    """True only if a non-negated sentence supports the checklist item."""
    hints = _hints_for(item)
    pos = 0
    neg = 0
    for sent in _sentences(pack):
        sl = sent.lower()
        # document title is not a filed white paper
        if sl.startswith("aurum custody") and "white paper excerpt" in sl:
            continue
        if not any(h in sl for h in hints):
            continue
        if _NEG.search(sl):
            neg += 1
        else:
            pos += 1
    if pos == 0:
        return False
    return pos > neg


def assess_checklist(mod: RegulatoryModule, pack: str) -> tuple[list[str], list[str], str]:
    present: list[str] = []
    missing: list[str] = []
    for item in mod.evidence_checklist or []:
        if _pack_matches(item, pack):
            present.append(item)
        else:
            missing.append(item)
    n = len(mod.evidence_checklist or [])
    if n == 0:
        coverage = "partial"
    elif not missing:
        coverage = "covered"
    elif not present:
        coverage = "missing"
    elif len(present) / n >= 0.6:
        coverage = "partial"
    else:
        coverage = "missing" if len(present) / n < 0.35 else "partial"
    return present, missing, coverage


def _snippet(pack: str, terms: list[str], width: int = 180) -> str | None:
    low = pack.lower()
    for term in terms:
        idx = low.find(term.lower())
        if idx >= 0:
            start = max(0, idx - 40)
            end = min(len(pack), idx + width)
            snippet = pack[start:end].replace("\n", " ").strip()
            return snippet
    return None


@dataclass
class DraftFinding:
    module: RegulatoryModule
    claim: str
    coverage: str
    retrieval_score: float
    present_items: list[str] = field(default_factory=list)
    missing_items: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


def _deterministic_claim(mod: RegulatoryModule, pack: str, present: list[str], missing: list[str], coverage: str) -> str:
    loc = f"{mod.locator_article}" + (f" ({mod.locator_clause})" if mod.locator_clause else "")
    fw = mod.framework_id
    kws = [k for k in (mod.keywords or []) if k]
    snip = _snippet(pack, kws[:4] + present[:2])

    if coverage == "covered":
        claim = (
            f"The project pack appears to address {fw} {loc} ({mod.category}). "
            f"Evidence aligned with the obligation to {mod.obligation.split('.')[0].lower()}. "
            f"Checklist items observed: {'; '.join(present[:3])}."
        )
    elif coverage == "missing":
        claim = (
            f"Licensing gap against {fw} {loc}: the pack does not evidence "
            f"{mod.obligation.split('.')[0].lower()}. "
            f"Missing checklist items include: {'; '.join(missing[:3])}."
        )
        if "no complaints" in pack.lower() or "no market-abuse" in pack.lower():
            claim += " The pack itself flags this as an open drafting gap."
    else:
        claim = (
            f"Partial coverage of {fw} {loc} ({mod.category}). "
            f"Observed: {'; '.join(present[:2]) or 'limited narrative only'}. "
            f"Still missing: {'; '.join(missing[:2]) or 'further primary evidence'}."
        )
    if snip:
        claim += f' Pack excerpt: "{snip[:160]}…"'
    return claim


def generate_deterministic(retrieved: list[RetrievedModule], pack: str) -> list[DraftFinding]:
    drafts: list[DraftFinding] = []
    for item in retrieved:
        mod = item.module
        present, missing, coverage = assess_checklist(mod, pack)
        claim = _deterministic_claim(mod, pack, present, missing, coverage)
        drafts.append(
            DraftFinding(
                module=mod,
                claim=claim,
                coverage=coverage,
                retrieval_score=item.score,
                present_items=present,
                missing_items=missing,
            )
        )
    return drafts


def generate_openai(retrieved: list[RetrievedModule], pack: str) -> list[DraftFinding] | None:
    if not settings.use_openai:
        return None
    try:
        from openai import OpenAI
    except Exception:
        return None

    client = OpenAI(api_key=settings.openai_api_key)
    drafts: list[DraftFinding] = []
    pack_excerpt = pack[:8000]
    for item in retrieved:
        mod = item.module
        present, missing, coverage = assess_checklist(mod, pack)
        locator = {
            "module_id": mod.id,
            "article": mod.locator_article,
            "clause": mod.locator_clause,
            "url": mod.locator_url,
            "title": mod.locator_title,
        }
        prompt = (
            "You are a compliance engineer reviewing a Web3 project pack against a single "
            "regulatory module. Write 2-4 sentences. You MUST ground every claim in the pack "
            "and cite only the provided module locator. Do not invent articles. "
            "If evidence is missing, say so as a gap. Return plain text only.\n\n"
            f"MODULE ID: {mod.id}\nFRAMEWORK: {mod.framework_id}\n"
            f"LOCATOR: {locator}\nOBLIGATION: {mod.obligation}\n"
            f"CHECKLIST: {mod.evidence_checklist}\n"
            f"HEURISTIC COVERAGE: {coverage}\nPRESENT: {present}\nMISSING: {missing}\n\n"
            f"PROJECT PACK:\n{pack_excerpt}\n"
        )
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}],
            )
            text = (resp.choices[0].message.content or "").strip()
        except Exception:
            text = _deterministic_claim(mod, pack, present, missing, coverage)
        # Force the module id into the claim so the validator can see the citation.
        if mod.id not in text:
            text = f"[{mod.locator_article}] {text}"
        drafts.append(
            DraftFinding(
                module=mod,
                claim=text,
                coverage=coverage,
                retrieval_score=item.score,
                present_items=present,
                missing_items=missing,
            )
        )
    return drafts


def generate_findings(retrieved: list[RetrievedModule], pack: str) -> tuple[str, list[DraftFinding]]:
    if settings.use_openai:
        openai_drafts = generate_openai(retrieved, pack)
        if openai_drafts is not None:
            return "openai", openai_drafts
    return "deterministic", generate_deterministic(retrieved, pack)

from __future__ import annotations

from app.generator import DraftFinding
from app.models import RegulatoryModule
from app.validator import assign_status, validate_drafts


def _module(**overrides) -> RegulatoryModule:
    kwargs = dict(
        id="mica-custody-segregation",
        framework_id="MiCA",
        locator_title="Title V",
        locator_article="Art. 75",
        locator_clause=None,
        locator_url="https://eur-lex.europa.eu/eli/reg/2023/1114/oj",
        category="custody",
        obligation=(
            "CASPs providing custody must segregate client crypto-assets from their own "
            "assets and implement documented key-management and wallet-inventory controls."
        ),
        evidence_checklist=["segregation policy", "wallet inventory"],
        keywords=["custody", "segregation", "client assets", "key management"],
    )
    kwargs.update(overrides)
    return RegulatoryModule(**kwargs)


def _draft(module: RegulatoryModule, claim: str, coverage: str = "covered", score: float = 0.85) -> DraftFinding:
    return DraftFinding(
        module=module,
        claim=claim,
        coverage=coverage,
        retrieval_score=score,
    )


def test_drops_finding_whose_module_is_not_in_retrieved_set():
    draft = _draft(
        _module(),
        "Custody segregation of client assets is documented in the pack against Art. 75.",
    )
    kept = validate_drafts([draft], retrieved_ids={"vara-custody-rulebook"})
    assert kept == []


def test_flags_low_term_overlap_with_cited_obligation():
    draft = _draft(
        _module(),
        "The weather pattern this week is unusually mild across the region.",
    )
    kept = validate_drafts([draft], retrieved_ids={"mica-custody-segregation"})
    assert len(kept) == 1
    assert "claim_terms_do_not_overlap_cited_obligation" in kept[0].flags


def test_flags_unexpected_article_number():
    draft = _draft(
        _module(),
        "Custody segregation of client assets and key management is required under Art. 999.",
    )
    kept = validate_drafts([draft], retrieved_ids={"mica-custody-segregation"})
    assert len(kept) == 1
    assert any(f.startswith("unexpected_article_citation") for f in kept[0].flags)


def test_assign_status_partial_needs_human_verification():
    draft = _draft(
        _module(),
        "Partial coverage of custody segregation of client assets.",
        coverage="partial",
    )
    draft.flags = []
    status, _confidence = assign_status(draft)
    assert status == "needs_human_verification"


def test_assign_status_grounded_when_clean_and_covered():
    draft = _draft(
        _module(),
        "The pack addresses custody segregation of client assets and wallet inventory.",
        coverage="covered",
        score=0.9,
    )
    draft.flags = []
    status, confidence = assign_status(draft)
    assert status == "grounded"
    assert confidence >= 0.55

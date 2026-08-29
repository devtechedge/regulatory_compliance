"""Orchestrate retrieval → generation → citation validation → persistence."""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.generator import generate_findings
from app.models import (
    Document,
    EvaluationRun,
    EvidenceGap,
    Finding,
    Project,
    RegulatoryModule,
)
from app.retrieval import retrieve
from app.schemas import (
    Citation,
    FindingOut,
    GapOut,
    Locator,
    ReadinessBucket,
    ReviewActionOut,
    RunOut,
)
from app.validator import assign_status, validate_drafts


def _citation_for(mod: RegulatoryModule) -> dict:
    return Citation(
        module_id=mod.id,
        framework=mod.framework_id,
        title=mod.locator_title,
        article=mod.locator_article,
        clause=mod.locator_clause,
        url=mod.locator_url,
        category=mod.category,
    ).model_dump()


def project_pack_text(db: Session, project_id: str) -> str:
    docs = db.scalars(select(Document).where(Document.project_id == project_id)).all()
    return "\n\n".join(f"{d.title}\n{d.content}" for d in docs)


def run_evaluation(db: Session, project: Project, frameworks: list[str]) -> EvaluationRun:
    pack = project_pack_text(db, project.id)
    modules = db.scalars(select(RegulatoryModule)).all()
    retrieved = retrieve(list(modules), pack, frameworks=frameworks, top_k=40)
    retrieved_ids = {r.module.id for r in retrieved}

    generator_name, drafts = generate_findings(retrieved, pack)
    drafts = validate_drafts(drafts, retrieved_ids)

    run = EvaluationRun(
        project_id=project.id,
        frameworks=frameworks,
        generator=generator_name,
        module_count=len(retrieved),
        retrieved_module_ids=sorted(retrieved_ids),
    )
    db.add(run)
    db.flush()

    seen_modules: set[str] = set()
    for draft in drafts:
        status, confidence = assign_status(draft)
        finding = Finding(
            run_id=run.id,
            module_id=draft.module.id,
            framework=draft.module.framework_id,
            category=draft.module.category,
            status=status,
            confidence=round(confidence, 3),
            claim=draft.claim,
            citations=[_citation_for(draft.module)],
            flags=draft.flags,
            coverage=draft.coverage,
            retrieval_score=round(draft.retrieval_score, 4),
        )
        db.add(finding)
        gap = EvidenceGap(
            run_id=run.id,
            module_id=draft.module.id,
            framework=draft.module.framework_id,
            category=draft.module.category,
            coverage=draft.coverage,
            missing_items=draft.missing_items,
            present_items=draft.present_items,
        )
        db.add(gap)
        seen_modules.add(draft.module.id)

    db.commit()
    db.refresh(run)
    return run


def _latest_review(finding: Finding):
    if not finding.reviews:
        return None
    return sorted(finding.reviews, key=lambda r: r.created_at)[-1]


def serialize_finding(finding: Finding) -> FindingOut:
    review = _latest_review(finding)
    return FindingOut(
        id=finding.id,
        run_id=finding.run_id,
        module_id=finding.module_id,
        framework=finding.framework,
        category=finding.category,
        status=finding.status,  # type: ignore[arg-type]
        confidence=finding.confidence,
        claim=finding.claim,
        citations=[Citation.model_validate(c) for c in (finding.citations or [])],
        flags=finding.flags or [],
        coverage=finding.coverage,
        retrieval_score=finding.retrieval_score,
        review_action=review.action if review else None,
    )


def serialize_gap(gap: EvidenceGap) -> GapOut:
    loc = None
    obligation = None
    if gap.module is not None:
        obligation = gap.module.obligation
        loc = Locator(
            title=gap.module.locator_title,
            article=gap.module.locator_article,
            clause=gap.module.locator_clause,
            url=gap.module.locator_url,
        )
    return GapOut(
        id=gap.id,
        module_id=gap.module_id,
        framework=gap.framework,
        category=gap.category,
        coverage=gap.coverage,  # type: ignore[arg-type]
        missing_items=gap.missing_items or [],
        present_items=gap.present_items or [],
        obligation=obligation,
        locator=loc,
    )


def readiness_from_gaps(gaps: list[EvidenceGap]) -> list[ReadinessBucket]:
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"covered": 0, "partial": 0, "missing": 0})
    for g in gaps:
        buckets[g.framework][g.coverage] = buckets[g.framework].get(g.coverage, 0) + 1
    out: list[ReadinessBucket] = []
    for fw, counts in buckets.items():
        total = counts["covered"] + counts["partial"] + counts["missing"]
        out.append(
            ReadinessBucket(
                framework=fw,
                covered=counts["covered"],
                partial=counts["partial"],
                missing=counts["missing"],
                total=total,
            )
        )
    return sorted(out, key=lambda b: b.framework)


def serialize_run(run: EvaluationRun) -> RunOut:
    reviews: list[ReviewActionOut] = []
    for f in run.findings:
        for ra in f.reviews:
            reviews.append(
                ReviewActionOut(
                    id=ra.id,
                    finding_id=ra.finding_id,
                    action=ra.action,
                    original_text=ra.original_text,
                    override_text=ra.override_text,
                    note=ra.note,
                    created_at=ra.created_at,
                    framework=f.framework,
                    module_id=f.module_id,
                    run_id=run.id,
                )
            )
    reviews.sort(key=lambda r: r.created_at, reverse=True)
    return RunOut(
        id=run.id,
        project_id=run.project_id,
        frameworks=list(run.frameworks or []),
        generator=run.generator,
        created_at=run.created_at,
        module_count=run.module_count,
        findings=[serialize_finding(f) for f in run.findings],
        gaps=[serialize_gap(g) for g in run.gaps],
        reviews=reviews,
        readiness=readiness_from_gaps(list(run.gaps)),
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.evaluate import serialize_finding
from app.models import Finding, ReviewAction
from app.demo_gate import require_demo_token
from app.schemas import FindingOut, ReviewRequest

router = APIRouter()


@router.post("/findings/{finding_id}/review", response_model=FindingOut)
def review_finding(
    finding_id: str,
    body: ReviewRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_demo_token),
) -> FindingOut:
    finding = db.scalar(
        select(Finding)
        .options(selectinload(Finding.reviews))
        .where(Finding.id == finding_id)
    )
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    action = ReviewAction(
        finding_id=finding.id,
        action=body.action,
        original_text=finding.claim,
        override_text=body.override_text if body.action == "edit" else None,
        note=body.note,
    )
    db.add(action)
    if body.action == "edit" and body.override_text:
        finding.claim = body.override_text
        flags = list(finding.flags or [])
        if "hitl_edited" not in flags:
            flags.append("hitl_edited")
        finding.flags = flags
        finding.status = "needs_human_verification"
    elif body.action == "reject":
        flags = list(finding.flags or [])
        if "hitl_rejected" not in flags:
            flags.append("hitl_rejected")
        finding.flags = flags
        finding.status = "unsupported"
    elif body.action == "accept":
        flags = list(finding.flags or [])
        if "hitl_accepted" not in flags:
            flags.append("hitl_accepted")
        finding.flags = flags
        if finding.status == "needs_human_verification":
            finding.status = "grounded"
    db.commit()
    db.refresh(finding)
    finding = db.scalar(
        select(Finding).options(selectinload(Finding.reviews)).where(Finding.id == finding_id)
    )
    return serialize_finding(finding)

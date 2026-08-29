from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models import Finding, ReviewAction
from app.schemas import ReviewActionOut

router = APIRouter()


@router.get("/eval-cases", response_model=list[ReviewActionOut])
def list_eval_cases(db: Session = Depends(get_db)) -> list[ReviewActionOut]:
    rows = db.scalars(
        select(ReviewAction)
        .options(selectinload(ReviewAction.finding))
        .order_by(ReviewAction.created_at.desc())
    ).all()
    out: list[ReviewActionOut] = []
    for ra in rows:
        f: Finding | None = ra.finding
        out.append(
            ReviewActionOut(
                id=ra.id,
                finding_id=ra.finding_id,
                action=ra.action,
                original_text=ra.original_text,
                override_text=ra.override_text,
                note=ra.note,
                created_at=ra.created_at,
                framework=f.framework if f else None,
                module_id=f.module_id if f else None,
                run_id=f.run_id if f else None,
            )
        )
    return out

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.evaluate import serialize_run
from app.export import render_markdown
from app.models import EvidenceGap, EvaluationRun, Finding, Project
from app.schemas import RunOut

router = APIRouter()


def _load_run(db: Session, run_id: str) -> EvaluationRun | None:
    return db.scalar(
        select(EvaluationRun)
        .options(
            selectinload(EvaluationRun.findings).selectinload(Finding.reviews),
            selectinload(EvaluationRun.gaps).selectinload(EvidenceGap.module),
        )
        .where(EvaluationRun.id == run_id)
    )


@router.get("/runs/{run_id}", response_model=RunOut)
def get_run(run_id: str, db: Session = Depends(get_db)) -> RunOut:
    run = _load_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return serialize_run(run)


@router.get("/runs/{run_id}/export.md")
def export_run(run_id: str, db: Session = Depends(get_db)) -> PlainTextResponse:
    run = _load_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    project = db.get(Project, run.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    md = render_markdown(run, project)
    filename = f"regtrace-{project.id}-{run.id[:8]}.md"
    return PlainTextResponse(
        content=md,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

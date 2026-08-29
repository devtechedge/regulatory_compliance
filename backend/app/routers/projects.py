from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.evaluate import run_evaluation, serialize_run
from app.models import EvidenceGap, EvaluationRun, Finding, Project
from app.schemas import DocumentOut, EvaluateRequest, ProjectOut, ProjectSummary, RunOut

router = APIRouter()


def _last_run(project: Project) -> EvaluationRun | None:
    if not project.runs:
        return None
    return sorted(project.runs, key=lambda r: r.created_at, reverse=True)[0]


def _summary(project: Project) -> ProjectSummary:
    last = _last_run(project)
    return ProjectSummary(
        id=project.id,
        name=project.name,
        tagline=project.tagline,
        jurisdictions=list(project.jurisdictions or []),
        offerings=list(project.offerings or []),
        target_licences=list(project.target_licences or []),
        summary=project.summary,
        document_count=len(project.documents or []),
        last_run_id=last.id if last else None,
        last_run_at=last.created_at if last else None,
    )


@router.get("/projects", response_model=list[ProjectSummary])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectSummary]:
    rows = db.scalars(
        select(Project).options(
            selectinload(Project.documents),
            selectinload(Project.runs),
        )
    ).all()
    return [_summary(p) for p in rows]


@router.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, db: Session = Depends(get_db)) -> ProjectOut:
    project = db.scalar(
        select(Project)
        .options(selectinload(Project.documents), selectinload(Project.runs))
        .where(Project.id == project_id)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    base = _summary(project)
    return ProjectOut(
        **base.model_dump(),
        documents=[
            DocumentOut(id=d.id, title=d.title, kind=d.kind, content=d.content)
            for d in project.documents
        ],
    )


@router.post("/projects/{project_id}/evaluate", response_model=RunOut)
def evaluate_project(
    project_id: str,
    body: EvaluateRequest,
    db: Session = Depends(get_db),
) -> RunOut:
    project = db.scalar(
        select(Project)
        .options(selectinload(Project.documents))
        .where(Project.id == project_id)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    frameworks = body.frameworks or ["MiCA", "VARA"]
    run = run_evaluation(db, project, frameworks)
    run = db.scalar(
        select(EvaluationRun)
        .options(
            selectinload(EvaluationRun.findings).selectinload(Finding.reviews),
            selectinload(EvaluationRun.gaps).selectinload(EvidenceGap.module),
        )
        .where(EvaluationRun.id == run.id)
    )
    return serialize_run(run)

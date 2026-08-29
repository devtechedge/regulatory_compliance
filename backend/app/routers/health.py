from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import Framework, RegulatoryModule
from app.schemas import HealthOut

router = APIRouter()


@router.get("/health", response_model=HealthOut)
def health(db: Session = Depends(get_db)) -> HealthOut:
    fw = db.scalar(select(func.count()).select_from(Framework)) or 0
    mods = db.scalar(select(func.count()).select_from(RegulatoryModule)) or 0
    dialect = settings.sqlalchemy_url.split(":")[0]
    return HealthOut(
        status="ok",
        generator="openai" if settings.use_openai else "deterministic",
        database=dialect,
        frameworks=int(fw),
        modules=int(mods),
    )

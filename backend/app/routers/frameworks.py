from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Framework, RegulatoryModule
from app.schemas import FrameworkOut

router = APIRouter()


@router.get("/frameworks", response_model=list[FrameworkOut])
def list_frameworks(db: Session = Depends(get_db)) -> list[FrameworkOut]:
    rows = db.scalars(select(Framework).order_by(Framework.id)).all()
    out: list[FrameworkOut] = []
    for fw in rows:
        n = db.scalar(
            select(func.count()).select_from(RegulatoryModule).where(
                RegulatoryModule.framework_id == fw.id
            )
        ) or 0
        out.append(
            FrameworkOut(
                id=fw.id,
                name=fw.name,
                jurisdiction=fw.jurisdiction,
                instrument=fw.instrument,
                source_url=fw.source_url,
                description=fw.description,
                module_count=int(n),
            )
        )
    return out

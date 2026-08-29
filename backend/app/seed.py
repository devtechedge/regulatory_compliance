"""Load MiCA/VARA modules and the Aurum Custody sample project if the DB is empty."""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.models import Document, Framework, Project, RegulatoryModule


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def seed_frameworks(db: Session, data_dir: Path) -> int:
    count = db.scalar(select(func.count()).select_from(Framework)) or 0
    if count:
        return int(count)

    inserted = 0
    for fname in ("mica.json", "vara.json"):
        payload = _load_json(data_dir / "frameworks" / fname)
        fw = Framework(
            id=payload["id"],
            name=payload["name"],
            jurisdiction=payload.get("jurisdiction", ""),
            instrument=payload.get("instrument", ""),
            source_url=payload.get("source_url", ""),
            description=payload.get("description", ""),
        )
        db.add(fw)
        for mod in payload.get("modules", []):
            loc = mod.get("locator") or {}
            db.add(
                RegulatoryModule(
                    id=mod["id"],
                    framework_id=payload["id"],
                    locator_title=loc.get("title") or "",
                    locator_article=loc.get("article") or "",
                    locator_clause=loc.get("clause"),
                    locator_url=loc.get("url") or "",
                    category=mod.get("category") or "other",
                    obligation=mod["obligation"],
                    evidence_checklist=mod.get("evidence_checklist") or [],
                    keywords=mod.get("keywords") or [],
                )
            )
        inserted += 1
    db.flush()
    return inserted


def seed_projects(db: Session, data_dir: Path) -> int:
    count = db.scalar(select(func.count()).select_from(Project)) or 0
    if count:
        return int(count)

    inserted = 0
    projects_dir = data_dir / "projects"
    if not projects_dir.exists():
        return 0
    for path in sorted(projects_dir.glob("*.json")):
        payload = _load_json(path)
        project = Project(
            id=payload["id"],
            name=payload["name"],
            tagline=payload.get("tagline", ""),
            jurisdictions=payload.get("jurisdictions") or [],
            offerings=payload.get("offerings") or [],
            target_licences=payload.get("target_licences") or [],
            summary=payload.get("summary", ""),
        )
        db.add(project)
        for doc in payload.get("documents") or []:
            kwargs = dict(
                project_id=payload["id"],
                title=doc.get("title") or "Untitled",
                kind=doc.get("kind") or "whitepaper",
                content=doc.get("content") or "",
            )
            if doc.get("id"):
                kwargs["id"] = doc["id"]
            db.add(Document(**kwargs))
        inserted += 1
    db.flush()
    return inserted


def seed_if_empty(db: Session | None = None) -> None:
    data_dir = settings.resolved_data_dir
    own_session = db is None
    if own_session:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
    try:
        seed_frameworks(db, data_dir)
        seed_projects(db, data_dir)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        if own_session:
            db.close()


def main() -> None:
    seed_if_empty()
    print("Seed complete.")


if __name__ == "__main__":
    main()

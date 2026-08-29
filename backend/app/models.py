from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db import Base

JsonType = JSON().with_variant(JSONB, "postgresql")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid.uuid4())


class Framework(Base):
    __tablename__ = "frameworks"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    jurisdiction: Mapped[str] = mapped_column(String(128), default="")
    instrument: Mapped[str] = mapped_column(String(512), default="")
    source_url: Mapped[str] = mapped_column(String(512), default="")
    description: Mapped[str] = mapped_column(Text, default="")

    modules: Mapped[list[RegulatoryModule]] = relationship(
        back_populates="framework", cascade="all, delete-orphan"
    )


class RegulatoryModule(Base):
    __tablename__ = "regulatory_modules"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    framework_id: Mapped[str] = mapped_column(ForeignKey("frameworks.id"), index=True)
    locator_title: Mapped[str] = mapped_column(String(255), default="")
    locator_article: Mapped[str] = mapped_column(String(128), default="")
    locator_clause: Mapped[str | None] = mapped_column(String(255), nullable=True)
    locator_url: Mapped[str] = mapped_column(String(512), default="")
    category: Mapped[str] = mapped_column(String(64), index=True)
    obligation: Mapped[str] = mapped_column(Text)
    evidence_checklist: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    keywords: Mapped[list[Any]] = mapped_column(JsonType, default=list)

    framework: Mapped[Framework] = relationship(back_populates="modules")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    tagline: Mapped[str] = mapped_column(String(512), default="")
    jurisdictions: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    offerings: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    target_licences: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    summary: Mapped[str] = mapped_column(Text, default="")

    documents: Mapped[list[Document]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    runs: Mapped[list[EvaluationRun]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    kind: Mapped[str] = mapped_column(String(64), default="whitepaper")
    content: Mapped[str] = mapped_column(Text)

    project: Mapped[Project] = relationship(back_populates="documents")


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    frameworks: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    generator: Mapped[str] = mapped_column(String(32), default="deterministic")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    module_count: Mapped[int] = mapped_column(Integer, default=0)
    retrieved_module_ids: Mapped[list[Any]] = mapped_column(JsonType, default=list)

    project: Mapped[Project] = relationship(back_populates="runs")
    findings: Mapped[list[Finding]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )
    gaps: Mapped[list[EvidenceGap]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(ForeignKey("evaluation_runs.id"), index=True)
    module_id: Mapped[str] = mapped_column(ForeignKey("regulatory_modules.id"), index=True)
    framework: Mapped[str] = mapped_column(String(32), index=True)
    category: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(48), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    claim: Mapped[str] = mapped_column(Text)
    citations: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    flags: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    coverage: Mapped[str] = mapped_column(String(32), default="partial")
    retrieval_score: Mapped[float] = mapped_column(Float, default=0.0)

    run: Mapped[EvaluationRun] = relationship(back_populates="findings")
    module: Mapped[RegulatoryModule] = relationship()
    reviews: Mapped[list[ReviewAction]] = relationship(
        back_populates="finding", cascade="all, delete-orphan"
    )


class ReviewAction(Base):
    __tablename__ = "review_actions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    finding_id: Mapped[str] = mapped_column(ForeignKey("findings.id"), index=True)
    action: Mapped[str] = mapped_column(String(16))
    original_text: Mapped[str] = mapped_column(Text, default="")
    override_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    finding: Mapped[Finding] = relationship(back_populates="reviews")


class EvidenceGap(Base):
    __tablename__ = "evidence_gaps"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(ForeignKey("evaluation_runs.id"), index=True)
    module_id: Mapped[str] = mapped_column(ForeignKey("regulatory_modules.id"))
    framework: Mapped[str] = mapped_column(String(32), index=True)
    category: Mapped[str] = mapped_column(String(64), default="")
    coverage: Mapped[str] = mapped_column(String(32), default="missing")
    missing_items: Mapped[list[Any]] = mapped_column(JsonType, default=list)
    present_items: Mapped[list[Any]] = mapped_column(JsonType, default=list)

    run: Mapped[EvaluationRun] = relationship(back_populates="gaps")
    module: Mapped[RegulatoryModule] = relationship()

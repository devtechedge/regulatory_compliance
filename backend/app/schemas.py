from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class Locator(BaseModel):
    title: str
    article: str
    clause: str | None = None
    url: str


class Citation(BaseModel):
    module_id: str
    framework: str
    title: str
    article: str
    clause: str | None = None
    url: str
    category: str = ""


class ModuleOut(BaseModel):
    id: str
    framework: str
    locator: Locator
    category: str
    obligation: str
    evidence_checklist: list[str]
    keywords: list[str]


class FrameworkOut(BaseModel):
    id: str
    name: str
    jurisdiction: str
    instrument: str
    source_url: str
    description: str
    module_count: int


class DocumentOut(BaseModel):
    id: str
    title: str
    kind: str
    content: str


class ProjectSummary(BaseModel):
    id: str
    name: str
    tagline: str
    jurisdictions: list[str]
    offerings: list[str]
    target_licences: list[str]
    summary: str
    document_count: int = 0
    last_run_id: str | None = None
    last_run_at: datetime | None = None


class ProjectOut(ProjectSummary):
    documents: list[DocumentOut] = Field(default_factory=list)


class EvaluateRequest(BaseModel):
    frameworks: list[str] = Field(default_factory=lambda: ["MiCA", "VARA"])


class FindingOut(BaseModel):
    id: str
    run_id: str
    module_id: str
    framework: str
    category: str
    status: Literal["grounded", "needs_human_verification", "unsupported"]
    confidence: float
    claim: str
    citations: list[Citation]
    flags: list[str]
    coverage: str
    retrieval_score: float
    review_action: str | None = None


class GapOut(BaseModel):
    id: str
    module_id: str
    framework: str
    category: str
    coverage: Literal["covered", "partial", "missing"]
    missing_items: list[str]
    present_items: list[str]
    obligation: str | None = None
    locator: Locator | None = None


class ReviewActionOut(BaseModel):
    id: str
    finding_id: str
    action: str
    original_text: str
    override_text: str | None
    note: str | None
    created_at: datetime
    framework: str | None = None
    module_id: str | None = None
    run_id: str | None = None


class ReadinessBucket(BaseModel):
    framework: str
    covered: int
    partial: int
    missing: int
    total: int


class RunOut(BaseModel):
    id: str
    project_id: str
    frameworks: list[str]
    generator: str
    created_at: datetime
    module_count: int
    findings: list[FindingOut] = Field(default_factory=list)
    gaps: list[GapOut] = Field(default_factory=list)
    reviews: list[ReviewActionOut] = Field(default_factory=list)
    readiness: list[ReadinessBucket] = Field(default_factory=list)


class ReviewRequest(BaseModel):
    action: Literal["accept", "edit", "reject"]
    override_text: str | None = None
    note: str | None = None


class HealthOut(BaseModel):
    status: str
    service: str = "regtrace-ai"
    generator: str
    database: str
    frameworks: int = 0
    modules: int = 0

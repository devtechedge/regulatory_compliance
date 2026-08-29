from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers import eval_cases, findings, frameworks, health, projects, runs
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_if_empty()
    yield


app = FastAPI(
    title="RegTrace-AI",
    description=(
        "Web3 regulatory compliance copilot with Human-in-the-Loop (HITL) review, "
        "source-traced MiCA / VARA framework mapping, and hallucination mitigation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(frameworks.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(runs.router, prefix="/api")
app.include_router(findings.router, prefix="/api")
app.include_router(eval_cases.router, prefix="/api")


@app.get("/")
def root() -> dict:
    return {"service": "regtrace-ai", "docs": "/docs", "health": "/api/health"}

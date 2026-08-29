# RegTrace-AI

HITL Web3 compliance copilot for VASP licensing: source-traced MiCA / VARA mapping, hallucination flags, and a human review dashboard.

[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Live Demo

No public hosted backend yet. Clone, Compose, then open the seeded **Aurum Custody** pack.

> **Status:** Local Docker Compose demo with seeded MiCA / VARA modules and a fictional VASP pack. Deterministic retrieval-bounded generator; no API key. Findings are not legal advice.

```bash
cp .env.example .env
docker compose up --build
```

Then http://localhost:3000 (web) and http://localhost:8000/docs (API).

---

## Screenshots

| Overview | HITL workspace |
|----------|----------------|
| ![Dashboard](docs/screenshots/01-overview.png) | ![Split-screen review](docs/screenshots/02-hitl-workspace.png) |

| Gap analysis |
|--------|
| ![Licensing readiness](docs/screenshots/03-gap-analysis.png) |

---

## Features

- HITL accept/edit/reject with logged eval cases
- Source-traced MiCA article and VARA rule citations
- Hallucination flags via citation validator
- 12 MiCA + 12 VARA VASP licensing modules
- Markdown gap export for the licence file

This is compliance engineering, not a smart-contract auditor.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js App Router, TypeScript, Tailwind |
| API | FastAPI, SQLAlchemy 2, pydantic v2 |
| Retrieval | BM25 + TF-IDF (no embedding API) |
| Data | Postgres in Compose; SQLite locally; seeded demo |
| Generator | Deterministic writer; optional OpenAI |
| Hosting | Local Docker Compose (no public demo) |

---

## Quick Start

### Docker Compose (preferred)

Copy `.env.example` to `.env`, then start postgres, api, and web with compose.

- API: http://localhost:8000/docs and GET /api/health
- Web: http://localhost:3000
- Postgres: localhost:5432 (user/password/db: regtrace)

No OpenAI key required.

### Local (no Docker)

Postgres is optional. The API defaults to SQLite if DATABASE_URL is unset.

From `backend/`, create a virtualenv, install the Python requirements file, export `DATA_DIR=../data` and a sqlite `DATABASE_URL`, then start uvicorn on `app.main:app` port 8000.

From `frontend/`, install Node dependencies, export `NEXT_PUBLIC_API_URL=http://localhost:8000`, then start the Next.js dev server.

Seed runs on API startup. To re-seed after wiping the DB, from backend/: `python -m app.seed`.

### Smoke

```
GET  /api/health
GET  /api/frameworks
POST /api/projects/aurum-custody/evaluate   {"frameworks":["MiCA","VARA"]}
```

## License

MIT. See [LICENSE](LICENSE).

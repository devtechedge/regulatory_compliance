# Security

RegTrace-AI is a **demo** (local Compose or Vercel demo-mode). It is not a production compliance platform. This document describes the threat model as shipped, not a target-state control list.

**Date:** 2026-09-06

Repos stay **public until deliberately made private**. Honest demo threat model — **not** a bank-grade guarantee.

## What this demo is

An open Human-in-the-Loop dashboard plus API. Reviewers load a project pack, run a retrieval-bounded evaluation against seeded MiCA / VARA modules, and accept / edit / reject findings. Seeded **Aurum Custody** is fictional demo data, not a real VASP.

## Threat model

### Demo mutation gate (Vercel)

Public **GET** of the seeded demo pack stays open (frameworks, project, runs, health).

**Mutating** routes (`POST /api/projects/{id}/evaluate`, `POST /api/findings/{id}/review`) require:

1. `x-demo-token` matching `DEMO_TOKEN` (default published password `Demo123!` — see README)
2. Soft Origin allowlist (`https://regtrace-ai.vercel.app`, localhost, or same Host)
3. Best-effort in-memory rate limit (~30 mutations / minute / IP)

The Next.js client sends `x-demo-token: Demo123!` by default (override via `localStorage.regtrace_demo_token` or `NEXT_PUBLIC_DEMO_TOKEN`). Set `DEMO_TOKEN=` (empty) on the server to disable the token check for a trusted local network.

**Residual risk:** the demo password is public by design; this stops anonymous drive-by POSTs and cross-origin abuse, not a determined attacker who reads the README. HITL state is still in-memory and resets on cold start.

### Cross-site scripting (rendered findings)

Generator output (`finding.claim`), validator flags, reviewer notes, and pack text are **untrusted**. The UI renders them as React text children (`{finding.claim}` and similar). React escapes HTML in text nodes. The app does **not** use `dangerouslySetInnerHTML` and does **not** run an HTML sanitizer (no DOMPurify).

**Residual risk:** XSS via claim text is mitigated by React escaping today. Do not later interpolate model text as HTML. Markdown/HTML rendering would need a sanitizer that is not present.

### SQL injection

Persistence uses SQLAlchemy 2 ORM with bound parameters (Compose/local FastAPI). Application code does not concatenate user input into SQL strings. Vercel demo-mode uses in-memory JSON, not SQL.

### CORS / headers

Frontend ships security headers via `next.config.mjs` / `vercel.json` (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, CSP). FastAPI Compose default `CORS_ORIGINS` is localhost. CORS is not access control.

### Secrets

- `OPENAI_API_KEY` is **optional**. With it unset, the API uses the deterministic citation-bound (retrieval-only) generator.
- `.env` is gitignored. Copy from `.env.example` (empty key). Never commit `.env` or live keys.
- Compose/local defaults (`regtrace` / `regtrace`) are demo credentials, not production secrets.
- `DEMO_TOKEN` defaults to the published demo password; rotate it in Vercel env if you want a private review link.

### Payments

None. No billing, wallets, or card data.

### Supply chain / demo data

Framework JSON under `data/` is curated locator text, not a live legal feed. Do not treat citations as advice.

## Out of scope (not claimed)

Durable HITL persistence on Vercel, SSO/OIDC, encryption at rest, WAF-grade distributed rate limits, and bank-grade guarantees.

## Reporting

This is a personal demo repository. Open a GitHub issue on the same repo if you find a vulnerability in the shipped code.

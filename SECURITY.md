# Security

RegTrace-AI is a **demo** (local Compose or Vercel demo-mode). It is not a production compliance platform. This document describes the threat model as shipped, not a target-state control list.

## What this demo is

An open Human-in-the-Loop dashboard plus API. Reviewers load a project pack, run a retrieval-bounded evaluation against seeded MiCA / VARA modules, and accept / edit / reject findings. Seeded **Aurum Custody** is fictional demo data, not a real VASP.

## Threat model

### No authentication

There is no login, session, CSRF token, or role model. The dashboard and `/api/*` are reachable by anyone who can hit the process (typically `localhost`). The Vercel demo has no auth and in-memory HITL (reviews reset on cold start).

**Residual risk:** anyone who can reach the API can list projects, trigger evaluations, and **accept or reject findings**. Treat the local Compose path as trusted-network; treat the Vercel demo as public and ephemeral.

### Cross-site scripting (rendered findings)

Generator output (`finding.claim`), validator flags, reviewer notes, and pack text are **untrusted**. The UI renders them as React text children (`{finding.claim}` and similar). React escapes HTML in text nodes. The app does **not** use `dangerouslySetInnerHTML` and does **not** run an HTML sanitizer (no DOMPurify).

**Residual risk:** XSS via claim text is mitigated by React escaping today. Do not later interpolate model text as HTML. Markdown/HTML rendering would need a sanitizer that is not present.

### SQL injection

Persistence uses SQLAlchemy 2 ORM with bound parameters. Application code does not concatenate user input into SQL strings.

### CORS

Default `CORS_ORIGINS` is `http://localhost:3000` and `http://127.0.0.1:3000`. CORS is not access control; it only limits browser origins for credentialed XHR. Combined with no auth, a browser on an allowed origin can call every mutating endpoint.

### Secrets

- `OPENAI_API_KEY` is **optional**. With it unset, the API uses the deterministic citation-bound generator.
- `.env` is gitignored. Copy from `.env.example` (empty key). Never commit `.env` or live keys.
- Compose/local defaults (`regtrace` / `regtrace`) are demo credentials, not production secrets.

### Payments

None. No billing, wallets, or card data.

### Supply chain / demo data

Framework JSON under `data/` is curated locator text, not a live legal feed. Do not treat citations as advice.

## Out of scope (not claimed)

Rate limiting, durable HITL persistence on Vercel, audit log export beyond the in-app eval-case list, encryption at rest, and SSO.

## Reporting

This is a personal demo repository. Open a GitHub issue on the same repo if you find a vulnerability in the shipped code.

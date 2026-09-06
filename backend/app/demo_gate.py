"""Demo mutation gate for Compose/local FastAPI (mirrors Vercel x-demo-token)."""
from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import Header, HTTPException, Request

from app.config import settings

_WINDOW = 60.0
_MAX = 30
_hits: dict[str, deque[float]] = defaultdict(deque)


def _ip(request: Request) -> str:
    xf = request.headers.get("x-forwarded-for")
    if xf:
        return xf.split(",")[0].strip() or "unknown"
    if request.client:
        return request.client.host or "unknown"
    return "unknown"


def require_demo_token(
    request: Request,
    x_demo_token: str | None = Header(default=None, alias="x-demo-token"),
) -> None:
    expected = (settings.demo_token or "").strip()
    # Empty DEMO_TOKEN disables the check (trusted LAN)
    if expected:
        if not x_demo_token or x_demo_token != expected:
            raise HTTPException(status_code=401, detail="Missing or invalid x-demo-token")
    now = time.monotonic()
    ip = _ip(request)
    q = _hits[ip]
    while q and now - q[0] > _WINDOW:
        q.popleft()
    if len(q) >= _MAX:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    q.append(now)

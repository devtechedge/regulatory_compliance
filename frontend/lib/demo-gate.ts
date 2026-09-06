/**
 * Lightweight demo gate for mutating Vercel API routes.
 * - Optional DEMO_TOKEN (default Demo123!) via x-demo-token header
 * - Best-effort in-memory rate limit per IP
 * - Soft origin check (same-origin / allowlisted hosts)
 */

import { NextResponse } from "next/server";

const DEFAULT_TOKEN = "Demo123!";
const WINDOW_MS = 60_000;
const MAX_MUTATIONS = 30;

type Bucket = { ts: number[] };
const g = globalThis as typeof globalThis & { __regtraceRate?: Map<string, Bucket> };

function rateMap(): Map<string, Bucket> {
  if (!g.__regtraceRate) g.__regtraceRate = new Map();
  return g.__regtraceRate;
}

export function demoToken(): string {
  return (process.env.DEMO_TOKEN || DEFAULT_TOKEN).trim();
}

export function allowedOrigins(): string[] {
  const raw = (process.env.CORS_ORIGINS || "").trim();
  const defaults = [
    "https://regtrace-ai.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
  ];
  if (!raw) return defaults;
  return [...new Set([...defaults, ...raw.split(",").map((s) => s.trim()).filter(Boolean)])];
}

function clientIp(req: Request): string {
  const xf = req.headers.get("x-forwarded-for");
  if (xf) return xf.split(",")[0]?.trim() || "unknown";
  return req.headers.get("x-real-ip") || "unknown";
}

export function checkRateLimit(req: Request): NextResponse | null {
  const ip = clientIp(req);
  const now = Date.now();
  const map = rateMap();
  const bucket = map.get(ip) || { ts: [] };
  bucket.ts = bucket.ts.filter((t) => now - t < WINDOW_MS);
  if (bucket.ts.length >= MAX_MUTATIONS) {
    return NextResponse.json({ detail: "Rate limit exceeded" }, { status: 429 });
  }
  bucket.ts.push(now);
  map.set(ip, bucket);
  return null;
}

export function checkOrigin(req: Request): NextResponse | null {
  const origin = req.headers.get("origin");
  // Same-origin navigations / server components often omit Origin
  if (!origin) return null;
  const allowed = allowedOrigins();
  if (allowed.includes(origin)) return null;
  // Also allow the request Host as https://host (Vercel preview)
  try {
    const host = req.headers.get("host");
    if (host) {
      const candidates = [`https://${host}`, `http://${host}`];
      if (candidates.includes(origin)) return null;
    }
  } catch {
    /* ignore */
  }
  return NextResponse.json({ detail: "Origin not allowed" }, { status: 403 });
}

export function checkDemoToken(req: Request): NextResponse | null {
  const expected = demoToken();
  // If DEMO_TOKEN explicitly set to empty string, skip gate (local libre mode)
  if (process.env.DEMO_TOKEN === "") return null;
  const got = (req.headers.get("x-demo-token") || "").trim();
  if (got && got === expected) return null;
  return NextResponse.json(
    { detail: "Missing or invalid x-demo-token (see README demo password)" },
    { status: 401 },
  );
}

/** Run all mutation gates; return a NextResponse error or null if OK. */
export function gateMutation(req: Request): NextResponse | null {
  return checkRateLimit(req) || checkOrigin(req) || checkDemoToken(req);
}

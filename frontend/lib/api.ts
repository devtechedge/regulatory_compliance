import type { Finding, Framework, Project, ProjectSummary, ReviewAction, Run } from "./types";

// Empty string = same-origin Next.js demo API (Vercel / local without FastAPI).
// Set NEXT_PUBLIC_API_URL=http://localhost:8000 to hit FastAPI (Compose / local backend).
const API = process.env.NEXT_PUBLIC_API_URL ?? "";

/** Published demo password for HITL/eval mutations (override via localStorage.regtrace_demo_token). */
const DEMO_TOKEN_DEFAULT = "Demo123!";

function demoTokenHeader(): Record<string, string> {
  try {
    const fromStore = typeof window !== "undefined" ? window.localStorage.getItem("regtrace_demo_token") : null;
    const token = (fromStore || process.env.NEXT_PUBLIC_DEMO_TOKEN || DEMO_TOKEN_DEFAULT).trim();
    return token ? { "x-demo-token": token } : {};
  } catch {
    return { "x-demo-token": DEMO_TOKEN_DEFAULT };
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const method = (init?.method || "GET").toUpperCase();
  const mutationHeaders = method !== "GET" && method !== "HEAD" ? demoTokenHeader() : {};
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...mutationHeaders,
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${body}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string; generator: string; modules: number }>("/api/health"),
  frameworks: () => request<Framework[]>("/api/frameworks"),
  projects: () => request<ProjectSummary[]>("/api/projects"),
  project: (id: string) => request<Project>(`/api/projects/${id}`),
  evaluate: (id: string, frameworks: string[]) =>
    request<Run>(`/api/projects/${id}/evaluate`, {
      method: "POST",
      body: JSON.stringify({ frameworks }),
    }),
  run: (id: string) => request<Run>(`/api/runs/${id}`),
  review: (id: string, body: { action: "accept" | "edit" | "reject"; override_text?: string; note?: string }) =>
    request<Finding>(`/api/findings/${id}/review`, {
      method: "POST",
      body: JSON.stringify(body),
    }),
  evalCases: () => request<ReviewAction[]>("/api/eval-cases"),
  exportUrl: (runId: string) => `${API}/api/runs/${runId}/export.md`,
};

export { API };

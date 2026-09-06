import { randomUUID } from "crypto";
import micaJson from "@/data/frameworks/mica.json";
import varaJson from "@/data/frameworks/vara.json";
import aurumJson from "@/data/projects/aurum-custody.json";
import demoRunJson from "@/data/demo-run.json";
import type {
  Finding,
  Framework,
  Project,
  ProjectSummary,
  ReviewAction,
  Run,
} from "./types";

type FrameworkFile = {
  id: string;
  name: string;
  jurisdiction: string;
  instrument: string;
  source_url: string;
  description: string;
  modules: Array<{
    id: string;
    framework: string;
    locator: { title: string; article: string; clause: string | null; url: string };
    category: string;
    obligation: string;
    evidence_checklist: string[];
    keywords: string[];
  }>;
};

const MICA = micaJson as FrameworkFile;
const VARA = varaJson as FrameworkFile;
const AURUM = aurumJson as Project;
const DEMO_RUN = demoRunJson as Run;

export const DEMO_PROJECT_ID = AURUM.id;

type Store = {
  runs: Map<string, Run>;
  reviews: ReviewAction[];
  lastRunId: string | null;
  lastRunAt: string | null;
};

const g = globalThis as typeof globalThis & { __regtraceDemo?: Store };

function seed(): Store {
  const run = structuredClone(DEMO_RUN) as Run;
  const runs = new Map<string, Run>();
  runs.set(run.id, run);
  return {
    runs,
    reviews: [],
    lastRunId: run.id,
    lastRunAt: run.created_at,
  };
}

function store(): Store {
  if (!g.__regtraceDemo) g.__regtraceDemo = seed();
  return g.__regtraceDemo;
}

export function health() {
  return {
    status: "ok" as const,
    service: "regtrace-ai",
    generator: "deterministic",
    database: "demo",
    frameworks: 2,
    modules: MICA.modules.length + VARA.modules.length,
    mode: "demo",
  };
}

export function listFrameworks(): Framework[] {
  return [MICA, VARA].map((fw) => ({
    id: fw.id,
    name: fw.name,
    jurisdiction: fw.jurisdiction,
    instrument: fw.instrument,
    source_url: fw.source_url,
    description: fw.description,
    module_count: fw.modules.length,
  }));
}

function summary(): ProjectSummary {
  const s = store();
  return {
    id: AURUM.id,
    name: AURUM.name,
    tagline: AURUM.tagline,
    jurisdictions: AURUM.jurisdictions,
    offerings: AURUM.offerings,
    target_licences: AURUM.target_licences,
    summary: AURUM.summary,
    document_count: AURUM.documents.length,
    last_run_id: s.lastRunId,
    last_run_at: s.lastRunAt,
  };
}

export function listProjects(): ProjectSummary[] {
  return [summary()];
}

export function getProject(id: string): Project | null {
  if (id !== AURUM.id) return null;
  return { ...summary(), documents: AURUM.documents };
}

function cloneRun(source: Run): Run {
  const id = randomUUID();
  const createdAt = new Date().toISOString();
  return {
    ...structuredClone(source),
    id,
    created_at: createdAt,
    generator: "deterministic",
    reviews: [],
    findings: source.findings.map((f) => ({
      ...structuredClone(f),
      id: randomUUID(),
      run_id: id,
      review_action: null,
      flags: (f.flags || []).filter((flag) => !flag.startsWith("hitl_")),
    })),
    gaps: source.gaps.map((g) => ({
      ...structuredClone(g),
      id: randomUUID(),
    })),
  };
}

function attachReviews(run: Run): Run {
  const related = store().reviews.filter((r) => r.run_id === run.id);
  const latest = new Map<string, ReviewAction>();
  for (const r of [...related].sort((a, b) => a.created_at.localeCompare(b.created_at))) {
    latest.set(r.finding_id, r);
  }
  return {
    ...run,
    findings: run.findings.map((f) => ({
      ...f,
      review_action: latest.get(f.id)?.action ?? f.review_action,
    })),
    reviews: [...related].sort((a, b) => b.created_at.localeCompare(a.created_at)),
  };
}

export function evaluateProject(id: string): Run | null {
  if (id !== AURUM.id) return null;
  const s = store();
  const next = cloneRun(DEMO_RUN);
  s.runs.set(next.id, next);
  s.lastRunId = next.id;
  s.lastRunAt = next.created_at;
  return attachReviews(next);
}

export function getRun(id: string): Run | null {
  const run = store().runs.get(id);
  if (!run) return null;
  return attachReviews(run);
}

export function reviewFinding(
  findingId: string,
  body: { action: "accept" | "edit" | "reject"; override_text?: string; note?: string },
): Finding | null {
  const s = store();
  let finding: Finding | undefined;
  Array.from(s.runs.values()).some((run) => {
    finding = run.findings.find((x: Finding) => x.id === findingId);
    return Boolean(finding);
  });
  if (!finding) return null;

  const ra: ReviewAction = {
    id: randomUUID(),
    finding_id: finding.id,
    action: body.action,
    original_text: finding.claim,
    override_text: body.action === "edit" ? (body.override_text ?? null) : null,
    note: body.note ?? null,
    created_at: new Date().toISOString(),
    framework: finding.framework,
    module_id: finding.module_id,
    run_id: finding.run_id,
  };
  s.reviews.unshift(ra);

  if (body.action === "edit" && body.override_text) {
    finding.claim = body.override_text;
    if (!finding.flags.includes("hitl_edited")) finding.flags.push("hitl_edited");
    finding.status = "needs_human_verification";
  } else if (body.action === "reject") {
    if (!finding.flags.includes("hitl_rejected")) finding.flags.push("hitl_rejected");
    finding.status = "unsupported";
  } else if (body.action === "accept") {
    if (!finding.flags.includes("hitl_accepted")) finding.flags.push("hitl_accepted");
    if (finding.status === "needs_human_verification") finding.status = "grounded";
  }
  finding.review_action = body.action;
  return { ...finding, flags: [...finding.flags] };
}

export function listEvalCases(): ReviewAction[] {
  return [...store().reviews].sort((a, b) => b.created_at.localeCompare(a.created_at));
}

export function projectName(): string {
  return AURUM.name;
}

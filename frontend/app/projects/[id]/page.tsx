"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { DocumentPane } from "@/components/DocumentPane";
import { FindingCard } from "@/components/FindingCard";
import { GapPanel } from "@/components/GapPanel";
import { api } from "@/lib/api";
import type { Finding, Project, Run } from "@/lib/types";

export default function ProjectWorkspacePage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [project, setProject] = useState<Project | null>(null);
  const [run, setRun] = useState<Run | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | "MiCA" | "VARA">("all");

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const p = await api.project(id);
        if (cancelled) return;
        setProject(p);
        if (p.last_run_id) {
          const r = await api.run(p.last_run_id);
          if (!cancelled) setRun(r);
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Load failed");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id]);

  async function evaluate() {
    setBusy(true);
    setError(null);
    try {
      const r = await api.evaluate(id, ["MiCA", "VARA"]);
      setRun(r);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Evaluate failed");
    } finally {
      setBusy(false);
    }
  }

  function onUpdated(next: Finding) {
    setRun((current) => {
      if (!current) return current;
      return {
        ...current,
        findings: current.findings.map((f) => (f.id === next.id ? next : f)),
      };
    });
  }

  const findings = useMemo(() => {
    if (!run) return [];
    return run.findings.filter((f) => (filter === "all" ? true : f.framework === filter));
  }, [run, filter]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-mint">
            HITL workspace · source traceability on
          </p>
          <h1 className="text-2xl font-semibold">{project?.name || "Loading…"}</h1>
          <p className="text-sm text-slate-400">{project?.tagline}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={evaluate}
            disabled={busy}
            data-testid="evaluate-button"
            className="rounded-sm bg-mint px-3 py-1.5 text-sm font-medium text-ink-950 hover:bg-white disabled:opacity-50"
          >
            {busy ? "Evaluating…" : "Run MiCA + VARA evaluation"}
          </button>
          {run && (
            <a
              href={api.exportUrl(run.id)}
              className="rounded-sm border border-line px-3 py-1.5 text-sm text-slate-200 hover:border-mint"
            >
              Export markdown
            </a>
          )}
        </div>
      </div>
      {error && <p className="text-sm text-danger">{error}</p>}

      <div
        data-testid="workspace-split"
        className="grid min-h-[72vh] grid-cols-1 overflow-hidden border border-line lg:grid-cols-2"
      >
        <div className="min-h-[50vh] border-b border-line lg:border-b-0 lg:border-r">
          <DocumentPane documents={project?.documents || []} />
        </div>
        <div data-testid="findings-pane" className="flex min-h-0 flex-col bg-ink-950">
          <div className="flex items-center justify-between border-b border-line px-4 py-2">
            <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-slate-500">
              AI findings · citation-bound
            </p>
            <div className="flex gap-1">
              {(["all", "MiCA", "VARA"] as const).map((key) => (
                <button
                  key={key}
                  onClick={() => setFilter(key)}
                  className={`chip ${filter === key ? "border-mint text-mint" : ""}`}
                >
                  {key}
                </button>
              ))}
            </div>
          </div>
          <div className="min-h-0 flex-1 overflow-y-auto">
            {!run && (
              <p className="p-6 text-sm text-slate-500">
                Run an evaluation to retrieve MiCA / VARA modules, generate findings, and validate
                citations. Works with no API key (deterministic generator).
              </p>
            )}
            {findings.map((f) => (
              <FindingCard key={f.id} finding={f} onUpdated={onUpdated} />
            ))}
          </div>
        </div>
      </div>

      {run && <GapPanel gaps={run.gaps} readiness={run.readiness} />}
    </div>
  );
}

"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Framework, ProjectSummary, Run } from "@/lib/types";

export default function DashboardPage() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [frameworks, setFrameworks] = useState<Framework[]>([]);
  const [run, setRun] = useState<Run | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [p, f] = await Promise.all([api.projects(), api.frameworks()]);
        if (cancelled) return;
        setProjects(p);
        setFrameworks(f);
        const last = p.find((x) => x.last_run_id);
        if (last?.last_run_id) {
          const r = await api.run(last.last_run_id);
          if (!cancelled) setRun(r);
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "API unavailable");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-8">
      <section className="border border-line bg-ink-900 p-6">
        <p className="font-mono text-[11px] uppercase tracking-[0.22em] text-mint">
          Compliance engineering · not a smart-contract auditor
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">
          AI-powered Web3 regulatory copilot with Human-in-the-Loop audit.
        </h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">
          Reviewer opens a project pack, evaluates against MiCA and VARA-style VASP rules, and
          reviews AI findings. Every finding is bound to a retrieved module locator. Ungrounded
          claims are dropped or flagged for human verification.
        </p>
      </section>

      {error && (
        <p className="border border-danger/40 bg-danger/10 px-4 py-2 text-sm text-danger">
          Cannot reach API at {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}. {error}
        </p>
      )}

      <section>
        <h2 className="mb-3 font-mono text-[11px] uppercase tracking-[0.18em] text-slate-500">
          Seeded project pack
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          {projects.map((p) => (
            <Link
              key={p.id}
              href={`/projects/${p.id}`}
              data-testid="project-card"
              className="block border border-line bg-ink-900 p-5 hover:border-mint/50"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-lg font-semibold">{p.name}</h3>
                  <p className="text-sm text-slate-400">{p.tagline}</p>
                </div>
                <span className="chip">VASP</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-slate-300">{p.summary}</p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {p.jurisdictions.map((j) => (
                  <span key={j} className="chip">
                    {j}
                  </span>
                ))}
                {p.offerings.map((o) => (
                  <span key={o} className="chip">
                    {o}
                  </span>
                ))}
              </div>
              <p className="mt-3 font-mono text-[11px] text-slate-500">
                {p.last_run_id ? `Last run ${p.last_run_id.slice(0, 8)}…` : "No evaluation yet"}
              </p>
            </Link>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-3 font-mono text-[11px] uppercase tracking-[0.18em] text-slate-500">
          Framework mapping
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          {frameworks.map((f) => (
            <article key={f.id} className="border border-line bg-ink-900 p-5">
              <div className="flex items-baseline justify-between">
                <h3 className="text-lg font-semibold">{f.id}</h3>
                <span className="font-mono text-xs text-mint">{f.module_count} modules</span>
              </div>
              <p className="mt-1 text-xs text-slate-500">{f.instrument}</p>
              <p className="mt-2 text-sm leading-6 text-slate-300">{f.description}</p>
              <a
                href={f.source_url}
                target="_blank"
                rel="noreferrer"
                className="mt-3 inline-block font-mono text-[11px] text-mint underline"
              >
                Official source
              </a>
            </article>
          ))}
        </div>
      </section>

      {run && (
        <section className="border border-line bg-ink-900 p-5">
          <h2 className="font-mono text-[11px] uppercase tracking-[0.18em] text-slate-500">
            Last evaluation run
          </h2>
          <p className="mt-2 text-sm text-slate-300">
            Generator <span className="text-mint">{run.generator}</span> · {run.findings.length}{" "}
            findings · {run.gaps.length} gaps · frameworks {run.frameworks.join(", ")}
          </p>
          <div className="mt-3 flex flex-wrap gap-4 text-sm">
            {run.readiness.map((b) => (
              <span key={b.framework}>
                {b.framework}:{" "}
                <span className="text-ok">{b.covered} covered</span> ·{" "}
                <span className="text-warn">{b.partial} partial</span> ·{" "}
                <span className="text-danger">{b.missing} missing</span>
              </span>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

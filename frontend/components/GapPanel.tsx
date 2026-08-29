import type { Gap, Readiness } from "@/lib/types";

const TONE: Record<string, string> = {
  covered: "text-ok border-ok/30",
  partial: "text-warn border-warn/30",
  missing: "text-danger border-danger/30",
};

export function GapPanel({ gaps, readiness }: { gaps: Gap[]; readiness: Readiness[] }) {
  return (
    <section className="border-t border-line bg-ink-950">
      <div className="border-b border-line px-4 py-2">
        <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-slate-500">
          Licensing readiness · evidence gaps
        </p>
      </div>
      <div className="grid grid-cols-1 gap-3 p-4 md:grid-cols-2">
        {readiness.map((b) => (
          <div key={b.framework} className="rounded-sm border border-line bg-ink-900 p-3">
            <div className="mb-2 flex items-baseline justify-between">
              <h3 className="font-semibold">{b.framework}</h3>
              <span className="font-mono text-[11px] text-slate-500">{b.total} modules</span>
            </div>
            <div className="flex gap-3 text-xs">
              <span className="text-ok">covered {b.covered}</span>
              <span className="text-warn">partial {b.partial}</span>
              <span className="text-danger">missing {b.missing}</span>
            </div>
            <div className="mt-2 flex h-1.5 overflow-hidden rounded-full bg-ink-700">
              <div className="bg-ok" style={{ width: `${(b.covered / b.total) * 100}%` }} />
              <div className="bg-warn" style={{ width: `${(b.partial / b.total) * 100}%` }} />
              <div className="bg-danger" style={{ width: `${(b.missing / b.total) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>
      <ul className="max-h-72 space-y-2 overflow-y-auto px-4 pb-4">
        {gaps.map((g) => (
          <li key={g.id} className={`rounded-sm border bg-ink-900 p-3 ${TONE[g.coverage]}`}>
            <div className="mb-1 flex flex-wrap items-center gap-2 text-xs">
              <span className="font-mono uppercase tracking-[0.12em]">{g.framework}</span>
              <span className="chip">{g.category}</span>
              <span className="chip">{g.coverage}</span>
              {g.locator && (
                <a href={g.locator.url} target="_blank" rel="noreferrer" className="text-mint underline">
                  {g.locator.article}
                  {g.locator.clause ? ` · ${g.locator.clause}` : ""}
                </a>
              )}
            </div>
            {g.missing_items.length > 0 && (
              <ul className="list-disc pl-4 text-[12px] text-slate-300">
                {g.missing_items.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

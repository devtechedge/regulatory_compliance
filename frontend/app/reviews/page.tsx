"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { ReviewAction } from "@/lib/types";

export default function ReviewsPage() {
  const [rows, setRows] = useState<ReviewAction[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .evalCases()
      .then(setRows)
      .catch((err) => setError(err instanceof Error ? err.message : "Load failed"));
  }, []);

  return (
    <div className="space-y-5">
      <div>
        <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-mint">
          HITL eval-case log
        </p>
        <h1 className="text-2xl font-semibold">Human overrides</h1>
        <p className="mt-1 max-w-2xl text-sm text-slate-400">
          Accept / edit / reject actions are stored with original claim, optional override text,
          reviewer note, and timestamp. This is the evaluation set for hallucination mitigation.
        </p>
      </div>
      {error && <p className="text-sm text-danger">{error}</p>}
      {rows.length === 0 && !error && (
        <p className="border border-line bg-ink-900 p-5 text-sm text-slate-500">
          No HITL actions yet. Open the Aurum Custody workspace, run an evaluation, then Accept /
          Edit / Reject a finding.
        </p>
      )}
      <ul className="space-y-3">
        {rows.map((r) => (
          <li key={r.id} className="border border-line bg-ink-900 p-4">
            <div className="mb-2 flex flex-wrap items-center gap-2 text-xs">
              <span className="chip">{r.action}</span>
              <span className="font-mono text-mint">{r.framework}</span>
              <span className="font-mono text-slate-500">{r.module_id}</span>
              <span className="ml-auto font-mono text-slate-500">
                {new Date(r.created_at).toLocaleString()}
              </span>
            </div>
            <p className="text-[12px] text-slate-500">Original</p>
            <p className="text-sm text-slate-300">{r.original_text}</p>
            {r.override_text && (
              <>
                <p className="mt-2 text-[12px] text-slate-500">Override</p>
                <p className="text-sm text-mint">{r.override_text}</p>
              </>
            )}
            {r.note && <p className="mt-2 text-xs text-warn">Note: {r.note}</p>}
          </li>
        ))}
      </ul>
    </div>
  );
}

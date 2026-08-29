"use client";

import { useState } from "react";
import type { Finding } from "@/lib/types";
import { api } from "@/lib/api";
import { ConfidenceBar } from "./ConfidenceBar";
import { StatusBadge } from "./StatusBadge";

export function FindingCard({
  finding,
  onUpdated,
}: {
  finding: Finding;
  onUpdated: (next: Finding) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [text, setText] = useState(finding.claim);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const cite = finding.citations[0];

  async function act(action: "accept" | "edit" | "reject") {
    setBusy(true);
    setError(null);
    try {
      const next = await api.review(finding.id, {
        action,
        override_text: action === "edit" ? text : undefined,
        note: note || undefined,
      });
      onUpdated(next);
      setEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Review failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <article className="border-b border-line bg-ink-900 p-4">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-mint">
          {finding.framework}
        </span>
        <span className="chip">{finding.category}</span>
        <StatusBadge status={finding.status} />
        {finding.review_action && <span className="chip">HITL {finding.review_action}</span>}
        <div className="ml-auto">
          <ConfidenceBar value={finding.confidence} />
        </div>
      </div>

      {cite && (
        <p className="mb-2 font-mono text-[11px] text-slate-400">
          Citation:{" "}
          <a
            href={cite.url}
            target="_blank"
            rel="noreferrer"
            className="text-mint underline decoration-mint/30 underline-offset-2 hover:text-white"
          >
            {cite.title} · {cite.article}
            {cite.clause ? ` · ${cite.clause}` : ""}
          </a>
          <span className="text-slate-600"> · {cite.module_id}</span>
        </p>
      )}

      <p className="text-[13.5px] leading-6 text-slate-200">{finding.claim}</p>

      {finding.flags.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {finding.flags.map((f) => (
            <span key={f} className="chip border-warn/30 text-warn">
              {f}
            </span>
          ))}
        </div>
      )}

      {editing && (
        <div className="mt-3 space-y-2">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="h-28 w-full rounded-sm border border-line bg-ink-950 p-2 text-sm text-slate-100 outline-none focus:border-mint"
          />
        </div>
      )}

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <input
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="HITL note (logged)"
          className="min-w-[180px] flex-1 rounded-sm border border-line bg-ink-950 px-2 py-1 text-xs text-slate-200 outline-none focus:border-mint"
        />
        <button
          disabled={busy}
          onClick={() => act("accept")}
          className="rounded-sm border border-ok/40 bg-ok/10 px-2.5 py-1 text-xs text-ok hover:bg-ok/20 disabled:opacity-50"
        >
          Accept
        </button>
        {editing ? (
          <button
            disabled={busy}
            onClick={() => act("edit")}
            className="rounded-sm border border-mint/40 bg-mint/10 px-2.5 py-1 text-xs text-mint hover:bg-mint/20 disabled:opacity-50"
          >
            Save edit
          </button>
        ) : (
          <button
            disabled={busy}
            onClick={() => setEditing(true)}
            className="rounded-sm border border-line px-2.5 py-1 text-xs text-slate-300 hover:border-mint hover:text-mint disabled:opacity-50"
          >
            Edit
          </button>
        )}
        <button
          disabled={busy}
          onClick={() => act("reject")}
          className="rounded-sm border border-danger/40 bg-danger/10 px-2.5 py-1 text-xs text-danger hover:bg-danger/20 disabled:opacity-50"
        >
          Reject
        </button>
      </div>
      {error && <p className="mt-2 text-xs text-danger">{error}</p>}
    </article>
  );
}

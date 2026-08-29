"use client";

import type { Document } from "@/lib/types";

export function DocumentPane({ documents }: { documents: Document[] }) {
  const doc = documents[0];
  if (!doc) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-slate-500">
        No project pack loaded.
      </div>
    );
  }
  const paragraphs = doc.content.split(/\n\n+/);

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="flex items-center justify-between border-b border-line px-4 py-2">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-slate-500">
            Project pack · {doc.kind}
          </p>
          <p className="text-sm text-slate-200">{doc.title}</p>
        </div>
        <span className="chip">source-traced review surface</span>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto bg-ink-900 p-4">
        <article className="mx-auto max-w-[720px] rounded-sm border border-line bg-[#0e131b] p-8 shadow-inner">
          {paragraphs.map((p, i) => (
            <p key={i} className="mb-4 whitespace-pre-wrap text-[13.5px] leading-6 text-slate-300">
              {p}
            </p>
          ))}
        </article>
      </div>
    </div>
  );
}

"use client";

import { useState } from "react";
import Link from "next/link";
import ThemeToggle from "@/components/ThemeToggle";

const RAIL = [
  "Human-in-the-Loop (HITL)",
  "Source Traceability",
  "VASP Licensing",
  "Hallucination Mitigation",
  "MiCA / VARA Framework Mapping",
];

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/projects/aurum-custody", label: "HITL workspace" },
  { href: "/reviews", label: "Eval cases" },
] as const;

export function Chrome() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-30 border-b border-line bg-ink-950/90 backdrop-blur">
      <div className="mx-auto flex w-full min-w-0 max-w-[1440px] items-center justify-between gap-3 px-4 py-3 sm:px-5">
        <Link href="/" className="flex min-w-0 items-baseline gap-2 sm:gap-3">
          <span className="font-mono text-[11px] tracking-[0.28em] text-mint">REGTRACE</span>
          <span className="truncate text-lg font-semibold tracking-tight">RegTrace-AI</span>
        </Link>
        <div className="flex shrink-0 items-center gap-2 sm:gap-3">
          <nav className="hidden items-center gap-5 text-sm text-slate-300 md:flex">
            {NAV_LINKS.map((l) => (
              <Link key={l.href} href={l.href} className="hover:text-mint">
                {l.label}
              </Link>
            ))}
            <a
              href="https://eur-lex.europa.eu/eli/reg/2023/1114/oj"
              target="_blank"
              rel="noreferrer"
              className="hidden text-xs text-slate-500 hover:text-slate-300 lg:inline"
            >
              MiCA source
            </a>
          </nav>
          <ThemeToggle />
          <button
            type="button"
            className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-line text-slate-300 hover:text-mint md:hidden"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
                <path d="M4 7h16M4 12h16M4 17h16" />
              </svg>
            )}
          </button>
        </div>
      </div>
      {open && (
        <nav className="border-t border-line bg-ink-950 px-4 py-3 md:hidden">
          <div className="mx-auto flex max-w-[1440px] flex-col gap-1 text-sm text-slate-300">
            {NAV_LINKS.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className="rounded-md px-2 py-2.5 hover:bg-ink-900 hover:text-mint"
                onClick={() => setOpen(false)}
              >
                {l.label}
              </Link>
            ))}
            <a
              href="https://eur-lex.europa.eu/eli/reg/2023/1114/oj"
              target="_blank"
              rel="noreferrer"
              className="rounded-md px-2 py-2.5 text-xs text-slate-500 hover:bg-ink-900 hover:text-slate-300"
              onClick={() => setOpen(false)}
            >
              MiCA source
            </a>
          </div>
        </nav>
      )}
      <div className="border-t border-line bg-ink-900">
        <div className="mx-auto flex w-full min-w-0 max-w-[1440px] flex-wrap gap-x-6 gap-y-1 px-4 py-1.5 font-mono text-[10px] uppercase tracking-[0.18em] text-slate-400 sm:px-5 lg:flex-nowrap lg:overflow-x-auto">
          {RAIL.map((item) => (
            <span key={item} className="whitespace-nowrap">
              {item}
            </span>
          ))}
        </div>
      </div>
    </header>
  );
}

import Link from "next/link";
import ThemeToggle from "@/components/ThemeToggle";

const RAIL = [
  "Human-in-the-Loop (HITL)",
  "Source Traceability",
  "VASP Licensing",
  "Hallucination Mitigation",
  "MiCA / VARA Framework Mapping",
];

export function Chrome() {
  return (
    <header className="sticky top-0 z-30 border-b border-line bg-ink-950/90 backdrop-blur">
      <div className="mx-auto flex max-w-[1440px] items-center justify-between gap-4 px-5 py-3">
        <Link href="/" className="flex items-baseline gap-3">
          <span className="font-mono text-[11px] tracking-[0.28em] text-mint">REGTRACE</span>
          <span className="text-lg font-semibold tracking-tight">RegTrace-AI</span>
        </Link>
        <nav className="flex items-center gap-5 text-sm text-slate-300">
          <Link href="/" className="hover:text-mint">
            Dashboard
          </Link>
          <Link href="/projects/aurum-custody" className="hover:text-mint">
            HITL workspace
          </Link>
          <Link href="/reviews" className="hover:text-mint">
            Eval cases
          </Link>
          <a
            href="https://eur-lex.europa.eu/eli/reg/2023/1114/oj"
            target="_blank"
            rel="noreferrer"
            className="hidden text-xs text-slate-500 hover:text-slate-300 md:inline"
          >
            MiCA source
          </a>
          <ThemeToggle />
        </nav>
      </div>
      <div className="border-t border-line bg-ink-900">
        <div className="mx-auto flex max-w-[1440px] gap-6 overflow-x-auto px-5 py-1.5 font-mono text-[10px] uppercase tracking-[0.18em] text-slate-400">
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

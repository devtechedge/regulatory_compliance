export function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(Math.max(0, Math.min(1, value)) * 100);
  const color = pct >= 70 ? "bg-ok" : pct >= 45 ? "bg-warn" : "bg-danger";
  return (
    <div className="flex items-center gap-2">
      <div className="h-1.5 w-24 overflow-hidden rounded-full bg-ink-700">
        <div className={`h-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="font-mono text-[11px] text-slate-400">{pct}%</span>
    </div>
  );
}

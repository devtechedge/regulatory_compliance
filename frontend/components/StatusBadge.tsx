import type { FindingStatus } from "@/lib/types";

const STYLES: Record<FindingStatus, string> = {
  grounded: "border-ok/40 bg-ok/10 text-ok",
  needs_human_verification: "border-warn/40 bg-warn/10 text-warn",
  unsupported: "border-danger/40 bg-danger/10 text-danger",
};

const LABEL: Record<FindingStatus, string> = {
  grounded: "grounded",
  needs_human_verification: "needs human verification",
  unsupported: "unsupported",
};

export function StatusBadge({ status }: { status: FindingStatus }) {
  return (
    <span className={`chip ${STYLES[status]}`}>
      {LABEL[status]}
    </span>
  );
}

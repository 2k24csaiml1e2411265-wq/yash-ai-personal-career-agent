import type { TraceStep } from "../../types";

const STATUS_COLOR: Record<TraceStep["status"], string> = {
  ok: "var(--color-teal)",
  empty: "var(--color-amber)",
  skipped: "var(--color-muted)",
};

export function AgentTrace({ steps }: { steps: TraceStep[] }) {
  return (
    <ol className="space-y-0">
      {steps.map((step, i) => (
        <li key={step.stage} className="relative flex gap-3 pb-5 last:pb-0">
          {i < steps.length - 1 && (
            <span className="absolute left-[5px] top-3 h-full w-px bg-border" aria-hidden="true" />
          )}
          <span
            className="relative mt-1.5 h-[11px] w-[11px] shrink-0 rounded-full border-2"
            style={{
              borderColor: STATUS_COLOR[step.status],
              backgroundColor: step.status === "ok" ? STATUS_COLOR[step.status] : "transparent",
            }}
            aria-hidden="true"
          />
          <div>
            <p className="font-mono text-[11px] uppercase tracking-wide text-muted">{step.stage}</p>
            <p className="text-sm text-text">{step.label}</p>
            <p className="text-xs text-muted">{step.detail}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}

/** Static, illustrative version of the pipeline for the hero section — labels
 * match the real stage names in TraceStep so it's an accurate preview, not
 * decoration. */
export function AgentTracePreview() {
  const steps: { stage: string; label: string }[] = [
    { stage: "intent", label: "Query understood" },
    { stage: "tool_selection", label: "Relevant tools chosen" },
    { stage: "retrieval", label: "Verified knowledge retrieved" },
    { stage: "grounding", label: "Checked against source data" },
    { stage: "generation", label: "Grounded answer composed" },
  ];
  return (
    <ol className="space-y-0">
      {steps.map((step, i) => (
        <li key={step.stage} className="relative flex gap-3 pb-5 last:pb-0">
          {i < steps.length - 1 && (
            <span className="absolute left-[5px] top-3 h-full w-px bg-border" aria-hidden="true" />
          )}
          <span
            className="relative mt-1.5 h-[11px] w-[11px] shrink-0 rounded-full border-2 border-amber"
            aria-hidden="true"
          />
          <div>
            <p className="font-mono text-[11px] uppercase tracking-wide text-muted">{step.stage}</p>
            <p className="text-sm text-text">{step.label}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}

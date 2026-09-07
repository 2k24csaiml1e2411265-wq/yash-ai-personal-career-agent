import type { AgentMode } from "../../types";

const MODES: { key: AgentMode; label: string }[] = [
  { key: "recruiter", label: "Recruiter" },
  { key: "technical", label: "Technical" },
  { key: "project", label: "Project" },
  { key: "about", label: "About" },
];

export function ModeSelector({
  mode,
  onChange,
}: {
  mode: AgentMode;
  onChange: (mode: AgentMode) => void;
}) {
  return (
    <div className="flex gap-1 rounded-md border border-border p-1" role="tablist" aria-label="Agent mode">
      {MODES.map((m) => (
        <button
          key={m.key}
          role="tab"
          aria-selected={mode === m.key}
          onClick={() => onChange(m.key)}
          className={`rounded px-3 py-1.5 text-xs font-medium transition-colors ${
            mode === m.key ? "bg-text text-bg" : "text-muted hover:text-text"
          }`}
        >
          {m.label}
        </button>
      ))}
    </div>
  );
}

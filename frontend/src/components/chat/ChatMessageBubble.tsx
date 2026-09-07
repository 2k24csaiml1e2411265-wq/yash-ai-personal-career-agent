import { useState } from "react";
import { Check, Copy, ChevronDown, RefreshCw } from "lucide-react";
import type { ChatMessage } from "../../types";
import { AgentTrace } from "./AgentTrace";

export function ChatMessageBubble({
  message,
  onRetry,
}: {
  message: ChatMessage;
  onRetry?: () => void;
}) {
  const [copied, setCopied] = useState(false);
  const [traceOpen, setTraceOpen] = useState(false);

  const isUser = message.role === "user";

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-lg bg-text px-4 py-2.5 text-sm text-bg">
          {message.content}
        </div>
      </div>
    );
  }

  if (message.error) {
    return (
      <div className="flex justify-start">
        <div className="max-w-[85%] rounded-lg border border-amber/40 bg-surface px-4 py-3 text-sm text-text">
          <p>{message.error}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-2 inline-flex items-center gap-1.5 text-xs text-amber hover:underline"
            >
              <RefreshCw size={12} /> Retry
            </button>
          )}
        </div>
      </div>
    );
  }

  const response = message.response;

  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] rounded-lg border border-border bg-surface px-4 py-3 text-sm text-text">
        <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>

        {response && response.sources.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5 border-t border-border pt-3">
            {response.sources.map((s) => (
              <span
                key={s.label}
                className="rounded border border-border px-2 py-0.5 font-mono text-[10px] text-muted"
              >
                {s.label}
              </span>
            ))}
          </div>
        )}

        <div className="mt-3 flex items-center gap-3 text-xs text-muted">
          <button onClick={handleCopy} className="inline-flex items-center gap-1 hover:text-text">
            {copied ? <Check size={12} /> : <Copy size={12} />}
            {copied ? "Copied" : "Copy"}
          </button>

          {response && (
            <button
              onClick={() => setTraceOpen((o) => !o)}
              className="inline-flex items-center gap-1 hover:text-text"
            >
              <ChevronDown size={12} className={traceOpen ? "rotate-180 transition-transform" : "transition-transform"} />
              {response.llm_used ? "LLM-generated" : "Fallback mode"} · {response.latency_ms}ms
            </button>
          )}
        </div>

        {response && traceOpen && (
          <div className="mt-3 border-t border-border pt-3">
            <AgentTrace steps={response.trace} />
          </div>
        )}
      </div>
    </div>
  );
}

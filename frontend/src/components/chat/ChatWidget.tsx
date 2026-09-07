import { useEffect, useRef, useState } from "react";
import { Send, Trash2 } from "lucide-react";
import { useChat } from "../../hooks/useChat";
import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { ModeSelector } from "./ModeSelector";
import { ChatMessageBubble } from "./ChatMessageBubble";

export function ChatWidget() {
  const { mode, setMode, messages, pending, send, retry } = useChat("recruiter");
  const modes = useFetch(api.getModes, []);
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, pending]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    send(input);
    setInput("");
  };

  const suggestions =
    modes.status === "success" ? modes.data[mode]?.suggested_questions ?? [] : [];

  return (
    <div className="rounded-lg border border-border bg-surface">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border p-4">
        <ModeSelector mode={mode} onChange={setMode} />
        {messages.length > 0 && (
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-1.5 text-xs text-muted hover:text-text"
          >
            <Trash2 size={12} /> Clear
          </button>
        )}
      </div>

      <div ref={scrollRef} className="max-h-[480px] min-h-[240px] space-y-4 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div>
            <p className="text-sm text-muted">
              Ask about my projects, technical skills, experience, or the systems I've built.
            </p>
            {suggestions.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {suggestions.map((q) => (
                  <button
                    key={q}
                    onClick={() => send(q)}
                    className="rounded-md border border-border px-3 py-1.5 text-left text-xs text-text/90 hover:border-amber/50 hover:text-amber"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {messages.map((m, i) => (
          <ChatMessageBubble key={i} message={m} onRetry={m.error ? retry : undefined} />
        ))}

        {pending && (
          <div className="flex justify-start">
            <div className="flex items-center gap-1.5 rounded-lg border border-border bg-surface px-4 py-3">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-amber" />
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-amber [animation-delay:0.15s]" />
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-amber [animation-delay:0.3s]" />
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 border-t border-border p-4">
        <label htmlFor="chat-input" className="sr-only">
          Ask Yash AI a question
        </label>
        <input
          id="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          disabled={pending}
          className="flex-1 rounded-md border border-border bg-bg px-3 py-2 text-sm text-text placeholder:text-muted focus:border-amber/60"
        />
        <button
          type="submit"
          disabled={pending || !input.trim()}
          aria-label="Send"
          className="inline-flex items-center justify-center rounded-md bg-text px-4 py-2 text-bg disabled:opacity-40"
        >
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}

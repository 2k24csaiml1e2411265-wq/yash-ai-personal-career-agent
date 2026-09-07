import { useCallback, useState } from "react";
import { api, ApiError } from "../api/client";
import type { AgentMode, ChatMessage } from "../types";

export function useChat(initialMode: AgentMode = "recruiter") {
  const [mode, setMode] = useState<AgentMode>(initialMode);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [pending, setPending] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState<string | null>(null);

  const send = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || pending) return;

      setLastFailedMessage(null);
      const userMessage: ChatMessage = { role: "user", content: trimmed };
      setMessages((prev) => [...prev, userMessage]);
      setPending(true);

      try {
        const response = await api.chat(trimmed, mode, messages);
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: response.answer, response },
        ]);
      } catch (err) {
        const message =
          err instanceof ApiError ? err.message : "Something went wrong answering that.";
        setMessages((prev) => [...prev, { role: "assistant", content: "", error: message }]);
        setLastFailedMessage(trimmed);
      } finally {
        setPending(false);
      }
    },
    [mode, messages, pending]
  );

  const retry = useCallback(() => {
    if (!lastFailedMessage) return;
    setMessages((prev) => prev.slice(0, -1)); // drop the failed assistant entry
    send(lastFailedMessage);
  }, [lastFailedMessage, send]);

  const clear = useCallback(() => {
    setMessages([]);
    setLastFailedMessage(null);
  }, []);

  return { mode, setMode, messages, pending, send, retry, clear, lastFailedMessage };
}

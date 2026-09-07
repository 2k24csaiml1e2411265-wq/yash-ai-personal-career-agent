import { ChatWidget } from "../chat/ChatWidget";

export function AskYashAI() {
  return (
    <section id="ask-yash-ai" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">AI Agent</p>
      <h2 className="font-display text-2xl font-semibold text-text">Ask Yash AI</h2>
      <p className="mt-2 max-w-lg text-sm text-muted">
        Explore my work, skills, projects, and experience — answered only from verified
        information, with sources.
      </p>
      <div className="mt-8">
        <ChatWidget />
      </div>
    </section>
  );
}

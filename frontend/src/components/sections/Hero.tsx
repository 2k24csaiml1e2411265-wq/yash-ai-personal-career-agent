import { Github, Linkedin, FileText } from "lucide-react";
import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { AgentTracePreview } from "../chat/AgentTrace";
import { Skeleton } from "../ui/primitives";

export function Hero() {
  const profile = useFetch(api.getProfile, []);
  const links = useFetch(api.getLinks, []);

  return (
    <section className="mx-auto grid max-w-content gap-12 px-5 pb-20 pt-16 md:grid-cols-[1.2fr,1fr] md:items-center md:pt-24">
      <div>
        <p className="section-eyebrow mb-4">Personal AI Career Agent</p>

        {profile.status === "loading" && (
          <>
            <Skeleton className="mb-3 h-12 w-72" />
            <Skeleton className="h-6 w-96 max-w-full" />
          </>
        )}

        {profile.status === "error" && (
          <p className="text-sm text-muted">Couldn't load profile data right now.</p>
        )}

        {profile.status === "success" && (
          <>
            <h1 className="font-display text-4xl font-semibold tracking-tight text-text sm:text-5xl">
              {profile.data.name}
            </h1>
            <p className="mt-3 text-lg text-muted">{profile.data.tagline}</p>
            <p className="mt-6 max-w-xl text-base leading-relaxed text-text/90">
              {profile.data.positioning_statement}
            </p>
          </>
        )}

        <div className="mt-8 flex flex-wrap items-center gap-3">
          <a
            href="#projects"
            className="rounded-md bg-text px-5 py-2.5 text-sm font-medium text-bg hover:opacity-90"
          >
            Explore Projects
          </a>
          <a
            href="#ask-yash-ai"
            className="rounded-md border border-border px-5 py-2.5 text-sm font-medium text-text hover:border-amber/60 hover:text-amber"
          >
            Ask Yash AI
          </a>
          {links.status === "success" && (
            <div className="ml-1 flex items-center gap-1">
              <a
                href={links.data.github}
                target="_blank"
                rel="noreferrer"
                aria-label="GitHub"
                className="rounded-md p-2.5 text-muted hover:text-text"
              >
                <Github size={18} />
              </a>
              <a
                href={links.data.linkedin}
                target="_blank"
                rel="noreferrer"
                aria-label="LinkedIn"
                className="rounded-md p-2.5 text-muted hover:text-text"
              >
                <Linkedin size={18} />
              </a>
              {links.data.resume !== "Not provided" && (
                <a
                  href={links.data.resume}
                  target="_blank"
                  rel="noreferrer"
                  aria-label="Resume"
                  className="rounded-md p-2.5 text-muted hover:text-text"
                >
                  <FileText size={18} />
                </a>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="rounded-lg border border-border bg-surface p-6">
        <p className="section-eyebrow mb-5">// agent pipeline</p>
        <AgentTracePreview />
        <a
          href="#ask-yash-ai"
          className="mt-6 block text-center text-xs text-muted underline decoration-border underline-offset-4 hover:text-amber"
        >
          See it run live →
        </a>
      </div>
    </section>
  );
}

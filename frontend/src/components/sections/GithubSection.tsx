import { Github } from "lucide-react";
import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { Skeleton } from "../ui/primitives";

export function GithubSection() {
  const github = useFetch(api.getGithub, []);
  const links = useFetch(api.getLinks, []);

  return (
    <section id="github" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">GitHub</p>
      <div className="rounded-lg border border-border bg-surface p-6">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-text">
            <Github size={18} />
            <span className="text-sm font-medium">Public activity</span>
          </div>
          {links.status === "success" && (
            <a
              href={links.data.github}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-muted hover:text-amber"
            >
              View profile →
            </a>
          )}
        </div>

        {github.status === "loading" && (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        )}

        {github.status === "success" && github.data.available && (
          <pre className="whitespace-pre-wrap font-mono text-xs leading-relaxed text-text/90">
            {github.data.summary}
          </pre>
        )}

        {github.status === "success" && !github.data.available && (
          <p className="text-sm text-muted">{github.data.note}</p>
        )}

        {github.status === "error" && (
          <p className="text-sm text-muted">Live GitHub data isn't available right now.</p>
        )}
      </div>
    </section>
  );
}

import { useParams, Link } from "react-router-dom";
import { ArrowLeft, ExternalLink } from "lucide-react";
import { api } from "../api/client";
import { useFetch } from "../hooks/useFetch";
import { Badge, Skeleton } from "../components/ui/primitives";

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const project = useFetch(() => api.getProject(id ?? ""), [id]);

  return (
    <div className="mx-auto max-w-content px-5 py-16">
      <Link
        to="/#projects"
        className="mb-8 inline-flex items-center gap-2 text-sm text-muted hover:text-text"
      >
        <ArrowLeft size={16} /> Back to projects
      </Link>

      {project.status === "loading" && (
        <div className="space-y-4">
          <Skeleton className="h-10 w-96 max-w-full" />
          <Skeleton className="h-5 w-full" />
          <Skeleton className="h-5 w-full" />
        </div>
      )}

      {project.status === "error" && (
        <div>
          <h1 className="font-display text-2xl font-semibold text-text">Project not found</h1>
          <p className="mt-2 text-sm text-muted">{project.error}</p>
        </div>
      )}

      {project.status === "success" && (
        <article>
          <p className="section-eyebrow mb-3">{project.data.category.join(" · ")}</p>
          <h1 className="font-display text-3xl font-semibold text-text sm:text-4xl">
            {project.data.name}
          </h1>
          <p className="mt-3 text-lg text-muted">{project.data.tagline}</p>

          <div className="mt-6 flex flex-wrap gap-2">
            {project.data.technologies.map((t) => (
              <Badge key={t}>{t}</Badge>
            ))}
          </div>

          <div className="mt-6 flex flex-wrap gap-3">
            {project.data.github !== "Not provided" && (
              <a
                href={project.data.github}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 rounded-md border border-border px-4 py-2 text-sm text-text hover:border-amber/60 hover:text-amber"
              >
                GitHub <ExternalLink size={14} />
              </a>
            )}
            {project.data.demo !== "Not provided" && (
              <a
                href={project.data.demo}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 rounded-md border border-border px-4 py-2 text-sm text-text hover:border-amber/60 hover:text-amber"
              >
                Live demo <ExternalLink size={14} />
              </a>
            )}
          </div>

          <div className="mt-12 grid gap-10 md:grid-cols-2">
            <section>
              <h2 className="font-display text-lg font-semibold text-text">Problem</h2>
              <p className="mt-2 text-sm leading-relaxed text-text/90">{project.data.problem}</p>
            </section>
            <section>
              <h2 className="font-display text-lg font-semibold text-text">Solution</h2>
              <p className="mt-2 text-sm leading-relaxed text-text/90">{project.data.solution}</p>
            </section>
          </div>

          <section className="mt-10">
            <h2 className="font-display text-lg font-semibold text-text">Key features</h2>
            <ul className="mt-3 grid gap-2 sm:grid-cols-2">
              {project.data.features.map((f) => (
                <li
                  key={f}
                  className="flex items-start gap-2 rounded-md border border-border bg-surface px-3 py-2 text-sm text-text/90"
                >
                  <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-teal" aria-hidden="true" />
                  {f}
                </li>
              ))}
            </ul>
          </section>

          {project.data.engineering_decisions.length > 0 && (
            <section className="mt-10">
              <h2 className="font-display text-lg font-semibold text-text">
                Engineering decisions
              </h2>
              <ul className="mt-3 space-y-2">
                {project.data.engineering_decisions.map((d) => (
                  <li key={d} className="text-sm leading-relaxed text-text/90">
                    — {d}
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section className="mt-10">
            <h2 className="font-display text-lg font-semibold text-text">Architecture</h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">{project.data.architecture}</p>
          </section>
        </article>
      )}
    </div>
  );
}

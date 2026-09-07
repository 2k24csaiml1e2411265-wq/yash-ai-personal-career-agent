import { useMemo, useState } from "react";
import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { ProjectCard } from "../projects/ProjectCard";
import { Skeleton } from "../ui/primitives";

export function Projects() {
  const projects = useFetch(api.getProjects, []);
  const [filter, setFilter] = useState<string>("All");

  const categories = useMemo(() => {
    if (projects.status !== "success") return ["All"];
    const set = new Set<string>();
    projects.data.forEach((p) => p.category.forEach((c) => set.add(c)));
    return ["All", ...Array.from(set)];
  }, [projects]);

  const filtered = useMemo(() => {
    if (projects.status !== "success") return [];
    if (filter === "All") return projects.data;
    return projects.data.filter((p) => p.category.includes(filter));
  }, [projects, filter]);

  return (
    <section id="projects" className="mx-auto max-w-content px-5 py-20">
      <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="section-eyebrow mb-3">Projects</p>
          <h2 className="font-display text-2xl font-semibold text-text">What I've built</h2>
        </div>
        {categories.length > 1 && (
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setFilter(cat)}
                className={`rounded-md border px-3 py-1.5 text-xs font-medium transition-colors ${
                  filter === cat
                    ? "border-amber text-amber"
                    : "border-border text-muted hover:text-text"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        )}
      </div>

      {projects.status === "loading" && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48" />
          ))}
        </div>
      )}

      {projects.status === "error" && (
        <p className="text-sm text-muted">Couldn't load projects right now — try refreshing.</p>
      )}

      {projects.status === "success" && filtered.length === 0 && (
        <p className="text-sm text-muted">No projects in this category yet.</p>
      )}

      {projects.status === "success" && filtered.length > 0 && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}
    </section>
  );
}

import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";
import type { Project } from "../../types";
import { Badge } from "../ui/primitives";

export function ProjectCard({ project }: { project: Project }) {
  return (
    <Link
      to={`/projects/${project.id}`}
      className="group flex flex-col rounded-lg border border-border bg-surface p-6 transition-colors hover:border-amber/50"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-display text-lg font-semibold text-text">{project.name}</h3>
        <ArrowUpRight
          size={18}
          className="mt-1 shrink-0 text-muted transition-colors group-hover:text-amber"
        />
      </div>
      <p className="mt-2 text-sm leading-relaxed text-muted">{project.short_description}</p>
      <div className="mt-4 flex flex-wrap gap-1.5">
        {project.technologies.slice(0, 4).map((tech) => (
          <Badge key={tech}>{tech}</Badge>
        ))}
      </div>
      <div className="mt-4 flex items-center gap-2 border-t border-border pt-4 text-xs text-muted">
        <span
          className="h-1.5 w-1.5 rounded-full bg-teal"
          aria-hidden="true"
        />
        {project.status}
      </div>
    </Link>
  );
}

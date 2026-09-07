import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { Badge, Skeleton } from "../ui/primitives";

export function Experience() {
  const experience = useFetch(api.getExperience, []);

  return (
    <section id="experience" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">Experience</p>
      <h2 className="mb-8 font-display text-2xl font-semibold text-text">Where I've worked</h2>

      {experience.status === "loading" && (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24" />
          ))}
        </div>
      )}

      {experience.status === "error" && (
        <p className="text-sm text-muted">Couldn't load experience right now.</p>
      )}

      {experience.status === "success" && (
        <div className="space-y-0 border-l border-border">
          {experience.data.map((exp) => (
            <div key={exp.id} className="relative pb-10 pl-8 last:pb-0">
              <span
                className="absolute -left-[5px] top-1.5 h-[9px] w-[9px] rounded-full bg-amber"
                aria-hidden="true"
              />
              <p className="font-mono text-xs text-muted">{exp.duration}</p>
              <h3 className="mt-1 font-display text-base font-semibold text-text">
                {exp.role} · {exp.organization}
              </h3>
              <p className="text-sm text-muted">{exp.location}</p>
              <p className="mt-2 max-w-2xl text-sm leading-relaxed text-text/90">
                {exp.description}
              </p>
              {exp.highlights.length > 0 && (
                <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-muted">
                  {exp.highlights.map((h) => (
                    <li key={h}>{h}</li>
                  ))}
                </ul>
              )}
              {exp.technologies.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {exp.technologies.map((t) => (
                    <Badge key={t}>{t}</Badge>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

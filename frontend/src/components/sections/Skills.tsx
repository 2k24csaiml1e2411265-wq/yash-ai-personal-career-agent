import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { Skeleton } from "../ui/primitives";

const CATEGORY_LABELS: Record<string, string> = {
  programming: "Programming",
  ai_ml: "AI / ML",
  backend: "Backend",
  cloud_data: "Cloud & Data",
};

export function Skills() {
  const skills = useFetch(api.getSkills, []);

  return (
    <section id="skills" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">Skills</p>
      <h2 className="mb-8 font-display text-2xl font-semibold text-text">Technical toolkit</h2>

      {skills.status === "loading" && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
      )}

      {skills.status === "error" && (
        <p className="text-sm text-muted">Couldn't load skills right now.</p>
      )}

      {skills.status === "success" && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {Object.entries(skills.data).map(([category, items]) => (
            <div key={category} className="rounded-lg border border-border bg-surface p-5">
              <p className="font-mono text-[11px] uppercase tracking-wide text-amber">
                {CATEGORY_LABELS[category] ?? category}
              </p>
              <ul className="mt-3 space-y-1.5">
                {items.map((item) => (
                  <li key={item} className="text-sm text-text/90">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

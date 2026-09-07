import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { Skeleton } from "../ui/primitives";

export function About() {
  const profile = useFetch(api.getProfile, []);
  const education = useFetch(api.getEducation, []);

  return (
    <section id="about" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">About</p>
      <div className="grid gap-10 md:grid-cols-[1.4fr,1fr]">
        <div>
          {profile.status === "loading" && (
            <div className="space-y-2">
              <Skeleton className="h-5 w-full" />
              <Skeleton className="h-5 w-full" />
              <Skeleton className="h-5 w-2/3" />
            </div>
          )}
          {profile.status === "error" && (
            <p className="text-sm text-muted">Couldn't load this section right now.</p>
          )}
          {profile.status === "success" && (
            <p className="text-base leading-relaxed text-text/90">{profile.data.about}</p>
          )}
        </div>

        <div className="space-y-6">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-wide text-muted">Education</p>
            {education.status === "success" &&
              education.data.map((edu) => (
                <div key={edu.institution} className="mt-2">
                  <p className="text-sm font-medium text-text">{edu.institution}</p>
                  <p className="text-sm text-muted">{edu.degree}</p>
                  <p className="text-sm text-muted">
                    {edu.duration} · {edu.status}
                  </p>
                  {edu.highlights.length > 0 && (
                    <ul className="mt-1 list-inside list-disc text-sm text-muted">
                      {edu.highlights.map((h) => (
                        <li key={h}>{h}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
          </div>

          {profile.status === "success" && (
            <div>
              <p className="font-mono text-[11px] uppercase tracking-wide text-muted">
                Currently learning
              </p>
              <p className="mt-2 text-sm text-text/90">{profile.data.currently_learning}</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

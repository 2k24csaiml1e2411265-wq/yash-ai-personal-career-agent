import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";
import { Skeleton } from "../ui/primitives";

export function Certifications() {
  const certs = useFetch(api.getCertifications, []);

  return (
    <section id="certifications" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">Certifications</p>
      <h2 className="mb-8 font-display text-2xl font-semibold text-text">Credentials</h2>

      {certs.status === "loading" && (
        <div className="grid gap-4 sm:grid-cols-2">
          {[1, 2].map((i) => (
            <Skeleton key={i} className="h-20" />
          ))}
        </div>
      )}

      {certs.status === "error" && (
        <p className="text-sm text-muted">Couldn't load certifications right now.</p>
      )}

      {certs.status === "success" && certs.data.length === 0 && (
        <p className="text-sm text-muted">
          No verified certifications on file yet — this section will fill in as they're added.
        </p>
      )}

      {certs.status === "success" && certs.data.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2">
          {certs.data.map((cert) => (
            <div key={cert.name} className="rounded-lg border border-border bg-surface p-5">
              <p className="font-medium text-text">{cert.name}</p>
              <p className="text-sm text-muted">
                {cert.issuer} · {cert.date}
              </p>
              {cert.credential_link && (
                <a
                  href={cert.credential_link}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-2 inline-block text-sm text-amber hover:underline"
                >
                  View credential
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

import { Github, Linkedin, Mail } from "lucide-react";
import { useFetch } from "../../hooks/useFetch";
import { api } from "../../api/client";

export function Contact() {
  const links = useFetch(api.getLinks, []);

  return (
    <section id="contact" className="mx-auto max-w-content px-5 py-20">
      <p className="section-eyebrow mb-3">Contact</p>
      <h2 className="font-display text-2xl font-semibold text-text">Let's talk</h2>
      <p className="mt-3 max-w-lg text-sm leading-relaxed text-muted">
        Open to AI/ML and software engineering internships. The quickest way to reach me is
        email or LinkedIn.
      </p>

      {links.status === "success" && (
        <div className="mt-6 flex flex-wrap gap-3">
          <a
            href={`mailto:${links.data.email}`}
            className="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2.5 text-sm text-text hover:border-amber/60 hover:text-amber"
          >
            <Mail size={16} /> {links.data.email}
          </a>
          <a
            href={links.data.linkedin}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2.5 text-sm text-text hover:border-amber/60 hover:text-amber"
          >
            <Linkedin size={16} /> LinkedIn
          </a>
          <a
            href={links.data.github}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2.5 text-sm text-text hover:border-amber/60 hover:text-amber"
          >
            <Github size={16} /> GitHub
          </a>
        </div>
      )}
    </section>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-content flex-col items-center justify-between gap-3 px-5 py-8 text-xs text-muted sm:flex-row">
        <p>© {new Date().getFullYear()} Yash Kushwaha</p>
        <p className="font-mono">Built with React, FastAPI, and a grounded RAG pipeline.</p>
      </div>
    </footer>
  );
}

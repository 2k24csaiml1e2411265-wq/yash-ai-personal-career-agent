import type {
  Profile,
  Education,
  Links,
  Experience,
  Project,
  SkillCategories,
  Certification,
  ModeInfo,
  ChatResponse,
  AgentMode,
  ChatMessage,
  GithubActivity,
} from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(
      "Can't reach the Yash AI backend right now. It may be asleep (free-tier hosting) or offline."
    );
  }

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      /* ignore parse failure, use default detail */
    }
    throw new ApiError(detail, res.status);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getProfile: () => request<Profile>("/api/profile"),
  getEducation: () => request<Education[]>("/api/education"),
  getLinks: () => request<Links>("/api/links"),
  getExperience: () => request<Experience[]>("/api/experience"),
  getSkills: () => request<SkillCategories>("/api/skills"),
  getCertifications: () => request<Certification[]>("/api/certifications"),
  getProjects: () => request<Project[]>("/api/projects"),
  getProject: (id: string) => request<Project>(`/api/projects/${id}`),
  getModes: () => request<Record<AgentMode, ModeInfo>>("/api/modes"),
  getGithub: () => request<GithubActivity>("/api/github"),
  chat: (message: string, mode: AgentMode, history: ChatMessage[]) =>
    request<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        mode,
        history: history
          .filter((m) => !m.error)
          .slice(-10)
          .map((m) => ({ role: m.role, content: m.content })),
      }),
    }),
};

export { ApiError };

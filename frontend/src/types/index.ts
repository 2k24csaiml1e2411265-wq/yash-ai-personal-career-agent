export interface Profile {
  name: string;
  tagline: string;
  positioning_statement: string;
  about: string;
  location: string;
  career_direction: string;
  currently_learning: string;
  resume_url: string;
  open_to: string[];
}

export interface Education {
  institution: string;
  degree: string;
  duration: string;
  status: string;
  highlights: string[];
}

export interface Links {
  github: string;
  linkedin: string;
  email: string;
  resume: string;
}

export interface Experience {
  id: string;
  organization: string;
  role: string;
  duration: string;
  location: string;
  description: string;
  technologies: string[];
  highlights: string[];
}

export interface Project {
  id: string;
  name: string;
  tagline: string;
  category: string[];
  short_description: string;
  problem: string;
  solution: string;
  features: string[];
  technologies: string[];
  architecture: string;
  engineering_decisions: string[];
  status: string;
  github: string;
  demo: string;
}

export type SkillCategories = Record<string, string[]>;

export interface Certification {
  name: string;
  issuer: string;
  date: string;
  credential_link?: string;
}

export type AgentMode = "recruiter" | "technical" | "project" | "about";

export interface ModeInfo {
  label: string;
  description: string;
  suggested_questions: string[];
}

export interface Source {
  label: string;
  section: string;
  ref_id?: string | null;
  url?: string | null;
}

export interface TraceStep {
  stage: "intent" | "tool_selection" | "retrieval" | "grounding" | "generation";
  label: string;
  detail: string;
  status: "ok" | "empty" | "skipped";
}

export interface ChatResponse {
  answer: string;
  grounded: boolean;
  sources: Source[];
  suggested_followups: string[];
  tools_used: string[];
  trace: TraceStep[];
  latency_ms: number;
  llm_used: boolean;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  response?: ChatResponse;
  error?: string;
}

export interface GithubActivity {
  available: boolean;
  summary: string | null;
  note: string | null;
}

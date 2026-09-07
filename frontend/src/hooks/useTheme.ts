import { useCallback, useEffect, useState } from "react";

export type ThemePreference = "dark" | "light" | "system";
type ResolvedTheme = "dark" | "light";

const STORAGE_KEY = "yash-ai-theme";

function resolveSystemTheme(): ResolvedTheme {
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

export function useTheme() {
  const [preference, setPreferenceState] = useState<ThemePreference>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored === "light" || stored === "dark" ? stored : "system";
  });
  const [resolved, setResolved] = useState<ResolvedTheme>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored === "light" || stored === "dark" ? stored : resolveSystemTheme();
  });

  useEffect(() => {
    const applied = preference === "system" ? resolveSystemTheme() : preference;
    setResolved(applied);
    document.documentElement.classList.remove("dark", "light");
    document.documentElement.classList.add(applied);
  }, [preference]);

  useEffect(() => {
    if (preference !== "system") return;
    const mq = window.matchMedia("(prefers-color-scheme: light)");
    const handler = () => {
      const applied = resolveSystemTheme();
      setResolved(applied);
      document.documentElement.classList.remove("dark", "light");
      document.documentElement.classList.add(applied);
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [preference]);

  const setPreference = useCallback((next: ThemePreference) => {
    setPreferenceState(next);
    if (next === "system") {
      localStorage.removeItem(STORAGE_KEY);
    } else {
      localStorage.setItem(STORAGE_KEY, next);
    }
  }, []);

  return { preference, resolved, setPreference };
}

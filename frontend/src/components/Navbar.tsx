import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Menu, X, Moon, Sun, Laptop } from "lucide-react";
import { useTheme } from "../hooks/useTheme";

const NAV_ITEMS = [
  { label: "About", href: "#about" },
  { label: "Projects", href: "#projects" },
  { label: "Experience", href: "#experience" },
  { label: "Skills", href: "#skills" },
  { label: "Ask Yash AI", href: "#ask-yash-ai" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);
  const { preference, setPreference } = useTheme();
  const location = useLocation();
  const navigate = useNavigate();

  const handleNavClick = (href: string) => {
    setOpen(false);
    if (location.pathname !== "/") {
      navigate("/" + href);
    } else {
      document.querySelector(href)?.scrollIntoView({ behavior: "smooth" });
    }
  };

  const cycleTheme = () => {
    const order: Array<typeof preference> = ["dark", "light", "system"];
    const next = order[(order.indexOf(preference) + 1) % order.length];
    setPreference(next);
  };

  const ThemeIcon = preference === "dark" ? Moon : preference === "light" ? Sun : Laptop;

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-bg/85 backdrop-blur">
      <nav className="mx-auto flex max-w-content items-center justify-between px-5 py-4">
        <Link to="/" className="font-display text-sm font-semibold tracking-tight text-text">
          Yash Kushwaha
        </Link>

        <div className="hidden items-center gap-7 md:flex">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.href}
              onClick={() => handleNavClick(item.href)}
              className="text-sm text-muted transition-colors hover:text-text"
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="hidden items-center gap-3 md:flex">
          <button
            onClick={cycleTheme}
            aria-label={`Theme: ${preference}. Click to change.`}
            className="rounded-md border border-border p-2 text-muted hover:text-amber"
          >
            <ThemeIcon size={16} />
          </button>
          <button
            onClick={() => handleNavClick("#ask-yash-ai")}
            className="rounded-md bg-text px-4 py-2 text-sm font-medium text-bg hover:opacity-90"
          >
            Ask Yash AI
          </button>
        </div>

        <button
          className="text-text md:hidden"
          onClick={() => setOpen((o) => !o)}
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>

      {open && (
        <div className="border-t border-border px-5 py-4 md:hidden">
          <div className="flex flex-col gap-4">
            {NAV_ITEMS.map((item) => (
              <button
                key={item.href}
                onClick={() => handleNavClick(item.href)}
                className="text-left text-sm text-muted hover:text-text"
              >
                {item.label}
              </button>
            ))}
            <button
              onClick={cycleTheme}
              className="flex items-center gap-2 text-left text-sm text-muted hover:text-text"
            >
              <ThemeIcon size={16} /> Theme: {preference}
            </button>
          </div>
        </div>
      )}
    </header>
  );
}

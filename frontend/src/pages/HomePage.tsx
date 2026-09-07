import { Hero } from "../components/sections/Hero";
import { About } from "../components/sections/About";
import { Projects } from "../components/sections/Projects";
import { Experience } from "../components/sections/Experience";
import { Skills } from "../components/sections/Skills";
import { Certifications } from "../components/sections/Certifications";
import { AskYashAI } from "../components/sections/AskYashAI";
import { GithubSection } from "../components/sections/GithubSection";
import { Contact } from "../components/sections/Contact";

export function HomePage() {
  return (
    <>
      <Hero />
      <About />
      <Projects />
      <Experience />
      <Skills />
      <AskYashAI />
      <Certifications />
      <GithubSection />
      <Contact />
    </>
  );
}

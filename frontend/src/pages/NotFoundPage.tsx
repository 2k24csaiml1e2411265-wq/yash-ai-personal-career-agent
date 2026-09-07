import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="mx-auto flex max-w-content flex-col items-center px-5 py-24 text-center">
      <p className="section-eyebrow mb-3">404</p>
      <h1 className="font-display text-2xl font-semibold text-text">Page not found</h1>
      <Link to="/" className="mt-6 rounded-md bg-text px-4 py-2 text-sm text-bg">
        Back home
      </Link>
    </div>
  );
}

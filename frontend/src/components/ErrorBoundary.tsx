import { Component, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: unknown) {
    // Logged for local debugging only — never shown to the visitor.
    console.error("Unhandled UI error:", error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="mx-auto flex max-w-content flex-col items-center px-5 py-24 text-center">
          <h1 className="font-display text-xl font-semibold text-text">Something went wrong</h1>
          <p className="mt-2 max-w-sm text-sm text-muted">
            This part of the page hit an unexpected error. Refreshing usually fixes it.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-6 rounded-md bg-text px-4 py-2 text-sm text-bg"
          >
            Refresh
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

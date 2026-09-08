import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <p className="eyebrow">Agentic RAG Platform</p>
      <h1>Build inspectable AI workflows.</h1>
      <p className="lede">A focused local workspace for ingestion, retrieval, and agent experiments.</p>
      <div className="status">Backend foundation ready</div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);


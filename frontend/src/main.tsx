import { FormEvent, StrictMode, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { askQuestion, ChatResponse, deleteDocument, Document, listDocuments, uploadDocument } from "./api";
import "./styles.css";

const demoDocuments = [
  ["architecture.md", "# Atlas architecture\n\nAtlas uses Qdrant for document chunks and PostgreSQL for metadata. Chunks are 800 characters with 150 characters of overlap."],
  ["incident-response.md", "# Incident response\n\nFor Sev-1 incidents, the incident commander is paged within 15 minutes. Customer updates go to the public status page."],
  ["engineering-handbook.md", "# Engineering handbook\n\nBackend services use Python 3.11. Ruff enforces 100 character lines and pull requests need two approvals."],
] as const;

type ConversationEntry = { question: string; response: ChatResponse };

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState<ConversationEntry[]>([]);
  const [activeResponse, setActiveResponse] = useState<ChatResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("Loading workspace…");
  const fileInput = useRef<HTMLInputElement>(null);

  const refreshDocuments = async () => {
    try { setDocuments(await listDocuments()); setMessage(""); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Could not load documents"); }
  };
  useEffect(() => { void refreshDocuments(); }, []);

  const handleUpload = async (file: File) => {
    setBusy(true); setMessage(`Indexing ${file.name}…`);
    try { await uploadDocument(file); await refreshDocuments(); setMessage(`${file.name} is ready for retrieval.`); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Upload failed"); }
    finally { setBusy(false); }
  };
  const loadDemoDocuments = async () => {
    setBusy(true); setMessage("Loading demo corpus…");
    try { for (const [name, text] of demoDocuments) await uploadDocument(new File([text], name, { type: "text/markdown" })); await refreshDocuments(); setMessage("Demo corpus loaded."); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Demo loading failed"); }
    finally { setBusy(false); }
  };
  const handleDelete = async (document: Document) => {
    if (!window.confirm(`Delete ${document.name}?`)) return;
    setBusy(true);
    try { await deleteDocument(document.id); await refreshDocuments(); setMessage(`${document.name} deleted.`); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Delete failed"); }
    finally { setBusy(false); }
  };
  const submitQuestion = async (event: FormEvent) => {
    event.preventDefault();
    if (!question.trim() || busy) return;
    setBusy(true); setMessage("Running bounded retrieval…");
    try { const submittedQuestion = question.trim(); const response = await askQuestion(submittedQuestion); setConversation((items) => [...items, { question: submittedQuestion, response }]); setActiveResponse(response); setQuestion(""); setMessage(""); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Question failed"); }
    finally { setBusy(false); }
  };

  const diagnostics = activeResponse?.diagnostics;
  return (
    <main className="app-shell">
      <header className="topbar"><div className="brand-mark">AR</div><div><p className="eyebrow">Agentic RAG / local workspace</p><h1>Inspectable retrieval studio</h1></div><div className="system-state"><span className="pulse" /> API connected</div></header>
      <div className="workspace-grid">
        <aside className="panel library-panel"><div className="panel-heading"><div><p className="section-kicker">01 / corpus</p><h2>Documents</h2></div><span className="count-badge">{documents.length}</span></div><p className="panel-copy">Manage the indexed context available to the retrieval pipeline.</p>
          <label className="primary-button upload-button">+ Upload document<input ref={fileInput} type="file" accept=".txt,.md,.pdf" disabled={busy} onChange={(event) => { const file = event.target.files?.[0]; if (file) void handleUpload(file); event.target.value = ""; }} /></label><button className="secondary-button" disabled={busy} onClick={() => void loadDemoDocuments()}>Load demo corpus <span>↗</span></button>
          <div className="document-list">{documents.length === 0 && <div className="empty-state"><span className="empty-icon">◌</span><p>No documents indexed yet.</p><small>Upload a file or load the demo corpus to begin.</small></div>}{documents.map((document) => <div className="document-row" key={document.id}><div className="file-icon">{document.source_type.toUpperCase()}</div><div className="document-info"><strong>{document.name}</strong><small>{document.chunk_count} chunks · indexed</small></div><button className="icon-button" aria-label={`Delete ${document.name}`} disabled={busy} onClick={() => void handleDelete(document)}>×</button></div>)}</div>
        </aside>
        <section className="main-panel"><div className="conversation-header"><div><p className="section-kicker">02 / ask the system</p><h2>Retrieval console</h2></div><span className="mode-chip">bounded agent · v0.1</span></div><div className="conversation">
          {conversation.length === 0 && <div className="welcome"><div className="orb">✦</div><h3>Ask a question about your corpus</h3><p>Every answer stays inspectable: sources, scores, tools, and timing are surfaced alongside the response.</p><div className="suggestions"><button onClick={() => setQuestion("Which systems store document chunks?")}>Which systems store document chunks?</button><button onClick={() => setQuestion("What happens during a Sev-1 incident?")}>What happens during a Sev-1 incident?</button></div></div>}
          {conversation.map(({ question: submittedQuestion, response }, index) => <article className="answer-card" key={`${response.diagnostics.request_id}-${index}`}><div className="question-line"><span className="user-dot">you</span><span>{index === conversation.length - 1 && activeResponse === response ? "Latest question" : "Question"}</span></div><p className="submitted-question">{submittedQuestion}</p><div className="answer-label">retrieval answer</div><p className="answer-text">{response.answer}</p><div className="citation-list">{response.citations.map((citation) => <button className="citation" key={citation.chunk_id} onClick={() => setActiveResponse(response)}><span>↳</span><span><strong>{citation.document_name}</strong><small>{citation.excerpt}</small></span></button>)}</div></article>)}
        </div><form className="question-form" onSubmit={submitQuestion}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask about the indexed documents…" aria-label="Question" /><button className="send-button" disabled={busy || !question.trim()}>{busy ? "…" : "Run query"}<span>↗</span></button></form>{message && <p className="status-message">{message}</p>}</section>
        <aside className="panel diagnostics-panel"><div className="panel-heading"><div><p className="section-kicker">03 / observability</p><h2>Diagnostics</h2></div><span className="live-badge">LIVE</span></div>{!diagnostics ? <div className="diagnostics-empty"><span>⌁</span><p>Run a query to inspect the retrieval trace.</p></div> : <div className="diagnostics-content"><div className="metric-grid"><Metric label="Total" value={`${diagnostics.total_latency_ms.toFixed(0)} ms`} /><Metric label="Retrieval" value={`${diagnostics.retrieval_latency_ms.toFixed(0)} ms`} /><Metric label="Provider" value={diagnostics.provider} /><Metric label="Chunks" value={`${diagnostics.retrieved_chunks} → ${diagnostics.reranked_chunks}`} /></div><div className="trace-block"><div className="trace-title">Request trace <code>{diagnostics.request_id.slice(0, 8)}</code></div><TraceStep label="retrieve" value={`${diagnostics.retrieval_latency_ms.toFixed(1)} ms`} /><TraceStep label="rerank" value={`${diagnostics.retrieval.length} candidates`} /><TraceStep label="generate" value={`${diagnostics.generation_latency_ms.toFixed(1)} ms`} /></div><div className="score-block"><div className="trace-title">Retrieval scores <span>top candidates</span></div>{diagnostics.retrieval.map((item) => <div className="score-row" key={item.chunk_id}><span>{item.document_name}</span><span className="score-value">{item.hybrid_score.toFixed(2)}</span><div className="score-bar"><i style={{ width: `${Math.min(100, item.hybrid_score * 100)}%` }} /></div></div>)}</div><div className="token-footer">Estimated tokens <strong>{diagnostics.estimated_input_tokens + diagnostics.estimated_output_tokens}</strong><span>{activeResponse.tools_used.length ? activeResponse.tools_used.join(", ") : "no tools"}</span></div></div>}</aside>
      </div>
    </main>
  );
}
function Metric({ label, value }: { label: string; value: string }) { return <div className="metric"><small>{label}</small><strong>{value}</strong></div>; }
function TraceStep({ label, value }: { label: string; value: string }) { return <div className="trace-step"><span className="trace-dot" /><span>{label}</span><code>{value}</code></div>; }
createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);

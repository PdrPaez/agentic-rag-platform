export type Document = {
  id: string;
  name: string;
  source_type: string;
  chunk_count: number;
};

export type Citation = {
  document_id: string;
  document_name: string;
  chunk_id: string;
  excerpt: string;
};

export type RetrievalDiagnostic = {
  chunk_id: string;
  document_name: string;
  bm25_score: number;
  vector_score: number;
  hybrid_score: number;
  reranker_score: number;
};

export type ChatResponse = {
  answer: string;
  citations: Citation[];
  tools_used: string[];
  diagnostics: {
    request_id: string;
    retrieved_chunks: number;
    reranked_chunks: number;
    total_latency_ms: number;
    retrieval_latency_ms: number;
    generation_latency_ms: number;
    provider: string;
    estimated_input_tokens: number;
    estimated_output_tokens: number;
    retrieval: RetrievalDiagnostic[];
  };
};

const request = async <T,>(path: string, init?: RequestInit): Promise<T> => {
  const response = await fetch(`/api${path}`, init);
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(body.detail ?? "Request failed");
  }
  return response.status === 204 ? (undefined as T) : response.json();
};

export const listDocuments = () => request<Document[]>("/documents");
export const uploadDocument = (file: File) => {
  const form = new FormData();
  form.append("file", file);
  return request<Document>("/documents", { method: "POST", body: form });
};
export const deleteDocument = (id: string) => request<void>(`/documents/${id}`, { method: "DELETE" });
export const askQuestion = (question: string) => request<ChatResponse>("/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question }),
});

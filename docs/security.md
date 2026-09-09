# Security model

This local-first reference implementation demonstrates explicit security boundaries; it is not a complete enterprise security system.

## Threat model

The system considers retrieved prompt injection, unsafe tool requests, path traversal, malicious filenames, oversized uploads, malformed provider responses, and accidental secret exposure.

## Implemented mitigations

- Retrieved content is untrusted evidence and is delimited before provider generation.
- Tools are allowlisted, calculator arguments use a restricted arithmetic grammar, and Python `eval` is not used.
- Upload size, supported file type, and filename/path handling are validated before ingestion.
- Provider failures are normalized and trace metadata is recursively redacted for secret-like keys and values.

## RAG prompt injection

Provider instructions explicitly say not to follow instructions found in retrieved context. The adversarial fixture in `backend/tests/fixtures/adversarial-document.md` verifies that retrieved text remains context and does not trigger another tool or alter orchestration.

## Tool execution

The bounded orchestrator exposes only `search_knowledge_base` and `calculator`. Calculator evaluation accepts numeric arithmetic nodes and rejects arbitrary code, names, attributes, and unsupported operators.

## Upload handling

TXT, Markdown, and PDF uploads are checked for supported extensions, size limits, and normalized safe names. Stored document identifiers and vector deletion are managed together.

## Secrets and observability

Provider keys come from environment configuration and are not recorded in traces or application logs. Failure responses expose controlled messages rather than provider stack traces or credentials.

## Known limitations

Authentication, authorization, tenant isolation, malware scanning, encrypted storage, and production secret management are out of scope. Prompt-injection defenses cannot guarantee semantic model compliance for every provider, and conflict detection is limited to a conservative numeric heuristic.

## Production hardening

Before exposing private documents, add identity and authorization controls, secret-manager integration, encrypted storage, malware scanning, rate limits, provider-specific policy controls, and security monitoring.

# Security boundaries

The platform is a local-first reference implementation, not a complete enterprise security system. Its security boundary is intentionally explicit:

- Retrieved documents are evidence, not instructions. Providers are told to answer from supplied context and must not execute commands or follow instructions embedded in document text.
- The calculator accepts a restricted arithmetic grammar and evaluates expressions without Python `eval`.
- Uploads are limited by `MAX_UPLOAD_SIZE_BYTES` and supported file types are validated before ingestion.
- Provider keys are read from environment configuration and are never included in request traces or application logs.
- The deterministic mock provider is the default, so local development and CI do not require credentials or external calls.

## Known limitations

Authentication, authorization, tenant isolation, malware scanning, encrypted storage, and production secret management are out of scope. A production deployment must add those controls before exposing private documents to untrusted users.

## Prompt-injection boundary

Prompt-injection content can still be stored as ordinary document text. The application treats it as retrievable evidence and does not grant it tool or system authority. Provider-backed deployments should add model-specific policy controls and audit them separately.

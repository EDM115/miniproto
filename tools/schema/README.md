# Schema Tooling

Status: placeholder for deterministic Telegram schema pinning and generation.

## Planned Responsibilities

- Store pinned schema metadata with layer, source URL, fetch date, and SHA-256.
- Generate typed raw constructors under `src/miniproto/raw/`.
- Generate serializer/deserializer golden fixtures for CI.
- Fail CI when generated files are stale.

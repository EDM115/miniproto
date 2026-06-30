# Schema Tooling

Status: deterministic Telegram Layer 214 schema pinning and generation is active.

## Pinned Inputs

- `tools/schema/schema.tl` is fetched from the official Telegram schema page at <https://core.telegram.org/schema>.
- `tools/schema/schema-metadata.json` records layer, source URL, fetch date, schema SHA-256, generator version, generated file manifest, and RPC error database metadata.
- `tools/schema/rpc-errors.json` is fetched from the Telegram error database linked by <https://core.telegram.org/api/errors>.

## Generate

```powershell
uv run python -m tools.schema.generate
```

This rewrites `src/miniproto/raw/base.py`, `src/miniproto/raw/types.py`, `src/miniproto/raw/functions.py`, `src/miniproto/raw/errors.py`, `docs/raw-api.md`, and `tools/schema/schema-metadata.json`.

## Stale Check

```powershell
uv run python -m tools.schema.generate --check
```

The command exits non-zero when generated files or metadata do not match the pinned schema and generator. CI runs this command so raw API drift is visible before release.

## Current Scope

Phase 3 generated classes expose constructor IDs, result types, field metadata, namespace aliases, and RPC error mappings. Binary TL serialization/deserialization intentionally remains a Phase 4 task.
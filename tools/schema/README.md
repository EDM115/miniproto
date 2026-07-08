# Schema Tooling

Status: deterministic Telegram Schema Layer 223 JSON pinning and generation is active, with RPC error metadata pinned at layer 227.

## Pinned Inputs

- `tools/schema/schema.json` is the canonical pinned schema fetched from the official Telegram JSON schema endpoint at <https://core.telegram.org/schema/json>.
- `tools/schema/schema.tl` is kept as a review/interoperability mirror. The updater extracts it from <https://core.telegram.org/schema> when possible and falls back to deriving equivalent TL declarations from `schema.json`.
- `tools/schema/rpc-errors.json` is fetched from the official Telegram error database permalink at <https://core.telegram.org/api/errors.json>.
- `tools/schema/schema-metadata.json` records schema layer, latest changelog layer observed from <https://core.telegram.org/api/layers>, RPC error layer, source URLs, fetch date, SHA-256 values, generator version, generated file manifest, and RPC error database metadata.

## Update Pinned Inputs

```powershell
uv run python -m tools.schema.update
```

This fetches the upstream schema JSON, schema page, layer changelog, and RPC error JSON, then rewrites `tools/schema/schema.json`, `tools/schema/schema.tl`, `tools/schema/rpc-errors.json`, and `tools/schema/schema-metadata.json`.

## Upstream Freshness Check

```powershell
uv run python -m tools.schema.update --check-upstream
```

This fetches upstream sources and exits non-zero when any pinned schema input differs. This command is network-dependent, so keep it manual or scheduled rather than part of routine offline generation.

## Generate

```powershell
uv run python -m tools.schema.generate
```

This rewrites `src/miniproto/raw/base.py`, `src/miniproto/raw/types.py`, `src/miniproto/raw/functions.py`, `src/miniproto/raw/errors.py`, `docs/raw-api.md`, and `tools/schema/schema-metadata.json` from the pinned schema inputs.

## Stale Check

```powershell
uv run python -m tools.schema.generate --check
```

The command exits non-zero when generated files or metadata do not match the pinned schema inputs and generator. CI runs this command so raw API drift is visible before release without fetching upstream.

## Current Scope

Generated classes expose constructor IDs, result types, field metadata, namespace aliases, RPC error mappings, and binary TL serialization/deserialization for generated objects.

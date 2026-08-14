# Schema Tooling

Status: deterministic Telegram Schema Layer 228 pinning and generation is active. TDLib `master` is the canonical structural source, Telegram Desktop `dev` supplies the layer after strict overlap validation, and core RPC error metadata remains independently pinned at layer 227.

## Pinned Inputs

- `tools/schema/schema.tl` is the verbatim canonical TDLib schema fetched from <https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl>.
- `tools/schema/schema.json` is the deterministic normalized model derived from the canonical TDLib TL declarations. Generated Python code and later schema consumers read this model.
- `tools/schema/schema-tdesktop.tl` is the verbatim Telegram Desktop schema fetched from <https://raw.githubusercontent.com/telegramdesktop/tdesktop/refs/heads/dev/Telegram/SourceFiles/mtproto/scheme/api.tl>. Its strict final `// LAYER N` comment is the only accepted layer source.
- `tools/schema/schema-core.json` is the verbatim core schema JSON fetched from <https://core.telegram.org/schema/json>.
- `tools/schema/schema-core.tl` is the TL block extracted from <https://core.telegram.org/schema>, or a deterministic JSON-derived mirror when the page exposes no valid raw block.
- `tools/schema/rpc-errors.json` is the verbatim error database fetched from <https://core.telegram.org/api/errors.json>.
- `tools/schema/schema-source-diff.json` is the deterministic declaration-level TDLib/Desktop/core comparison.
- `tools/schema/schema-metadata.json` records the validated layer, canonical and supporting roles, documentation precedence, every source URL/hash/byte and declaration count, normalized-output hashes, generator version, generated manifest, RPC error provenance, and a compact source-comparison summary.

Core schema inputs enrich missing descriptions and expose drift; they never replace TDLib constructor IDs, flags, parameters, result types, or declarations. Descriptions merge by qualified declaration and parameter name in this order: TDLib comments, Telegram Desktop comments, then core JSON descriptions. RPC error definitions and method mappings continue to come from the independently versioned core error database.

## Safety Rules

The updater fetches every allowlisted source into memory, decodes, parses, compares, and validates the complete snapshot before replacing any pin. Telegram Desktop must contain exactly one positive `// LAYER N` marker at end of file. Every overlapping TDLib/Desktop declaration must have the same kind, constructor ID, result, parameters, flags, and generic structure. Unknown constructor-ID-free declarations, malformed structured comments, unexpected duplicate IDs, and partial/invalid sources abort before pinned files change.

Core schema and layer HTML end with a server-render timing comment whose value changes on every request. Source metadata removes only that exact trailing `<!-- page generated in …ms -->` comment before computing the recorded byte count and SHA-256; the extracted TL block, changelog layer values, and all other page bytes remain strict. This prevents timing noise from masquerading as schema drift.

TDLib intentionally contains four prefix/canonical function pairs that share constructor IDs. Only those exact official pairs are accepted; constructor-ID decoding resolves to the canonical function while both named request classes remain available.

## Check Upstream Without Updating Pins

```pwsh
uv run miniproto-schema-update --check-upstream --report .tmp/schema-upstream-report.json
```

This network-dependent command fetches and validates every upstream source, writes a machine-readable comparison artifact outside the pinned input directory, reports each stale pin, and exits non-zero without modifying pinned schema files. `.github/workflows/schema-upstream.yml` runs it on a schedule and through manual dispatch. Pull-request CI deliberately remains offline.

## Update And Review Sequence

```pwsh
uv run miniproto-schema-update --report .tmp/schema-upstream-report.json
uv run miniproto-schema-generate
uv run miniproto-schema-generate --check
uv run pytest tests/test_schema_parser.py tests/test_schema_update.py tests/test_schema_generation.py tests/test_tl_codec.py tests/test_invoke.py
```

Review `tools/schema/schema-source-diff.json`, `tools/schema/schema-metadata.json`, the generated raw API diff, and the focused test results before accepting an update. A newer source is not sufficient evidence: the Desktop layer marker and TDLib/Desktop overlap validation must both succeed. The current TDLib snapshot adds 12 declarations relative to Telegram Desktop and omits Desktop's `null`; consequently, the previously generated `miniproto.raw.types.Null` class is intentionally absent from Layer 228.

## Generate

```pwsh
uv run miniproto-schema-generate
```

This rewrites `src/miniproto/raw/base.py`, lazy type/function facades and stubs, registry and implementation shards, RPC error mappings, `docs/raw-api.md`, and generator-owned metadata from the pinned inputs. It also removes stale generator-owned shards.

## Deterministic Offline Stale Check

```pwsh
uv run miniproto-schema-generate --check
```

The command performs no network access and exits non-zero when generated files, owned shard membership, or metadata do not match the pinned inputs and generator. Normal CI uses this command so pull requests remain reproducible even when Telegram or GitHub is unavailable.

## Current Scope

Generated classes expose constructor IDs, result types, field metadata, namespace aliases, RPC error mappings, and binary TL serialization/deserialization for generated objects.

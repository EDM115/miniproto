---
title: External Integrations
description: Telegram, storage, proxy, schema, observability, and documentation-hosting boundaries used by miniproto.
slug: /project/codebase/integrations/
generated: false
---

# External integrations

## Integration inventory

| System                                     | Type                          | Purpose                                                                                       | Authentication                                                                           | Criticality                                | Evidence                                                                      |
| ------------------------------------------ | ----------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------- |
| Telegram MTProto datacenters               | Stateful TCP API              | Authorization, RPCs, updates, messages, files, and CDN redirects                              | Telegram API ID/hash plus generated user or bot authorization keys                       | High                                       | `src/miniproto/auth/`, `src/miniproto/connection/`, `src/miniproto/client.py` |
| Telegram HTTP/SOCKS proxy                  | Optional network intermediary | Reach a Telegram DC through HTTP CONNECT or SOCKS5                                            | Optional proxy URL username/password                                                     | Medium                                     | `src/miniproto/connection/transport.py`, `src/miniproto/config.py`            |
| TDLib `telegram_api.tl`                    | Build-time upstream schema    | Canonical raw API structure                                                                   | Public HTTPS                                                                             | High for schema updates, absent at runtime | `tools/schema/update.py`, `tools/schema/schema-metadata.json`                 |
| Telegram Desktop `api.tl`                  | Build-time upstream schema    | Validated layer marker and secondary descriptions                                             | Public HTTPS                                                                             | High for layer updates, absent at runtime  | `tools/schema/update.py`, `tools/schema/schema-metadata.json`                 |
| Telegram core schema/error/changelog pages | Build-time upstream metadata  | Independent drift, prose, and RPC error mappings                                              | Public HTTPS                                                                             | Medium, absent at runtime                  | `tools/schema/README.md`, `tools/schema/schema-metadata.json`                 |
| Local SQLite                               | Embedded datastore            | Auth keys, DCs, identity, peer cache, updates, salts, and media authorization state           | Application-supplied encryption key                                                      | High for durable clients                   | `src/miniproto/session/storage.py`                                            |
| GitHub Actions/Pages                       | CI and static hosting         | Quality matrices, artifacts, upstream freshness, docs deployment                              | Repository permissions/secrets controlled by the maintainer                              | Development/release only                   | `.github/workflows/`                                                          |
| Alpine/NGINX documentation image           | Self-hosted static serving    | Package the root-base Astro/Pagefind artifact for VPS deployment as an unprivileged container | No application credential; TLS and access control belong to the operator's reverse proxy | Documentation deployment only              | `docs-site/Dockerfile`, `docs-site/nginx.conf`, `docs/project/deployment.md`  |
| PyPI/crates.io                             | Package registries            | Python wheel/sdist and synchronized Rust accelerator-source distribution                       | Short-lived GitHub OIDC credentials from protected Trusted Publishers; local scoped tokens are emergency-only | Release only                               | `.github/workflows/publish-release.yml`, `docs/project/release.md`            |

`miniproto` has no Bot API HTTP integration, remote SQL/NoSQL database, application message queue, service mesh, hosted search, or default telemetry backend. Pagefind is compiled into the static documentation artifact and runs locally in the browser.

## Data stores

| Store                                 | Role                                                                       | Access layer                                          | Key risk                                                                                | Evidence                                                             |
| ------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Encrypted SQLite session              | Durable per-account MTProto/session state split into authenticated domains | `EncryptedSQLiteSessionStorage`                       | Reusing a path/key across unrelated accounts or exposing the database/key               | `src/miniproto/session/storage.py`, `docs/session-security.md`       |
| In-memory session                     | Explicit ephemeral tests/throwaway clients                                 | `InMemorySessionStorage`                              | Authorization disappears on process exit and remains readable in process memory         | `src/miniproto/session/storage.py`                                   |
| Portable session string               | Transfer/backup credential, not a database                                 | `session/strings.py`, client import/export methods    | Bearer credential theft, lossy third-party formats, unsafe overwrite/mismatch overrides | `src/miniproto/session/strings.py`, `docs/guides/string-sessions.md` |
| In-memory peer/range/scheduler caches | Process-local performance/state coordination                               | `peers.py`, `media/download.py`, `media/scheduler.py` | No cross-process sharing; bounds and revision reconciliation must remain correct        | respective source files                                              |

## Secrets and credentials

- `ClientConfig` receives API ID/hash and optional bot token; sensitive fields are excluded from ordinary representations. Phone codes/passwords enter only through authorization callbacks.
- Durable storage resolves explicit key material first, then `MINIPROTO_SESSION_KEY`, and rejects missing or under-16-byte material before creating persistent state.
- `.env.example` is the variable-name inventory for local live tests and benchmarks. Real `.env`, session databases, session strings, credentials, and live artifacts are ignored/private inputs and must not be read into documentation or committed.
- GitHub live workflows consume repository secrets only in manually dispatched credentialed jobs. Ordinary pull requests receive no Telegram credentials or Pages deployment permission.
- Rotation depends on the credential: revoke Telegram authorizations after auth-key/session exposure, regenerate bot tokens/passwords/proxy credentials at their authority, and replace local storage keys through a deliberate reauthorization or migration rather than assuming re-encryption revokes copied bearer data.

## Reliability and failure behavior

- TCP connect/read/write/request timeouts and bounded reconnect backoff are configured in `TransportConfig`/`ClientConfig`.
- Retry eligibility is method-aware. Ambiguous unsafe writes do not replay; eligible transient requests retain one logical pending slot across attempts.
- Method flood waits are cached by method; eligible waits under policy can sleep, while larger waits surface as typed errors. Media floods use fixed request slots, separate caps, bounded jitter, launch pacing, and premium-flood contraction.
- DC migration reselects primary/media connections and imports authorization as required. CDN redirects use dedicated CDN requests, reupload tokens, AES-CTR decryption, and mandatory hash validation.
- Native capability absence selects a documented fallback where one exists; invalid network data never triggers a fallback retry that could reinterpret the same malformed bytes.
- No general circuit breaker exists. Explicit retry, reconnect, capacity, timeout, and fail-closed protocol rules are the reliability controls.

## Observability

- `observability.py` emits standard-library logs and caller-selected text/JSON formatting, records events through an optional `MetricsSink`, and exposes process/tracemalloc snapshots.
- Sender, transport, auth, storage, update, media, native, RPC, flood, scheduler, and benchmark paths emit stable event/metric names with redacted context.
- No telemetry leaves the process by default. Applications must install their own logging handler or metrics sink and preserve the redaction boundary.
- Live behavior still has external visibility gaps when no authorized account, relevant DC/CDN/proxy, or hosted matrix is available. Offline fake-server evidence must remain labeled separately.

## Evidence

- `src/miniproto/auth/dc.py`
- `src/miniproto/connection/transport.py`
- `src/miniproto/session/storage.py`
- `src/miniproto/session/strings.py`
- `src/miniproto/observability.py`
- `tools/schema/update.py`
- `tools/schema/schema-metadata.json`
- `.env.example`
- `.github/workflows/live-media-bench.yml`
- `.github/workflows/docs.yml`
- `docs-site/Dockerfile`
- `docs-site/nginx.conf`

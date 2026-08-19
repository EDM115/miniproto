---
title: Codebase Structure
description: Source, generated, test, tooling, documentation, and workflow boundaries in the miniproto repository.
slug: /project/codebase/structure/
generated: false
---

# Codebase structure

## Top-level map

| Path                 | Purpose                                                                                                 | Evidence                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `src/miniproto/`     | Installable Python package and private native extension destination                                     | `pyproject.toml`, `src/miniproto/__init__.py`                    |
| `rust/miniproto/`    | Rust/PyO3 native extension crate                                                                        | `Cargo.toml`, `rust/miniproto/Cargo.toml`                        |
| `tools/schema/`      | Pinned Telegram inputs, updater, parser, generator, binding manifest, and generated-fast-path selection | `tools/schema/README.md`                                         |
| `tools/docs/`        | Static Python/Telegram/Rust reference extraction, audits, manifest handling, and site orchestration     | `tools/docs/__main__.py`                                         |
| `tools/bench/`       | Offline, live, matrix, compatibility, and reporting benchmarks                                          | `src/miniproto/_cli.py`, `docs/development.md`                   |
| `tests/`             | Offline unit/fake-server/workflow/docs tests plus gated `integration/` and `stress/` suites             | `pyproject.toml`, `tests/integration/README.md`                  |
| `docs/`              | Canonical authored Markdown, internal `THOUGHTS.md`, and committed generated reference pages            | `docs/reference-surface.toml`, `docs-site/src/content.config.ts` |
| `docs-site/`         | Astro/Starlight presentation, Pagefind, assets, browser acceptance, and ignored static output           | `docs-site/package.json`, `docs-site/astro.config.ts`            |
| `.github/workflows/` | CI, docs, schema-upstream, live-benchmark, dispatch-only release construction, and protected OIDC publication | `.github/workflows/`                                             |
| `plans/`             | Historical and active implementation plans; not proof of runtime behavior by themselves                 | `plans/README.md`, `PROGRESS.md`                                 |

Root `PLAN.md`, `PROGRESS.md`, `README.md`, `CHANGELOG.md`, `SECURITY.md`, and `CONTRIBUTING.md` describe implementation intent, verified progress, public usage, release capabilities, security, and contribution. Documentation-product direction and branding live under `docs/project/`, especially `docs/project/index.md` and `docs/project/brand.md`. Code and current test/config evidence take precedence when an older plan statement disagrees with implementation.

## Entry points

- The import surface is `src/miniproto/__init__.py`, which re-exports the reviewed client, config, storage, session, media, type, error, file-ID, event-loop, and observability APIs.
- Application code constructs `Client(ClientConfig(...))`; there is no always-running package process or web-server main. Lifecycle starts through `connect()`, `async with Client(...)`, or caller-owned `event_loop.run()`.
- Generated raw imports enter through `miniproto.raw.functions`, `miniproto.raw.types`, and their namespace facades. Implementation shards under `src/miniproto/raw/_function_shards/` and `_types_shards/` are generator-owned.
- Operational tools enter through `[project.scripts]` in `pyproject.toml`; `src/miniproto/_cli.py` bridges installed launchers to `tools.schema`, `tools.docs`, `tools.bench`, `tools.release_check`, and `tools.release_artifacts` modules.
- The native module is built from `rust/miniproto/src/lib.rs` and imported privately as `miniproto._native`; Python wrappers own capability selection and fallbacks.

## Python module boundaries

| Boundary                           | Owns                                                                                           | Must not own                                                | Evidence                                                                |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------- |
| `auth/`                            | RSA/DH key exchange, DC configuration, phone/bot/2FA authorization                             | Message/media framework helpers                             | `src/miniproto/auth/`                                                   |
| `connection/`                      | TCP transports, proxy handshakes, framing, sender lifecycle, correlation, quick ACK            | Persistent domain models or application routing             | `src/miniproto/connection/`                                             |
| `mtproto/` and `tl/`               | MTProto envelopes/state/service constructors and generic/generated TL codecs                   | Socket ownership or high-level client workflows             | `src/miniproto/mtproto/`, `src/miniproto/tl/`                           |
| `session/`                         | Typed session state, atomic storage, peer merging, portable strings                            | Telegram network calls                                      | `src/miniproto/session/`                                                |
| `updates/`                         | Cursor/deduplication state, gap recovery, public queues, handlers                              | Application exactly-once semantics                          | `src/miniproto/updates/`                                                |
| `media/`                           | Upload/download/CDN/integrity/scheduling primitives                                            | Broad media ergonomics reserved for `mpgram`                | `src/miniproto/media/`, `docs/media.md`                                 |
| `raw/`                             | Generated Layer 228 Python bindings, registries, facades, and shards                           | Handwritten business logic                                  | `tools/schema/generate.py`, `src/miniproto/raw/`                        |
| `client.py`                        | Public orchestration across auth, senders, peers, updates, messages, sessions, and media pools | Schema definition or low-level cryptographic implementation | `src/miniproto/client.py`                                               |
| `observability.py` and `security/` | Local logging/metrics/resource snapshots and redaction                                         | External telemetry transport or secret storage              | `src/miniproto/observability.py`, `src/miniproto/security/redaction.py` |

## Generated and authored ownership

- Never hand-edit raw binding shards, `src/miniproto/raw/functions.py`, `src/miniproto/raw/types.py`, their stubs/registry, `rust/miniproto/src/generated_tl.rs`, or `src/miniproto/tl/fast_metadata.py`; change pinned inputs/generators and run `miniproto-schema-generate`.
- Never hand-edit `docs/reference/**`; change source docstrings, schema metadata, Rust docs, or docs generators and run `miniproto-docs`.
- Handwritten pages outside `docs/reference/` remain canonical authored sources. `docs/THOUGHTS.md` is internal and deliberately excluded from the site.
- `docs-site/dist/`, `.astro/`, Pagefind output, rustdoc JSON, caches, wheels, and local native build products are derived artifacts and are not source conventions.

## Naming and organization rules

- Python source/test files and packages use lowercase `snake_case`; public Python types use `PascalCase`, and private helpers/modules use a leading underscore where appropriate.
- Rust modules use lowercase `snake_case`; types/variants use `PascalCase`; constants use `UPPER_SNAKE_CASE`.
- Generated Telegram Python class names translate qualified TL names to `PascalCase`, while exact Telegram qualified names remain in constructor metadata and reference headings.
- Documentation content is organized by user journey (`start`, `guides`, `concepts`, `recipes`, `faq`, `project`) while generated references are organized by language.
- Python uses absolute `miniproto...` imports for package boundaries; package `__all__` declarations define reviewed public facades.

## Evidence

- `src/miniproto/__init__.py`
- `src/miniproto/_cli.py`
- `src/miniproto/client.py`
- `tools/schema/README.md`
- `tools/docs/__main__.py`
- `docs/reference-surface.toml`
- `docs-site/src/content.config.ts`
- `pyproject.toml`

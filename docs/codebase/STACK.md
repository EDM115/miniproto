---
title: Technology Stack
description: Runtime, dependency, build, documentation, and environment map for contributors working on miniproto.
slug: /project/codebase/stack/
generated: false
---

# Technology stack

## Runtime summary

| Area                       | Value                                                                                                                        | Evidence                                               |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Public implementation      | Python package with a `src/` layout                                                                                          | `pyproject.toml`, `src/miniproto/__init__.py`          |
| Python runtime             | CPython 3.13+; CI covers 3.13, 3.14, and GIL-disabled 3.14t                                                                  | `pyproject.toml`, `.github/workflows/ci.yml`           |
| Native runtime             | Rust 2024 edition, minimum Rust 1.97, compiled as the `miniproto_native` `cdylib`                                            | `rust/miniproto/Cargo.toml`                            |
| Python build system        | Maturin/PyO3 mixed Python-Rust package                                                                                       | `pyproject.toml`, `rust/miniproto/Cargo.toml`          |
| Package managers           | `uv` for Python, Cargo for Rust, the current pnpm 11 release for the site                                                    | `uv.lock`, `Cargo.lock`, `docs-site/package.json`      |
| Documentation frontend     | Astro 7.2.2 and Starlight 0.41.7, statically prerendered with Pagefind 1.5.2                                                 | `docs-site/package.json`, `docs-site/astro.config.ts`  |
| Documentation Node runtime | The current Node.js 26 release with strict Astro TypeScript configuration                                                    | `docs-site/.node-version`, `docs-site/tsconfig.json`   |
| Documentation container    | Node.js 26.7.0 on Alpine 3.24 for the optional source build; unprivileged NGINX 1.31.3 on Alpine 3.24 for the static runtime | `docs-site/Dockerfile`, `docs-site/nginx.conf`         |

The Python API is the supported product surface. The Rust crate is packaged primarily as the private `miniproto._native` acceleration module; its `0.1.x` public Rust API is not separately stability-promised. The documentation-only nightly in `rust/miniproto/rust-toolchain-docs.toml` does not replace stable Rust for builds, tests, wheels, or releases.

## Production frameworks and dependencies

| Dependency                                   | Version policy                                                            | Role                                                      | Evidence                                        |
| -------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| `cryptography`                               | Exactly 50.0.0, except Windows ARM64 until an upstream wheel is available | Supported crypto/session fallback and CFFI dependency     | `pyproject.toml`                                |
| `uvloop`                                     | Exactly 0.22.1 on Linux/macOS                                             | Optional optimized asyncio loop selected lazily           | `pyproject.toml`, `src/miniproto/event_loop.py` |
| `winloop`                                    | Exactly 0.6.3 on Windows                                                  | Optional optimized asyncio loop selected lazily           | `pyproject.toml`, `src/miniproto/event_loop.py` |
| PyO3                                         | `~0.29.2` with experimental async support                                 | Python extension bindings and free-threaded compatibility | `rust/miniproto/Cargo.toml`                     |
| RustCrypto AES/GCM/cipher/hash/Scrypt crates | Exact or compatible versions in Cargo metadata and lockfile               | Native MTProto, hashing, and protected-session operations | `rust/miniproto/Cargo.toml`, `Cargo.lock`       |
| SQLite                                       | Python standard-library `sqlite3`                                         | Per-domain encrypted durable session storage              | `src/miniproto/session/storage.py`              |

There is no application web framework, ORM, remote database client, telemetry exporter, or message-queue dependency in the runtime package. Telegram MTProto is the external service protocol; asyncio streams own network I/O.

## Development toolchain

| Tool                                      | Purpose                                                                                         | Evidence                                                                 |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Ruff 0.16.3                               | Python formatting, imports, linting, security/style rules                                       | `pyproject.toml`, `uv.lock`                                              |
| ty 0.0.72                                 | Python static type checking against Python 3.13 semantics                                       | `pyproject.toml`, `uv.lock`                                              |
| pytest 9.1.1                              | Unit, fake-server, integration, stress, workflow, and documentation tests                       | `pyproject.toml`, `tests/`                                               |
| Maturin 1.14.1                            | Editable native builds, wheels, and source distributions                                        | `pyproject.toml`, `.github/workflows/build-wheels.yml`                   |
| Griffe 2.2.0 + griffe2md 1.5.0            | Static Python API extraction and Markdown rendering without importing the package               | `pyproject.toml`, `tools/docs/generate_python.py`                        |
| nightly-2026-08-12 + cargo-docs-md 0.2.4  | Rustdoc JSON extraction and Markdown fragments for committed Rust reference pages               | `rust/miniproto/rust-toolchain-docs.toml`, `tools/docs/generate_rust.py` |
| Astro/Starlight/Pagefind/Playwright/Sharp | Static docs, search, browser acceptance, and deterministic brand derivatives                    | `docs-site/package.json`, `docs-site/playwright.config.ts`               |
| Oxfmt 0.63.0 + Oxlint 1.78.0              | Formatting for supported docs-site files and type-aware linting for maintained TypeScript        | `docs-site/package.json`, `docs-site/oxfmt.config.ts`, `docs-site/oxlint.config.ts` |
| Jiti 2.7.0 + `@types/node` 26.2.0         | Direct execution and Node.js typing for the docs-site TypeScript helper CLIs                     | `docs-site/package.json`, `docs-site/scripts/`                                     |
| GitHub Actions                            | Python/Rust quality, benchmarks, schema freshness, docs, live opt-ins, attested dispatch-only release artifacts, and protected OIDC publication | `.github/workflows/`                                                     |

## Key commands

```pwsh
uv sync --extra dev,docs --frozen
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
pnpm --dir docs-site format:check
pnpm --dir docs-site lint
pnpm --dir docs-site check
cargo fmt --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
uv run miniproto-docs --check --build --skip-install
uv run miniproto-release-artifacts --help
uv run miniproto-release-check --offline --artifacts-dir .tmp/release-offline
```

Every executable Python tool is registered under `[project.scripts]` and must expose side-effect-free `--help`. Use the focused commands in the [development guide](../development.md) when an aggregate stage fails.

## Environment and configuration

- Public client configuration is immutable `ClientConfig`/`TransportConfig` data. Credentials, session storage, timeouts, queue bounds, retry limits, datacenter selection, and media budgets enter through those objects; see `src/miniproto/config.py`.
- Durable default storage obtains its key from constructor material or `MINIPROTO_SESSION_KEY`. Live/integration/benchmark environment names are documented in `.env.example`; the real `.env` is ignored and must not be inspected, committed, or copied into artifacts.
- Normal operation is a Python process with network access to Telegram and filesystem access only when durable sessions or path downloads are selected. The documentation artifact is static and has no runtime Node/Python/Rust/search service dependency.
- The checked-in documentation container serves the prepared root-base artifact as unprivileged UID 101 on port 8080. Its default target packages `docs-site/dist/`; the optional `source-runtime` target builds the same artifact with Node.js and pnpm inside Alpine before copying only the static files into NGINX. It is a documentation deployment image, not a container contract for the Python SDK or its wheel matrix.
- No Kubernetes, Compose, or other orchestration configuration is checked in. Wheel automation uses GitHub-hosted runners and official manylinux/musllinux build environments independently of the documentation image.

## Evidence

- `pyproject.toml`
- `uv.lock`
- `Cargo.toml`
- `rust/miniproto/Cargo.toml`
- `rust/miniproto/rust-toolchain-docs.toml`
- `docs-site/package.json`
- `docs-site/Dockerfile`
- `docs-site/nginx.conf`
- `.github/workflows/ci.yml`
- `.github/workflows/build-wheels.yml`
- `.github/workflows/publish-release.yml`
- `.env.example`

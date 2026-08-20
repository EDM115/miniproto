---
title: Deployment
description: Lifecycle, event-loop, storage-key, credential, and acceptance boundaries for running miniproto in a service.
slug: /project/deployment/
generated: false
---

## Own the application lifecycle

Create a `Client` in the component that owns its lifecycle, connect it before invoking raw requests, and disconnect it during orderly shutdown. An async context manager is the simplest shape when the service startup/shutdown scope maps to one client. Disconnect stops updates, senders, media schedulers and pools, auxiliary clients, and storage; callers should still handle cleanup errors according to their service policy.

Do not let a library import replace the host application's asyncio policy. Scripts that own their top-level coroutine can use `miniproto.event_loop.run()`. Embedded applications retain their own running loop; advanced standalone integrations can supply `miniproto.event_loop.new_event_loop` to `asyncio.Runner`. The legacy global policy installer is deprecated and unsuitable for coordinated service startup.

## Provision durable state deliberately

Production clients use encrypted SQLite by default and require `MINIPROTO_SESSION_KEY` or constructor key material. Obtain it from the platform secret manager, never from a committed environment file or command-line argument. Use an absolute, private, per-account session path when a working-directory-relative default would be ambiguous. Keep bot tokens, API hashes, phone/2FA values, auth keys, proxy credentials, and session strings out of logs and artifacts.

`InMemorySessionStorage()` is for tests and intentionally ephemeral work. It is not a durable production substitute. Portable session strings are bearer credentials and require the same access controls as an active session database.

## Operate within Telegram and local resource limits

Telegram controls authorization, FloodWaits, and transport behavior. Bound work at the application layer, use the SDK's pending-RPC, queue, payload, and scheduler limits, and handle `FloodWait`/ambiguous requests as product events rather than trying to bypass them. A successful quick acknowledgement does not confirm an RPC result.

## Acceptance boundary

Ordinary CI disables real integration credentials. Live tests and live benchmarks are explicitly guarded and require secrets plus Telegram-side prerequisites. When those are unavailable, report the gate as not run or externally blocked; do not claim that deterministic fake coverage proves a production deployment against Telegram.

## Build the documentation as a portable static artifact

The documentation site reads its canonical Markdown directly from `docs/`, validates the committed Python/Telegram/Rust reference, builds Astro/Starlight, creates a local Pagefind index, runs browser acceptance, and then validates the emitted routes and assets. From a clean checkout:

```pwsh
rustup toolchain install nightly-2026-08-12
cargo install cargo-docs-md --version 0.2.4 --locked
uv sync --extra dev,docs --frozen
pnpm --dir docs-site install --frozen-lockfile
uv run miniproto-docs --check --build --skip-install
```

The artifact is `docs-site/dist/`. Deploy or copy that directory as an indivisible output; do not regenerate search separately or combine HTML from one build with assets from another. The deployed site requires no Node.js, Python, Rust, database, or search process at runtime.

The default build uses the origin root `/`. Configure only the canonical origin when building for an origin-root host:

```pwsh
$env:MINIPROTO_DOCS_SITE = "https://miniproto.edm115.dev"
uv run miniproto-docs --check --build --skip-install
```

For a subpath host, set `MINIPROTO_DOCS_BASE` to that public prefix, for example `/miniproto`. The GitHub workflow does this explicitly because `https://miniproto.edm115.dev/` is a project Pages URL. Serve `docs-site/dist/` with any static web server or copy it into the server's immutable release directory, then point the web root at those bytes. Preserve trailing-slash routing and the generated `404.html`; do not proxy Pagefind queries to an application server.

## Run the Alpine documentation image

The repository also provides a multi-stage, root-base image. Build and validate the static output first, then package it from the repository root:

```sh
MINIPROTO_DOCS_SITE=https://miniproto.edm115.dev MINIPROTO_DOCS_BASE=/ pnpm --dir docs-site build
docker build --file docs-site/Dockerfile --tag miniproto-docs .
docker rm -f miniproto-docs
docker run --detach --name miniproto-docs --publish 6743:6743 miniproto-docs
```

The default Docker target checks the prepared artifact in Alpine 3.24 and packages it in unprivileged NGINX on Alpine 3.24. This path works on small builders where Astro cannot fit the complete reference collection into the daemon's memory allocation. The runtime listens on port 6743 as UID 101 and includes a local HTTP health check. It contains the static output only: no Python, Rust toolchain, Node.js, pnpm, source Markdown, or server-side search process. Set `MINIPROTO_DOCS_SITE` during the Astro build because canonical metadata is prerendered. The container deliberately uses `MINIPROTO_DOCS_BASE=/`; deploy it at the origin root or configure the reverse proxy without adding a path prefix.

On a builder with at least 2 GiB available, `docker build --file docs-site/Dockerfile --target source-runtime --build-arg MINIPROTO_DOCS_SITE=https://miniproto.edm115.dev --tag miniproto-docs .` performs the root-base Astro build inside Node.js 26.7.0 on Alpine 3.24 with pnpm 11.22.0, then copies the output into the same NGINX runtime. BuildKit caches the pnpm store, while every production build forces a fresh Astro content layer so imported Markdown-transform changes cannot leave stale rendered pages behind.

The repository's documentation workflow builds and tests a pull request only after it transitions from draft to ready for review, without publication credentials, and uploads the exact static artifact for inspection. A trusted `master` push downloads those same validated bytes, publishes them at the root of `gh-pages`, and preserves that branch's deployment history; `docs-site/dist/` remains ignored and is never committed alongside source on `master`. Configure GitHub Pages once to publish from the root of `gh-pages`. No custom domain or `CNAME` is assumed.

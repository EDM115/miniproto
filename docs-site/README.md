# miniproto documentation site

This static Astro/Starlight shell loads the repository’s canonical Markdown directly from `../docs`; it does not copy, move, or symlink handwritten files. `docs/THOUGHTS.md` is intentionally excluded from content loading and search.

## Frontend-only iteration

Use the current Node.js 26 release from `.node-version` and the current pnpm 11 release declared in `packageManager`. Corepack is not used. From this directory, invoke pnpm directly:

```sh
pnpm install --frozen-lockfile
pnpm dev
pnpm check
pnpm build
pnpm test:site
pnpm brand:check
```

`MINIPROTO_DOCS_SITE` sets the canonical site origin and `MINIPROTO_DOCS_BASE` sets its deploy path. The default base is `/`, which is suitable for local previews, the VPS container, and any origin-root static host. The GitHub workflow explicitly sets `MINIPROTO_DOCS_BASE=/miniproto` because a project Pages site is served below the repository name.

## Alpine container

Build and validate the root-hosted static artifact, then package it in the unprivileged NGINX runtime from the repository root:

```sh
MINIPROTO_DOCS_SITE=https://docs.example.com MINIPROTO_DOCS_BASE=/ pnpm --dir docs-site build
docker build --file docs-site/Dockerfile --tag miniproto-docs .
docker run --rm --publish 8080:8080 miniproto-docs
```

The default Docker target validates the prepared root-base artifact in Alpine 3.24 and copies it into unprivileged NGINX on Alpine 3.24. This keeps image packaging reliable on small builders; the full reference site can exceed a 768 MiB Node heap while Astro ingests it. The final image contains only the generated site and NGINX listening on port 8080. `MINIPROTO_DOCS_SITE` is set during the preceding Astro build because canonical and social metadata is prerendered. Mount the container at the origin root or place it behind a reverse proxy that preserves root paths. The image health check requests `/` locally.

Builders with at least 2 GiB available can instead compile and package from canonical source in one Docker invocation:

```sh
docker build --file docs-site/Dockerfile --target source-runtime --build-arg MINIPROTO_DOCS_SITE=https://docs.example.com --tag miniproto-docs .
```

That optional target uses Node.js 26.7.0 and pnpm 11.22.0 on Alpine 3.24 and keeps the pnpm dependency store in BuildKit. Production builds force a fresh Astro content layer so imported Markdown-transform changes cannot reuse stale rendered pages. Both targets produce the same root-base NGINX runtime.

## Complete repository pipeline

From the repository root, install the Python documentation group and run the single orchestrator:

```sh
rustup toolchain install nightly-2026-08-12
cargo install cargo-docs-md --version 0.2.4 --locked
uv sync --extra dev,docs
uv run miniproto-docs
uv run miniproto-docs --check
uv run miniproto-docs --check --build
```

The default command generates and reconciles only `docs/reference/`. `--check` generates into an isolated task-owned tree and fails on committed drift without modifying the reference. `--build` additionally performs the frozen pnpm install, Astro content/type check, static Pagefind build, browser acceptance, and route/link/search/artifact validation. Generated Python, Telegram, and Rust Markdown stays committed; only dependency caches, intermediate extractors, and static build output are ignored.

Packet Loom is the provisional identity while the community poll is open. `src/assets/brand/concepts/03-packet-loom/logo.svg` is the immutable inner mark used by `scripts/build-brand.mjs`; `pnpm brand:build` regenerates the complete derivative set and `pnpm brand:check` fails on drift. Promoting a different approved concept later should change that canonical input boundary and its generated assets, not site content structure.

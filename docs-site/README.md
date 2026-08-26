# miniproto documentation site

This static Astro/Starlight shell loads the repository’s canonical Markdown directly from `../docs`, it does not copy, move or symlink handwritten files. `docs/THOUGHTS.md` is intentionally excluded from content loading and search.

## Frontend-only iteration

Use the current Node.js 26 with PNPM 11. From this directory, invoke pnpm directly :

```zsh
pnpm install --frozen-lockfile
pnpm dev
pnpm format
pnpm lint
pnpm check
pnpm build
pnpm test:site
pnpm brand:check
```

`MINIPROTO_DOCS_SITE` sets the canonical site origin and `MINIPROTO_DOCS_BASE` sets its deploy path. The default base is `/`, which is suitable for local previews, a VPS container and any origin-root static host. The GitHub workflow explicitly sets `MINIPROTO_DOCS_BASE=/miniproto` because a project Pages site is served below the repository name.

## Alpine container

Build and validate the root-hosted static artifact, then package it in the unprivileged NGINX runtime from the repository root :

```zsh
MINIPROTO_DOCS_SITE=https://miniproto.edm115.dev MINIPROTO_DOCS_BASE=/ pnpm --dir docs-site build
docker build --file docs-site/Dockerfile --tag miniproto-docs .
docker run --rm --publish 6743:6743 miniproto-docs
```

Builders with at least 2 GiB available can instead compile and package from canonical source in one Docker invocation :

```zsh
docker build --file docs-site/Dockerfile --target source-runtime --build-arg MINIPROTO_DOCS_SITE=https://miniproto.edm115.dev --tag miniproto-docs .
```

## Complete repository pipeline

From the repository root, install the Python documentation group and run the single orchestrator :

```zsh
rustup toolchain install nightly
cargo install cargo-docs-md --locked
uv sync --extra dev,docs
uv run miniproto-docs
uv run miniproto-docs --check
uv run miniproto-docs --check --build
```

The default command generates and reconciles only `docs/reference/`. `--check` generates into an isolated task-owned tree and fails on committed drift without modifying the reference. `--build` additionally performs the frozen pnpm install, Astro content/type check, static Pagefind build, browser acceptance and route/link/search/artifact validation. Generated Python, Telegram and Rust Markdown stays committed, only dependency caches, intermediate extractors and static build output are ignored.

## GitHub Pages publication

Pull-request documentation automation starts only after the required draft pull request is marked ready for review, then reruns on later pushes. A trusted `master` push publishes the already validated `docs-site/dist/` bytes at the root of `gh-pages` while preserving the branch's deployment history. The static output remains ignored on `master`.

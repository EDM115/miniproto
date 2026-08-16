# miniproto documentation site

This static Astro/Starlight shell loads the repository’s canonical Markdown directly from `../docs`; it does not copy, move, or symlink handwritten files. `docs/THOUGHTS.md` is intentionally excluded from content loading and search.

## Frontend-only iteration

Use Node.js `24.19.0` from `.node-version` and pnpm `11.21.0`. From this directory, use the pinned frontend commands directly:

```sh
pnpm install --frozen-lockfile
pnpm dev
pnpm check
pnpm build
```

`MINIPROTO_DOCS_SITE` sets the canonical site origin and `MINIPROTO_DOCS_BASE` sets its deploy path. Their defaults target GitHub Pages at `https://edm115.github.io/miniproto/`; set `MINIPROTO_DOCS_BASE=/` for an origin-hosted preview or portable static deployment.

## Complete repository pipeline

From the repository root, install the Python documentation group and run the single orchestrator:

```sh
uv sync --extra dev --extra docs
uv run miniproto-docs
uv run miniproto-docs --check
uv run miniproto-docs --check --build
```

The default command generates and reconciles only `docs/reference/`. `--check` generates into an isolated task-owned tree and fails on committed drift without modifying the reference. `--build` additionally performs the frozen pnpm install, Astro content/type check, and static Pagefind build. Generated Python, Telegram, and Rust Markdown stays committed; only dependency caches, intermediate extractors, and static build output are ignored.

# Contributing

## Local Tooling

- Use `uv` for Python environments and dependency resolution
- Use `ruff` for Python formatting and linting
- Use `ty` for type checking
- Use Cargo, `cargo fmt`, `cargo clippy`, and `cargo test` for Rust
- Use Oxfmt for supported documentation-site files, Oxlint for the site's maintained `.ts` sources, and `astro check` for Astro templates/content

## Expected Checks

Run the narrow checks for your change first, then the full release acceptance set when the protocol surface grows: `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, `uv run pytest`, `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, and `cargo test --all-features`.

## Pull Requests

Open every pull request as a draft. Pull-request Actions intentionally begin only after a PR explicitly transitions from Draft → Ready for review. Once the PR is ready, each subsequent push will rerun the relevant workflows. Return an unready change to draft instead of using failing automation as a readiness marker.

## Command Reference

Use [docs/development.md](docs/development.md) as the canonical local command reference for dependency sync, linting, formatting, testing, building, and publishing.

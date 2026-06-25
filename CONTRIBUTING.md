# Contributing

This project is early-stage and follows the implementation plan in `PLAN.md`.

## Local Tooling

- Use `uv` for Python environments and dependency resolution.
- Use `ruff` for Python formatting and linting.
- Use `ty` for type checking as the type checker matures.
- Use Cargo, `cargo fmt`, `cargo clippy`, and `cargo test` for Rust.

## Expected Checks

Run the narrow checks for your change first, then the full release acceptance set when the protocol surface grows: `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, `uv run pytest`, `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, and `cargo test --all-features`.

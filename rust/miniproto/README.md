# miniproto native

`miniproto` is the Rust/PyO3 acceleration layer bundled with the [miniproto Python MTProto SDK](https://github.com/EDM115/miniproto). It provides measured crypto, transport framing, MTProto envelope and generated TL fast paths to Python through the `miniproto_native` extension module.

## Current package boundary

The `0.1.x` Cargo package records source provenance for the bundled accelerator and stays version-aligned with the Python distribution. Its library target is named `miniproto_native` and builds only a `cdylib` for the Python extension.
The crate does not yet provide a supported standalone Rust API. Direct Rust use is deferred until it exposes an `rlib`, separates the PyO3 boundary from Rust-facing modules, documents an API stability policy and passes external-consumer tests.
Install the supported Python package with:

```zsh
uv add miniproto
```

See the [documentation website](https://miniproto.edm115.dev/) for the Python SDK and generated native reference or the [repository release guide](https://github.com/EDM115/miniproto/blob/master/docs/project/release.md) for the synchronized PyPI/crates.io provenance model.

## License

MIT

# miniproto native

`miniproto` is the Rust/PyO3 acceleration layer bundled with the [miniproto Python MTProto SDK](https://github.com/EDM115/miniproto). It provides measured crypto, transport framing, MTProto envelope, and generated TL fast paths to Python through the `miniproto_native` extension module.

## Current package boundary

The `0.1.x` crate is published to crates.io for source provenance, documentation, and exact version parity with the Python distribution. Its library target is named `miniproto_native` and currently builds only a `cdylib` for the Python accelerator.

This package is not yet a supported standalone Rust library API. Depending on it from another Rust project and writing `use miniproto_native::...` is deliberately deferred until the crate exposes an `rlib`, separates the PyO3 boundary from its Rust-facing modules, documents a stability policy, and passes external-consumer tests.

Install the supported Python package with:

```console
python -m pip install miniproto
```

See the [documentation website](https://edm115.github.io/miniproto/) for the Python SDK and generated native reference, or the [repository release guide](https://github.com/EDM115/miniproto/blob/master/docs/project/release.md) for the synchronized PyPI/crates.io provenance model.

## License

MIT

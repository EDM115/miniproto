---
title: "miniproto_native"
description: "Bundled PyO3 acceleration module for [`miniproto`](https://pypi.org/project/miniproto/)."
generated: true
editUrl: false
language: "rust"
kind: "crate"
qualified_name: "miniproto_native"
source_path: "rust/miniproto/src/lib.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/lib.rs#L1"
python_visible: false
---

## Provenance

- Rust visibility: `public`
- Source: [`rust/miniproto/src/lib.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/lib.rs#L1)
- Python exposure: Not evidenced by static PyO3 attributes.

## Documented items

- [`miniproto_native::mtproto`](./mtproto/)
- [`miniproto_native::tl`](./tl/)
- [`miniproto_native::transport`](./transport/)
- [`miniproto_native::crypto`](./crypto/)

## cargo-docs-md rendering

# Crate `miniproto_native`

Bundled PyO3 acceleration module for [`miniproto`](https://pypi.org/project/miniproto/).

Python imports this crate as `miniproto._native` for cryptography, encrypted MTProto envelopes, selected TL codecs and TCP framing. Python wrappers select these functions or their fallbacks per operation.

## Quick Reference

| Item | Kind | Description |
|------|------|-------------|
| [`crypto`](#crypto) | mod | Registers cryptographic Python callables. |
| [`generated_tl`](#generated-tl) | mod | Generated TL constructor metadata and field specifications. |
| [`mtproto`](#mtproto) | mod | Registers encrypted MTProto message-envelope callables. |
| [`tl`](#tl) | mod | Registers primitive and generated fast-path TL codec callables. |
| [`transport`](#transport) | mod | Registers TCP transport framing callables and the stateful codec class. |
| [`_native`](#native) | fn | Initializes Python module `miniproto._native`. |

## Modules

- [`crypto`](crypto/index.md) — Registers cryptographic Python callables.
- `generated_tl` — Generated TL constructor metadata and field specifications.
- [`mtproto`](mtproto/index.md) — Registers encrypted MTProto message-envelope callables.
- [`tl`](tl/index.md) — Registers primitive and generated fast-path TL codec callables.
- [`transport`](transport/index.md) — Registers TCP transport framing callables and the stateful codec class.

## Functions

### `_native`

```rust
fn _native(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/lib.rs:29-35`*

Initializes Python module `miniproto._native`.

`gil_used = false` declares support for free-threaded Python. Python-object access still requires an attached thread, which holds the GIL on GIL-enabled builds. Selected exports detach for native work. Registration errors propagate as Python exceptions.

# Arguments

- `m`: The newly-created `miniproto._native` Python module receiving the registered exports.

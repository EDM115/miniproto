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
crate: "miniproto_native"
python_visible: false
---

## Provenance

- Crate: `miniproto_native`
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

Python imports this crate as `miniproto._native`.  It registers native implementations for
cryptographic primitives, encrypted MTProto envelopes, selected TL codecs, and TCP transport
framing.  These routines are an optional acceleration layer: the Python package owns the
public fallback policy and must remain correct when this extension cannot be imported.

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

*Defined in `rust\miniproto\src\lib.rs:34-40`*

Initializes Python module `miniproto._native`.

PyO3 declares this module usable without the GIL (`gil_used = false`), but individual exports
still acquire or release it as required by their Python-object interactions.  Returns a Python
exception if any submodule registration fails.

# Arguments

- `m`: The newly-created `miniproto._native` Python module receiving the registered exports.

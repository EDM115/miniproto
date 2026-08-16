---
title: "miniproto_native::crypto::pq_factorize"
description: "Factorizes Python `pq_factorize(pq)` into ordered nontrivial `u64` factors."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::pq_factorize"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L468"
aliases: ["miniproto._native.pq_factorize"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L468)
- Python exposure: `miniproto._native.pq_factorize` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn pq_factorize(py: _, pq: u64) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach the factorization search.
- `pq`: Composite MTProto handshake value to split into ordered factors.

## cargo-docs-md rendering

### `pq_factorize`

```rust
fn pq_factorize(py: Python<'_>, pq: u64) -> PyResult<(u64, u64)>
```

*Defined in `rust\miniproto\src\crypto.rs:468-470`*

Factorizes Python `pq_factorize(pq)` into ordered nontrivial `u64` factors.

Returns `ValueError` for non-composite values and runs the potentially expensive search with
the GIL released.

# Arguments

- `py`: The acquired GIL token used to detach the factorization search.
- `pq`: Composite MTProto handshake value to split into ordered factors.

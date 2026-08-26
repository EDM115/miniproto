---
title: "miniproto_native::crypto::scrypt_derive"
description: "Derives Python `scrypt_derive` bytes from password, salt and scrypt cost parameters."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::scrypt_derive"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L446"
aliases: ["miniproto._native.scrypt_derive"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L446)
- Python exposure: `miniproto._native.scrypt_derive` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn scrypt_derive(py: _, password: _, salt: _, n: u32, r: u32, p: u32, length: usize) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach only sufficiently large scrypt work.
- `password`: Password bytes accepted by scrypt.
- `salt`: Salt bytes accepted by scrypt.
- `n`: CPU/memory cost, required to be a power of two greater than one.
- `r`: scrypt block-size cost parameter.
- `p`: scrypt parallelization cost parameter.
- `length`: Requested derived-key length in the inclusive range 1..=1024.

## cargo-docs-md rendering

### `scrypt_derive`

```rust
fn scrypt_derive(py: Python<'_>, password: Vec<u8>, salt: Vec<u8>, n: u32, r: u32, p: u32, length: usize) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:446-463`*

Derives Python `scrypt_derive` bytes from password, salt and scrypt cost parameters.

`n` must be a power of two above one and `length` is limited to 1..=1024; invalid parameters
return `ValueError`. Estimated memory is capped at 256 MiB and aggregate work at 1 GiB. The
GIL is released when the `128 * n * r * p` work estimate exceeds 4 KiB.

# Arguments

- `py`: The acquired GIL token used to detach only sufficiently large scrypt work.
- `password`: Password bytes accepted by scrypt.
- `salt`: Salt bytes accepted by scrypt.
- `n`: CPU/memory cost, required to be a power of two greater than one.
- `r`: scrypt block-size cost parameter.
- `p`: scrypt parallelization cost parameter.
- `length`: Requested derived-key length in the inclusive range 1..=1024.

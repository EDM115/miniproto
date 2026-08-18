---
title: Native Rust acceleration and fallback
description: Capability-based Rust selection, output parity, and the limits of native availability.
slug: /concepts/native-acceleration/
generated: false
---

## One Python contract, several implementations

The bundled Rust/PyO3 extension is imported as the private `miniproto._native` module. Public crypto, TL, framing, and session helpers use backend-neutral Python wrappers so callers depend on results, validation errors, and documented lifecycle behavior rather than calling the extension directly.

If the compiled module cannot import or does not expose the required baseline symbols, the wrappers select the internal pure-Python fallback and record a diagnostic through project observability. A successful import alone is not enough for every capability: for example, native transport framing is available only when the module exposes `TransportCodec`.

## Native availability is not a blanket promise

`native_available()` says that a complete baseline Rust backend was selected at import time. It is not a benchmark result, a security property, a promise that every public operation uses Rust, or a guarantee that an operation releases the GIL. Several small scalar and hash paths deliberately keep the benchmarked C-backed Python or `cryptography` route even while Rust is available.

For selected Rust crypto work, GIL detachment is operation- and input-size-dependent. Fallback and `cryptography` paths make no matching GIL-release claim. Application concurrency should therefore be designed around async I/O and bounded work rather than around a presumed native speedup.

## Parity before performance

Native and fallback paths are intended to agree on output and validation behavior. The framing adapter accepts fragmented TCP input and emits payload, quick-ack, or negative transport-error events; malformed or oversized frames become Python errors rather than native process termination. A native codec initialization race/capability failure is distinct from an ordinary invalid-input `ValueError`.

Rust acceleration is part of the wheel's implementation, not a separately stable Rust SDK for the `0.1.x` Alpha line. When diagnosing a deployment, distinguish a missing/partial extension from an application error and retain the correct fallback rather than forcing a native-only path without capability evidence.

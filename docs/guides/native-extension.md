---
title: Native extension diagnosis
description: Identify Rust extension loading and understand the supported Python fallback and mixed-dispatch behavior.
slug: /guides/native-extension
generated: false
---

# Native extension diagnosis

Miniproto exposes one Python crypto/TL API whether the bundled Rust extension is available or not. The compiled module is `miniproto._native`; `miniproto.crypto.native` selects it when it imports and exposes the required baseline symbols, otherwise public operations use the Python fallback or a mixed dispatch path.

```python
from miniproto.crypto.native import native_available


if native_available():
    print("Bundled Rust baseline is available")
else:
    print("Using the supported fallback or mixed dispatch path")
```

`native_available()` reports import-time selection state. It is not a benchmark result, a promise that every operation uses Rust, a statement about optional native session-crypto capabilities or a security verdict. Some small scalar operations deliberately use C-backed Python implementations because the call boundary costs more than the Rust path for those inputs. Larger and batched paths can select native work independently.

## Diagnose before rebuilding

1. Run the probe in the same interpreter and environment that runs the application. A shell with a different `uv` environment can see a different extension.
2. Confirm the minimum runtime declaration: Python 3.13 or newer.
3. Run an offline import and focused tests before assuming that an extension issue is a Telegram transport or credential problem.
4. For a local editable native build, use the repository's documented command:

```powershell
uv run maturin develop
```

The fallback is part of the supported runtime boundary, so an unavailable extension is not by itself an API failure for operations whose fallback dependencies are present. AES/Scrypt fallback uses `cryptography`. This project excludes that dependency from its Windows ARM64 base dependencies, so those operations need available native capabilities there unless `cryptography` is installed separately. Native absence can change workload performance. Measure the operation and input sizes that matter after rebuilding. Do not infer a whole-application speedup from a successful import.

## Session crypto and errors

The session-string layer can request optional native session crypto for specific operations and emits a stable capability error when a no-fallback variant is unavailable. The ordinary portable session-string APIs use the supported crypto paths. AES/Scrypt fallback still depends on `cryptography`, which the Windows ARM64 base dependencies exclude. Read [string-session migration](./string-sessions.md) and [session storage and credential handling](../session-security.md) before testing with real authorization state.

Native loading should also remain separate from event-loop selection. The event loop may use `uvloop`, `winloop` or the standard library independently of the Rust extension; see [event-loop ownership](./event-loop-ownership.md).

---
title: "miniproto.auth.key_exchange.ServerDHInnerData"
description: "Validated plaintext DH group and server public value from Telegram."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.ServerDHInnerData"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L291"
aliases: ["miniproto.auth.ServerDHInnerData"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ServerDHInnerData`

```python
ServerDHInnerData(nonce: int, server_nonce: int, g: int, dh_prime: bytes, g_a: bytes, server_time: int) -> None
```

Validated plaintext DH group and server public value from Telegram.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce that must match the active exchange.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce that must match the active exchange.
- **g** (<code>[int](#int)</code>) – Telegram DH generator.
- **dh_prime** (<code>[bytes](#bytes)</code>) – Big-endian 2048-bit Telegram safe-prime modulus.
- **g_a** (<code>[bytes](#bytes)</code>) – Big-endian server DH public value.
- **server_time** (<code>[int](#int)</code>) – Server Unix time used to calculate client time offset.

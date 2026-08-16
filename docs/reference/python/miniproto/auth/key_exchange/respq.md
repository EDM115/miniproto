---
title: "miniproto.auth.key_exchange.ResPQ"
description: "Decoded ``resPQ`` response received at the start of key exchange."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.ResPQ"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L100"
aliases: ["miniproto.auth.ResPQ"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ResPQ`

```python
ResPQ(nonce: int, server_nonce: int, pq: bytes, server_public_key_fingerprints: tuple[int, ...]) -> None
```

Decoded ``resPQ`` response received at the start of key exchange.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server's random 128-bit nonce.
- **pq** (<code>[bytes](#bytes)</code>) – Big-endian composite factorization challenge.
- **server_public_key_fingerprints** (<code>[tuple](#tuple)[[int](#int), ...]</code>) – RSA key fingerprints offered by the server.

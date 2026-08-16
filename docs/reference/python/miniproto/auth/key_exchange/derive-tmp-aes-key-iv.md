---
title: "miniproto.auth.key_exchange.derive_tmp_aes_key_iv"
description: "Derive the temporary AES-256-IGE key and IV defined by MTProto key exchange."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.derive_tmp_aes_key_iv"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L757"
aliases: ["miniproto.auth.derive_tmp_aes_key_iv"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.derive_tmp_aes_key_iv`

```python
derive_tmp_aes_key_iv(new_nonce: int, server_nonce: int) -> tuple[bytes, bytes]
```

Derive the temporary AES-256-IGE key and IV defined by MTProto key exchange.

**Parameters:**

- **new_nonce** (<code>[int](#int)</code>) – Fresh 256-bit client nonce for the active exchange.
- **server_nonce** (<code>[int](#int)</code>) – 128-bit server nonce from ``resPQ``.

---
title: "miniproto.auth.key_exchange.decrypt_server_dh_answer"
description: "Decrypt, integrity-check, and decode Telegram's encrypted DH inner payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.decrypt_server_dh_answer"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L791"
aliases: ["miniproto.auth.decrypt_server_dh_answer"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.decrypt_server_dh_answer`

```python
decrypt_server_dh_answer(encrypted_answer: bytes, *, new_nonce: int, server_nonce: int) -> ServerDHInnerData
```

Decrypt, integrity-check, and decode Telegram's encrypted DH inner payload.

**Parameters:**

- **encrypted_answer** (<code>[bytes](#bytes)</code>) – AES-IGE ciphertext returned in ``server_DH_params_ok``.
- **new_nonce** (<code>[int](#int)</code>) – Fresh client nonce used to derive the temporary cipher key.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce used to derive the temporary cipher key.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ciphertext is too short or no SHA-1-prefixed payload validates.
- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the validated payload does not decode as server DH inner data.

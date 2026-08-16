---
title: "miniproto.auth.key_exchange.ReqDHParams"
description: "Serialized ``req_DH_params`` request containing RSA-encrypted inner data."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.ReqDHParams"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L182"
aliases: ["miniproto.auth.ReqDHParams"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ReqDHParams`

```python
ReqDHParams(nonce: int, server_nonce: int, p: bytes, q: bytes, public_key_fingerprint: int, encrypted_data: bytes) -> None
```

Serialized ``req_DH_params`` request containing RSA-encrypted inner data.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce from the initial ``req_pq_multi`` request.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce returned by ``resPQ``.
- **p** (<code>[bytes](#bytes)</code>) – First factor of Telegram's ``pq`` challenge.
- **q** (<code>[bytes](#bytes)</code>) – Second factor of Telegram's ``pq`` challenge.
- **public_key_fingerprint** (<code>[int](#int)</code>) – Signed fingerprint identifying the selected server RSA key.
- **encrypted_data** (<code>[bytes](#bytes)</code>) – RSA_PAD ciphertext of :class:`PQInnerDataDC` bytes.

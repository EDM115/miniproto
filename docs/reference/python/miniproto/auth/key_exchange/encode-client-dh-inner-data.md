---
title: "miniproto.auth.key_exchange.encode_client_dh_inner_data"
description: "Serialize ``client_DH_inner_data`` before temporary AES-IGE encryption."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.encode_client_dh_inner_data"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L628"
aliases: ["miniproto.auth.encode_client_dh_inner_data"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.encode_client_dh_inner_data`

```python
encode_client_dh_inner_data(inner: ClientDHInnerData) -> bytes
```

Serialize ``client_DH_inner_data`` before temporary AES-IGE encryption.

**Parameters:**

- **inner** (<code>[ClientDHInnerData](#miniproto.auth.key_exchange.ClientDHInnerData)</code>) – Client DH nonces, retry identifier, and public value to encode.

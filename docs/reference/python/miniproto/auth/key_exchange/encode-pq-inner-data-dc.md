---
title: "miniproto.auth.key_exchange.encode_pq_inner_data_dc"
description: "Serialize ``p_q_inner_data_dc`` before applying Telegram RSA padding."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.encode_pq_inner_data_dc"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L607"
aliases: ["miniproto.auth.encode_pq_inner_data_dc"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.encode_pq_inner_data_dc`

```python
encode_pq_inner_data_dc(inner: PQInnerDataDC) -> bytes
```

Serialize ``p_q_inner_data_dc`` before applying Telegram RSA padding.

**Parameters:**

- **inner** (<code>[PQInnerDataDC](#miniproto.auth.key_exchange.PQInnerDataDC)</code>) – Exchange-specific factors, nonces, and target DC payload.

**Returns:**

- <code>[bytes](#bytes)</code> – Constructor-prefixed Telegram TL bytes.

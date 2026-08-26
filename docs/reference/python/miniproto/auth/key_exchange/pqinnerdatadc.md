---
title: "miniproto.auth.key_exchange.PQInnerDataDC"
description: "Plaintext ``p_q_inner_data_dc`` encrypted into ``req_DH_params``."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.PQInnerDataDC"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L152"
aliases: ["miniproto.auth.PQInnerDataDC"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.PQInnerDataDC`

```python
PQInnerDataDC(pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int, dc_id: int) -> None
```

Plaintext ``p_q_inner_data_dc`` encrypted into ``req_DH_params``.

The random ``new_nonce`` binds every exchange and must stay secret until the
authorization key is established.

**Parameters:**

- **pq** (<code>[bytes](#bytes)</code>) – Original big-endian composite value returned by Telegram.
- **p** (<code>[bytes](#bytes)</code>) – First factor of ``pq`` in minimal big-endian form.
- **q** (<code>[bytes](#bytes)</code>) – Second factor of ``pq`` in minimal big-endian form.
- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce returned in ``resPQ``.
- **new_nonce** (<code>[int](#int)</code>) – Fresh random nonce that binds this key exchange.
- **dc_id** (<code>[int](#int)</code>) – Target Telegram DC ID, encoded for test mode when applicable.

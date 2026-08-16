---
title: "miniproto.crypto.native.pq_factorize"
description: "Factor the composite integer used by the MTProto handshake."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.pq_factorize"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L1114"
aliases: ["miniproto.crypto.pq_factorize"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.pq_factorize`

```python
pq_factorize(pq: int) -> tuple[int, int]
```

Factor the composite integer used by the MTProto handshake.

**Parameters:**

- **pq** (<code>[int](#int)</code>) – A composite integer greater than or equal to four.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – The two factors in ascending order.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``pq`` is too small or prime.

Uses the selected backend's Pollard-rho-style implementation.  It is a
protocol helper, not a general-purpose factorization service; runtime grows
with the input and no fixed latency guarantee is made.

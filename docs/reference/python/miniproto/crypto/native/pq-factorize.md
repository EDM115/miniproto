---
title: "miniproto.crypto.native.pq_factorize"
description: "Factor the composite integer used by the MTProto handshake."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.pq_factorize"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L1110"
aliases: ["miniproto.crypto.pq_factorize"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.pq_factorize`

```python
pq_factorize(pq: int) -> tuple[int, int]
```

Factor the composite integer used by the MTProto handshake.

**Parameters:**

- **pq** (<code>[int](#int)</code>) – A composite integer in the inclusive range four through ``2**64 - 1``.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – The two factors in ascending order.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``pq`` is outside the supported range, prime or exceeds the factorization work budget.

Both backends limit Pollard-rho to sixteen attempts of at most 100,000 iterations each. This synchronous protocol helper has a finite work budget, not a fixed latency guarantee.

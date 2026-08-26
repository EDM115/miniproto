---
title: "miniproto.auth.key_exchange.factorize_pq"
description: "Factor Telegram's small composite ``pq`` and return its factors in ascending order."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.factorize_pq"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L728"
aliases: ["miniproto.auth.factorize_pq"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.factorize_pq`

```python
factorize_pq(pq: int) -> tuple[int, int]
```

Factor Telegram's small composite ``pq`` and return its factors in ascending order.

**Parameters:**

- **pq** (<code>[int](#int)</code>) – Positive composite challenge decoded from Telegram's ``resPQ`` response.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the native factorizer returns invalid factors.

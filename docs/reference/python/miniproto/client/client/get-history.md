---
title: "miniproto.client.Client.get_history"
description: "Fetch normalized message history for a peer using Telegram pagination fields."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.get_history"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L710"
aliases: ["miniproto.Client.get_history"]
module: "miniproto.client"
---

## `miniproto.client.Client.get_history`

```python
get_history(peer: Peer | str | int, *, limit: int = 100, offset_id: int = 0, offset_date: int = 0, add_offset: int = 0, max_id: int = 0, min_id: int = 0, hash: int = 0, request_timeout: float | None = None, flood_sleep_threshold: int | None = None, retry: bool | None = None) -> tuple[Message, ...]
```

Fetch normalized message history for a peer using Telegram pagination fields.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Peer object, numeric ID, or username.
- **limit** (<code>[int](#int)</code>) – Maximum messages to request, defaulting to 100; zero is allowed.
- **offset_id** (<code>[int](#int)</code>) – Message ID pagination offset.
- **offset_date** (<code>[int](#int)</code>) – Unix timestamp pagination offset.
- **add_offset** (<code>[int](#int)</code>) – Additional relative offset.
- **max_id** (<code>[int](#int)</code>) – Upper exclusive message-ID boundary.
- **min_id** (<code>[int](#int)</code>) – Lower exclusive message-ID boundary.
- **hash** (<code>[int](#int)</code>) – Telegram history hash for not-modified responses.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-request timeout overriding configuration.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Optional automatic flood-wait ceiling.
- **retry** (<code>[bool](#bool) | None</code>) – Whether to force or suppress retry eligibility.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``limit`` is negative.

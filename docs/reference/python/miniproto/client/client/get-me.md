---
title: "miniproto.client.Client.get_me"
description: "Return the authorized user, optionally bypassing the peer cache."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.get_me"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L692"
aliases: ["miniproto.Client.get_me"]
module: "miniproto.client"
---

## `miniproto.client.Client.get_me`

```python
get_me(*, refresh: bool = False) -> User
```

Return the authorized user, optionally bypassing the peer cache.

**Parameters:**

- **refresh** (<code>[bool](#bool)</code>) – Attempt a Telegram fetch before reading cached identity. If the response contains no concrete user, the peer cache can still return its stored identity.

**Raises:**

- <code>[Unauthorized](#miniproto.errors.Unauthorized)</code> – If no authorized session is available.

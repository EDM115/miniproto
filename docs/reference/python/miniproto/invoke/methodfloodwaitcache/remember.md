---
title: "miniproto.invoke.MethodFloodWaitCache.remember"
description: "Record a cacheable Telegram method flood wait without shortening it."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.MethodFloodWaitCache.remember"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L376"
module: "miniproto.invoke"
---

## `miniproto.invoke.MethodFloodWaitCache.remember`

```python
remember(request: object, error: FloodWait) -> bool
```

Record a cacheable Telegram method flood wait without shortening it.

**Parameters:**

- **request** (<code>[object](#object)</code>) – Request whose innermost Telegram method identifies the wait.
- **error** (<code>[FloodWait](#miniproto.errors.FloodWait)</code>) – Classified flood-wait RPC error to reconstruct for future calls.

**Returns:**

- <code>[bool](#bool)</code> – ``True`` when the error has a cacheable generic or premium wait name;
- <code>[bool](#bool)</code> – otherwise ``False`` without modifying the cache.

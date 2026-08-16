---
title: "miniproto.invoke.MethodFloodWaitCache.get"
description: "Return a reconstructed remaining flood wait for ``request``, if any."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.MethodFloodWaitCache.get"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L408"
module: "miniproto.invoke"
---

## `miniproto.invoke.MethodFloodWaitCache.get`

```python
get(request: object) -> FloodWait | None
```

Return a reconstructed remaining flood wait for ``request``, if any.

The selected entry is removed lazily when this lookup observes its
expiration. A returned wait uses the current request as context while
preserving the original error type and metadata.

**Parameters:**

- **request** (<code>[object](#object)</code>) – Request whose innermost method selects a cached flood wait.

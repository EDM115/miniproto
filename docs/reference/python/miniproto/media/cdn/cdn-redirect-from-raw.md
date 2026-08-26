---
title: "miniproto.media.cdn.cdn_redirect_from_raw"
description: "Convert a raw CDN redirect response to stable transfer metadata."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.cdn.cdn_redirect_from_raw"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L217"
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.cdn_redirect_from_raw`

```python
cdn_redirect_from_raw(result: object) -> CdnRedirect | None
```

Convert a raw CDN redirect response to stable transfer metadata.

**Parameters:**

- **result** (<code>[object](#object)</code>) – Raw result returned by ``upload.getFile``.

**Returns:**

- **A** (<code>[CdnRedirect](#miniproto.media.cdn.CdnRedirect) | None</code>) – class:`CdnRedirect` for a CDN redirect, otherwise ``None``.

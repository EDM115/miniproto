---
title: "miniproto.media.download.MediaIntegrityError"
description: "Raised when declared file hashes or download-range invariants are violated."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.download.MediaIntegrityError"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L41"
aliases: ["miniproto.MediaIntegrityError","miniproto.media.MediaIntegrityError"]
module: "miniproto.media.download"
---

## `miniproto.media.download.MediaIntegrityError`

```python
MediaIntegrityError(reason: str, *, offset: int, limit: int) -> None
```

Bases: <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code>

Raised when declared file hashes or download-range invariants are violated.

**Parameters:**

- **reason** (<code>[str](#str)</code>) – Machine-readable explanation of the integrity failure.
- **offset** (<code>[int](#int)</code>) – First affected media byte offset.
- **limit** (<code>[int](#int)</code>) – Number of affected bytes.

Record the corrupted interval and format the transfer error message.

**Parameters:**

- **reason** (<code>[str](#str)</code>) – Integrity-failure classification included in the exception message.
- **offset** (<code>[int](#int)</code>) – First affected byte offset.
- **limit** (<code>[int](#int)</code>) – Number of affected bytes.

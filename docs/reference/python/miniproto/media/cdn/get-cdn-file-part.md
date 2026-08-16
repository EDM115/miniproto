---
title: "miniproto.media.cdn.get_cdn_file_part"
description: "Fetch, decrypt, and hash-verify one CDN file range."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.cdn.get_cdn_file_part"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L60"
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.get_cdn_file_part`

```python
get_cdn_file_part(invoke: RawInvoker, redirect: CdnRedirect, *, offset: int, limit: int, request_timeout: float | None = None) -> bytes
```

Fetch, decrypt, and hash-verify one CDN file range.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.cdn.RawInvoker)</code>) – Async raw-RPC invoker bound to the appropriate data center.
- **redirect** (<code>[CdnRedirect](#miniproto.media.cdn.CdnRedirect)</code>) – CDN credentials and encryption metadata returned by Telegram.
- **offset** (<code>[int](#int)</code>) – Byte offset of the requested range and CTR stream.
- **limit** (<code>[int](#int)</code>) – Maximum ciphertext/plaintext bytes to retrieve.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-RPC timeout in seconds.

**Returns:**

- <code>[bytes](#bytes)</code> – The decrypted, integrity-verified bytes returned for the requested range.

**Raises:**

- <code>[CdnIntegrityError](#miniproto.media.cdn.CdnIntegrityError)</code> – The range lacks coverage, has an invalid/short declared
hash range, or its digest mismatches.
- <code>[CdnError](#miniproto.media.cdn.CdnError)</code> – Telegram returns an unsupported CDN response.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The caller cancels the awaited transfer.

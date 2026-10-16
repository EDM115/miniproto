---
title: "miniproto.media.cdn.get_cdn_file_part"
description: "Fetch, decrypt and hash-verify one CDN file range."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.cdn.get_cdn_file_part"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L54"
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.get_cdn_file_part`

```python
get_cdn_file_part(origin_invoke: RawInvoker, cdn_invoke: RawInvoker, redirect: CdnRedirect, *, offset: int, limit: int, request_timeout: float | None = None) -> bytes
```

Fetch, decrypt and hash-verify one CDN file range.

**Parameters:**

- **origin_invoke** (<code>[RawInvoker](#miniproto.media.cdn.RawInvoker)</code>) – Async master-DC invoker used for hashes and reupload authorization.
- **cdn_invoke** (<code>[RawInvoker](#miniproto.media.cdn.RawInvoker)</code>) – Async CDN-DC invoker used only for ``upload.getCdnFile``.
- **redirect** (<code>[CdnRedirect](#miniproto.media.cdn.CdnRedirect)</code>) – CDN credentials and encryption metadata returned by Telegram.
- **offset** (<code>[int](#int)</code>) – Byte offset of the requested range and CTR stream.
- **limit** (<code>[int](#int)</code>) – Maximum plaintext bytes to return. Retrieval covers complete hash intervals and can overfetch aligned ciphertext ranges.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-RPC timeout in seconds.

**Returns:**

- <code>[bytes](#bytes)</code> – The requested slice of complete SHA-256-verified plaintext intervals, at most ``limit`` bytes.

**Raises:**

- <code>[ValueError](#ValueError)</code> – ``offset`` or ``limit`` is invalid, or redirect key/IV lengths or the CTR offset violate decryption constraints.
- <code>[CdnIntegrityError](#miniproto.media.cdn.CdnIntegrityError)</code> – The range lacks complete valid hash coverage, its digest mismatches or a hash interval cannot fit a legal CDN request.
- <code>[CdnError](#miniproto.media.cdn.CdnError)</code> – Telegram returns an unsupported CDN response.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The caller cancels the awaited transfer.

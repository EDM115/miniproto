---
title: "miniproto.media.cdn.verify_cdn_part"
description: "Verify a decrypted CDN chunk against complete declared SHA-256 hash intervals."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.cdn.verify_cdn_part"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L146"
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.verify_cdn_part`

```python
verify_cdn_part(invoke: RawInvoker, redirect: CdnRedirect, *, offset: int, data: bytes, known_hashes: dict[int, types.FileHash] | None = None, request_timeout: float | None = None) -> None
```

Verify a decrypted CDN chunk against complete declared SHA-256 hash intervals.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.cdn.RawInvoker)</code>) – Async raw-RPC invoker used to request missing CDN hash metadata.
- **redirect** (<code>[CdnRedirect](#miniproto.media.cdn.CdnRedirect)</code>) – CDN token and redirect-provided hash metadata for this file.
- **offset** (<code>[int](#int)</code>) – File offset of the first byte in ``data``.
- **data** (<code>[bytes](#bytes)</code>) – Decrypted bytes beginning at a hash interval's exact offset, bytes are not zeroized.
- **known_hashes** (<code>[dict](#dict)[[int](#int), [FileHash](#miniproto.raw.types.FileHash)] | None</code>) – Optional mutable offset-to-hash cache shared by the caller, redirect hashes seed a new cache only when it is omitted.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-RPC timeout in seconds for missing hash fetches.

**Raises:**

- <code>[CdnIntegrityError](#miniproto.media.cdn.CdnIntegrityError)</code> – Any byte lacks a complete declared hash interval, hash metadata is invalid or a SHA-256 digest mismatches.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The awaited metadata request is cancelled.

Missing metadata is fetched from the master DC with ``upload.getCdnFileHashes``. ``data`` must contain complete consecutive hash intervals, each starting at the declared ``FileHash.offset`` and containing exactly ``FileHash.limit`` bytes. This helper does not retrieve missing plaintext for partial intervals.

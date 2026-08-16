---
title: "miniproto.media.cdn.CdnRedirect"
description: "Validated information supplied by Telegram when a file moves to its CDN."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.cdn.CdnRedirect"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L39"
aliases: ["miniproto.media.CdnRedirect"]
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.CdnRedirect`

```python
CdnRedirect(dc_id: int, file_token: bytes, encryption_key: bytes, encryption_iv: bytes, file_hashes: tuple[object, ...], raw: types.UploadFileCdnRedirect) -> None
```

Validated information supplied by Telegram when a file moves to its CDN.

**Attributes:**

- [**dc_id**](#miniproto.media.cdn.CdnRedirect.dc_id) (<code>[int](#int)</code>) – CDN data-center identifier.
- [**file_token**](#miniproto.media.cdn.CdnRedirect.file_token) (<code>[bytes](#bytes)</code>) – Opaque token authorizing CDN file and hash requests.
- [**encryption_key**](#miniproto.media.cdn.CdnRedirect.encryption_key) (<code>[bytes](#bytes)</code>) – 32-byte AES-CTR key for CDN ciphertext; retained as immutable bytes and not zeroized.
- [**encryption_iv**](#miniproto.media.cdn.CdnRedirect.encryption_iv) (<code>[bytes](#bytes)</code>) – 16-byte initial counter block for CDN ciphertext; retained as immutable bytes and not zeroized.
- [**file_hashes**](#miniproto.media.cdn.CdnRedirect.file_hashes) (<code>[tuple](#tuple)[[object](#object), ...]</code>) – Hash metadata supplied with the redirect.
- [**raw**](#miniproto.media.cdn.CdnRedirect.raw) (<code>[UploadFileCdnRedirect](#miniproto.raw.types.UploadFileCdnRedirect)</code>) – Original raw Telegram redirect object.

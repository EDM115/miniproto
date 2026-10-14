---
title: "miniproto.media.cdn.CdnRedirect"
description: "Metadata supplied by Telegram when it redirects a file to its CDN."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.cdn.CdnRedirect"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L33"
aliases: ["miniproto.media.CdnRedirect"]
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.CdnRedirect`

```python
CdnRedirect(dc_id: int, file_token: bytes, encryption_key: bytes, encryption_iv: bytes, file_hashes: tuple[object, ...], raw: types.UploadFileCdnRedirect) -> None
```

Metadata supplied by Telegram when it redirects a file to its CDN.

**Attributes:**

- [**dc_id**](#miniproto.media.cdn.CdnRedirect.dc_id) (<code>[int](#int)</code>) – CDN data-center identifier.
- [**file_token**](#miniproto.media.cdn.CdnRedirect.file_token) (<code>[bytes](#bytes)</code>) – Opaque bearer token for CDN file, hash and reupload requests.
- [**encryption_key**](#miniproto.media.cdn.CdnRedirect.encryption_key) (<code>[bytes](#bytes)</code>) – Expected 32-byte AES-CTR key, validated at decryption, retained as immutable bytes without zeroization.
- [**encryption_iv**](#miniproto.media.cdn.CdnRedirect.encryption_iv) (<code>[bytes](#bytes)</code>) – Expected 16-byte IV, validated at decryption. Its first 12 bytes form the counter prefix, the file block offset replaces its final four bytes. Retained without zeroization.
- [**file_hashes**](#miniproto.media.cdn.CdnRedirect.file_hashes) (<code>[tuple](#tuple)[[object](#object), ...]</code>) – Hash metadata supplied with the redirect.
- [**raw**](#miniproto.media.cdn.CdnRedirect.raw) (<code>[UploadFileCdnRedirect](#miniproto.raw.types.UploadFileCdnRedirect)</code>) – Original raw Telegram redirect object.

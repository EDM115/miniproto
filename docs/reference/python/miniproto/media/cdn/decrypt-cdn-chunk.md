---
title: "miniproto.media.cdn.decrypt_cdn_chunk"
description: "Decrypt a CDN ciphertext range with the counter aligned to its file offset."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.cdn.decrypt_cdn_chunk"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L188"
aliases: ["miniproto.media.decrypt_cdn_chunk"]
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.decrypt_cdn_chunk`

```python
decrypt_cdn_chunk(data: bytes, *, key: bytes, iv: bytes, offset: int = 0) -> bytes
```

Decrypt a CDN ciphertext range with the counter aligned to its file offset.

**Parameters:**

- **data** (<code>[bytes](#bytes)</code>) – Ciphertext bytes for a contiguous CDN response; immutable buffers are not zeroized.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES key material; immutable buffers are not zeroized.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes forming the initial CTR counter; immutable buffers are not zeroized.
- **offset** (<code>[int](#int)</code>) – Non-negative file offset of ``data``; defaults to ``0``.

**Returns:**

- <code>[bytes](#bytes)</code> – Plaintext bytes of the same length as ``data``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – ``key``, ``iv``, or ``offset`` violates CDN cryptographic constraints.

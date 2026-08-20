---
title: "miniproto.crypto.native.xor_bytes"
description: "Return the byte-wise XOR of equal-length inputs."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.xor_bytes"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L771"
aliases: ["miniproto.crypto.xor_bytes"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.xor_bytes`

```python
xor_bytes(left: bytes, right: bytes) -> bytes
```

Return the byte-wise XOR of equal-length inputs.

**Parameters:**

- **left** (<code>[bytes](#bytes)</code>) – First byte string.
- **right** (<code>[bytes](#bytes)</code>) – Second byte string of the same length.

**Returns:**

- <code>[bytes](#bytes)</code> – A byte string of that shared length.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the input lengths differ.

The public wrapper uses the fallback big-integer implementation because it
wins the benchmarked handshake-sized cases; it offers no secret-zeroization.

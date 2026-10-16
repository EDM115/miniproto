---
title: "miniproto.crypto.native.native_available"
description: "Report whether a complete bundled Rust backend was selected."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.native_available"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L523"
aliases: ["miniproto.crypto.native_available"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.native_available`

```python
native_available() -> bool
```

Report whether a complete bundled Rust backend was selected.

**Returns:**

- <code>[bool](#bool)</code> – ``True`` when the selected extension reports native support and exposes the required baseline symbols. Individual operations may still use the fallback.

This reports import-time selection. Optional session-crypto symbols are checked separately.

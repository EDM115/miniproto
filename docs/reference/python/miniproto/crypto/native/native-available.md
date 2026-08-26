---
title: "miniproto.crypto.native.native_available"
description: "Report whether a complete bundled Rust backend was selected."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.native_available"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L532"
aliases: ["miniproto.crypto.native_available"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.native_available`

```python
native_available() -> bool
```

Report whether a complete bundled Rust backend was selected.

**Returns:**

- <code>[bool](#bool)</code> – ``True`` only when the compiled extension imported and exposed the
- <code>[bool](#bool)</code> – required baseline symbols; ``False`` means public operations use the
- <code>[bool](#bool)</code> – fallback or a mixed dispatch path.

The result is import-time state, not a benchmark, a capability guarantee for
optional session crypto or a security property.

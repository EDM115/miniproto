---
title: "miniproto.invoke.validate_result_type"
description: "Raise when a concrete TL response does not match the request result contract."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.validate_result_type"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L250"
module: "miniproto.invoke"
---

## `miniproto.invoke.validate_result_type`

```python
validate_result_type(result: object, expected_type: str | None, raw_request: object) -> None
```

Raise when a concrete TL response does not match the request result contract.

Generic and absent result types deliberately bypass runtime checking.

**Parameters:**

- **result** (<code>[object](#object)</code>) – Decoded RPC result to validate.
- **expected_type** (<code>[str](#str) | None</code>) – Declared TL result type or ``None`` when unavailable.
- **raw_request** (<code>[object](#object)</code>) – Original request attached to a mismatch error for diagnostics.

**Raises:**

- <code>[ResultTypeMismatch](#miniproto.errors.ResultTypeMismatch)</code> – If the concrete response has an incompatible type.

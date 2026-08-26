---
title: "miniproto.invoke.decode_result_payload"
description: "Decode bytes or gzip-packed RPC results while leaving decoded values unchanged."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.decode_result_payload"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L228"
module: "miniproto.invoke"
---

## `miniproto.invoke.decode_result_payload`

```python
decode_result_payload(raw_result: object, expected_type: str | None = None) -> object
```

Decode bytes or gzip-packed RPC results while leaving decoded values unchanged.

**Parameters:**

- **raw_result** (<code>[object](#object)</code>) – Encoded or already decoded sender result.
- **expected_type** (<code>[str](#str) | None</code>) – Optional TL result type used to decode primitive result payloads.

**Returns:**

- <code>[object](#object)</code> – The recursively unpacked and decoded result object.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the payload cannot be decoded exactly.

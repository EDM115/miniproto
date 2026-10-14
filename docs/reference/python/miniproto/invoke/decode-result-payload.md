---
title: "miniproto.invoke.decode_result_payload"
description: "Decode RPC result bytes through at most 16 gzip wrappers, preserving decoded values."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.decode_result_payload"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L236"
module: "miniproto.invoke"
---

## `miniproto.invoke.decode_result_payload`

```python
decode_result_payload(raw_result: object, expected_type: str | None = None, *, max_output_size: int = DEFAULT_GZIP_MAX_OUTPUT_SIZE) -> object
```

Decode RPC result bytes through at most 16 gzip wrappers, preserving decoded values.

**Parameters:**

- **raw_result** (<code>[object](#object)</code>) – Encoded or already decoded sender result.
- **expected_type** (<code>[str](#str) | None</code>) – Optional TL result type used to decode primitive result payloads.
- **max_output_size** (<code>[int](#int)</code>) – Maximum decompressed bytes per gzip wrapper, defaulting to 16 MiB.

**Returns:**

- <code>[object](#object)</code> – The recursively unpacked and decoded result object.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the payload cannot be decoded exactly.
- <code>[ProtocolValidationError](#miniproto.errors.ProtocolValidationError)</code> – If gzip expansion, nesting or stream validity violates the decoding bounds.

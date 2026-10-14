---
title: "miniproto.invoke.decode_rpc_response"
description: "Decode and validate an RPC result, translating Telegram error bodies."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.decode_rpc_response"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L211"
module: "miniproto.invoke"
---

## `miniproto.invoke.decode_rpc_response`

```python
decode_rpc_response(raw_result: object, raw_request: object, *, max_output_size: int = DEFAULT_GZIP_MAX_OUTPUT_SIZE) -> object
```

Decode and validate an RPC result, translating Telegram error bodies.

**Parameters:**

- **raw_result** (<code>[object](#object)</code>) – Sender result, possibly encoded bytes or an MTProto error object.
- **raw_request** (<code>[object](#object)</code>) – Original request used to infer and validate its result type.
- **max_output_size** (<code>[int](#int)</code>) – Maximum decompressed bytes per gzip wrapper, defaulting to 16 MiB.

**Returns:**

- <code>[object](#object)</code> – The decoded result matching the request's declared TL result type.

**Raises:**

- <code>[RpcError](#miniproto.errors.RpcError)</code> – A classified Telegram RPC error when the result is an error body.
- <code>[ResultTypeMismatch](#miniproto.errors.ResultTypeMismatch)</code> – If a non-generic decoded result disagrees with the request contract.
- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If an encoded result is malformed or contains trailing bytes.
- <code>[ProtocolValidationError](#miniproto.errors.ProtocolValidationError)</code> – If gzip expansion, nesting or stream validity violates the decoding bounds.

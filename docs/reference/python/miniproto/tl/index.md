---
title: "miniproto.tl"
description: "Public TL primitive and object codec APIs."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.tl"
source_path: "src/miniproto/tl/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/__init__.py"
module: "miniproto.tl"
---

## `miniproto.tl`

Public TL primitive and object codec APIs.

## Public objects

- [`BOOL_FALSE_ID`](./codec/bool-false-id/) — Public attribute `miniproto.tl.codec.BOOL_FALSE_ID`.
- [`BOOL_TRUE_ID`](./codec/bool-true-id/) — Public attribute `miniproto.tl.codec.BOOL_TRUE_ID`.
- [`TLCodecError`](./codec/tlcodecerror/) — Raised when TL wire data, types or generated metadata cannot be encoded or decoded.
- [`VECTOR_CONSTRUCTOR_ID`](./codec/vector-constructor-id/) — Public attribute `miniproto.tl.codec.VECTOR_CONSTRUCTOR_ID`.
- [`decode_bool`](./codec/decode-bool/) — Decode a TL ``Bool`` constructor.
- [`decode_bytes`](./codec/decode-bytes/) — Decode a TL length-prefixed byte string.
- [`decode_constructor_id`](./codec/decode-constructor-id/) — Decode an unsigned TL constructor identifier.
- [`decode_double`](./codec/decode-double/) — Decode a TL ``double``.
- [`decode_int`](./codec/decode-int/) — Decode a signed TL ``int``.
- [`decode_int128`](./codec/decode-int128/) — Decode an unsigned 128-bit TL integer.
- [`decode_int256`](./codec/decode-int256/) — Decode an unsigned 256-bit TL integer.
- [`decode_long`](./codec/decode-long/) — Decode a signed TL ``long``.
- [`decode_object`](./codec/decode-object/) — Decode a primitive or generated TL object selected by its constructor.
- [`decode_string`](./codec/decode-string/) — Decode a UTF-8 TL string.
- [`decode_uint`](./codec/decode-uint/) — Decode an unsigned 32-bit TL value.
- [`decode_vector`](./codec/decode-vector/) — Decode a boxed TL vector.
- [`deserialize_object`](./codec/deserialize-object/) — Deserialize one generated TL object of an expected class.
- [`encode_bool`](./codec/encode-bool/) — Encode a TL ``Bool`` constructor.
- [`encode_bytes`](./codec/encode-bytes/) — Encode TL's length-prefixed, padded byte-string value.
- [`encode_constructor_id`](./codec/encode-constructor-id/) — Encode a TL constructor identifier as an unsigned 32-bit value.
- [`encode_double`](./codec/encode-double/) — Encode a TL ``double``.
- [`encode_int`](./codec/encode-int/) — Encode a signed TL ``int``.
- [`encode_int128`](./codec/encode-int128/) — Encode an unsigned 128-bit TL integer.
- [`encode_int256`](./codec/encode-int256/) — Encode an unsigned 256-bit TL integer.
- [`encode_long`](./codec/encode-long/) — Encode a signed TL ``long``.
- [`encode_string`](./codec/encode-string/) — UTF-8 encode a string as a TL byte string.
- [`encode_uint`](./codec/encode-uint/) — Encode an unsigned 32-bit TL value.
- [`encode_vector`](./codec/encode-vector/) — Encode a boxed TL vector.
- [`serialize_object`](./codec/serialize-object/) — Serialize a generated TL object using its generated or generic metadata path.

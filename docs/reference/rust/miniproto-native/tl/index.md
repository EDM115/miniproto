---
title: "miniproto_native::tl"
description: "Registers primitive and generated fast-path TL codec callables."
generated: true
editUrl: false
language: "rust"
kind: "module"
qualified_name: "miniproto_native::tl"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L1"
crate: "miniproto_native"
python_visible: false
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `crate`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L1)
- Python exposure: Not evidenced by static PyO3 attributes.

## Documented items

- [`miniproto_native::tl::register`](./register/)
- [`miniproto_native::tl::tl_fast_encode`](./tl-fast-encode/)
- [`miniproto_native::tl::tl_fast_decode`](./tl-fast-decode/)
- [`miniproto_native::tl::tl_encode_int`](./tl-encode-int/)
- [`miniproto_native::tl::tl_decode_int`](./tl-decode-int/)
- [`miniproto_native::tl::tl_encode_uint`](./tl-encode-uint/)
- [`miniproto_native::tl::tl_decode_uint`](./tl-decode-uint/)
- [`miniproto_native::tl::tl_encode_long`](./tl-encode-long/)
- [`miniproto_native::tl::tl_decode_long`](./tl-decode-long/)
- [`miniproto_native::tl::tl_encode_int128`](./tl-encode-int128/)
- [`miniproto_native::tl::tl_decode_int128`](./tl-decode-int128/)
- [`miniproto_native::tl::tl_encode_int256`](./tl-encode-int256/)
- [`miniproto_native::tl::tl_decode_int256`](./tl-decode-int256/)
- [`miniproto_native::tl::tl_encode_double`](./tl-encode-double/)
- [`miniproto_native::tl::tl_decode_double`](./tl-decode-double/)
- [`miniproto_native::tl::tl_encode_bytes`](./tl-encode-bytes/)
- [`miniproto_native::tl::tl_decode_bytes`](./tl-decode-bytes/)
- [`miniproto_native::tl::tl_encode_string`](./tl-encode-string/)
- [`miniproto_native::tl::tl_decode_string`](./tl-decode-string/)
- [`miniproto_native::tl::tl_encode_int_vector`](./tl-encode-int-vector/)
- [`miniproto_native::tl::tl_decode_int_vector`](./tl-decode-int-vector/)
- [`miniproto_native::tl::tl_encode_long_vector`](./tl-encode-long-vector/)
- [`miniproto_native::tl::tl_decode_long_vector`](./tl-decode-long-vector/)

## cargo-docs-md rendering

*miniproto_native / [tl](index.md)*

---

# Module `tl`

Registers primitive and generated fast-path TL codec callables.
Native primitive and generated fast-path codecs for Telegram's Type Language (TL).

The primitive Python-visible `tl_*` functions mirror the pure-Python fallback API. In contrast,
`tl_fast_encode` and `tl_fast_decode` are native-only optional accelerators: Python callers
receive `None` when a selected generated fast path is unavailable and use their fallback path.
They return `ValueError` or `MemoryError` for malformed wire input or failed allocation, release
the GIL only for large primitive-vector work, and do not expose unsafe Rust operations.
Incompatible Python-to-Rust values instead fail during PyO3 conversion with its original
`TypeError`, `OverflowError`, or source exception before these algorithms run.
`generated_tl.rs` is trusted, build-time-generated metadata consumed—not hand-maintained—by
this module. Descriptor indices and bit positions are code-generation invariants rather than
values validated on every hot-path call.

## Contents

- [Structs](#structs)
  - [`FastConstructorSpec`](#fastconstructorspec)
- [Enums](#enums)
  - [`FastWireType`](#fastwiretype)
  - [`FastFieldSpec`](#fastfieldspec)
- [Functions](#functions)
  - [`register`](#register)
  - [`tl_fast_encode`](#tl-fast-encode)
  - [`__pyfunction_tl_fast_encode`](#pyfunction-tl-fast-encode)
  - [`tl_fast_decode`](#tl-fast-decode)
  - [`__pyfunction_tl_fast_decode`](#pyfunction-tl-fast-decode)
  - [`encode_fast_value`](#encode-fast-value)
  - [`decode_fast_value`](#decode-fast-value)
  - [`decode_message_container`](#decode-message-container)
  - [`append_tl_bytes`](#append-tl-bytes)
  - [`decode_tl_bytes_slice`](#decode-tl-bytes-slice)
  - [`tl_encode_int`](#tl-encode-int)
  - [`__pyfunction_tl_encode_int`](#pyfunction-tl-encode-int)
  - [`tl_decode_int`](#tl-decode-int)
  - [`__pyfunction_tl_decode_int`](#pyfunction-tl-decode-int)
  - [`tl_encode_uint`](#tl-encode-uint)
  - [`__pyfunction_tl_encode_uint`](#pyfunction-tl-encode-uint)
  - [`tl_decode_uint`](#tl-decode-uint)
  - [`__pyfunction_tl_decode_uint`](#pyfunction-tl-decode-uint)
  - [`tl_encode_long`](#tl-encode-long)
  - [`__pyfunction_tl_encode_long`](#pyfunction-tl-encode-long)
  - [`tl_decode_long`](#tl-decode-long)
  - [`__pyfunction_tl_decode_long`](#pyfunction-tl-decode-long)
  - [`tl_encode_int128`](#tl-encode-int128)
  - [`__pyfunction_tl_encode_int128`](#pyfunction-tl-encode-int128)
  - [`tl_decode_int128`](#tl-decode-int128)
  - [`__pyfunction_tl_decode_int128`](#pyfunction-tl-decode-int128)
  - [`tl_encode_int256`](#tl-encode-int256)
  - [`__pyfunction_tl_encode_int256`](#pyfunction-tl-encode-int256)
  - [`tl_decode_int256`](#tl-decode-int256)
  - [`__pyfunction_tl_decode_int256`](#pyfunction-tl-decode-int256)
  - [`tl_encode_double`](#tl-encode-double)
  - [`__pyfunction_tl_encode_double`](#pyfunction-tl-encode-double)
  - [`tl_decode_double`](#tl-decode-double)
  - [`__pyfunction_tl_decode_double`](#pyfunction-tl-decode-double)
  - [`tl_encode_bytes`](#tl-encode-bytes)
  - [`__pyfunction_tl_encode_bytes`](#pyfunction-tl-encode-bytes)
  - [`tl_decode_bytes`](#tl-decode-bytes)
  - [`__pyfunction_tl_decode_bytes`](#pyfunction-tl-decode-bytes)
  - [`tl_encode_string`](#tl-encode-string)
  - [`__pyfunction_tl_encode_string`](#pyfunction-tl-encode-string)
  - [`tl_decode_string`](#tl-decode-string)
  - [`__pyfunction_tl_decode_string`](#pyfunction-tl-decode-string)
  - [`tl_encode_int_vector`](#tl-encode-int-vector)
  - [`__pyfunction_tl_encode_int_vector`](#pyfunction-tl-encode-int-vector)
  - [`tl_decode_int_vector`](#tl-decode-int-vector)
  - [`__pyfunction_tl_decode_int_vector`](#pyfunction-tl-decode-int-vector)
  - [`tl_encode_long_vector`](#tl-encode-long-vector)
  - [`__pyfunction_tl_encode_long_vector`](#pyfunction-tl-encode-long-vector)
  - [`tl_decode_long_vector`](#tl-decode-long-vector)
  - [`__pyfunction_tl_decode_long_vector`](#pyfunction-tl-decode-long-vector)
  - [`read_slice`](#read-slice)
  - [`read_fixed`](#read-fixed)
  - [`encode_tl_bytes`](#encode-tl-bytes)
  - [`decode_tl_bytes`](#decode-tl-bytes)
  - [`py_int_to_le_bytes`](#py-int-to-le-bytes)
  - [`py_int_from_le_bytes`](#py-int-from-le-bytes)
  - [`encode_i32_vector`](#encode-i32-vector)
  - [`decode_i32_vector`](#decode-i32-vector)
  - [`encode_i64_vector`](#encode-i64-vector)
  - [`decode_i64_vector`](#decode-i64-vector)
  - [`decode_vector_layout`](#decode-vector-layout)
  - [`normalize_vector_offset`](#normalize-vector-offset)
  - [`validate_vector_allocation`](#validate-vector-allocation)
  - [`checked_vector_capacity`](#checked-vector-capacity)
- [Constants](#constants)
  - [`TL_VECTOR_CONSTRUCTOR_ID`](#tl-vector-constructor-id)
  - [`MAX_TL_BYTES_LENGTH`](#max-tl-bytes-length)

## Quick Reference

| Item | Kind | Description |
|------|------|-------------|
| [`FastConstructorSpec`](#fastconstructorspec) | struct | Generated metadata for one selected TL constructor fast path. |
| [`FastWireType`](#fastwiretype) | enum | Wire representation supported by the generated fast-constructor codec. |
| [`FastFieldSpec`](#fastfieldspec) | enum | One generated field action used to encode or decode a fast TL constructor. |
| [`register`](#register) | fn | Registers the fallback-compatible `tl_*` Python functions on `miniproto._native`. |
| [`tl_fast_encode`](#tl-fast-encode) | fn | Attempts Python `tl_fast_encode` for a generated constructor. |
| [`__pyfunction_tl_fast_encode`](#pyfunction-tl-fast-encode) | fn |  |
| [`tl_fast_decode`](#tl-fast-decode) | fn | Attempts Python `tl_fast_decode` for a generated constructor at `offset`. |
| [`__pyfunction_tl_fast_decode`](#pyfunction-tl-fast-decode) | fn |  |
| [`encode_fast_value`](#encode-fast-value) | fn | Appends one generated field value to a fast-path TL output buffer. |
| [`decode_fast_value`](#decode-fast-value) | fn | Decodes one generated field from `data`, advancing `cursor` and creating a Python value. |
| [`decode_message_container`](#decode-message-container) | fn | Decodes an MTProto message-container field into a Python tuple of `(id, seq_no, body)` tuples. |
| [`append_tl_bytes`](#append-tl-bytes) | fn | Encodes and appends a bounded TL bytes value, reserving its output atomically. |
| [`decode_tl_bytes_slice`](#decode-tl-bytes-slice) | fn | Borrows one padded TL bytes payload and returns it with its next aligned offset. |
| [`tl_encode_int`](#tl-encode-int) | fn | Encodes Python `tl_encode_int(value)` as a four-byte little-endian signed integer. |
| [`__pyfunction_tl_encode_int`](#pyfunction-tl-encode-int) | fn |  |
| [`tl_decode_int`](#tl-decode-int) | fn | Decodes Python `tl_decode_int(data, offset)` and returns `(value, next_offset)` or `ValueError`. |
| [`__pyfunction_tl_decode_int`](#pyfunction-tl-decode-int) | fn |  |
| [`tl_encode_uint`](#tl-encode-uint) | fn | Encodes Python `tl_encode_uint(value)` as a four-byte little-endian unsigned integer. |
| [`__pyfunction_tl_encode_uint`](#pyfunction-tl-encode-uint) | fn |  |
| [`tl_decode_uint`](#tl-decode-uint) | fn | Decodes Python `tl_decode_uint(data, offset)` and returns `(value, next_offset)` or `ValueError`. |
| [`__pyfunction_tl_decode_uint`](#pyfunction-tl-decode-uint) | fn |  |
| [`tl_encode_long`](#tl-encode-long) | fn | Encodes Python `tl_encode_long(value)` as an eight-byte little-endian signed integer. |
| [`__pyfunction_tl_encode_long`](#pyfunction-tl-encode-long) | fn |  |
| [`tl_decode_long`](#tl-decode-long) | fn | Decodes Python `tl_decode_long(data, offset)` and returns `(value, next_offset)` or `ValueError`. |
| [`__pyfunction_tl_decode_long`](#pyfunction-tl-decode-long) | fn |  |
| [`tl_encode_int128`](#tl-encode-int128) | fn | Encodes Python `tl_encode_int128(value)` to 16 little-endian bytes via `int.to_bytes`. |
| [`__pyfunction_tl_encode_int128`](#pyfunction-tl-encode-int128) | fn |  |
| [`tl_decode_int128`](#tl-decode-int128) | fn | Decodes Python `tl_decode_int128(data, offset)` to a Python integer and next offset. |
| [`__pyfunction_tl_decode_int128`](#pyfunction-tl-decode-int128) | fn |  |
| [`tl_encode_int256`](#tl-encode-int256) | fn | Encodes Python `tl_encode_int256(value)` to 32 little-endian bytes via `int.to_bytes`. |
| [`__pyfunction_tl_encode_int256`](#pyfunction-tl-encode-int256) | fn |  |
| [`tl_decode_int256`](#tl-decode-int256) | fn | Decodes Python `tl_decode_int256(data, offset)` to a Python integer and next offset. |
| [`__pyfunction_tl_decode_int256`](#pyfunction-tl-decode-int256) | fn |  |
| [`tl_encode_double`](#tl-encode-double) | fn | Encodes Python `tl_encode_double(value)` as eight IEEE-754 little-endian bytes. |
| [`__pyfunction_tl_encode_double`](#pyfunction-tl-encode-double) | fn |  |
| [`tl_decode_double`](#tl-decode-double) | fn | Decodes Python `tl_decode_double(data, offset)` and returns `(value, next_offset)` or `ValueError`. |
| [`__pyfunction_tl_decode_double`](#pyfunction-tl-decode-double) | fn |  |
| [`tl_encode_bytes`](#tl-encode-bytes) | fn | Encodes Python `tl_encode_bytes(value)` with TL's short/long length prefix and zero padding. |
| [`__pyfunction_tl_encode_bytes`](#pyfunction-tl-encode-bytes) | fn |  |
| [`tl_decode_bytes`](#tl-decode-bytes) | fn | Decodes Python `tl_decode_bytes(data, offset)` and returns bytes plus the next aligned offset. |
| [`__pyfunction_tl_decode_bytes`](#pyfunction-tl-decode-bytes) | fn |  |
| [`tl_encode_string`](#tl-encode-string) | fn | Encodes Python `tl_encode_string(value)` as UTF-8 TL bytes. |
| [`__pyfunction_tl_encode_string`](#pyfunction-tl-encode-string) | fn |  |
| [`tl_decode_string`](#tl-decode-string) | fn | Decodes Python `tl_decode_string(data, offset)` as UTF-8 and returns it with the next offset. |
| [`__pyfunction_tl_decode_string`](#pyfunction-tl-decode-string) | fn |  |
| [`tl_encode_int_vector`](#tl-encode-int-vector) | fn | Encodes Python `tl_encode_int_vector(values)` as a generic TL vector of 32-bit integers. |
| [`__pyfunction_tl_encode_int_vector`](#pyfunction-tl-encode-int-vector) | fn |  |
| [`tl_decode_int_vector`](#tl-decode-int-vector) | fn | Decodes Python `tl_decode_int_vector(data, offset)` into values and a next offset. |
| [`__pyfunction_tl_decode_int_vector`](#pyfunction-tl-decode-int-vector) | fn |  |
| [`tl_encode_long_vector`](#tl-encode-long-vector) | fn | Encodes Python `tl_encode_long_vector(values)` as a generic TL vector of 64-bit integers. |
| [`__pyfunction_tl_encode_long_vector`](#pyfunction-tl-encode-long-vector) | fn |  |
| [`tl_decode_long_vector`](#tl-decode-long-vector) | fn | Decodes Python `tl_decode_long_vector(data, offset)` into values and a next offset. |
| [`__pyfunction_tl_decode_long_vector`](#pyfunction-tl-decode-long-vector) | fn |  |
| [`read_slice`](#read-slice) | fn | Borrows `length` bytes at `offset` from a TL buffer. |
| [`read_fixed`](#read-fixed) | fn | Reads an exactly `N`-byte TL field at `offset`. |
| [`encode_tl_bytes`](#encode-tl-bytes) | fn | Serializes bytes with the TL short/long length prefix and zero alignment padding. |
| [`decode_tl_bytes`](#decode-tl-bytes) | fn | Parses and copies one padded TL bytes value, returning it and its next aligned offset. |
| [`py_int_to_le_bytes`](#py-int-to-le-bytes) | fn | Calls Python `int.to_bytes(width, "little")` for fixed-width unsigned TL integer fields. |
| [`py_int_from_le_bytes`](#py-int-from-le-bytes) | fn | Calls Python `int.from_bytes(bytes, "little")` while holding the supplied GIL token. |
| [`encode_i32_vector`](#encode-i32-vector) | fn | Serializes signed 32-bit values as a generic boxed TL vector. |
| [`decode_i32_vector`](#decode-i32-vector) | fn | Decodes a generic TL vector of signed 32-bit values at `offset`. |
| [`encode_i64_vector`](#encode-i64-vector) | fn | Serializes signed 64-bit values as a generic boxed TL vector. |
| [`decode_i64_vector`](#decode-i64-vector) | fn | Decodes a generic TL vector of signed 64-bit values at `offset`. |
| [`decode_vector_layout`](#decode-vector-layout) | fn | Validates a generic vector header and returns its count, payload start, and next offset. |
| [`normalize_vector_offset`](#normalize-vector-offset) | fn | Converts the Python-facing signed offset to a safe Rust index. |
| [`validate_vector_allocation`](#validate-vector-allocation) | fn | Checks that a decoded vector's requested allocation fits the platform's `isize` limit. |
| [`checked_vector_capacity`](#checked-vector-capacity) | fn | Computes encoder capacity including the eight-byte TL vector header. |
| [`TL_VECTOR_CONSTRUCTOR_ID`](#tl-vector-constructor-id) | const | Constructor identifier serialized before every generic TL `Vector`. |
| [`MAX_TL_BYTES_LENGTH`](#max-tl-bytes-length) | const | Largest byte-string payload representable by TL's three-byte long length prefix. |

## Structs

### `FastConstructorSpec`

```rust
struct FastConstructorSpec {
    constructor_id: u32,
    name: &'static str,
    encode: bool,
    decode: bool,
    value_count: usize,
    fields: &'static [FastFieldSpec],
}
```

*Defined in `rust/miniproto/src/tl.rs:80-93`*

Generated metadata for one selected TL constructor fast path.

#### Fields

- **`constructor_id`**: `u32`

  Constructor id serialized for boxed values.

- **`name`**: `&'static str`

  Generated schema name used in validation errors.

- **`encode`**: `bool`

  Whether this constructor has a native encoder.

- **`decode`**: `bool`

  Whether this constructor has a native decoder.

- **`value_count`**: `usize`

  Exact number of Python tuple values expected by the fast path.

- **`fields`**: `&'static [FastFieldSpec]`

  Ordered generated field descriptors.

#### Trait Implementations

##### `impl Same for FastConstructorSpec`

- <span id="fastconstructorspec-same-type-output"></span>`type Output = T`

##### `impl Ungil for FastConstructorSpec`

## Enums

### `FastWireType`

```rust
enum FastWireType {
    Int,
    Long,
    UInt64,
    Bytes,
    String,
    VectorLong,
    Object,
    EmptyObject,
    Raw,
    MessageContainer,
}
```

*Defined in `rust/miniproto/src/tl.rs:30-51`*

Wire representation supported by the generated fast-constructor codec.

#### Variants

- **`Int`**

  Signed 32-bit little-endian integer.

- **`Long`**

  Signed 64-bit little-endian integer.

- **`UInt64`**

  Unsigned 64-bit little-endian integer.

- **`Bytes`**

  TL length-prefixed bytes.

- **`String`**

  UTF-8 TL length-prefixed bytes.

- **`VectorLong`**

  A generic TL vector of signed 64-bit integers.

- **`Object`**

  A generated object field supported only while encoding.

- **`EmptyObject`**

  A constructor id represented by an otherwise fieldless object.

- **`Raw`**

  The complete remaining wire suffix.

- **`MessageContainer`**

  MTProto's message-container sequence.

#### Trait Implementations

##### `impl Clone for FastWireType`

- <span id="fastwiretype-clone"></span>`fn clone(&self) -> FastWireType` — [`FastWireType`](#fastwiretype)

##### `impl Copy for FastWireType`

##### `impl Same for FastWireType`

- <span id="fastwiretype-same-type-output"></span>`type Output = T`

##### `impl Ungil for FastWireType`

### `FastFieldSpec`

```rust
enum FastFieldSpec {
    Flags {
        group: usize,
    },
    True {
        value: usize,
        group: usize,
        bit: u32,
    },
    Value {
        value: usize,
        wire_type: FastWireType,
    },
}
```

*Defined in `rust/miniproto/src/tl.rs:55-77`*

One generated field action used to encode or decode a fast TL constructor.

#### Variants

- **`Flags`**

  Reads or writes one flags word in the specified flags group.

- **`True`**

  Maps a generated boolean value to one bit in a flags word.

- **`Value`**

  Maps a Python tuple value to a non-flag wire representation.

#### Trait Implementations

##### `impl Clone for FastFieldSpec`

- <span id="fastfieldspec-clone"></span>`fn clone(&self) -> FastFieldSpec` — [`FastFieldSpec`](#fastfieldspec)

##### `impl Copy for FastFieldSpec`

##### `impl Same for FastFieldSpec`

- <span id="fastfieldspec-same-type-output"></span>`type Output = T`

##### `impl Ungil for FastFieldSpec`

## Functions

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/tl.rs:102-126`*

Registers the fallback-compatible `tl_*` Python functions on `miniproto._native`.

Returns a PyO3 error if any function cannot be exported.

# Arguments

- `m`: The Python extension module receiving the TL callables.

### `tl_fast_encode`

```rust
fn tl_fast_encode(constructor_id: u32, values: &Bound<'_, pyo3::types::PyTuple>, boxed: bool) -> PyResult<Option<Vec<u8>>>
```

*Defined in `rust/miniproto/src/tl.rs:143-191`*

Attempts Python `tl_fast_encode` for a generated constructor.

`values` must have the generated constructor's exact tuple arity; `boxed` controls whether the
constructor id is emitted. Returns `None` if no native encoder exists, encoded bytes on
success, or a Python exception for incompatible values or generated metadata. PyO3 conversion
failures from tuple lookup/extraction propagate as `TypeError`, `OverflowError`, or the source
Python exception; algorithm and descriptor validation failures intentionally use `ValueError`.

# Arguments

- `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
- `values`: Python tuple whose exact arity and value types must match that descriptor.
- `boxed`: Whether to serialize the constructor id before its fields.

### `__pyfunction_tl_fast_encode`

```rust
unsafe fn __pyfunction_tl_fast_encode<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:141`*

### `tl_fast_decode`

```rust
fn tl_fast_decode(py: Python<'_>, constructor_id: u32, data: &[u8], offset: usize, boxed: bool) -> PyResult<Option<(Py<pyo3::types::PyTuple>, usize)>>
```

*Defined in `rust/miniproto/src/tl.rs:210-266`*

Attempts Python `tl_fast_decode` for a generated constructor at `offset`.

`boxed` requires and verifies the constructor id. Returns `None` if no native decoder exists,
otherwise `(values_tuple, next_offset)`; malformed wire input raises a Python exception. This
conversion necessarily holds the GIL to create Python objects. PyO3 conversion errors are
propagated unchanged, whereas malformed TL bytes use `ValueError`. Descriptor indices and flag
bits come from trusted generated metadata and are not revalidated on every hot-path call.

# Arguments

- `py`: The acquired GIL token used to construct decoded Python values.
- `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
- `data`: TL wire bytes to decode.
- `offset`: Byte offset at which this constructor begins.
- `boxed`: Whether `data` starts with and must match the constructor id.

### `__pyfunction_tl_fast_decode`

```rust
unsafe fn __pyfunction_tl_fast_decode<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:208`*

### `encode_fast_value`

```rust
fn encode_fast_value(output: &mut Vec<u8>, value: &Bound<'_, PyAny>, wire_type: FastWireType) -> PyResult<()>
```

*Defined in `rust/miniproto/src/tl.rs:278-312`*

Appends one generated field value to a fast-path TL output buffer.

Returns a Python exception for incompatible Python values, unrepresentable sizes, or an
encode-only generated object mismatch.

# Arguments

- `output`: Destination buffer receiving the encoded field.
- `value`: Python value to convert according to `wire_type`.
- `wire_type`: Trusted generated representation directive for `value`.

### `decode_fast_value`

```rust
fn decode_fast_value(py: Python<'_>, data: &[u8], cursor: &mut usize, wire_type: FastWireType) -> PyResult<Py<PyAny>>
```

*Defined in `rust/miniproto/src/tl.rs:325-380`*

Decodes one generated field from `data`, advancing `cursor` and creating a Python value.

Returns a Python exception for malformed data or unsupported generated decode types; requires
the GIL through `py` because the result is a Python object.

# Arguments

- `py`: The acquired GIL token used to create the decoded Python value.
- `data`: Complete TL input buffer.
- `cursor`: Mutable offset advanced past the decoded field.
- `wire_type`: Trusted generated representation directive for the field.

### `decode_message_container`

```rust
fn decode_message_container(py: Python<'_>, data: &[u8], cursor: &mut usize) -> PyResult<Py<PyAny>>
```

*Defined in `rust/miniproto/src/tl.rs:392-442`*

Decodes an MTProto message-container field into a Python tuple of `(id, seq_no, body)` tuples.

Advances `cursor` and returns Python exceptions for truncated, negative, oversized, or
unallocatable container contents.

# Arguments

- `py`: The acquired GIL token used to create the result tuple and bytes objects.
- `data`: Complete TL input buffer containing the container.
- `cursor`: Mutable offset advanced past every decoded member.

### `append_tl_bytes`

```rust
fn append_tl_bytes(output: &mut Vec<u8>, value: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/tl.rs:452-464`*

Encodes and appends a bounded TL bytes value, reserving its output atomically.

Returns `ValueError` above TL's 24-bit limit or `MemoryError` on allocation failure.

# Arguments

- `output`: Destination buffer receiving the encoded TL bytes field.
- `value`: Raw bytes to prefix and pad.

### `decode_tl_bytes_slice`

```rust
fn decode_tl_bytes_slice(data: &[u8], offset: usize) -> PyResult<(&[u8], usize)>
```

*Defined in `rust/miniproto/src/tl.rs:474-496`*

Borrows one padded TL bytes payload and returns it with its next aligned offset.

Returns `ValueError` if the length prefix, payload, padding, or offset is malformed.

# Arguments

- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the TL bytes length prefix starts.

### `tl_encode_int`

```rust
fn tl_encode_int(value: i32) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:504-506`*

Encodes Python `tl_encode_int(value)` as a four-byte little-endian signed integer.

# Arguments

- `value`: Signed 32-bit integer to serialize.

### `__pyfunction_tl_encode_int`

```rust
unsafe fn __pyfunction_tl_encode_int<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:503`*

### `tl_decode_int`

```rust
fn tl_decode_int(data: &[u8], offset: usize) -> PyResult<(i32, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:515-518`*

Decodes Python `tl_decode_int(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing a four-byte signed integer.
- `offset`: Byte offset at which the integer starts.

### `__pyfunction_tl_decode_int`

```rust
unsafe fn __pyfunction_tl_decode_int<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:514`*

### `tl_encode_uint`

```rust
fn tl_encode_uint(value: u32) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:526-528`*

Encodes Python `tl_encode_uint(value)` as a four-byte little-endian unsigned integer.

# Arguments

- `value`: Unsigned 32-bit integer to serialize.

### `__pyfunction_tl_encode_uint`

```rust
unsafe fn __pyfunction_tl_encode_uint<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:525`*

### `tl_decode_uint`

```rust
fn tl_decode_uint(data: &[u8], offset: usize) -> PyResult<(u32, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:537-540`*

Decodes Python `tl_decode_uint(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing a four-byte unsigned integer.
- `offset`: Byte offset at which the integer starts.

### `__pyfunction_tl_decode_uint`

```rust
unsafe fn __pyfunction_tl_decode_uint<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:536`*

### `tl_encode_long`

```rust
fn tl_encode_long(value: i64) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:548-550`*

Encodes Python `tl_encode_long(value)` as an eight-byte little-endian signed integer.

# Arguments

- `value`: Signed 64-bit integer to serialize.

### `__pyfunction_tl_encode_long`

```rust
unsafe fn __pyfunction_tl_encode_long<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:547`*

### `tl_decode_long`

```rust
fn tl_decode_long(data: &[u8], offset: usize) -> PyResult<(i64, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:559-562`*

Decodes Python `tl_decode_long(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing an eight-byte signed integer.
- `offset`: Byte offset at which the integer starts.

### `__pyfunction_tl_decode_long`

```rust
unsafe fn __pyfunction_tl_decode_long<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:558`*

### `tl_encode_int128`

```rust
fn tl_encode_int128(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:572-574`*

Encodes Python `tl_encode_int128(value)` to 16 little-endian bytes via `int.to_bytes`.

Python raises if `value` cannot fit the requested unsigned representation.

# Arguments

- `value`: Python integer to convert to exactly 16 little-endian bytes.

### `__pyfunction_tl_encode_int128`

```rust
unsafe fn __pyfunction_tl_encode_int128<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:571`*

### `tl_decode_int128`

```rust
fn tl_decode_int128(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:586-589`*

Decodes Python `tl_decode_int128(data, offset)` to a Python integer and next offset.

Returns `ValueError` for truncated input and holds the GIL to construct the Python integer.

# Arguments

- `py`: The acquired GIL token used to construct the Python integer.
- `data`: TL bytes containing a 16-byte integer field.
- `offset`: Byte offset at which the fixed-width field starts.

### `__pyfunction_tl_decode_int128`

```rust
unsafe fn __pyfunction_tl_decode_int128<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:585`*

### `tl_encode_int256`

```rust
fn tl_encode_int256(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:599-601`*

Encodes Python `tl_encode_int256(value)` to 32 little-endian bytes via `int.to_bytes`.

Python raises if `value` cannot fit the requested unsigned representation.

# Arguments

- `value`: Python integer to convert to exactly 32 little-endian bytes.

### `__pyfunction_tl_encode_int256`

```rust
unsafe fn __pyfunction_tl_encode_int256<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:598`*

### `tl_decode_int256`

```rust
fn tl_decode_int256(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:613-616`*

Decodes Python `tl_decode_int256(data, offset)` to a Python integer and next offset.

Returns `ValueError` for truncated input and holds the GIL to construct the Python integer.

# Arguments

- `py`: The acquired GIL token used to construct the Python integer.
- `data`: TL bytes containing a 32-byte integer field.
- `offset`: Byte offset at which the fixed-width field starts.

### `__pyfunction_tl_decode_int256`

```rust
unsafe fn __pyfunction_tl_decode_int256<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:612`*

### `tl_encode_double`

```rust
fn tl_encode_double(value: f64) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:624-626`*

Encodes Python `tl_encode_double(value)` as eight IEEE-754 little-endian bytes.

# Arguments

- `value`: Double-precision value to serialize.

### `__pyfunction_tl_encode_double`

```rust
unsafe fn __pyfunction_tl_encode_double<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:623`*

### `tl_decode_double`

```rust
fn tl_decode_double(data: &[u8], offset: usize) -> PyResult<(f64, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:635-638`*

Decodes Python `tl_decode_double(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing an eight-byte double.
- `offset`: Byte offset at which the double starts.

### `__pyfunction_tl_decode_double`

```rust
unsafe fn __pyfunction_tl_decode_double<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:634`*

### `tl_encode_bytes`

```rust
fn tl_encode_bytes(value: &[u8]) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:646-648`*

Encodes Python `tl_encode_bytes(value)` with TL's short/long length prefix and zero padding.

# Arguments

- `value`: Bytes to prefix and pad according to TL rules.

### `__pyfunction_tl_encode_bytes`

```rust
unsafe fn __pyfunction_tl_encode_bytes<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:645`*

### `tl_decode_bytes`

```rust
fn tl_decode_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:659-661`*

Decodes Python `tl_decode_bytes(data, offset)` and returns bytes plus the next aligned offset.

Returns `ValueError` for malformed or truncated TL data.

# Arguments

- `data`: TL bytes containing one length-prefixed byte field.
- `offset`: Byte offset at which the field starts.

### `__pyfunction_tl_decode_bytes`

```rust
unsafe fn __pyfunction_tl_decode_bytes<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:658`*

### `tl_encode_string`

```rust
fn tl_encode_string(value: &str) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:669-671`*

Encodes Python `tl_encode_string(value)` as UTF-8 TL bytes.

# Arguments

- `value`: UTF-8 Rust string to encode as TL bytes.

### `__pyfunction_tl_encode_string`

```rust
unsafe fn __pyfunction_tl_encode_string<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:668`*

### `tl_decode_string`

```rust
fn tl_decode_string(data: &[u8], offset: usize) -> PyResult<(String, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:682-687`*

Decodes Python `tl_decode_string(data, offset)` as UTF-8 and returns it with the next offset.

Returns `ValueError` for malformed TL data or non-UTF-8 payload bytes.

# Arguments

- `data`: TL bytes containing one length-prefixed string field.
- `offset`: Byte offset at which the field starts.

### `__pyfunction_tl_decode_string`

```rust
unsafe fn __pyfunction_tl_decode_string<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:681`*

### `tl_encode_int_vector`

```rust
fn tl_encode_int_vector(py: Python<'_>, values: Vec<i32>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:698-701`*

Encodes Python `tl_encode_int_vector(values)` as a generic TL vector of 32-bit integers.

Large vector encoding releases the GIL; invalid size or allocation raises a Python exception.

# Arguments

- `py`: The acquired GIL token used to detach large vector encoding.
- `values`: Signed 32-bit values to serialize.

### `__pyfunction_tl_encode_int_vector`

```rust
unsafe fn __pyfunction_tl_encode_int_vector<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:697`*

### `tl_decode_int_vector`

```rust
fn tl_decode_int_vector(py: Python<'_>, data: Vec<u8>, offset: i128) -> PyResult<(Vec<i32>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:714-722`*

Decodes Python `tl_decode_int_vector(data, offset)` into values and a next offset.

The signed Python offset must fit `usize`; large decoding releases the GIL and malformed input
returns a Python exception.

# Arguments

- `py`: The acquired GIL token used to detach large vector decoding.
- `data`: TL bytes containing a generic integer vector.
- `offset`: Python-facing signed byte offset that must convert to `usize`.

### `__pyfunction_tl_decode_int_vector`

```rust
unsafe fn __pyfunction_tl_decode_int_vector<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:713`*

### `tl_encode_long_vector`

```rust
fn tl_encode_long_vector(py: Python<'_>, values: Vec<i64>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:733-736`*

Encodes Python `tl_encode_long_vector(values)` as a generic TL vector of 64-bit integers.

Large vector encoding releases the GIL; invalid size or allocation raises a Python exception.

# Arguments

- `py`: The acquired GIL token used to detach large vector encoding.
- `values`: Signed 64-bit values to serialize.

### `__pyfunction_tl_encode_long_vector`

```rust
unsafe fn __pyfunction_tl_encode_long_vector<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:732`*

### `tl_decode_long_vector`

```rust
fn tl_decode_long_vector(py: Python<'_>, data: Vec<u8>, offset: i128) -> PyResult<(Vec<i64>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:749-757`*

Decodes Python `tl_decode_long_vector(data, offset)` into values and a next offset.

The signed Python offset must fit `usize`; large decoding releases the GIL and malformed input
returns a Python exception.

# Arguments

- `py`: The acquired GIL token used to detach large vector decoding.
- `data`: TL bytes containing a generic long vector.
- `offset`: Python-facing signed byte offset that must convert to `usize`.

### `__pyfunction_tl_decode_long_vector`

```rust
unsafe fn __pyfunction_tl_decode_long_vector<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/tl.rs:748`*

### `read_slice`

```rust
fn read_slice(data: &[u8], offset: usize, length: usize) -> PyResult<&[u8]>
```

*Defined in `rust/miniproto/src/tl.rs:768-773`*

Borrows `length` bytes at `offset` from a TL buffer.

Returns `ValueError` rather than panicking if the requested range is not present.

# Arguments

- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the requested range begins.
- `length`: Number of bytes to borrow.

### `read_fixed`

```rust
fn read_fixed<const N: usize>(data: &[u8], offset: usize) -> PyResult<[u8; N]>
```

*Defined in `rust/miniproto/src/tl.rs:785-787`*

Reads an exactly `N`-byte TL field at `offset`.

Returns `ValueError` for a truncated buffer; its `expect` is safe after `read_slice` verified
the length.

# Arguments

- `N`: Compile-time fixed width required by the caller.
- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the fixed-width field begins.

### `encode_tl_bytes`

```rust
fn encode_tl_bytes(value: &[u8]) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:796-810`*

Serializes bytes with the TL short/long length prefix and zero alignment padding.

This internal helper assumes the caller has enforced TL's 24-bit long-length maximum.

# Arguments

- `value`: Bytes to length-prefix and pad to a four-byte boundary.

### `decode_tl_bytes`

```rust
fn decode_tl_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:820-841`*

Parses and copies one padded TL bytes value, returning it and its next aligned offset.

Returns `ValueError` for missing length, payload, or padding bytes.

# Arguments

- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the bytes field starts.

### `py_int_to_le_bytes`

```rust
fn py_int_to_le_bytes(value: &Bound<'_, PyAny>, width: usize) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:851-859`*

Calls Python `int.to_bytes(width, "little")` for fixed-width unsigned TL integer fields.

Propagates Python conversion exceptions and returns `ValueError` for an unexpected width.

# Arguments

- `value`: Python integer exposing `to_bytes`.
- `width`: Required serialized width in bytes.

### `py_int_from_le_bytes`

```rust
fn py_int_from_le_bytes(py: Python<'_>, bytes: &[u8]) -> PyResult<Py<PyAny>>
```

*Defined in `rust/miniproto/src/tl.rs:869-876`*

Calls Python `int.from_bytes(bytes, "little")` while holding the supplied GIL token.

Returns any exception raised while importing or invoking Python builtins.

# Arguments

- `py`: The acquired GIL token used to import and invoke Python builtins.
- `bytes`: Little-endian bytes to pass to `int.from_bytes`.

### `encode_i32_vector`

```rust
fn encode_i32_vector(values: &[i32]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:885-897`*

Serializes signed 32-bit values as a generic boxed TL vector.

Returns `ValueError` for an unrepresentable count or `MemoryError` on allocation failure.

# Arguments

- `values`: Signed 32-bit vector elements to serialize.

### `decode_i32_vector`

```rust
fn decode_i32_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i32>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:907-920`*

Decodes a generic TL vector of signed 32-bit values at `offset`.

Returns values with the next offset, or Python errors for malformed sizes or allocation failure.

# Arguments

- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the generic vector begins.

### `encode_i64_vector`

```rust
fn encode_i64_vector(values: &[i64]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:929-941`*

Serializes signed 64-bit values as a generic boxed TL vector.

Returns `ValueError` for an unrepresentable count or `MemoryError` on allocation failure.

# Arguments

- `values`: Signed 64-bit vector elements to serialize.

### `decode_i64_vector`

```rust
fn decode_i64_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i64>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:951-964`*

Decodes a generic TL vector of signed 64-bit values at `offset`.

Returns values with the next offset, or Python errors for malformed sizes or allocation failure.

# Arguments

- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the generic vector begins.

### `decode_vector_layout`

```rust
fn decode_vector_layout(data: &[u8], offset: usize, element_width: usize) -> PyResult<(usize, usize, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:979-1014`*

Validates a generic vector header and returns its count, payload start, and next offset.

Returns `ValueError` for a wrong constructor, negative/excessive count, or arithmetic overflow.
The subtraction used to calculate remaining bytes cannot underflow: the preceding checked
header slice exists only when `payload_offset <= data.len()`. This function has no panic path
for externally supplied `data`; its `expect` calls follow exact-width checked slices.

# Arguments

- `data`: Complete TL input buffer.
- `offset`: Byte offset at which the vector constructor id starts.
- `element_width`: Nonzero byte width of one decoded element; callers use 4 or 8. A zero width
  would panic in the remaining-bytes division and is therefore an internal precondition.

### `normalize_vector_offset`

```rust
fn normalize_vector_offset(offset: i128) -> PyResult<usize>
```

*Defined in `rust/miniproto/src/tl.rs:1023-1027`*

Converts the Python-facing signed offset to a safe Rust index.

Returns `ValueError` for negative or unrepresentable offsets.

# Arguments

- `offset`: Python-facing signed byte offset to convert.

### `validate_vector_allocation`

```rust
fn validate_vector_allocation(count: usize, element_width: usize) -> PyResult<()>
```

*Defined in `rust/miniproto/src/tl.rs:1037-1045`*

Checks that a decoded vector's requested allocation fits the platform's `isize` limit.

Returns `ValueError` before allocation on overflow or an excessive capacity.

# Arguments

- `count`: Number of vector elements requested by decoded wire data.
- `element_width`: Byte width of one element used for capacity calculation.

### `checked_vector_capacity`

```rust
fn checked_vector_capacity(count: usize, element_width: usize) -> PyResult<usize>
```

*Defined in `rust/miniproto/src/tl.rs:1055-1067`*

Computes encoder capacity including the eight-byte TL vector header.

Returns `ValueError` when the count cannot fit signed TL `int` or the capacity is excessive.

# Arguments

- `count`: Number of vector elements to encode.
- `element_width`: Byte width of one serialized element.

## Constants

### `TL_VECTOR_CONSTRUCTOR_ID`
```rust
const TL_VECTOR_CONSTRUCTOR_ID: u32 = 481_674_261u32;
```

*Defined in `rust/miniproto/src/tl.rs:24`*

Constructor identifier serialized before every generic TL `Vector`.

### `MAX_TL_BYTES_LENGTH`
```rust
const MAX_TL_BYTES_LENGTH: usize = 16_777_215usize;
```

*Defined in `rust/miniproto/src/tl.rs:26`*

Largest byte-string payload representable by TL's three-byte long length prefix.

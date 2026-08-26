---
title: "miniproto_native::transport"
description: "Registers TCP transport framing callables and the stateful codec class."
generated: true
editUrl: false
language: "rust"
kind: "module"
qualified_name: "miniproto_native::transport"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L1"
python_visible: false
---

## Provenance

- Rust visibility: `crate`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L1)
- Python exposure: Not evidenced by static PyO3 attributes.

## Documented items

- [`miniproto_native::transport::register`](./register/)
- [`miniproto_native::transport::quick_ack_token`](./quick-ack-token/)
- [`miniproto_native::transport::TransportCodec`](./transportcodec/)

## cargo-docs-md rendering

*miniproto_native / [transport](index.md)*

---

# Module `transport`

Registers TCP transport framing callables and the stateful codec class.
Stateful native codecs for Telegram TCP abridged, intermediate and padded-intermediate frames.

`TransportCodec` is exported to Python as `miniproto._native.TransportCodec` and mirrors the
Python fallback's framing contract.  It accepts arbitrary receive fragmentation, emits payload,
quick-ACK and transport-error events and returns Python exceptions for malformed or oversized
data rather than panicking. `FramePump` itself is Python-independent, but the PyO3 methods in
this module currently do not detach regular parsing or encoding work from the GIL; the GIL is
also required while their results are converted to Python objects.
Incompatible Python inputs retain PyO3's `TypeError`, `OverflowError` or source conversion
exception; framing validation that runs after conversion intentionally returns `ValueError`.

## Contents

- [Structs](#structs)
  - [`TransportCodec`](#transportcodec)
  - [`FramePump`](#framepump)
- [Enums](#enums)
  - [`TransportMode`](#transportmode)
  - [`FrameEvent`](#frameevent)
- [Functions](#functions)
  - [`register`](#register)
  - [`quick_ack_token`](#quick-ack-token)
  - [`__pyfunction_quick_ack_token`](#pyfunction-quick-ack-token)
  - [`quick_ack_token_raw`](#quick-ack-token-raw)
  - [`encode_length_prefixed`](#encode-length-prefixed)
  - [`padded_packet_length`](#padded-packet-length)
  - [`to_fixed`](#to-fixed)
- [Type Aliases](#type-aliases)
  - [`PythonFrameEvent`](#pythonframeevent)
- [Constants](#constants)
  - [`ABRIDGED_LONG_MARKER`](#abridged-long-marker)
  - [`QUICK_ACK_MASK`](#quick-ack-mask)
  - [`PADDED_QUICK_ACK_MARKER`](#padded-quick-ack-marker)
  - [`MAX_TRANSPORT_PADDING`](#max-transport-padding)
  - [`RETAINED_BUFFER_LIMIT`](#retained-buffer-limit)

## Quick Reference

| Item | Kind | Description |
|------|------|-------------|
| [`TransportCodec`](#transportcodec) | struct | Python-visible incremental TCP framing codec, exported as `miniproto._native.TransportCodec`. |
| [`FramePump`](#framepump) | struct | GIL-free incremental parser/encoder retaining incomplete receive data between calls. |
| [`TransportMode`](#transportmode) | enum | Supported Telegram TCP framing modes selected by their Python wire-name strings. |
| [`FrameEvent`](#frameevent) | enum | One native frame-pump result before it is converted to a Python return shape. |
| [`register`](#register) | fn | Registers Python `TransportCodec` and `quick_ack_token` on `miniproto._native`. |
| [`quick_ack_token`](#quick-ack-token) | fn | Computes the flagged quick-ACK token for Python `quick_ack_token`. |
| [`__pyfunction_quick_ack_token`](#pyfunction-quick-ack-token) | fn |  |
| [`quick_ack_token_raw`](#quick-ack-token-raw) | fn | Computes a quick-ACK token without Python argument conversion or GIL interaction. |
| [`encode_length_prefixed`](#encode-length-prefixed) | fn | Encodes a four-byte little-endian length prefix and payload, optionally setting quick-ACK bit. |
| [`padded_packet_length`](#padded-packet-length) | fn | Determines the embedded MTProto packet length within a padded-intermediate payload. |
| [`to_fixed`](#to-fixed) | fn | Converts a slice to an exact fixed-width array for frame header decoding. |
| [`PythonFrameEvent`](#pythonframeevent) | type | Python `feed_data` event tuple: kind, payload, numeric detail, quick-ACK request flag. |
| [`ABRIDGED_LONG_MARKER`](#abridged-long-marker) | const | Abridged header byte that introduces its three-byte word-length form. |
| [`QUICK_ACK_MASK`](#quick-ack-mask) | const | Wire bit that asks the peer to return a quick-ACK token. |
| [`PADDED_QUICK_ACK_MARKER`](#padded-quick-ack-marker) | const | Padded-intermediate payload marker identifying a quick-ACK response. |
| [`MAX_TRANSPORT_PADDING`](#max-transport-padding) | const | Maximum random padding bytes allowed by padded-intermediate TCP framing. |
| [`RETAINED_BUFFER_LIMIT`](#retained-buffer-limit) | const | Largest drained receive-buffer allocation retained for later chunks. |

## Structs

### `TransportCodec`

```rust
struct TransportCodec {
    pump: FramePump,
}
```

*Defined in `rust/miniproto/src/transport.rs:139-142`*

Python-visible incremental TCP framing codec, exported as `miniproto._native.TransportCodec`.

#### Fields

- **`pump`**: `FramePump`

  Stateful native parser and encoder backing this Python object.

#### Implementations

- <span id="transportcodec-new"></span>`fn new(mode: &str, max_payload_size: usize, server_side: bool) -> PyResult<Self>`

  Creates `TransportCodec(mode, max_payload_size, server_side=False)`.

  

  `mode` must be a supported Python transport name and `max_payload_size` must be positive;

  otherwise this constructor raises `ValueError`.

  

  # Arguments

  

  - `mode`: One of the supported Python TCP mode names.

  - `max_payload_size`: Positive upper bound for decoded application payload bytes.

  - `server_side`: Whether inbound quick-ACK request bits remain payload metadata instead of

    being interpreted as quick-ACK response frames.

- <span id="transportcodec-encode-packet"></span>`fn encode_packet(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>>`

  Encodes Python `encode_packet(payload, quick_ack=False)` into a single TCP frame.

  

  Returns `ValueError` for oversized payloads, invalid abridged alignment, length overflow,

  or operating-system randomness failure in padded mode.

  

  # Arguments

  

  - `payload`: Complete MTProto payload to frame.

  - `quick_ack`: Whether to set the outbound quick-ACK request bit where the mode supports it.

- <span id="transportcodec-feed-data"></span>`fn feed_data(&mut self, data: &[u8]) -> PyResult<Vec<(u8, Vec<u8>, i64, bool)>>`

  Feeds Python `feed_data(data)` and returns tagged native event tuples.

  

  Tuple kinds are `0` payload, `1` quick ACK and `2` negative transport error. It preserves

  incomplete trailing bytes for the next call and raises Python errors for invalid framing.

  

  # Arguments

  

  - `data`: Newly received TCP bytes to append to this codec's buffered stream.

- <span id="transportcodec-feed-transport-data"></span>`fn feed_transport_data(&mut self, py: Python<'_>, data: &[u8]) -> PyResult<Vec<Py<PyAny>>>`

  Feeds compatibility `feed_transport_data(data)` and returns bytes or integer Python events.

  

  The GIL token is used only for object conversion after native parsing; malformed framing

  returns a Python exception.

  

  # Arguments

  

  - `py`: The acquired GIL token used to build Python `bytes` and integer events.

  - `data`: Newly received TCP bytes to append to this codec's buffered stream.

#### Trait Implementations

##### `impl DerefToPyAny for TransportCodec`

##### `impl ExtractPyClassWithClone for TransportCodec`

##### `impl IntoPyObject for TransportCodec`

- <span id="transportcodec-intopyobject-type-target"></span>`type Target = TransportCodec`

- <span id="transportcodec-intopyobject-type-output"></span>`type Output = Bound<'py, <TransportCodec as IntoPyObject>::Target>`

- <span id="transportcodec-intopyobject-type-error"></span>`type Error = PyErr`

- <span id="transportcodec-intopyobject-into-pyobject"></span>`fn into_pyobject(self, py: ::pyo3::Python<'py>) -> ::std::result::Result<<Self as ::pyo3::conversion::IntoPyObject>::Output, <Self as ::pyo3::conversion::IntoPyObject>::Error>`

##### `impl IntoPyObjectExt for TransportCodec`

##### `impl PyClass for TransportCodec`

- <span id="transportcodec-pyclass-const-name"></span>`const NAME: &str`

- <span id="transportcodec-pyclass-type-frozen"></span>`type Frozen = False`

##### `impl PyClassImpl for TransportCodec`

- <span id="transportcodec-pyclassimpl-const-module"></span>`const MODULE: ::std::option::Option<&str>`

- <span id="transportcodec-pyclassimpl-const-is-basetype"></span>`const IS_BASETYPE: bool`

- <span id="transportcodec-pyclassimpl-const-is-subclass"></span>`const IS_SUBCLASS: bool`

- <span id="transportcodec-pyclassimpl-const-is-mapping"></span>`const IS_MAPPING: bool`

- <span id="transportcodec-pyclassimpl-const-is-sequence"></span>`const IS_SEQUENCE: bool`

- <span id="transportcodec-pyclassimpl-const-is-immutable-type"></span>`const IS_IMMUTABLE_TYPE: bool`

- <span id="transportcodec-pyclassimpl-type-layout"></span>`type Layout = <<TransportCodec as PyClassImpl>::BaseNativeType as PyClassBaseType>::Layout`

- <span id="transportcodec-pyclassimpl-type-basetype"></span>`type BaseType = PyAny`

- <span id="transportcodec-pyclassimpl-type-threadchecker"></span>`type ThreadChecker = NoopThreadChecker`

- <span id="transportcodec-pyclassimpl-type-pyclassmutability"></span>`type PyClassMutability = <<PyAny as PyClassBaseType>::PyClassMutability as PyClassMutability>::MutableChild`

- <span id="transportcodec-pyclassimpl-type-dict"></span>`type Dict = PyClassDummySlot`

- <span id="transportcodec-pyclassimpl-type-weakref"></span>`type WeakRef = PyClassDummySlot`

- <span id="transportcodec-pyclassimpl-type-basenativetype"></span>`type BaseNativeType = PyAny`

- <span id="transportcodec-pyclassimpl-items-iter"></span>`fn items_iter() -> ::pyo3::impl_::pyclass::PyClassItemsIter`

- <span id="transportcodec-pyclassimpl-const-raw-doc"></span>`const RAW_DOC: &'static ::std::ffi::CStr`

- <span id="transportcodec-pyclassimpl-const-doc"></span>`const DOC: &'static ::std::ffi::CStr`

- <span id="transportcodec-pyclassimpl-lazy-type-object"></span>`fn lazy_type_object() -> &'static ::pyo3::impl_::pyclass::LazyTypeObject<Self>`

##### `impl PyClassNewTextSignature for TransportCodec`

- <span id="transportcodec-pyclassnewtextsignature-const-text-signature"></span>`const TEXT_SIGNATURE: &'static str`

##### `impl PyErrArguments for TransportCodec`

- <span id="transportcodec-pyerrarguments-arguments"></span>`fn arguments(self, py: Python<'_>) -> Py<PyAny>`

##### `impl PyMethods for ::pyo3::impl_::pyclass::PyClassImplCollector<TransportCodec>`

- <span id="pyo3impl-pyclasspyclassimplcollector-pymethods-py-methods"></span>`fn py_methods(self) -> &'static ::pyo3::impl_::pyclass::PyClassItems`

##### `impl PyTypeCheck for TransportCodec`

- <span id="transportcodec-pytypecheck-type-check"></span>`fn type_check(object: &Bound<'_, PyAny>) -> bool`

- <span id="transportcodec-pytypecheck-classinfo-object"></span>`fn classinfo_object(py: Python<'_>) -> Bound<'_, PyAny>`

##### `impl PyTypeInfo for TransportCodec`

- <span id="transportcodec-pytypeinfo-const-name"></span>`const NAME: &str`

- <span id="transportcodec-pytypeinfo-const-module"></span>`const MODULE: ::std::option::Option<&str>`

- <span id="transportcodec-pytypeinfo-type-object-raw"></span>`fn type_object_raw(py: ::pyo3::Python<'_>) -> *mut ::pyo3::ffi::PyTypeObject`

##### `impl Same for TransportCodec`

- <span id="transportcodec-same-type-output"></span>`type Output = T`

##### `impl Ungil for TransportCodec`

### `FramePump`

```rust
struct FramePump {
    mode: TransportMode,
    max_payload_size: usize,
    server_side: bool,
    buffer: Vec<u8>,
    offset: usize,
}
```

*Defined in `rust/miniproto/src/transport.rs:228-239`*

GIL-free incremental parser/encoder retaining incomplete receive data between calls.

#### Fields

- **`mode`**: `TransportMode`

  Framing variant used for every operation.

- **`max_payload_size`**: `usize`

  Maximum permitted decoded MTProto payload size.

- **`server_side`**: `bool`

  Whether inbound quick-ACK request bits represent payload frames rather than ACK responses.

- **`buffer`**: `Vec<u8>`

  Accumulated unconsumed receive bytes.

- **`offset`**: `usize`

  Leading consumed byte count within `buffer`.

#### Implementations

- <span id="framepump-new"></span>`fn new(mode: TransportMode, max_payload_size: usize, server_side: bool) -> PyResult<Self>` — [`TransportMode`](#transportmode)

  Creates a framed-stream pump after validating its positive payload limit.

  

  Returns `ValueError` for zero `max_payload_size`.

  

  # Arguments

  

  - `mode`: Internal TCP framing strategy for this pump.

  - `max_payload_size`: Positive upper bound for decoded application payload bytes.

  - `server_side`: Whether quick-ACK request bits are decoded as payload metadata.

- <span id="framepump-encode-packet"></span>`fn encode_packet(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>>`

  Encodes one payload using the pump's configured TCP transport mode.

  

  Returns `ValueError` for size/alignment violations or downstream frame construction errors.

  

  # Arguments

  

  - `payload`: Complete MTProto payload to frame.

  - `quick_ack`: Whether to set the outbound quick-ACK request bit where allowed.

- <span id="framepump-encode-abridged"></span>`fn encode_abridged(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>>`

  Encodes an abridged frame with a one- or four-byte word-count header.

  

  Returns `ValueError` unless `payload` is four-byte aligned and representable on the wire.

  

  # Arguments

  

  - `payload`: Four-byte-aligned MTProto payload to frame.

  - `quick_ack`: Whether to set abridged's quick-ACK request bit.

- <span id="framepump-encode-intermediate"></span>`fn encode_intermediate(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>>`

  Encodes an intermediate frame with a flagged four-byte byte-count header.

  

  Returns `ValueError` for unrepresentable transport lengths.

  

  # Arguments

  

  - `payload`: MTProto payload to frame.

  - `quick_ack`: Whether to set intermediate's quick-ACK request bit.

- <span id="framepump-encode-padded-intermediate"></span>`fn encode_padded_intermediate(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>>`

  Encodes an intermediate frame with random zero-to-fifteen-byte padding.

  

  Returns `ValueError` for arithmetic, size or operating-system randomness failures.

  

  # Arguments

  

  - `payload`: MTProto payload to frame before random transport padding.

  - `quick_ack`: Whether to set the intermediate quick-ACK request bit.

- <span id="framepump-feed-data"></span>`fn feed_data(&mut self, data: &[u8]) -> PyResult<Vec<FrameEvent>>` — [`FrameEvent`](#frameevent)

  Buffers `data`, parses every complete frame and retains a partial suffix for later input.

  

  Returns parsed events or a Python exception for allocation, overflow or invalid framing.

  

  # Arguments

  

  - `data`: Newly received TCP bytes to append before parsing complete frames.

- <span id="framepump-parse-one"></span>`fn parse_one(&self) -> PyResult<Option<(FrameEvent, usize)>>` — [`FrameEvent`](#frameevent)

  Attempts to parse one complete frame without mutating the receive buffer.

  

  Returns `None` for an incomplete frame or a Python exception for malformed framing.

- <span id="framepump-parse-abridged"></span>`fn parse_abridged(&self) -> PyResult<Option<(FrameEvent, usize)>>` — [`FrameEvent`](#frameevent)

  Parses one abridged frame or client-side quick-ACK response from buffered input.

  

  Returns `None` while incomplete and `ValueError` for oversized or overflowing frames.

- <span id="framepump-parse-intermediate"></span>`fn parse_intermediate(&self, padded: bool) -> PyResult<Option<(FrameEvent, usize)>>` — [`FrameEvent`](#frameevent)

  Parses one intermediate or padded-intermediate frame from buffered input.

  

  `padded` selects padded payload processing. Returns `None` while incomplete or `ValueError`

  for invalid lengths and protocol-incompatible quick-ACK forms.

  

  # Arguments

  

  - `padded`: Whether the wire payload carries padded-intermediate transport suffix bytes.

- <span id="framepump-payload-event"></span>`fn payload_event(&self, payload: Vec<u8>, padded: bool, quick_ack_requested: bool) -> PyResult<FrameEvent>` — [`FrameEvent`](#frameevent)

  Converts a complete raw transport payload to an application, ACK or error event.

  

  Removes and validates padded-intermediate suffix bytes when `padded`; returns `ValueError`

  for invalid encapsulated packet shape or a payload above the configured maximum.

  

  # Arguments

  

  - `payload`: Complete raw payload after its transport frame prefix.

  - `padded`: Whether to classify and remove padded-intermediate suffix bytes.

  - `quick_ack_requested`: Whether the inbound frame header requested a quick ACK.

- <span id="framepump-validate-frame-length"></span>`fn validate_frame_length(&self, payload_length: usize, padded: bool) -> PyResult<()>`

  Validates a declared frame payload length against this pump's configured maximum.

  

  Adds the allowed padded-mode suffix and returns `ValueError` on overflow or excess.

  

  # Arguments

  

  - `payload_length`: Declared transport payload size in bytes.

  - `padded`: Whether the frame may include up to `MAX_TRANSPORT_PADDING` bytes.

- <span id="framepump-read-slice"></span>`fn read_slice(&self, offset: usize, length: usize) -> PyResult<&[u8]>`

  Borrows a checked range from the accumulated receive buffer.

  

  Returns `ValueError` rather than panicking on overflow or a truncated frame.

  

  # Arguments

  

  - `offset`: Absolute buffered-stream offset at which the range begins.

  - `length`: Number of bytes to borrow.

- <span id="framepump-read-fixed"></span>`fn read_fixed<const N: usize>(&self, offset: usize) -> PyResult<[u8; N]>`

  Reads an exactly `N`-byte receive-buffer field at `offset`.

  

  Returns `ValueError` for missing bytes.

  

  # Arguments

  

  - `N`: Compile-time field width to read.

  - `offset`: Absolute buffered-stream offset at which the field begins.

- <span id="framepump-compact"></span>`fn compact(&mut self)`

  Discards consumed data while retaining only bounded buffer capacity for future chunks.

#### Trait Implementations

##### `impl Same for FramePump`

- <span id="framepump-same-type-output"></span>`type Output = T`

##### `impl Ungil for FramePump`

## Enums

### `TransportMode`

```rust
enum TransportMode {
    Abridged,
    Intermediate,
    PaddedIntermediate,
}
```

*Defined in `rust/miniproto/src/transport.rs:88-95`*

Supported Telegram TCP framing modes selected by their Python wire-name strings.

#### Variants

- **`Abridged`**

  TCP abridged framing with a word-count prefix.

- **`Intermediate`**

  TCP intermediate framing with a four-byte byte-count prefix.

- **`PaddedIntermediate`**

  Intermediate framing with up to 15 random padding bytes.

#### Implementations

- <span id="transportmode-parse"></span>`fn parse(value: &str) -> PyResult<Self>`

  Parses one Python transport mode name into its internal framing strategy.

  

  Returns `ValueError` for unsupported values.

  

  # Arguments

  

  - `value`: Python transport mode name to map to a framing variant.

#### Trait Implementations

##### `impl Clone for TransportMode`

- <span id="transportmode-clone"></span>`fn clone(&self) -> TransportMode` — [`TransportMode`](#transportmode)

##### `impl Copy for TransportMode`

##### `impl Debug for TransportMode`

- <span id="transportmode-debug-fmt"></span>`fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result`

##### `impl Eq for TransportMode`

##### `impl PartialEq for TransportMode`

- <span id="transportmode-partialeq-eq"></span>`fn eq(&self, other: &TransportMode) -> bool` — [`TransportMode`](#transportmode)

##### `impl Same for TransportMode`

- <span id="transportmode-same-type-output"></span>`type Output = T`

##### `impl StructuralPartialEq for TransportMode`

##### `impl Ungil for TransportMode`

### `FrameEvent`

```rust
enum FrameEvent {
    Payload {
        payload: Vec<u8>,
        quick_ack_requested: bool,
    },
    QuickAck(u32),
    TransportError(i32),
}
```

*Defined in `rust/miniproto/src/transport.rs:119-135`*

One native frame-pump result before it is converted to a Python return shape.

#### Variants

- **`Payload`**

  A complete MTProto payload and whether the peer requested a quick ACK.

- **`QuickAck`**

  A quick-ACK token received from the peer.
  
  The contained `u32` is the wire token, including its quick-ACK mask bit.

- **`TransportError`**

  A negative MTProto transport error received in its dedicated wire form.
  
  The contained `i32` is the peer-provided negative transport error code.

#### Trait Implementations

##### `impl Debug for FrameEvent`

- <span id="frameevent-debug-fmt"></span>`fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result`

##### `impl Eq for FrameEvent`

##### `impl PartialEq for FrameEvent`

- <span id="frameevent-partialeq-eq"></span>`fn eq(&self, other: &FrameEvent) -> bool` — [`FrameEvent`](#frameevent)

##### `impl Same for FrameEvent`

- <span id="frameevent-same-type-output"></span>`type Output = T`

##### `impl StructuralPartialEq for FrameEvent`

##### `impl Ungil for FrameEvent`

## Functions

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/transport.rs:41-45`*

Registers Python `TransportCodec` and `quick_ack_token` on `miniproto._native`.

Returns a PyO3 exception if either export cannot be installed.

# Arguments

- `m`: The Python extension module receiving the transport exports.

### `quick_ack_token`

```rust
fn quick_ack_token(py: Python<'_>, auth_key: Vec<u8>, encrypted_packet: Vec<u8>) -> PyResult<u32>
```

*Defined in `rust/miniproto/src/transport.rs:58-63`*

Computes the flagged quick-ACK token for Python `quick_ack_token`.

The 256-byte `auth_key` and nonempty encrypted portion of `encrypted_packet` are validated.
Returns the token with the quick-ACK bit set or `ValueError` for invalid packet/key input.

# Arguments

- `py`: Acquired Python token used to detach hashing for sufficiently large packets.
- `auth_key`: 256-byte MTProto authorization key used by the quick-ACK hash schedule.
- `encrypted_packet`: Full MTProto packet whose nonempty encrypted suffix is hashed.

### `__pyfunction_quick_ack_token`

```rust
unsafe fn __pyfunction_quick_ack_token<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/transport.rs:57`*

### `quick_ack_token_raw`

```rust
fn quick_ack_token_raw(auth_key: &[u8], encrypted_packet: &[u8]) -> PyResult<u32>
```

*Defined in `rust/miniproto/src/transport.rs:71-84`*

Computes a quick-ACK token without Python argument conversion or GIL interaction.

# Arguments

- `auth_key`: 256-byte MTProto authorization key used by the quick-ACK hash schedule.
- `encrypted_packet`: Full MTProto packet whose nonempty encrypted suffix is hashed.

### `encode_length_prefixed`

```rust
fn encode_length_prefixed(payload: &[u8], payload_length: u32, quick_ack: bool) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/transport.rs:644-657`*

Encodes a four-byte little-endian length prefix and payload, optionally setting quick-ACK bit.

Returns `ValueError` if header-plus-payload length overflows `usize`.

# Arguments

- `payload`: Bytes to follow the four-byte header.
- `payload_length`: Already validated wire length, excluding the header.
- `quick_ack`: Whether to set the intermediate quick-ACK request bit.

### `padded_packet_length`

```rust
fn padded_packet_length(payload: &[u8]) -> PyResult<usize>
```

*Defined in `rust/miniproto/src/transport.rs:667-694`*

Determines the embedded MTProto packet length within a padded-intermediate payload.

Returns `ValueError` for malformed unencrypted or encrypted packet shapes; it deliberately
does not treat arbitrary encrypted payload bytes as transport error indicators.

# Arguments

- `payload`: Padded-intermediate contents containing an embedded MTProto packet and suffix.

### `to_fixed`

```rust
fn to_fixed<const N: usize>(data: &[u8]) -> PyResult<[u8; N]>
```

*Defined in `rust/miniproto/src/transport.rs:704-707`*

Converts a slice to an exact fixed-width array for frame header decoding.

Returns `ValueError` rather than panicking on an unexpected length.

# Arguments

- `N`: Compile-time width required by the caller.
- `data`: Slice expected to contain exactly `N` bytes.

## Type Aliases

### `PythonFrameEvent`

```rust
type PythonFrameEvent = (u8, Vec<u8>, i64, bool);
```

*Defined in `rust/miniproto/src/transport.rs:32`*

Python `feed_data` event tuple: kind, payload, numeric detail, quick-ACK request flag.

## Constants

### `ABRIDGED_LONG_MARKER`
```rust
const ABRIDGED_LONG_MARKER: u8 = 127u8;
```

*Defined in `rust/miniproto/src/transport.rs:22`*

Abridged header byte that introduces its three-byte word-length form.

### `QUICK_ACK_MASK`
```rust
const QUICK_ACK_MASK: u32 = 2_147_483_648u32;
```

*Defined in `rust/miniproto/src/transport.rs:24`*

Wire bit that asks the peer to return a quick-ACK token.

### `PADDED_QUICK_ACK_MARKER`
```rust
const PADDED_QUICK_ACK_MARKER: [u8; 4];
```

*Defined in `rust/miniproto/src/transport.rs:26`*

Padded-intermediate payload marker identifying a quick-ACK response.

### `MAX_TRANSPORT_PADDING`
```rust
const MAX_TRANSPORT_PADDING: usize = 15usize;
```

*Defined in `rust/miniproto/src/transport.rs:28`*

Maximum random padding bytes allowed by padded-intermediate TCP framing.

### `RETAINED_BUFFER_LIMIT`
```rust
const RETAINED_BUFFER_LIMIT: usize = 1_048_576usize;
```

*Defined in `rust/miniproto/src/transport.rs:30`*

Largest drained receive-buffer allocation retained for later chunks.

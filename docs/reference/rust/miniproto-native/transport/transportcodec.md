---
title: "miniproto_native::transport::TransportCodec"
description: "Python-visible incremental TCP framing codec, exported as `miniproto._native.TransportCodec`."
generated: true
editUrl: false
language: "rust"
kind: "struct"
qualified_name: "miniproto_native::transport::TransportCodec"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L123"
aliases: ["miniproto._native.TransportCodec"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L123)
- Python exposure: `miniproto._native.TransportCodec` (confirmed from adjacent PyO3 attributes)

## cargo-docs-md rendering

### `TransportCodec`

```rust
struct TransportCodec {
    pump: FramePump,
}
```

*Defined in `rust/miniproto/src/transport.rs:123-126`*

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

  

  Tuple kinds are `0` payload, `1` quick ACK, and `2` negative transport error. It preserves

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

---
title: "miniproto_native::mtproto"
description: "Registers encrypted MTProto message-envelope callables."
generated: true
editUrl: false
language: "rust"
kind: "module"
qualified_name: "miniproto_native::mtproto"
source_path: "rust/miniproto/src/mtproto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L1"
crate: "miniproto_native"
python_visible: false
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `crate`
- Source: [`rust/miniproto/src/mtproto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L1)
- Python exposure: Not evidenced by static PyO3 attributes.

## Documented items

- [`miniproto_native::mtproto::register`](./register/)
- [`miniproto_native::mtproto::mtproto_encode_message`](./mtproto-encode-message/)
- [`miniproto_native::mtproto::mtproto_decode_message`](./mtproto-decode-message/)

## cargo-docs-md rendering

*miniproto_native / [mtproto](index.md)*

---

# Module `mtproto`

Registers encrypted MTProto message-envelope callables.
Native encoding and decoding of encrypted MTProto 2.0 message envelopes.

The Python-visible functions in this module use the same argument and result layout as the
Python fallback. PyO3 preserves `TypeError`, `OverflowError`, and source conversion exceptions
before a function body runs; protocol validation after conversion returns `ValueError`. The
functions release the GIL for large byte workloads rather than exposing Rust panics.

## Contents

- [Structs](#structs)
  - [`DecodedEncryptedMessage`](#decodedencryptedmessage)
  - [`EnvelopeEncodeInput`](#envelopeencodeinput)
- [Functions](#functions)
  - [`register`](#register)
  - [`mtproto_encode_message`](#mtproto-encode-message)
  - [`__pyfunction_mtproto_encode_message`](#pyfunction-mtproto-encode-message)
  - [`mtproto_decode_message`](#mtproto-decode-message)
  - [`__pyfunction_mtproto_decode_message`](#pyfunction-mtproto-decode-message)
  - [`mtproto_encode_message_raw`](#mtproto-encode-message-raw)
  - [`mtproto_decode_message_raw`](#mtproto-decode-message-raw)
  - [`random_padding`](#random-padding)
  - [`padding_len`](#padding-len)
  - [`validate_padding`](#validate-padding)
- [Type Aliases](#type-aliases)
  - [`PyDecodedEnvelope`](#pydecodedenvelope)
- [Constants](#constants)
  - [`ENCRYPTED_PACKET_HEADER_LEN`](#encrypted-packet-header-len)
  - [`ENVELOPE_HEADER_LEN`](#envelope-header-len)
  - [`MIN_PADDING_LEN`](#min-padding-len)
  - [`MAX_PADDING_LEN`](#max-padding-len)

## Quick Reference

| Item | Kind | Description |
|------|------|-------------|
| [`DecodedEncryptedMessage`](#decodedencryptedmessage) | struct | Decoded contents of a validated encrypted MTProto packet for Rust-internal callers. |
| [`EnvelopeEncodeInput`](#envelopeencodeinput) | struct | Borrowed inputs used to build one encrypted MTProto envelope without Python interaction. |
| [`register`](#register) | fn | Adds the Python-visible MTProto envelope functions to `miniproto._native`. |
| [`mtproto_encode_message`](#mtproto-encode-message) | fn | Encodes one encrypted MTProto envelope as Python `mtproto_encode_message`. |
| [`__pyfunction_mtproto_encode_message`](#pyfunction-mtproto-encode-message) | fn |  |
| [`mtproto_decode_message`](#mtproto-decode-message) | fn | Decodes Python `mtproto_decode_message` packet bytes into its seven-element envelope tuple. |
| [`__pyfunction_mtproto_decode_message`](#pyfunction-mtproto-decode-message) | fn |  |
| [`mtproto_encode_message_raw`](#mtproto-encode-message-raw) | fn | Builds and encrypts an MTProto envelope from already borrowed Rust inputs. |
| [`mtproto_decode_message_raw`](#mtproto-decode-message-raw) | fn | Verifies, decrypts, and parses an encrypted MTProto packet for Rust callers. |
| [`random_padding`](#random-padding) | fn | Generates random MTProto padding that completes `plaintext_len` to an AES block boundary. |
| [`padding_len`](#padding-len) | fn | Computes the minimum valid padding length for an inner plaintext length. |
| [`validate_padding`](#validate-padding) | fn | Validates MTProto 2.0 padding bounds and the resulting AES block alignment. |
| [`PyDecodedEnvelope`](#pydecodedenvelope) | type | Python tuple returned by `mtproto_decode_message` in envelope field order. |
| [`ENCRYPTED_PACKET_HEADER_LEN`](#encrypted-packet-header-len) | const | Bytes preceding ciphertext in an encrypted MTProto packet: auth-key id plus message key. |
| [`ENVELOPE_HEADER_LEN`](#envelope-header-len) | const | Bytes in an unencrypted inner envelope before its application body. |
| [`MIN_PADDING_LEN`](#min-padding-len) | const | Smallest MTProto 2.0 random-padding length, in bytes. |
| [`MAX_PADDING_LEN`](#max-padding-len) | const | Largest accepted MTProto 2.0 random-padding length, in bytes. |

## Structs

### `DecodedEncryptedMessage`

```rust
struct DecodedEncryptedMessage {
    pub auth_key_id: Vec<u8>,
    pub server_salt: u64,
    pub session_id: u64,
    pub msg_id: i64,
    pub seq_no: i32,
    pub body: Vec<u8>,
    pub padding: Vec<u8>,
}
```

*Defined in `rust/miniproto/src/mtproto.rs:30-45`*

Decoded contents of a validated encrypted MTProto packet for Rust-internal callers.

#### Fields

- **`auth_key_id`**: `Vec<u8>`

  Eight-byte identifier derived from the packet's authentication key.

- **`server_salt`**: `u64`

  Server salt carried by the envelope.

- **`session_id`**: `u64`

  Session identifier carried by the envelope.

- **`msg_id`**: `i64`

  MTProto message identifier carried by the envelope.

- **`seq_no`**: `i32`

  MTProto sequence number carried by the envelope.

- **`body`**: `Vec<u8>`

  Application message body, excluding the envelope and random padding.

- **`padding`**: `Vec<u8>`

  Validated random padding trailing the body.

#### Trait Implementations

##### `impl Debug for DecodedEncryptedMessage`

- <span id="decodedencryptedmessage-debug-fmt"></span>`fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result`

##### `impl Eq for DecodedEncryptedMessage`

##### `impl PartialEq for DecodedEncryptedMessage`

- <span id="decodedencryptedmessage-partialeq-eq"></span>`fn eq(&self, other: &DecodedEncryptedMessage) -> bool` — [`DecodedEncryptedMessage`](#decodedencryptedmessage)

##### `impl Same for DecodedEncryptedMessage`

- <span id="decodedencryptedmessage-same-type-output"></span>`type Output = T`

##### `impl StructuralPartialEq for DecodedEncryptedMessage`

##### `impl Ungil for DecodedEncryptedMessage`

### `EnvelopeEncodeInput<'a>`

```rust
struct EnvelopeEncodeInput<'a> {
    pub auth_key: &'a [u8],
    pub server_salt: u64,
    pub session_id: u64,
    pub msg_id: i64,
    pub seq_no: i32,
    pub body: &'a [u8],
    pub client_to_server: bool,
    pub padding: Option<&'a [u8]>,
}
```

*Defined in `rust/miniproto/src/mtproto.rs:48-65`*

Borrowed inputs used to build one encrypted MTProto envelope without Python interaction.

#### Fields

- **`auth_key`**: `&'a [u8]`

  The 256-byte MTProto authentication key.

- **`server_salt`**: `u64`

  Salt to serialize in the envelope.

- **`session_id`**: `u64`

  Session identifier to serialize in the envelope.

- **`msg_id`**: `i64`

  Message identifier to serialize in the envelope.

- **`seq_no`**: `i32`

  Sequence number to serialize in the envelope.

- **`body`**: `&'a [u8]`

  Four-byte-aligned application body to serialize.

- **`client_to_server`**: `bool`

  Whether the packet direction is client-to-server for MTProto key derivation.

- **`padding`**: `Option<&'a [u8]>`

  Optional caller-selected padding; `None` requests securely random valid padding.

#### Trait Implementations

##### `impl Same for EnvelopeEncodeInput<'a>`

- <span id="envelopeencodeinput-same-type-output"></span>`type Output = T`

##### `impl Ungil for EnvelopeEncodeInput<'a>`

## Functions

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/mtproto.rs:77-81`*

Adds the Python-visible MTProto envelope functions to `miniproto._native`.

Returns a Python exception when PyO3 cannot register either callable.

# Arguments

- `m`: The Python extension module to receive the envelope callables.

### `mtproto_encode_message`

```rust
fn mtproto_encode_message(py: Python<'_>, auth_key: Vec<u8>, server_salt: u64, session_id: u64, msg_id: i64, seq_no: i32, body: Vec<u8>, client_to_server: bool, padding: Option<Vec<u8>>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/mtproto.rs:114-138`*

Encodes one encrypted MTProto envelope as Python `mtproto_encode_message`.

The salt, session/message identifiers, sequence number, body length, `body`, and padding form
the inner envelope; `auth_key` encrypts it but is not itself serialized in that envelope.
`client_to_server` chooses MTProto's directional key offset; optional `padding` replaces random
padding. Returns auth-key-id/message-key/ciphertext concatenated in wire
order, or `ValueError` for invalid key, body, or padding.  For large byte inputs it releases
the GIL while performing the native work.

# Arguments

- `py`: The acquired GIL token used only to detach large native work.
- `auth_key`: The 256-byte authorization key used to encrypt, but not serialize, the envelope.
- `server_salt`: The salt serialized at the start of the inner envelope.
- `session_id`: The session identifier serialized in the inner envelope.
- `msg_id`: The MTProto message identifier serialized in the inner envelope.
- `seq_no`: The MTProto sequence number serialized in the inner envelope.
- `body`: Four-byte-aligned application bytes serialized before the padding.
- `client_to_server`: Selects the directional MTProto key schedule.
- `padding`: Optional explicit padding; `None` requests operating-system random padding.

### `__pyfunction_mtproto_encode_message`

```rust
unsafe fn __pyfunction_mtproto_encode_message<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/mtproto.rs:103-112`*

### `mtproto_decode_message`

```rust
fn mtproto_decode_message(py: Python<'_>, auth_key: Vec<u8>, packet: Vec<u8>, client_to_server: bool) -> PyResult<(Vec<u8>, u64, u64, i64, i32, Vec<u8>, Vec<u8>)>
```

*Defined in `rust/miniproto/src/mtproto.rs:154-173`*

Decodes Python `mtproto_decode_message` packet bytes into its seven-element envelope tuple.

`client_to_server` selects the direction used to verify and decrypt `packet`.  Returns
`(auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding)`, or `ValueError` if
the wire packet, keys, body length, message key, or padding is invalid.  Large workloads run
with the GIL released.

# Arguments

- `py`: The acquired GIL token used only to detach large native work.
- `auth_key`: The 256-byte authorization key used to verify and decrypt `packet`.
- `packet`: Full encrypted MTProto packet including auth-key id and message key.
- `client_to_server`: Selects the directional MTProto key schedule used for verification.

### `__pyfunction_mtproto_decode_message`

```rust
unsafe fn __pyfunction_mtproto_decode_message<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/mtproto.rs:153`*

### `mtproto_encode_message_raw`

```rust
fn mtproto_encode_message_raw(input: EnvelopeEncodeInput<'_>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/mtproto.rs:184-212`*

Builds and encrypts an MTProto envelope from already borrowed Rust inputs.

Returns the complete encrypted packet or a Python `ValueError` for invalid protocol inputs or
unavailable operating-system randomness.  Callers must provide a body that is four-byte
aligned; this function does not interact with the GIL.

# Arguments

- `input`: Borrowed authorization key and envelope fields to serialize and encrypt.

### `mtproto_decode_message_raw`

```rust
fn mtproto_decode_message_raw(auth_key: &[u8], packet: &[u8], client_to_server: bool) -> PyResult<DecodedEncryptedMessage>
```

*Defined in `rust/miniproto/src/mtproto.rs:224-282`*

Verifies, decrypts, and parses an encrypted MTProto packet for Rust callers.

Returns the envelope fields and trailing padding, or a Python `ValueError` when any header,
cryptographic check, length, or padding constraint fails.  It does not interact with the GIL.

# Arguments

- `auth_key`: Valid 256-byte authorization key expected by the packet.
- `packet`: Complete encrypted MTProto packet to authenticate and parse.
- `client_to_server`: Selects the directional MTProto key schedule.

### `random_padding`

```rust
fn random_padding(plaintext_len: usize) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/mtproto.rs:292-297`*

Generates random MTProto padding that completes `plaintext_len` to an AES block boundary.

Returns `ValueError` if the operating-system randomness source fails.

# Arguments

- `plaintext_len`: Inner-envelope byte length before random padding; it must be representable
  after adding the selected padding length.

### `padding_len`

```rust
fn padding_len(plaintext_len: usize) -> usize
```

*Defined in `rust/miniproto/src/mtproto.rs:306-309`*

Computes the minimum valid padding length for an inner plaintext length.

# Arguments

- `plaintext_len`: Inner-envelope byte length before padding; callers must ensure
  `plaintext_len + MIN_PADDING_LEN` cannot overflow `usize`, because this arithmetic helper
  deliberately has no fallible return path.

### `validate_padding`

```rust
fn validate_padding(plaintext_len: usize, padding: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/mtproto.rs:321-333`*

Validates MTProto 2.0 padding bounds and the resulting AES block alignment.

Returns `ValueError` instead of panicking when the padding length is invalid. Callers must
ensure `plaintext_len + padding.len()` is representable; that sum is evaluated directly before
the modulus check.

# Arguments

- `plaintext_len`: Inner-envelope byte length before padding.
- `padding`: Candidate trailing random padding to validate.

## Type Aliases

### `PyDecodedEnvelope`

```rust
type PyDecodedEnvelope = (Vec<u8>, u64, u64, i64, i32, Vec<u8>, Vec<u8>);
```

*Defined in `rust/miniproto/src/mtproto.rs:68`*

Python tuple returned by `mtproto_decode_message` in envelope field order.

## Constants

### `ENCRYPTED_PACKET_HEADER_LEN`
```rust
const ENCRYPTED_PACKET_HEADER_LEN: usize = 24usize;
```

*Defined in `rust/miniproto/src/mtproto.rs:20`*

Bytes preceding ciphertext in an encrypted MTProto packet: auth-key id plus message key.

### `ENVELOPE_HEADER_LEN`
```rust
const ENVELOPE_HEADER_LEN: usize = 32usize;
```

*Defined in `rust/miniproto/src/mtproto.rs:22`*

Bytes in an unencrypted inner envelope before its application body.

### `MIN_PADDING_LEN`
```rust
const MIN_PADDING_LEN: usize = 12usize;
```

*Defined in `rust/miniproto/src/mtproto.rs:24`*

Smallest MTProto 2.0 random-padding length, in bytes.

### `MAX_PADDING_LEN`
```rust
const MAX_PADDING_LEN: usize = 1_024usize;
```

*Defined in `rust/miniproto/src/mtproto.rs:26`*

Largest accepted MTProto 2.0 random-padding length, in bytes.

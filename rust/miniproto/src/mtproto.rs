//! Native encoding and decoding of encrypted MTProto 2.0 message envelopes.
//!
//! The Python-visible functions in this module use the same argument and result layout as the
//! Python fallback. PyO3 preserves `TypeError`, `OverflowError` and source conversion exceptions
//! before a function body runs; protocol validation after conversion returns `ValueError`. The
//! functions release the GIL for large byte workloads rather than exposing Rust panics.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;

use crate::crypto::{
    AES_BLOCK_SIZE, detach_if_large, mtproto_auth_key_id_raw, mtproto_decrypt_payload_raw,
    mtproto_encrypt_payload_raw, validate_auth_key,
};
use crate::tl::read_fixed;

/// Bytes preceding ciphertext in an encrypted MTProto packet: auth-key id plus message key.
const ENCRYPTED_PACKET_HEADER_LEN: usize = 24;
/// Bytes in an unencrypted inner envelope before its application body.
const ENVELOPE_HEADER_LEN: usize = 32;
/// Smallest MTProto 2.0 random-padding length, in bytes.
const MIN_PADDING_LEN: usize = 12;
/// Largest accepted MTProto 2.0 random-padding length, in bytes.
const MAX_PADDING_LEN: usize = 1024;

/// Decoded contents of a validated encrypted MTProto packet for Rust-internal callers.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct DecodedEncryptedMessage {
    /// Eight-byte identifier derived from the packet's authentication key.
    pub auth_key_id: Vec<u8>,
    /// Server salt carried by the envelope.
    pub server_salt: u64,
    /// Session identifier carried by the envelope.
    pub session_id: u64,
    /// MTProto message identifier carried by the envelope.
    pub msg_id: i64,
    /// MTProto sequence number carried by the envelope.
    pub seq_no: i32,
    /// Application message body, excluding the envelope and random padding.
    pub body: Vec<u8>,
    /// Validated random padding trailing the body.
    pub padding: Vec<u8>,
}

/// Borrowed inputs used to build one encrypted MTProto envelope without Python interaction.
pub(crate) struct EnvelopeEncodeInput<'a> {
    /// The 256-byte MTProto authentication key.
    pub auth_key: &'a [u8],
    /// Salt to serialize in the envelope.
    pub server_salt: u64,
    /// Session identifier to serialize in the envelope.
    pub session_id: u64,
    /// Message identifier to serialize in the envelope.
    pub msg_id: i64,
    /// Sequence number to serialize in the envelope.
    pub seq_no: i32,
    /// Four-byte-aligned application body to serialize.
    pub body: &'a [u8],
    /// Whether the packet direction is client-to-server for MTProto key derivation.
    pub client_to_server: bool,
    /// Optional caller-selected padding; `None` requests securely random valid padding.
    pub padding: Option<&'a [u8]>,
}

/// Python tuple returned by `mtproto_decode_message` in envelope field order.
type PyDecodedEnvelope = (Vec<u8>, u64, u64, i64, i32, Vec<u8>, Vec<u8>);

/// Adds the Python-visible MTProto envelope functions to `miniproto._native`.
///
/// Returns a Python exception when PyO3 cannot register either callable.
///
/// # Arguments
///
/// - `m`: The Python extension module to receive the envelope callables.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mtproto_encode_message, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_decode_message, m)?)?;
    Ok(())
}

/// Encodes one encrypted MTProto envelope as Python `mtproto_encode_message`.
///
/// The salt, session/message identifiers, sequence number, body length, `body` and padding form
/// the inner envelope; `auth_key` encrypts it but is not itself serialized in that envelope.
/// `client_to_server` chooses MTProto's directional key offset; optional `padding` replaces random
/// padding. Returns auth-key-id/message-key/ciphertext concatenated in wire
/// order or `ValueError` for invalid key, body or padding.  For large byte inputs it releases
/// the GIL while performing the native work.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used only to detach large native work.
/// - `auth_key`: The 256-byte authorization key used to encrypt, but not serialize, the envelope.
/// - `server_salt`: The salt serialized at the start of the inner envelope.
/// - `session_id`: The session identifier serialized in the inner envelope.
/// - `msg_id`: The MTProto message identifier serialized in the inner envelope.
/// - `seq_no`: The MTProto sequence number serialized in the inner envelope.
/// - `body`: Four-byte-aligned application bytes serialized before the padding.
/// - `client_to_server`: Selects the directional MTProto key schedule.
/// - `padding`: Optional explicit padding; `None` requests operating-system random padding.
#[pyfunction(signature = (
    auth_key,
    server_salt,
    session_id,
    msg_id,
    seq_no,
    body,
    client_to_server = true,
    padding = None
))]
#[allow(clippy::too_many_arguments)]
fn mtproto_encode_message(
    py: Python<'_>,
    auth_key: Vec<u8>,
    server_salt: u64,
    session_id: u64,
    msg_id: i64,
    seq_no: i32,
    body: Vec<u8>,
    client_to_server: bool,
    padding: Option<Vec<u8>>,
) -> PyResult<Vec<u8>> {
    let work_bytes = auth_key.len() + body.len() + padding.as_ref().map_or(0, Vec::len);
    detach_if_large(py, work_bytes, move || {
        mtproto_encode_message_raw(EnvelopeEncodeInput {
            auth_key: &auth_key,
            server_salt,
            session_id,
            msg_id,
            seq_no,
            body: &body,
            client_to_server,
            padding: padding.as_deref(),
        })
    })
}

/// Decodes Python `mtproto_decode_message` packet bytes into its seven-element envelope tuple.
///
/// `client_to_server` selects the direction used to verify and decrypt `packet`.  Returns
/// `(auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding)` or `ValueError` if
/// the wire packet, keys, body length, message key or padding is invalid.  Large workloads run
/// with the GIL released.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used only to detach large native work.
/// - `auth_key`: The 256-byte authorization key used to verify and decrypt `packet`.
/// - `packet`: Full encrypted MTProto packet including auth-key id and message key.
/// - `client_to_server`: Selects the directional MTProto key schedule used for verification.
#[pyfunction(signature = (auth_key, packet, client_to_server = false))]
fn mtproto_decode_message(
    py: Python<'_>,
    auth_key: Vec<u8>,
    packet: Vec<u8>,
    client_to_server: bool,
) -> PyResult<PyDecodedEnvelope> {
    let work_bytes = auth_key.len() + packet.len();
    let decoded = detach_if_large(py, work_bytes, move || {
        mtproto_decode_message_raw(&auth_key, &packet, client_to_server)
    })?;
    Ok((
        decoded.auth_key_id,
        decoded.server_salt,
        decoded.session_id,
        decoded.msg_id,
        decoded.seq_no,
        decoded.body,
        decoded.padding,
    ))
}

/// Builds and encrypts an MTProto envelope from already borrowed Rust inputs.
///
/// Returns the complete encrypted packet or a Python `ValueError` for invalid protocol inputs or
/// unavailable operating-system randomness.  Callers must provide a body that is four-byte
/// aligned; this function does not interact with the GIL.
///
/// # Arguments
///
/// - `input`: Borrowed authorization key and envelope fields to serialize and encrypt.
pub(crate) fn mtproto_encode_message_raw(input: EnvelopeEncodeInput<'_>) -> PyResult<Vec<u8>> {
    validate_auth_key(input.auth_key)?;
    if !input.body.len().is_multiple_of(4) {
        return Err(PyValueError::new_err(
            "MTProto message body length must be divisible by 4",
        ));
    }
    let body_len = i32::try_from(input.body.len())
        .map_err(|_| PyValueError::new_err("MTProto message body is too large"))?;
    let padding = match input.padding {
        Some(value) => {
            validate_padding(ENVELOPE_HEADER_LEN + input.body.len(), value)?;
            value.to_vec()
        }
        None => random_padding(ENVELOPE_HEADER_LEN + input.body.len())?,
    };

    let mut plaintext = Vec::with_capacity(ENVELOPE_HEADER_LEN + input.body.len() + padding.len());
    plaintext.extend_from_slice(&input.server_salt.to_le_bytes());
    plaintext.extend_from_slice(&input.session_id.to_le_bytes());
    plaintext.extend_from_slice(&input.msg_id.to_le_bytes());
    plaintext.extend_from_slice(&input.seq_no.to_le_bytes());
    plaintext.extend_from_slice(&body_len.to_le_bytes());
    plaintext.extend_from_slice(input.body);
    plaintext.extend_from_slice(&padding);

    let (auth_key_id, msg_key, ciphertext) =
        mtproto_encrypt_payload_raw(input.auth_key, &plaintext, input.client_to_server)?;
    let mut packet = Vec::with_capacity(ENCRYPTED_PACKET_HEADER_LEN + ciphertext.len());
    packet.extend_from_slice(&auth_key_id);
    packet.extend_from_slice(&msg_key);
    packet.extend_from_slice(&ciphertext);
    Ok(packet)
}

/// Verifies, decrypts and parses an encrypted MTProto packet for Rust callers.
///
/// Returns the envelope fields and trailing padding or a Python `ValueError` when any header,
/// cryptographic check, length or padding constraint fails.  It does not interact with the GIL.
///
/// # Arguments
///
/// - `auth_key`: Valid 256-byte authorization key expected by the packet.
/// - `packet`: Complete encrypted MTProto packet to authenticate and parse.
/// - `client_to_server`: Selects the directional MTProto key schedule.
pub(crate) fn mtproto_decode_message_raw(
    auth_key: &[u8],
    packet: &[u8],
    client_to_server: bool,
) -> PyResult<DecodedEncryptedMessage> {
    validate_auth_key(auth_key)?;
    if packet.len() < ENCRYPTED_PACKET_HEADER_LEN {
        return Err(PyValueError::new_err(
            "encrypted MTProto packet is too short",
        ));
    }
    let auth_key_id = packet[..8].to_vec();
    let msg_key = &packet[8..24];
    let ciphertext = &packet[24..];
    let plaintext = mtproto_decrypt_payload_raw(auth_key, msg_key, ciphertext, client_to_server)?;
    if auth_key_id != mtproto_auth_key_id_raw(auth_key)? {
        return Err(PyValueError::new_err(
            "encrypted MTProto auth_key_id does not match auth_key",
        ));
    }
    if plaintext.len() < ENVELOPE_HEADER_LEN {
        return Err(PyValueError::new_err(
            "encrypted MTProto plaintext is too short",
        ));
    }
    let server_salt = u64::from_le_bytes(read_fixed::<8>(&plaintext, 0)?);
    let session_id = u64::from_le_bytes(read_fixed::<8>(&plaintext, 8)?);
    let msg_id = i64::from_le_bytes(read_fixed::<8>(&plaintext, 16)?);
    let seq_no = i32::from_le_bytes(read_fixed::<4>(&plaintext, 24)?);
    let body_len = i32::from_le_bytes(read_fixed::<4>(&plaintext, 28)?);
    if body_len < 0 {
        return Err(PyValueError::new_err(
            "encrypted MTProto body length is invalid",
        ));
    }
    let body_len = body_len as usize;
    if !body_len.is_multiple_of(4) {
        return Err(PyValueError::new_err(
            "encrypted MTProto body length must be divisible by 4",
        ));
    }
    let body_offset = ENVELOPE_HEADER_LEN;
    let padding_offset = body_offset + body_len;
    if padding_offset > plaintext.len() {
        return Err(PyValueError::new_err(
            "encrypted MTProto body length is invalid",
        ));
    }
    validate_padding(padding_offset, &plaintext[padding_offset..])?;
    Ok(DecodedEncryptedMessage {
        auth_key_id,
        server_salt,
        session_id,
        msg_id,
        seq_no,
        body: plaintext[body_offset..padding_offset].to_vec(),
        padding: plaintext[padding_offset..].to_vec(),
    })
}

/// Generates random MTProto padding that completes `plaintext_len` to an AES block boundary.
///
/// Returns `ValueError` if the operating-system randomness source fails.
///
/// # Arguments
///
/// - `plaintext_len`: Inner-envelope byte length before random padding; it must be representable
///   after adding the selected padding length.
fn random_padding(plaintext_len: usize) -> PyResult<Vec<u8>> {
    let mut padding = vec![0; padding_len(plaintext_len)];
    getrandom::fill(&mut padding)
        .map_err(|error| PyValueError::new_err(format!("OS random failed: {error}")))?;
    Ok(padding)
}

/// Computes the minimum valid padding length for an inner plaintext length.
///
/// # Arguments
///
/// - `plaintext_len`: Inner-envelope byte length before padding; callers must ensure
///   `plaintext_len + MIN_PADDING_LEN` cannot overflow `usize`, because this arithmetic helper
///   deliberately has no fallible return path.
fn padding_len(plaintext_len: usize) -> usize {
    MIN_PADDING_LEN
        + (AES_BLOCK_SIZE - ((plaintext_len + MIN_PADDING_LEN) % AES_BLOCK_SIZE)) % AES_BLOCK_SIZE
}

/// Validates MTProto 2.0 padding bounds and the resulting AES block alignment.
///
/// Returns `ValueError` instead of panicking when the padding length is invalid. Callers must
/// ensure `plaintext_len + padding.len()` is representable; that sum is evaluated directly before
/// the modulus check.
///
/// # Arguments
///
/// - `plaintext_len`: Inner-envelope byte length before padding.
/// - `padding`: Candidate trailing random padding to validate.
fn validate_padding(plaintext_len: usize, padding: &[u8]) -> PyResult<()> {
    if !(MIN_PADDING_LEN..=MAX_PADDING_LEN).contains(&padding.len()) {
        return Err(PyValueError::new_err(
            "MTProto 2.0 padding must be between 12 and 1024 bytes",
        ));
    }
    if !(plaintext_len + padding.len()).is_multiple_of(AES_BLOCK_SIZE) {
        return Err(PyValueError::new_err(
            "MTProto padded payload length must be a multiple of 16 bytes",
        ));
    }
    Ok(())
}

/// Unit tests for encrypted MTProto envelope encoding and validation.
#[cfg(test)]
mod tests {
    use super::*;
    use crate::crypto::mtproto_auth_key_id_raw;

    /// Stable server-salt fixture for deterministic envelope tests.
    const SERVER_SALT: u64 = 0x0102_0304_0506_0708;
    /// Stable session-id fixture for deterministic envelope tests.
    const SESSION_ID: u64 = 0x1112_1314_1516_1718;
    /// Stable message-id fixture for deterministic envelope tests.
    const MSG_ID: i64 = 0x2122_2324_2526_2728;
    /// Stable sequence-number fixture for deterministic envelope tests.
    const SEQ_NO: i32 = 3;

    #[test]
    /// Ensures an explicitly padded envelope survives native encrypt/decrypt round-tripping.
    fn envelope_roundtrips_with_explicit_padding() {
        let auth_key = auth_key();
        let body = b"body".to_vec();
        let padding = vec![0; 12];
        let packet = mtproto_encode_message_raw(EnvelopeEncodeInput {
            auth_key: &auth_key,
            server_salt: SERVER_SALT,
            session_id: SESSION_ID,
            msg_id: MSG_ID,
            seq_no: SEQ_NO,
            body: &body,
            client_to_server: true,
            padding: Some(&padding),
        })
        .unwrap();
        assert_eq!(
            &packet[..8],
            mtproto_auth_key_id_raw(&auth_key).unwrap().as_slice()
        );
        let decoded = mtproto_decode_message_raw(&auth_key, &packet, true).unwrap();
        assert_eq!(
            decoded,
            DecodedEncryptedMessage {
                auth_key_id: mtproto_auth_key_id_raw(&auth_key).unwrap(),
                server_salt: SERVER_SALT,
                session_id: SESSION_ID,
                msg_id: MSG_ID,
                seq_no: SEQ_NO,
                body,
                padding,
            }
        );
    }

    #[test]
    /// Ensures generated random padding meets MTProto bounds and AES alignment.
    fn envelope_generates_valid_random_padding() {
        let auth_key = auth_key();
        let body = vec![0xab; 128];
        let packet = mtproto_encode_message_raw(EnvelopeEncodeInput {
            auth_key: &auth_key,
            server_salt: SERVER_SALT,
            session_id: SESSION_ID,
            msg_id: MSG_ID,
            seq_no: SEQ_NO,
            body: &body,
            client_to_server: true,
            padding: None,
        })
        .unwrap();
        let decoded = mtproto_decode_message_raw(&auth_key, &packet, true).unwrap();
        assert_eq!(decoded.body, body);
        assert!((12..=1024).contains(&decoded.padding.len()));
        assert_eq!(
            (ENVELOPE_HEADER_LEN + decoded.body.len() + decoded.padding.len()) % AES_BLOCK_SIZE,
            0
        );
    }

    #[test]
    /// Ensures caller-provided padding is rejected before encryption when invalid.
    fn explicit_padding_is_validated() {
        Python::initialize();
        let auth_key = auth_key();
        let error = mtproto_encode_message_raw(EnvelopeEncodeInput {
            auth_key: &auth_key,
            server_salt: SERVER_SALT,
            session_id: SESSION_ID,
            msg_id: MSG_ID,
            seq_no: SEQ_NO,
            body: b"body",
            client_to_server: true,
            padding: Some(&[0; 11]),
        })
        .unwrap_err();
        assert!(error.to_string().contains("padding"));
    }

    #[test]
    /// Rejects message bodies that the decoder cannot accept because they are not TL-word aligned.
    fn envelope_rejects_unaligned_body_before_encryption() {
        Python::initialize();
        let auth_key = auth_key();
        let error = mtproto_encode_message_raw(EnvelopeEncodeInput {
            auth_key: &auth_key,
            server_salt: SERVER_SALT,
            session_id: SESSION_ID,
            msg_id: MSG_ID,
            seq_no: SEQ_NO,
            body: b"abc",
            client_to_server: true,
            padding: None,
        })
        .unwrap_err();
        assert!(error.to_string().contains("divisible by 4"));
    }

    #[test]
    /// Exercises padding-length boundary and alignment failures.
    fn padding_predicate_rejects_boundary_and_isolated_invalid_lengths() {
        Python::initialize();
        for padding_len in [8, 11, 1025, 1028] {
            let error = validate_padding(ENVELOPE_HEADER_LEN, &vec![0; padding_len]).unwrap_err();
            assert!(error.to_string().contains("padding"));
        }
    }

    /// Returns a deterministic 256-byte authentication-key fixture.
    fn auth_key() -> Vec<u8> {
        (0..=255).collect()
    }
}

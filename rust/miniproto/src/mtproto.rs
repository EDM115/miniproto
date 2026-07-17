use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;

use crate::crypto::{
    AES_BLOCK_SIZE, detach_if_large, mtproto_auth_key_id_raw, mtproto_decrypt_payload_raw,
    mtproto_encrypt_payload_raw, validate_auth_key,
};
use crate::tl::read_fixed;

const ENCRYPTED_PACKET_HEADER_LEN: usize = 24;
const ENVELOPE_HEADER_LEN: usize = 32;
const MIN_PADDING_LEN: usize = 12;
const MAX_PADDING_LEN: usize = 1024;

#[derive(Debug, PartialEq, Eq)]
pub(crate) struct DecodedEncryptedMessage {
    pub auth_key_id: Vec<u8>,
    pub server_salt: u64,
    pub session_id: u64,
    pub msg_id: i64,
    pub seq_no: i32,
    pub body: Vec<u8>,
    pub padding: Vec<u8>,
}

pub(crate) struct EnvelopeEncodeInput<'a> {
    pub auth_key: &'a [u8],
    pub server_salt: u64,
    pub session_id: u64,
    pub msg_id: i64,
    pub seq_no: i32,
    pub body: &'a [u8],
    pub client_to_server: bool,
    pub padding: Option<&'a [u8]>,
}

type PyDecodedEnvelope = (Vec<u8>, u64, u64, i64, i32, Vec<u8>, Vec<u8>);

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mtproto_encode_message, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_decode_message, m)?)?;
    Ok(())
}

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

pub(crate) fn mtproto_encode_message_raw(input: EnvelopeEncodeInput<'_>) -> PyResult<Vec<u8>> {
    validate_auth_key(input.auth_key)?;
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

fn random_padding(plaintext_len: usize) -> PyResult<Vec<u8>> {
    let mut padding = vec![0; padding_len(plaintext_len)];
    getrandom::fill(&mut padding)
        .map_err(|error| PyValueError::new_err(format!("OS random failed: {error}")))?;
    Ok(padding)
}

fn padding_len(plaintext_len: usize) -> usize {
    MIN_PADDING_LEN
        + (AES_BLOCK_SIZE - ((plaintext_len + MIN_PADDING_LEN) % AES_BLOCK_SIZE)) % AES_BLOCK_SIZE
}

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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::crypto::mtproto_auth_key_id_raw;

    const SERVER_SALT: u64 = 0x0102_0304_0506_0708;
    const SESSION_ID: u64 = 0x1112_1314_1516_1718;
    const MSG_ID: i64 = 0x2122_2324_2526_2728;
    const SEQ_NO: i32 = 3;

    #[test]
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
    fn padding_predicate_rejects_boundary_and_isolated_invalid_lengths() {
        Python::initialize();
        for padding_len in [8, 11, 1025, 1028] {
            let error = validate_padding(ENVELOPE_HEADER_LEN, &vec![0; padding_len]).unwrap_err();
            assert!(error.to_string().contains("padding"));
        }
    }

    fn auth_key() -> Vec<u8> {
        (0..=255).collect()
    }
}

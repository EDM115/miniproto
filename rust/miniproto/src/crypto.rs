use aes::Aes256;
use cipher::{BlockCipherDecrypt, BlockCipherEncrypt, KeyInit};
use pyo3::exceptions::PyValueError;
use pyo3::marker::Ungil;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;
use sha1::Sha1;
use sha2::{Digest, Sha256};

pub(crate) const AES_BLOCK_SIZE: usize = 16;
pub(crate) const MT_PROTO_AUTH_KEY_SIZE: usize = 256;
pub(crate) const MT_PROTO_MSG_KEY_SIZE: usize = 16;
pub(crate) const GIL_RELEASE_THRESHOLD_BYTES: usize = 4 * 1024;

pub(crate) fn detach_if_large<T, F>(py: Python<'_>, work_bytes: usize, f: F) -> T
where
    T: Ungil,
    F: Ungil + FnOnce() -> T,
{
    if work_bytes > GIL_RELEASE_THRESHOLD_BYTES {
        py.detach(f)
    } else {
        f()
    }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(native_available, m)?)?;
    m.add_function(wrap_pyfunction!(sha1_digest, m)?)?;
    m.add_function(wrap_pyfunction!(sha256_digest, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_auth_key_id, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_message_key, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_derive_aes_key_iv, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_encrypt_payload, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_decrypt_payload, m)?)?;
    m.add_function(wrap_pyfunction!(xor_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_ige_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_ige_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_ctr_crypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_cbc_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_cbc_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(pq_factorize, m)?)?;
    Ok(())
}

#[pyfunction]
fn native_available() -> bool {
    true
}

#[pyfunction]
fn sha1_digest(py: Python<'_>, data: Vec<u8>) -> Vec<u8> {
    detach_if_large(py, data.len(), || sha1_digest_raw(&data))
}

#[pyfunction]
fn sha256_digest(py: Python<'_>, data: Vec<u8>) -> Vec<u8> {
    detach_if_large(py, data.len(), || sha256_digest_raw(&data))
}

#[pyfunction]
fn mtproto_auth_key_id(auth_key: &[u8]) -> PyResult<Vec<u8>> {
    mtproto_auth_key_id_raw(auth_key)
}

#[pyfunction]
fn mtproto_message_key(
    py: Python<'_>,
    auth_key: Vec<u8>,
    plaintext_with_padding: Vec<u8>,
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    let work_bytes = auth_key.len() + plaintext_with_padding.len();
    detach_if_large(py, work_bytes, move || {
        validate_auth_key(&auth_key)?;
        Ok(mtproto_message_key_raw(
            &auth_key,
            &plaintext_with_padding,
            client_to_server,
        ))
    })
}

#[pyfunction]
fn mtproto_derive_aes_key_iv(
    py: Python<'_>,
    auth_key: Vec<u8>,
    msg_key: Vec<u8>,
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>)> {
    let work_bytes = auth_key.len() + msg_key.len();
    detach_if_large(py, work_bytes, move || {
        validate_auth_key(&auth_key)?;
        validate_msg_key(&msg_key)?;
        Ok(mtproto_derive_aes_key_iv_raw(
            &auth_key,
            &msg_key,
            client_to_server,
        ))
    })
}

#[pyfunction]
fn mtproto_encrypt_payload(
    py: Python<'_>,
    auth_key: Vec<u8>,
    plaintext_with_padding: Vec<u8>,
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)> {
    let work_bytes = auth_key.len() + plaintext_with_padding.len();
    detach_if_large(py, work_bytes, move || {
        mtproto_encrypt_payload_raw(&auth_key, &plaintext_with_padding, client_to_server)
    })
}

#[pyfunction]
fn mtproto_decrypt_payload(
    py: Python<'_>,
    auth_key: Vec<u8>,
    msg_key: Vec<u8>,
    ciphertext: Vec<u8>,
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    let work_bytes = auth_key.len() + msg_key.len() + ciphertext.len();
    detach_if_large(py, work_bytes, move || {
        mtproto_decrypt_payload_raw(&auth_key, &msg_key, &ciphertext, client_to_server)
    })
}

#[pyfunction]
fn xor_bytes(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>> {
    xor_bytes_raw(left, right)
}

#[pyfunction]
fn aes_256_ige_encrypt(
    py: Python<'_>,
    plaintext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = plaintext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_ige_encrypt_raw(&plaintext, &key, &iv)
    })
}

#[pyfunction]
fn aes_256_ige_decrypt(
    py: Python<'_>,
    ciphertext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = ciphertext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_ige_decrypt_raw(&ciphertext, &key, &iv)
    })
}

#[pyfunction]
fn aes_256_cbc_encrypt(
    py: Python<'_>,
    plaintext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = plaintext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_cbc_encrypt_raw(&plaintext, &key, &iv)
    })
}

#[pyfunction]
fn aes_256_cbc_decrypt(
    py: Python<'_>,
    ciphertext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = ciphertext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_cbc_decrypt_raw(&ciphertext, &key, &iv)
    })
}

#[pyfunction]
fn aes_256_ctr_crypt(
    py: Python<'_>,
    data: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = data.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_ctr_crypt_raw(&data, &key, &iv)
    })
}

#[pyfunction]
fn pq_factorize(py: Python<'_>, pq: u64) -> PyResult<(u64, u64)> {
    detach_if_large(py, 8 * 1024, move || pq_factorize_raw(pq))
}

pub(crate) fn sha1_digest_raw(data: &[u8]) -> Vec<u8> {
    Sha1::digest(data).to_vec()
}

pub(crate) fn sha256_digest_raw(data: &[u8]) -> Vec<u8> {
    Sha256::digest(data).to_vec()
}

pub(crate) fn mtproto_auth_key_id_raw(auth_key: &[u8]) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    let digest = Sha1::digest(auth_key);
    Ok(digest[12..20].to_vec())
}

pub(crate) fn mtproto_message_key_raw(
    auth_key: &[u8],
    plaintext_with_padding: &[u8],
    client_to_server: bool,
) -> Vec<u8> {
    let x = direction_offset(client_to_server);
    let mut hasher = Sha256::new();
    hasher.update(&auth_key[88 + x..120 + x]);
    hasher.update(plaintext_with_padding);
    let digest = hasher.finalize();
    digest[8..24].to_vec()
}

pub(crate) fn mtproto_derive_aes_key_iv_raw(
    auth_key: &[u8],
    msg_key: &[u8],
    client_to_server: bool,
) -> (Vec<u8>, Vec<u8>) {
    let x = direction_offset(client_to_server);
    let mut hasher_a = Sha256::new();
    hasher_a.update(msg_key);
    hasher_a.update(&auth_key[x..x + 36]);
    let sha256_a = hasher_a.finalize();

    let mut hasher_b = Sha256::new();
    hasher_b.update(&auth_key[40 + x..76 + x]);
    hasher_b.update(msg_key);
    let sha256_b = hasher_b.finalize();

    let mut aes_key = Vec::with_capacity(32);
    aes_key.extend_from_slice(&sha256_a[..8]);
    aes_key.extend_from_slice(&sha256_b[8..24]);
    aes_key.extend_from_slice(&sha256_a[24..32]);

    let mut aes_iv = Vec::with_capacity(32);
    aes_iv.extend_from_slice(&sha256_b[..8]);
    aes_iv.extend_from_slice(&sha256_a[8..24]);
    aes_iv.extend_from_slice(&sha256_b[24..32]);
    (aes_key, aes_iv)
}

pub(crate) fn mtproto_encrypt_payload_raw(
    auth_key: &[u8],
    plaintext_with_padding: &[u8],
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)> {
    validate_auth_key(auth_key)?;
    validate_block_multiple(plaintext_with_padding)?;
    let auth_key_id = mtproto_auth_key_id_raw(auth_key)?;
    let msg_key = mtproto_message_key_raw(auth_key, plaintext_with_padding, client_to_server);
    let (aes_key, aes_iv) = mtproto_derive_aes_key_iv_raw(auth_key, &msg_key, client_to_server);
    let ciphertext = aes_256_ige_encrypt_raw(plaintext_with_padding, &aes_key, &aes_iv)?;
    Ok((auth_key_id, msg_key, ciphertext))
}

pub(crate) fn mtproto_decrypt_payload_raw(
    auth_key: &[u8],
    msg_key: &[u8],
    ciphertext: &[u8],
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    validate_msg_key(msg_key)?;
    validate_block_multiple(ciphertext)?;
    let (aes_key, aes_iv) = mtproto_derive_aes_key_iv_raw(auth_key, msg_key, client_to_server);
    let plaintext_with_padding = aes_256_ige_decrypt_raw(ciphertext, &aes_key, &aes_iv)?;
    let expected_msg_key =
        mtproto_message_key_raw(auth_key, &plaintext_with_padding, client_to_server);
    if expected_msg_key.as_slice() != msg_key {
        return Err(PyValueError::new_err("MTProto msg_key verification failed"));
    }
    Ok(plaintext_with_padding)
}

pub(crate) fn xor_bytes_raw(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>> {
    if left.len() != right.len() {
        return Err(PyValueError::new_err(
            "xor inputs must have the same length",
        ));
    }
    Ok(left.iter().zip(right.iter()).map(|(a, b)| a ^ b).collect())
}

pub(crate) fn aes_256_ige_encrypt_raw(
    plaintext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_ige_iv(iv)?;
    validate_block_multiple(plaintext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous_cipher: [u8; AES_BLOCK_SIZE] = iv[..AES_BLOCK_SIZE]
        .try_into()
        .expect("validated IV length");
    let mut previous_plain: [u8; AES_BLOCK_SIZE] = iv[AES_BLOCK_SIZE..]
        .try_into()
        .expect("validated IV length");
    let mut output = Vec::with_capacity(plaintext.len());
    for block in plaintext.chunks_exact(AES_BLOCK_SIZE) {
        let plain_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut mixed = xor_block(&plain_block, &previous_cipher);
        cipher.encrypt_block((&mut mixed).into());
        let cipher_block = xor_block(&mixed, &previous_plain);
        output.extend_from_slice(&cipher_block);
        previous_cipher = cipher_block;
        previous_plain = plain_block;
    }
    Ok(output)
}

pub(crate) fn aes_256_ige_decrypt_raw(
    ciphertext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_ige_iv(iv)?;
    validate_block_multiple(ciphertext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous_cipher: [u8; AES_BLOCK_SIZE] = iv[..AES_BLOCK_SIZE]
        .try_into()
        .expect("validated IV length");
    let mut previous_plain: [u8; AES_BLOCK_SIZE] = iv[AES_BLOCK_SIZE..]
        .try_into()
        .expect("validated IV length");
    let mut output = Vec::with_capacity(ciphertext.len());
    for block in ciphertext.chunks_exact(AES_BLOCK_SIZE) {
        let cipher_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut mixed = xor_block(&cipher_block, &previous_plain);
        cipher.decrypt_block((&mut mixed).into());
        let plain_block = xor_block(&mixed, &previous_cipher);
        output.extend_from_slice(&plain_block);
        previous_cipher = cipher_block;
        previous_plain = plain_block;
    }
    Ok(output)
}

pub(crate) fn aes_256_cbc_encrypt_raw(
    plaintext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_cbc_ctr_iv(iv)?;
    validate_block_multiple(plaintext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous: [u8; AES_BLOCK_SIZE] = iv.try_into().expect("validated IV length");
    let mut output = Vec::with_capacity(plaintext.len());
    for block in plaintext.chunks_exact(AES_BLOCK_SIZE) {
        let plain_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut cipher_block = xor_block(&plain_block, &previous);
        cipher.encrypt_block((&mut cipher_block).into());
        output.extend_from_slice(&cipher_block);
        previous = cipher_block;
    }
    Ok(output)
}

pub(crate) fn aes_256_cbc_decrypt_raw(
    ciphertext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_cbc_ctr_iv(iv)?;
    validate_block_multiple(ciphertext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous: [u8; AES_BLOCK_SIZE] = iv.try_into().expect("validated IV length");
    let mut output = Vec::with_capacity(ciphertext.len());
    for block in ciphertext.chunks_exact(AES_BLOCK_SIZE) {
        let cipher_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut plain_block = cipher_block;
        cipher.decrypt_block((&mut plain_block).into());
        plain_block = xor_block(&plain_block, &previous);
        output.extend_from_slice(&plain_block);
        previous = cipher_block;
    }
    Ok(output)
}

pub(crate) fn aes_256_ctr_crypt_raw(data: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_cbc_ctr_iv(iv)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut counter: [u8; AES_BLOCK_SIZE] = iv.try_into().expect("validated IV length");
    let mut output = Vec::with_capacity(data.len());
    for block in data.chunks(AES_BLOCK_SIZE) {
        let mut stream_block = counter;
        cipher.encrypt_block((&mut stream_block).into());
        output.extend(block.iter().zip(stream_block.iter()).map(|(a, b)| a ^ b));
        increment_counter(&mut counter);
    }
    Ok(output)
}

fn pq_factorize_raw(pq: u64) -> PyResult<(u64, u64)> {
    if pq < 4 {
        return Err(PyValueError::new_err("pq must be a composite integer >= 4"));
    }
    let factor = factor_u64(pq);
    if factor == 1 || factor == pq {
        return Err(PyValueError::new_err("pq must be composite"));
    }
    let other = pq / factor;
    Ok(if factor <= other {
        (factor, other)
    } else {
        (other, factor)
    })
}

pub(crate) fn validate_auth_key(auth_key: &[u8]) -> PyResult<()> {
    if auth_key.len() != MT_PROTO_AUTH_KEY_SIZE {
        return Err(PyValueError::new_err("MTProto auth_key must be 256 bytes"));
    }
    Ok(())
}

pub(crate) fn validate_msg_key(msg_key: &[u8]) -> PyResult<()> {
    if msg_key.len() != MT_PROTO_MSG_KEY_SIZE {
        return Err(PyValueError::new_err("MTProto msg_key must be 16 bytes"));
    }
    Ok(())
}

pub(crate) fn validate_block_multiple(data: &[u8]) -> PyResult<()> {
    if !data.len().is_multiple_of(AES_BLOCK_SIZE) {
        return Err(PyValueError::new_err(
            "AES block mode input length must be a multiple of 16 bytes",
        ));
    }
    Ok(())
}

fn validate_aes_key(key: &[u8]) -> PyResult<()> {
    if key.len() != 32 {
        return Err(PyValueError::new_err("AES-256 key must be 32 bytes"));
    }
    Ok(())
}

fn validate_ige_iv(iv: &[u8]) -> PyResult<()> {
    if iv.len() != 32 {
        return Err(PyValueError::new_err("AES-IGE IV must be 32 bytes"));
    }
    Ok(())
}

fn validate_cbc_ctr_iv(iv: &[u8]) -> PyResult<()> {
    if iv.len() != AES_BLOCK_SIZE {
        return Err(PyValueError::new_err("AES IV must be 16 bytes"));
    }
    Ok(())
}

fn direction_offset(client_to_server: bool) -> usize {
    if client_to_server { 0 } else { 8 }
}

fn xor_block(left: &[u8; AES_BLOCK_SIZE], right: &[u8; AES_BLOCK_SIZE]) -> [u8; AES_BLOCK_SIZE] {
    let mut output = [0_u8; AES_BLOCK_SIZE];
    for index in 0..AES_BLOCK_SIZE {
        output[index] = left[index] ^ right[index];
    }
    output
}

fn increment_counter(counter: &mut [u8; AES_BLOCK_SIZE]) {
    for byte in counter.iter_mut().rev() {
        let (next, carry) = byte.overflowing_add(1);
        *byte = next;
        if !carry {
            break;
        }
    }
}

fn gcd(mut left: u64, mut right: u64) -> u64 {
    while right != 0 {
        let remainder = left % right;
        left = right;
        right = remainder;
    }
    left
}

fn mul_mod(left: u64, right: u64, modulus: u64) -> u64 {
    (((left as u128) * (right as u128)) % (modulus as u128)) as u64
}

fn pow_mod(mut base: u64, mut exponent: u64, modulus: u64) -> u64 {
    let mut result = 1_u64;
    while exponent > 0 {
        if exponent & 1 == 1 {
            result = mul_mod(result, base, modulus);
        }
        base = mul_mod(base, base, modulus);
        exponent >>= 1;
    }
    result
}

fn is_prime_u64(value: u64) -> bool {
    if value < 2 {
        return false;
    }
    for small in [2_u64, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
        if value == small {
            return true;
        }
        if value.is_multiple_of(small) {
            return false;
        }
    }
    let mut d = value - 1;
    let mut s = 0_u32;
    while d.is_multiple_of(2) {
        d /= 2;
        s += 1;
    }
    for base in [2_u64, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
        if base >= value {
            continue;
        }
        let mut x = pow_mod(base, d, value);
        if x == 1 || x == value - 1 {
            continue;
        }
        let mut witnessed = false;
        for _ in 1..s {
            x = mul_mod(x, x, value);
            if x == value - 1 {
                witnessed = true;
                break;
            }
        }
        if !witnessed {
            return false;
        }
    }
    true
}

fn factor_u64(value: u64) -> u64 {
    if value.is_multiple_of(2) {
        return 2;
    }
    if is_prime_u64(value) {
        return value;
    }
    let mut c = 1_u64;
    loop {
        let mut x = 2_u64;
        let mut y = 2_u64;
        let mut d = 1_u64;
        let step = |input: u64, constant: u64| -> u64 {
            (mul_mod(input, input, value) + constant) % value
        };
        for _ in 0..100_000 {
            x = step(x, c);
            y = step(step(y, c), c);
            d = gcd(x.abs_diff(y), value);
            if d > 1 {
                break;
            }
        }
        if d > 1 && d < value {
            return d;
        }
        c = c.wrapping_add(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sha_and_auth_key_outputs_are_stable() {
        assert_eq!(
            sha1_digest_raw(b"abc"),
            vec![
                0xa9, 0x99, 0x3e, 0x36, 0x47, 0x06, 0x81, 0x6a, 0xba, 0x3e, 0x25, 0x71, 0x78, 0x50,
                0xc2, 0x6c, 0x9c, 0xd0, 0xd8, 0x9d,
            ]
        );
        assert_eq!(
            sha256_digest_raw(b"abc"),
            vec![
                0xba, 0x78, 0x16, 0xbf, 0x8f, 0x01, 0xcf, 0xea, 0x41, 0x41, 0x40, 0xde, 0x5d, 0xae,
                0x22, 0x23, 0xb0, 0x03, 0x61, 0xa3, 0x96, 0x17, 0x7a, 0x9c, 0xb4, 0x10, 0xff, 0x61,
                0xf2, 0x00, 0x15, 0xad,
            ]
        );
        assert_eq!(
            mtproto_auth_key_id_raw(&auth_key()).unwrap(),
            vec![0x32, 0xd1, 0x58, 0x6e, 0xa4, 0x57, 0xdf, 0xc8]
        );
    }

    #[test]
    fn aes_ige_roundtrips() {
        let plaintext = bytes_mod(64, 1);
        let key = bytes_mod(32, 2);
        let iv = bytes_mod(32, 3);
        let ciphertext = aes_256_ige_encrypt_raw(&plaintext, &key, &iv).unwrap();
        assert_ne!(ciphertext, plaintext);
        assert_eq!(
            aes_256_ige_decrypt_raw(&ciphertext, &key, &iv).unwrap(),
            plaintext
        );
    }

    #[test]
    fn aes_ctr_is_symmetric() {
        let plaintext = bytes_mod(65, 4);
        let key = bytes_mod(32, 5);
        let iv = bytes_mod(16, 6);
        let ciphertext = aes_256_ctr_crypt_raw(&plaintext, &key, &iv).unwrap();
        assert_ne!(ciphertext, plaintext);
        assert_eq!(
            aes_256_ctr_crypt_raw(&ciphertext, &key, &iv).unwrap(),
            plaintext
        );
    }

    #[test]
    fn mtproto_payload_encrypt_decrypt_roundtrips() {
        let auth_key = auth_key();
        let plaintext = vec![0x58; 64];
        let (auth_key_id, msg_key, ciphertext) =
            mtproto_encrypt_payload_raw(&auth_key, &plaintext, true).unwrap();
        assert_eq!(auth_key_id, mtproto_auth_key_id_raw(&auth_key).unwrap());
        assert_eq!(
            mtproto_decrypt_payload_raw(&auth_key, &msg_key, &ciphertext, true).unwrap(),
            plaintext
        );
    }

    #[test]
    fn xor_and_pq_helpers_work() {
        assert_eq!(
            xor_bytes_raw(&[0x0f, 0xf0], &[0xf0, 0x0f]).unwrap(),
            vec![0xff, 0xff]
        );
        assert_eq!(
            pq_factorize_raw(1_000_003 * 1_000_033).unwrap(),
            (1_000_003, 1_000_033)
        );
    }

    fn auth_key() -> Vec<u8> {
        (0..=255).collect()
    }

    fn bytes_mod(len: usize, multiplier: u8) -> Vec<u8> {
        (0..len)
            .map(|index| (index as u8).wrapping_mul(multiplier))
            .collect()
    }
}

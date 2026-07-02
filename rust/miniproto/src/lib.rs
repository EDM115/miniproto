use aes::Aes256;
use cipher::{BlockCipherDecrypt, BlockCipherEncrypt, KeyInit};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyModule};
use sha1::Sha1;
use sha2::{Digest, Sha256};

const AES_BLOCK_SIZE: usize = 16;
const MT_PROTO_AUTH_KEY_SIZE: usize = 256;
const MT_PROTO_MSG_KEY_SIZE: usize = 16;
const TL_VECTOR_CONSTRUCTOR_ID: u32 = 0x1CB5C415;

#[pyfunction]
fn native_available() -> bool {
    true
}

#[pyfunction]
fn sha1_digest(data: &[u8]) -> Vec<u8> {
    Sha1::digest(data).to_vec()
}

#[pyfunction]
fn sha256_digest(data: &[u8]) -> Vec<u8> {
    Sha256::digest(data).to_vec()
}

#[pyfunction]
fn mtproto_auth_key_id(auth_key: &[u8]) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    let digest = Sha1::digest(auth_key);
    Ok(digest[12..20].to_vec())
}

#[pyfunction]
fn mtproto_message_key(
    auth_key: &[u8],
    plaintext_with_padding: &[u8],
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    Ok(mtproto_message_key_raw(
        auth_key,
        plaintext_with_padding,
        client_to_server,
    ))
}

#[pyfunction]
fn mtproto_derive_aes_key_iv(
    auth_key: &[u8],
    msg_key: &[u8],
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>)> {
    validate_auth_key(auth_key)?;
    validate_msg_key(msg_key)?;
    Ok(mtproto_derive_aes_key_iv_raw(
        auth_key,
        msg_key,
        client_to_server,
    ))
}

#[pyfunction]
fn mtproto_encrypt_payload(
    auth_key: &[u8],
    plaintext_with_padding: &[u8],
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)> {
    validate_auth_key(auth_key)?;
    validate_block_multiple(plaintext_with_padding)?;
    let auth_key_id = mtproto_auth_key_id(auth_key)?;
    let msg_key = mtproto_message_key_raw(auth_key, plaintext_with_padding, client_to_server);
    let (aes_key, aes_iv) = mtproto_derive_aes_key_iv_raw(auth_key, &msg_key, client_to_server);
    let ciphertext = aes_256_ige_encrypt(plaintext_with_padding, &aes_key, &aes_iv)?;
    Ok((auth_key_id, msg_key, ciphertext))
}

#[pyfunction]
fn mtproto_decrypt_payload(
    auth_key: &[u8],
    msg_key: &[u8],
    ciphertext: &[u8],
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    validate_msg_key(msg_key)?;
    validate_block_multiple(ciphertext)?;
    let (aes_key, aes_iv) = mtproto_derive_aes_key_iv_raw(auth_key, msg_key, client_to_server);
    let plaintext_with_padding = aes_256_ige_decrypt(ciphertext, &aes_key, &aes_iv)?;
    let expected_msg_key =
        mtproto_message_key_raw(auth_key, &plaintext_with_padding, client_to_server);
    if expected_msg_key.as_slice() != msg_key {
        return Err(PyValueError::new_err("MTProto msg_key verification failed"));
    }
    Ok(plaintext_with_padding)
}

#[pyfunction]
fn xor_bytes(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>> {
    if left.len() != right.len() {
        return Err(PyValueError::new_err(
            "xor inputs must have the same length",
        ));
    }
    Ok(left.iter().zip(right.iter()).map(|(a, b)| a ^ b).collect())
}

#[pyfunction]
fn aes_256_ige_encrypt(plaintext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
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

#[pyfunction]
fn aes_256_ige_decrypt(ciphertext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
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

#[pyfunction]
fn aes_256_cbc_encrypt(plaintext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
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

#[pyfunction]
fn aes_256_cbc_decrypt(ciphertext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
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

#[pyfunction]
fn aes_256_ctr_crypt(data: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
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

#[pyfunction]
fn pq_factorize(pq: u64) -> PyResult<(u64, u64)> {
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

#[pyfunction]
fn tl_encode_int(value: i32) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_int(data: &[u8], offset: usize) -> PyResult<(i32, usize)> {
    let bytes = read_fixed::<4>(data, offset)?;
    Ok((i32::from_le_bytes(bytes), offset + 4))
}

#[pyfunction]
fn tl_encode_uint(value: u32) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_uint(data: &[u8], offset: usize) -> PyResult<(u32, usize)> {
    let bytes = read_fixed::<4>(data, offset)?;
    Ok((u32::from_le_bytes(bytes), offset + 4))
}

#[pyfunction]
fn tl_encode_long(value: i64) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_long(data: &[u8], offset: usize) -> PyResult<(i64, usize)> {
    let bytes = read_fixed::<8>(data, offset)?;
    Ok((i64::from_le_bytes(bytes), offset + 8))
}

#[pyfunction]
fn tl_encode_int128(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    py_int_to_le_bytes(value, 16)
}

#[pyfunction]
fn tl_decode_int128(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)> {
    let value = py_int_from_le_bytes(py, read_slice(data, offset, 16)?)?;
    Ok((value, offset + 16))
}

#[pyfunction]
fn tl_encode_int256(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    py_int_to_le_bytes(value, 32)
}

#[pyfunction]
fn tl_decode_int256(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)> {
    let value = py_int_from_le_bytes(py, read_slice(data, offset, 32)?)?;
    Ok((value, offset + 32))
}

#[pyfunction]
fn tl_encode_double(value: f64) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_double(data: &[u8], offset: usize) -> PyResult<(f64, usize)> {
    let bytes = read_fixed::<8>(data, offset)?;
    Ok((f64::from_le_bytes(bytes), offset + 8))
}

#[pyfunction]
fn tl_encode_bytes(value: &[u8]) -> Vec<u8> {
    encode_tl_bytes(value)
}

#[pyfunction]
fn tl_decode_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)> {
    decode_tl_bytes(data, offset)
}

#[pyfunction]
fn tl_encode_string(value: &str) -> Vec<u8> {
    encode_tl_bytes(value.as_bytes())
}

#[pyfunction]
fn tl_decode_string(data: &[u8], offset: usize) -> PyResult<(String, usize)> {
    let (bytes, new_offset) = decode_tl_bytes(data, offset)?;
    String::from_utf8(bytes)
        .map(|value| (value, new_offset))
        .map_err(|_| PyValueError::new_err("TL string payload is not valid UTF-8"))
}

#[pyfunction]
fn tl_encode_int_vector(values: Vec<i32>) -> Vec<u8> {
    let mut output = Vec::with_capacity(8 + values.len() * 4);
    output.extend_from_slice(&TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes());
    output.extend_from_slice(&(values.len() as i32).to_le_bytes());
    for value in values {
        output.extend_from_slice(&value.to_le_bytes());
    }
    output
}

#[pyfunction]
fn tl_decode_int_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i32>, usize)> {
    validate_vector_constructor(data, offset)?;
    let count_bytes = read_fixed::<4>(data, offset + 4)?;
    let count = i32::from_le_bytes(count_bytes);
    if count < 0 {
        return Err(PyValueError::new_err("TL vector count cannot be negative"));
    }
    let count = count as usize;
    let mut next_offset = offset + 8;
    let mut values = Vec::with_capacity(count);
    for _ in 0..count {
        let bytes = read_fixed::<4>(data, next_offset)?;
        values.push(i32::from_le_bytes(bytes));
        next_offset += 4;
    }
    Ok((values, next_offset))
}

#[pyfunction]
fn tl_encode_long_vector(values: Vec<i64>) -> Vec<u8> {
    let mut output = Vec::with_capacity(8 + values.len() * 8);
    output.extend_from_slice(&TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes());
    output.extend_from_slice(&(values.len() as i32).to_le_bytes());
    for value in values {
        output.extend_from_slice(&value.to_le_bytes());
    }
    output
}

#[pyfunction]
fn tl_decode_long_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i64>, usize)> {
    validate_vector_constructor(data, offset)?;
    let count_bytes = read_fixed::<4>(data, offset + 4)?;
    let count = i32::from_le_bytes(count_bytes);
    if count < 0 {
        return Err(PyValueError::new_err("TL vector count cannot be negative"));
    }
    let count = count as usize;
    let mut next_offset = offset + 8;
    let mut values = Vec::with_capacity(count);
    for _ in 0..count {
        let bytes = read_fixed::<8>(data, next_offset)?;
        values.push(i64::from_le_bytes(bytes));
        next_offset += 8;
    }
    Ok((values, next_offset))
}

fn validate_auth_key(auth_key: &[u8]) -> PyResult<()> {
    if auth_key.len() != MT_PROTO_AUTH_KEY_SIZE {
        return Err(PyValueError::new_err("MTProto auth_key must be 256 bytes"));
    }
    Ok(())
}

fn validate_msg_key(msg_key: &[u8]) -> PyResult<()> {
    if msg_key.len() != MT_PROTO_MSG_KEY_SIZE {
        return Err(PyValueError::new_err("MTProto msg_key must be 16 bytes"));
    }
    Ok(())
}

fn direction_offset(client_to_server: bool) -> usize {
    if client_to_server { 0 } else { 8 }
}

fn mtproto_message_key_raw(
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

fn mtproto_derive_aes_key_iv_raw(
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

fn validate_block_multiple(data: &[u8]) -> PyResult<()> {
    if !data.len().is_multiple_of(AES_BLOCK_SIZE) {
        return Err(PyValueError::new_err(
            "AES block mode input length must be a multiple of 16 bytes",
        ));
    }
    Ok(())
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

fn read_slice(data: &[u8], offset: usize, length: usize) -> PyResult<&[u8]> {
    data.get(offset..offset.saturating_add(length))
        .ok_or_else(|| {
            PyValueError::new_err("TL data ended before the requested value could be decoded")
        })
}

fn read_fixed<const N: usize>(data: &[u8], offset: usize) -> PyResult<[u8; N]> {
    read_slice(data, offset, N).map(|slice| slice.try_into().expect("slice length checked"))
}

fn py_int_to_le_bytes(value: &Bound<'_, PyAny>, width: usize) -> PyResult<Vec<u8>> {
    let bytes = value
        .call_method1("to_bytes", (width, "little"))?
        .extract::<Vec<u8>>()?;
    if bytes.len() != width {
        return Err(PyValueError::new_err("integer width mismatch"));
    }
    Ok(bytes)
}

fn py_int_from_le_bytes(py: Python<'_>, bytes: &[u8]) -> PyResult<Py<PyAny>> {
    let builtins = PyModule::import(py, "builtins")?;
    let py_bytes = PyBytes::new(py, bytes);
    let value = builtins
        .getattr("int")?
        .call_method1("from_bytes", (py_bytes, "little"))?;
    Ok(value.unbind())
}

fn encode_tl_bytes(value: &[u8]) -> Vec<u8> {
    let length = value.len();
    let mut output = Vec::with_capacity(length + 8);
    if length <= 253 {
        output.push(length as u8);
    } else {
        output.push(254);
        output.extend_from_slice(&(length as u32).to_le_bytes()[..3]);
    }
    output.extend_from_slice(value);
    while output.len() % 4 != 0 {
        output.push(0);
    }
    output
}

fn decode_tl_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)> {
    let first = *data
        .get(offset)
        .ok_or_else(|| PyValueError::new_err("TL data ended before bytes length"))?;
    let (length, payload_offset) = if first == 254 {
        let length_bytes = read_slice(data, offset + 1, 3)?;
        let length =
            u32::from_le_bytes([length_bytes[0], length_bytes[1], length_bytes[2], 0]) as usize;
        (length, offset + 4)
    } else {
        (first as usize, offset + 1)
    };
    let payload = read_slice(data, payload_offset, length)?.to_vec();
    let mut next_offset = payload_offset + length;
    while next_offset % 4 != 0 {
        next_offset += 1;
    }
    if next_offset > data.len() {
        return Err(PyValueError::new_err("TL data ended before bytes padding"));
    }
    Ok((payload, next_offset))
}

fn validate_vector_constructor(data: &[u8], offset: usize) -> PyResult<()> {
    let bytes = read_fixed::<4>(data, offset)?;
    let constructor_id = u32::from_le_bytes(bytes);
    if constructor_id != TL_VECTOR_CONSTRUCTOR_ID {
        return Err(PyValueError::new_err(format!(
            "expected Vector constructor, got 0x{constructor_id:08x}",
        )));
    }
    Ok(())
}

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
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
    m.add_function(wrap_pyfunction!(tl_encode_int, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_uint, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_uint, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_long, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_long, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_int128, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int128, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_int256, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int256, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_double, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_double, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_string, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_string, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_int_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_long_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_long_vector, m)?)?;
    Ok(())
}

---
title: "miniproto.crypto"
description: "Public cryptographic primitives for MTProto and encrypted session storage."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.crypto"
source_path: "src/miniproto/crypto/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/__init__.py"
module: "miniproto.crypto"
---

## `miniproto.crypto`

Public cryptographic primitives for MTProto and encrypted session storage.

Exports preserve behavior across the optional Rust extension and fallback
implementations.  Individual wrappers document their backend dispatch,
cryptographic input constraints, and validation behavior.

## Public objects

- [`EncryptedPayload`](./mtproto/encryptedpayload/) — MTProto payload components produced by :func:`encrypt_payload`.
- [`auth_key_id`](./mtproto/auth-key-id/) — Return the MTProto auth-key identifier.
- [`decrypt_payload`](./mtproto/decrypt-payload/) — Verify an MTProto message key and decrypt its AES-IGE payload.
- [`derive_aes_key_iv`](./mtproto/derive-aes-key-iv/) — Derive the AES-256 key and 32-byte IGE IV required by MTProto 2.0.
- [`encrypt_payload`](./mtproto/encrypt-payload/) — Pad and AES-IGE-encrypt one MTProto payload.
- [`media_cbc_decrypt`](./mtproto/media-cbc-decrypt/) — Decrypt block-aligned AES-256-CBC media data without unpadding it.
- [`media_cbc_encrypt`](./mtproto/media-cbc-encrypt/) — Encrypt block-aligned media data with AES-256-CBC.
- [`media_ctr_crypt`](./mtproto/media-ctr-crypt/) — Apply AES-256-CTR to CDN/media bytes.
- [`message_key`](./mtproto/message-key/) — Derive the 16-byte MTProto 2.0 message key.
- [`aes_256_cbc_decrypt`](./native/aes-256-cbc-decrypt/) — Decrypt block-aligned AES-256-CBC bytes without unpadding.
- [`aes_256_cbc_encrypt`](./native/aes-256-cbc-encrypt/) — Encrypt block-aligned bytes with AES-256-CBC.
- [`aes_256_ctr_crypt`](./native/aes-256-ctr-crypt/) — Apply AES-256-CTR to bytes for encryption or decryption.
- [`aes_256_gcm_decrypt`](./native/aes-256-gcm-decrypt/) — Authenticate and decrypt AES-256-GCM session bytes.
- [`aes_256_gcm_decrypt_cryptography`](./native/aes-256-gcm-decrypt-cryptography/) — Authenticate and decrypt through the explicit ``cryptography`` AES-GCM path.
- [`aes_256_gcm_decrypt_native`](./native/aes-256-gcm-decrypt-native/) — Authenticate and decrypt with explicit compiled Rust AES-256-GCM.
- [`aes_256_gcm_encrypt`](./native/aes-256-gcm-encrypt/) — Encrypt and authenticate session bytes with AES-256-GCM.
- [`aes_256_gcm_encrypt_cryptography`](./native/aes-256-gcm-encrypt-cryptography/) — Encrypt and authenticate with the explicit ``cryptography`` AES-GCM path.
- [`aes_256_gcm_encrypt_native`](./native/aes-256-gcm-encrypt-native/) — Encrypt with the explicit compiled Rust AES-256-GCM capability.
- [`aes_256_ige_decrypt`](./native/aes-256-ige-decrypt/) — Decrypt block-aligned AES-256-IGE bytes.
- [`aes_256_ige_encrypt`](./native/aes-256-ige-encrypt/) — Encrypt block-aligned bytes with AES-256-IGE.
- [`mtproto_decode_message`](./native/mtproto-decode-message/) — Decrypt, authenticate, and parse an MTProto encrypted message.
- [`mtproto_encode_message`](./native/mtproto-encode-message/) — Build, pad, and encrypt a complete MTProto encrypted message.
- [`native_available`](./native/native-available/) — Report whether a complete bundled Rust backend was selected.
- [`pq_factorize`](./native/pq-factorize/) — Factor the composite integer used by the MTProto handshake.
- [`scrypt_derive`](./native/scrypt-derive/) — Derive key material with Scrypt through the available session backend.
- [`scrypt_derive_cryptography`](./native/scrypt-derive-cryptography/) — Derive Scrypt key material with the explicit ``cryptography`` backend.
- [`scrypt_derive_native`](./native/scrypt-derive-native/) — Derive Scrypt key material through explicit compiled Rust support.
- [`sha1_digest`](./native/sha1-digest/) — Compute a SHA-1 digest for MTProto compatibility.
- [`sha256_digest`](./native/sha256-digest/) — Compute a SHA-256 digest.
- [`xor_bytes`](./native/xor-bytes/) — Return the byte-wise XOR of equal-length inputs.

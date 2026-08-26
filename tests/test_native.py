from __future__ import annotations

import importlib
import logging
from types import SimpleNamespace
from typing import cast

import pytest

import miniproto._native_fallback as fallback
import miniproto.crypto.native as native_module
from miniproto.crypto import native_available, xor_bytes

_MT_PROTO_AUTH_KEY = bytes(range(256))


def _mutate_mtproto_envelope(body_len: int) -> bytes:
    packet = fallback.mtproto_encode_message(
        _MT_PROTO_AUTH_KEY, 1, 2, 3, 4, b"body", client_to_server=True, padding=b"\0" * 12
    )
    plaintext = bytearray(
        fallback.mtproto_decrypt_payload(_MT_PROTO_AUTH_KEY, packet[8:24], packet[24:], client_to_server=True)
    )
    plaintext[28:32] = body_len.to_bytes(4, "little", signed=True)
    auth_key_id, msg_key, ciphertext = fallback.mtproto_encrypt_payload(
        _MT_PROTO_AUTH_KEY, bytes(plaintext), client_to_server=True
    )
    return auth_key_id + msg_key + ciphertext


def test_xor_bytes_matches_expected_result() -> None:
    assert xor_bytes(b"\x0f\xf0", b"\xf0\x0f") == b"\xff\xff"


def test_xor_bytes_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError, match="same length"):
        xor_bytes(b"a", b"bb")


def test_native_available_returns_bool() -> None:
    assert isinstance(native_available(), bool)


@pytest.mark.parametrize(
    "decoder", [fallback.mtproto_decode_message, pytest.importorskip("miniproto._native").mtproto_decode_message]
)
def test_mtproto_decoder_rejects_wrong_envelope_auth_key_id(decoder) -> None:
    packet = fallback.mtproto_encode_message(
        _MT_PROTO_AUTH_KEY, 1, 2, 3, 4, b"body", client_to_server=True, padding=b"\0" * 12
    )
    wrong_auth_key_id = bytes(value ^ 0xFF for value in packet[:8])

    with pytest.raises(ValueError, match="auth_key_id"):
        decoder(_MT_PROTO_AUTH_KEY, wrong_auth_key_id + packet[8:], True)


@pytest.mark.parametrize(
    ("body_len", "error"), [(64, "body length is invalid"), (5, "body length must be divisible by 4")]
)
@pytest.mark.parametrize(
    "decoder", [fallback.mtproto_decode_message, pytest.importorskip("miniproto._native").mtproto_decode_message]
)
def test_mtproto_decoder_rejects_malformed_envelope_body_length(decoder, body_len: int, error: str) -> None:
    with pytest.raises(ValueError, match=error):
        decoder(_MT_PROTO_AUTH_KEY, _mutate_mtproto_envelope(body_len), True)


@pytest.mark.parametrize("padding_len", [8, 11, 1025, 1028])
def test_mtproto_padding_predicate_rejects_boundary_and_isolated_invalid_lengths(padding_len: int) -> None:
    with pytest.raises(ValueError, match="padding must be between 12 and 1024"):
        fallback._validate_mtproto_padding(32, b"\0" * padding_len)


def test_native_loader_falls_back_when_extension_import_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_import(name: str):
        if name == "miniproto._native":
            raise ImportError("native failed")
        return importlib.import_module(name)

    monkeypatch.setattr(native_module, "import_module", fake_import)
    impl, error = native_module._load_native_impl()
    assert impl.native_available() is False
    assert error == "ImportError: native failed"


def test_native_loader_falls_back_when_extension_is_incomplete(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_import(name: str):
        if name == "miniproto._native":
            return SimpleNamespace(native_available=lambda: True)
        return importlib.import_module(name)

    monkeypatch.setattr(native_module, "import_module", fake_import)
    impl, error = native_module._load_native_impl()
    assert impl.native_available() is False
    assert error is not None
    assert error.startswith("missing native symbols:")
    assert "sha1_digest" in error


def test_native_loader_keeps_extension_when_only_session_crypto_symbols_are_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    compiled = importlib.import_module("miniproto._native")

    class CompiledWithoutSessionCrypto:
        def __getattr__(self, name: str):
            if name in {"aes_256_gcm_encrypt", "aes_256_gcm_decrypt", "scrypt_derive"}:
                raise AttributeError(name)
            return getattr(compiled, name)

    partial = CompiledWithoutSessionCrypto()

    def fake_import(name: str):
        if name == "miniproto._native":
            return partial
        return importlib.import_module(name)

    monkeypatch.setattr(native_module, "import_module", fake_import)

    impl, error = native_module._load_native_impl()

    assert impl is partial
    assert error is None


def test_native_fallback_error_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR, logger="miniproto.crypto.native"):
        native_module._emit_native_fallback_error("missing native symbols: x")

    record = caplog.records[-1]
    event = cast(dict[str, object], record.__dict__["miniproto_event"])
    assert record.levelno == logging.ERROR
    assert event["event"] == "crypto.native.fallback"
    assert event["outcome"] == "fallback"
    assert event["error"] == "missing native symbols: x"


def test_native_loaded_event_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="miniproto.crypto.native"):
        native_module._emit_native_loaded(True)

    record = caplog.records[-1]
    event = cast(dict[str, object], record.__dict__["miniproto_event"])
    assert record.levelno == logging.INFO
    assert event["event"] == "crypto.native.loaded"
    assert event["backend"] == "rust"
    assert event["native_available"] is True


@pytest.mark.parametrize(("decoder_name", "width"), [("tl_decode_int_vector", 4), ("tl_decode_long_vector", 8)])
def test_fallback_vector_decoder_rejects_maximum_count_without_payload(decoder_name: str, width: int) -> None:
    del width
    decoder = getattr(fallback, decoder_name)
    data = (0x1CB5C415).to_bytes(4, "little") + (2**31 - 1).to_bytes(4, "little", signed=True)

    with pytest.raises(ValueError, match="vector count exceeds remaining payload"):
        decoder(data, 0)


@pytest.mark.parametrize(("decoder_name", "width"), [("tl_decode_int_vector", 4), ("tl_decode_long_vector", 8)])
def test_compiled_native_vector_decoder_rejects_maximum_count_without_payload(decoder_name: str, width: int) -> None:
    del width
    native = pytest.importorskip("miniproto._native")
    decoder = getattr(native, decoder_name)
    data = (0x1CB5C415).to_bytes(4, "little") + (2**31 - 1).to_bytes(4, "little", signed=True)

    with pytest.raises(ValueError, match="vector count exceeds remaining payload"):
        decoder(data, 0)


@pytest.mark.parametrize("decoder_name", ["tl_decode_int_vector", "tl_decode_long_vector"])
@pytest.mark.parametrize("offset", [-1, 1, 7, 2**63])
def test_compiled_native_vector_decoder_normalizes_invalid_offsets(decoder_name: str, offset: int) -> None:
    native = pytest.importorskip("miniproto._native")
    decoder = getattr(native, decoder_name)
    data = (0x1CB5C415).to_bytes(4, "little") + (0).to_bytes(4, "little", signed=True)

    with pytest.raises(ValueError, match="TL data ended before the requested value could be decoded"):
        decoder(data, offset)


def test_mtproto_encode_message_prefers_native_impl(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[bytes, bool, bytes | None]] = []

    class NativeImpl:
        def mtproto_encode_message(
            self,
            auth_key: bytes,
            server_salt: int,
            session_id: int,
            msg_id: int,
            seq_no: int,
            body: bytes,
            client_to_server: bool,
            padding: bytes | None,
        ) -> bytes:
            del auth_key, server_salt, session_id, msg_id, seq_no
            calls.append((body, client_to_server, padding))
            return b"native"

    class FallbackImpl:
        def mtproto_encode_message(
            self,
            auth_key: bytes,
            server_salt: int,
            session_id: int,
            msg_id: int,
            seq_no: int,
            body: bytes,
            client_to_server: bool,
            padding: bytes | None,
        ) -> bytes:
            del auth_key, server_salt, session_id, msg_id, seq_no, body, client_to_server, padding
            raise AssertionError("fallback encoder should not be used when native is loaded")

    monkeypatch.setattr(native_module, "_native_impl", NativeImpl())
    monkeypatch.setattr(native_module, "_fallback_impl", FallbackImpl())

    assert (
        native_module.mtproto_encode_message(
            b"k" * 256, 1, 2, 3, 4, b"payload", client_to_server=False, padding=b"\0" * 12
        )
        == b"native"
    )
    assert calls == [(b"payload", False, b"\0" * 12)]


def test_selected_session_crypto_falls_back_per_missing_native_capability(monkeypatch: pytest.MonkeyPatch) -> None:
    class PartialNative:
        @staticmethod
        def native_available() -> bool:
            return True

    class CryptographyImpl:
        @staticmethod
        def aes_256_gcm_encrypt(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
            del key, nonce, associated_data
            return b"cryptography:" + plaintext

        @staticmethod
        def scrypt_derive(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
            del password, salt, n, r, p
            return b"c" * length

    monkeypatch.setattr(native_module, "_native_impl", PartialNative())
    monkeypatch.setattr(native_module, "_fallback_impl", CryptographyImpl())

    assert native_module.aes_256_gcm_encrypt(b"payload", b"k" * 32, b"n" * 12, b"header") == b"cryptography:payload"
    assert native_module.scrypt_derive(b"password", b"salt", 2, 1, 1, 8) == b"c" * 8


def test_selected_session_crypto_prefers_available_native_capabilities(monkeypatch: pytest.MonkeyPatch) -> None:
    class NativeImpl:
        @staticmethod
        def native_available() -> bool:
            return True

        @staticmethod
        def aes_256_gcm_encrypt(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
            del key, nonce, associated_data
            return b"native:" + plaintext

        @staticmethod
        def scrypt_derive(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
            del password, salt, n, r, p
            return b"n" * length

    class CryptographyImpl:
        @staticmethod
        def aes_256_gcm_encrypt(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
            del plaintext, key, nonce, associated_data
            raise AssertionError("cryptography should not run when the native capability is available")

        @staticmethod
        def scrypt_derive(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
            del password, salt, n, r, p, length
            raise AssertionError("cryptography should not run when the native capability is available")

    monkeypatch.setattr(native_module, "_native_impl", NativeImpl())
    monkeypatch.setattr(native_module, "_fallback_impl", CryptographyImpl())

    assert native_module.aes_256_gcm_encrypt(b"payload", b"k" * 32, b"n" * 12, b"header") == b"native:payload"
    assert native_module.scrypt_derive(b"password", b"salt", 2, 1, 1, 8) == b"n" * 8


def test_selected_session_crypto_does_not_retry_native_operation_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    class NativeImpl:
        @staticmethod
        def native_available() -> bool:
            return True

        @staticmethod
        def aes_256_gcm_decrypt(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
            del ciphertext_and_tag, key, nonce, associated_data
            raise ValueError("AES-GCM authentication failed")

    class CryptographyImpl:
        @staticmethod
        def aes_256_gcm_decrypt(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
            del ciphertext_and_tag, key, nonce, associated_data
            raise AssertionError("cryptography must not retry a native authentication failure")

    monkeypatch.setattr(native_module, "_native_impl", NativeImpl())
    monkeypatch.setattr(native_module, "_fallback_impl", CryptographyImpl())

    with pytest.raises(ValueError, match="authentication failed"):
        native_module.aes_256_gcm_decrypt(b"ciphertext-and-tag", b"k" * 32, b"n" * 12, b"header")


def test_explicit_native_session_crypto_rejects_an_unavailable_capability(monkeypatch: pytest.MonkeyPatch) -> None:
    class UnavailableNative:
        @staticmethod
        def native_available() -> bool:
            return False

    monkeypatch.setattr(native_module, "_native_impl", UnavailableNative())

    with pytest.raises(RuntimeError, match="native session crypto capability is unavailable"):
        native_module.aes_256_gcm_encrypt_native(b"payload", b"k" * 32, b"n" * 12, b"header")

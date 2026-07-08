from __future__ import annotations

import importlib
import logging
from types import SimpleNamespace
from typing import cast

import pytest

import miniproto.crypto.native as native_module
from miniproto.crypto import native_available, xor_bytes


def test_xor_bytes_matches_expected_result() -> None:
    assert xor_bytes(b"\x0f\xf0", b"\xf0\x0f") == b"\xff\xff"


def test_xor_bytes_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError, match="same length"):
        xor_bytes(b"a", b"bb")


def test_native_available_returns_bool() -> None:
    assert isinstance(native_available(), bool)


def test_native_loader_falls_back_when_extension_import_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_import(name: str):
        if name == "miniproto._native":
            raise ImportError("native failed")
        return importlib.import_module(name)

    monkeypatch.setattr(native_module, "import_module", fake_import)
    impl, error = native_module._load_native_impl()
    assert impl.native_available() is False
    assert error == "ImportError: native failed"


def test_native_loader_falls_back_when_extension_is_incomplete(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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

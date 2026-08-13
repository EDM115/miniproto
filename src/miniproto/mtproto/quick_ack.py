"""MTProto quick-ACK token derivation with native capability fallback."""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import cast


def quick_ack_token(auth_key: bytes, encrypted_packet: bytes) -> int:
    """Return Telegram's high-bit-set quick-ACK token for an encrypted packet."""
    return int(_quick_ack_impl()(auth_key, encrypted_packet))


def _quick_ack_impl() -> Callable[[bytes, bytes], int]:
    try:
        native = import_module("miniproto._native")
    except Exception:
        native = None
    candidate = getattr(native, "quick_ack_token", None) if native is not None else None
    if callable(candidate):
        return cast(Callable[[bytes, bytes], int], candidate)
    fallback = import_module("miniproto._native_fallback")
    return cast(Callable[[bytes, bytes], int], fallback.quick_ack_token)


__all__ = ["quick_ack_token"]

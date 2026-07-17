from __future__ import annotations

import miniproto.errors as public_errors
from miniproto.errors import FloodPremiumWait, FloodWait, InvalidCode, PhoneCodeInvalid, RpcError, classify_rpc_error
from miniproto.raw.errors import RPC_ERROR_MAP


def _class_name(name: str) -> str:
    cleaned = name.replace("%d", "").replace("%D", "").strip("_")
    parts = [part for part in cleaned.replace("-", "_").split("_") if part]
    rendered = "".join(_part(part) for part in parts)
    return f"Rpc{rendered}" if rendered and rendered[0].isdigit() else rendered


def _part(part: str) -> str:
    if part.upper() == "2FA":
        return "TwoFa"
    if part.isdigit():
        return part
    return part[:1].upper() + part[1:].lower()


def test_public_errors_module_exposes_class_for_every_pinned_telegram_error() -> None:
    missing = sorted(
        {_class_name(name) for name, _code in RPC_ERROR_MAP if not hasattr(public_errors, _class_name(name))}
    )
    assert missing == []


def test_flood_premium_wait_is_a_typed_wait_exception() -> None:
    error = classify_rpc_error(RpcError("FLOOD_PREMIUM_WAIT_12", code=420))
    assert isinstance(error, FloodPremiumWait)
    assert isinstance(error, FloodWait)
    assert error.seconds == 12


def test_exact_rpc_errors_keep_specific_public_class_and_legacy_base_type() -> None:
    request = object()
    error = classify_rpc_error(RpcError("PHONE_CODE_INVALID", code=400, request=request))
    assert isinstance(error, PhoneCodeInvalid)
    assert isinstance(error, InvalidCode)
    assert error.request is request

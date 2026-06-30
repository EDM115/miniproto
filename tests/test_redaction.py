from __future__ import annotations

from miniproto.errors import RpcError
from miniproto.security.redaction import (
    REDACTED,
    is_sensitive_key,
    redact_mapping,
    redact_text,
    safe_repr,
)
from miniproto.session.models import AuthKey, SessionRecord, UserIdentity

SECRET_VALUE = "do-not-leak"  # noqa: S105 - intentional redaction-test sentinel


def test_sensitive_key_detection_is_case_insensitive_and_variant_aware() -> None:
    for key in (
        "api_hash",
        "API_HASH",
        "phone",
        "phone_number",
        "auth_key",
        "session_key",
        "bot_token",
        "password",
        "proxy",
        "proxy_password",
        "raw_session",
    ):
        assert is_sensitive_key(key)


def test_nested_mapping_redaction_covers_phase_two_secret_names() -> None:
    data = {
        "api_hash": SECRET_VALUE,
        "nested": {
            "phone": "+12025550123",
            "auth_key": b"binary-secret",
            "session_key": "session-secret",
            "bot_token": "123:abc",
            "password": "pw",
            "proxy": "socks5://user:pass@example.invalid:1080",
            "safe": "visible",
        },
    }
    redacted = redact_mapping(data)
    assert redacted["api_hash"] == REDACTED
    assert redacted["nested"]["phone"] == REDACTED
    assert redacted["nested"]["auth_key"] == REDACTED
    assert redacted["nested"]["session_key"] == REDACTED
    assert redacted["nested"]["bot_token"] == REDACTED
    assert redacted["nested"]["password"] == REDACTED
    assert redacted["nested"]["proxy"] == REDACTED
    assert redacted["nested"]["safe"] == "visible"
    assert SECRET_VALUE not in repr(redacted)


def test_redact_text_handles_log_style_key_value_pairs() -> None:
    rendered = redact_text(
        "api_hash=do-not-leak phone:+12025550123 bot-token='123:abc' proxy=socks5://secret"
    )
    assert "do-not-leak" not in rendered
    assert "+12025550123" not in rendered
    assert "123:abc" not in rendered
    assert "socks5://secret" not in rendered
    assert rendered.count(REDACTED) == 4


def test_safe_repr_redacts_dataclass_secret_fields() -> None:
    record = SessionRecord(
        auth_key=AuthKey(dc_id=1, key=b"auth-secret"),
        user=UserIdentity(id=1, phone="+12025550123", username="alice"),
        metadata={"session_key": "metadata-secret", "visible": "ok"},
    )
    rendered = safe_repr(record)
    assert "auth-secret" not in rendered
    assert "+12025550123" not in rendered
    assert "metadata-secret" not in rendered
    assert "alice" in rendered
    assert "ok" in rendered


def test_rpc_error_string_and_repr_redact_context_and_request_data() -> None:
    error = RpcError(
        "failed with password=do-not-leak",
        code=400,
        request={"api_hash": "hash-secret", "query": "visible"},
        context={"bot_token": "token-secret", "safe": "ok"},
    )
    rendered = str(error)
    debug = repr(error)
    assert "do-not-leak" not in rendered
    assert "hash-secret" not in rendered
    assert "token-secret" not in rendered
    assert "visible" in rendered
    assert "ok" in rendered
    assert "do-not-leak" not in debug
    assert "hash-secret" not in debug
    assert "token-secret" not in debug

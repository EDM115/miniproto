from __future__ import annotations

import io
import json
import traceback
from dataclasses import dataclass
from typing import ClassVar, cast

import pytest

from miniproto.auth.key_exchange import AuthKeyExchangeResult
from miniproto.config import ClientConfig, TransportConfig
from miniproto.errors import AmbiguousRpcResult, ClientDisconnected, ProtocolValidationError, RequestTimeout, RpcError
from miniproto.invoke import decode_rpc_response, wrap_transport_failure
from miniproto.mtproto.codec import RpcErrorBody
from miniproto.observability import LogFormat, configure_logging, get_logger
from miniproto.raw import functions, types
from miniproto.raw.base import TLRequest
from miniproto.security.redaction import REDACTED, is_sensitive_key, redact_mapping, redact_text, safe_repr
from miniproto.session.models import (
    AuthKey,
    DCOption,
    PeerCacheEntry,
    SessionRecord,
    UserIdentity,
    session_record_to_mapping,
)
from miniproto.session.storage import SessionStorage

SECRET_VALUE = "do-not-leak"  # noqa: S105 - intentional redaction-test sentinel


class _SentinelSessionStorage:
    def __repr__(self) -> str:
        return "storage-secret-sentinel"


def test_sensitive_key_detection_is_case_insensitive_and_variant_aware() -> None:
    for key in (
        "api_hash",
        "API_HASH",
        "phone",
        "phone_number",
        "auth_key",
        "session_key",
        "bot_token",
        "bot_auth_token",
        "web_auth_token",
        "autologin_token",
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
    rendered = redact_text("api_hash=do-not-leak phone:+12025550123 bot-token='123:abc' proxy=socks5://secret")
    assert "do-not-leak" not in rendered
    assert "+12025550123" not in rendered
    assert "123:abc" not in rendered
    assert "socks5://secret" not in rendered
    assert rendered.count(REDACTED) == 4


def test_redact_text_consumes_complete_quoted_values_with_spaces() -> None:
    rendered = redact_text('password="alpha beta" secret=\'gamma delta\' visible="keep me"')

    assert rendered == 'password="[redacted]" secret=\'[redacted]\' visible="keep me"'
    assert "alpha beta" not in rendered
    assert "gamma delta" not in rendered


def test_redact_text_fails_closed_for_unterminated_quoted_secret() -> None:
    rendered = redact_text('password="alpha beta')

    assert rendered == 'password="[redacted]"'
    assert "alpha beta" not in rendered


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


def test_config_dataclass_reprs_hide_secrets_and_keep_diagnostics() -> None:
    transport = TransportConfig(proxy="socks5://proxy-secret-sentinel")
    config = ClientConfig(
        api_id=12345,
        api_hash="api-hash-secret-sentinel",
        session_storage=cast("SessionStorage", _SentinelSessionStorage()),
        transport=transport,
        bot_token="bot-token-secret-sentinel",  # noqa: S106 - intentional sentinel
        dc_id=4,
    )

    transport_repr = repr(transport)
    config_repr = repr(config)
    for secret in (
        "proxy-secret-sentinel",
        "api-hash-secret-sentinel",
        "storage-secret-sentinel",
        "bot-token-secret-sentinel",
    ):
        assert secret not in transport_repr
        assert secret not in config_repr
    assert "mode='tcp_abridged'" in transport_repr
    assert "api_id=12345" in config_repr
    assert "dc_id=4" in config_repr


def test_session_dataclass_reprs_hide_direct_and_nested_secrets() -> None:
    auth_key = AuthKey(dc_id=2, key=b"auth-key-secret-sentinel", key_id=111)
    dc_option = DCOption(id=2, ip_address="149.154.167.40", port=443, secret=b"dc-secret-sentinel")
    user = UserIdentity(id=222, username="visible-user", phone="phone-secret-sentinel")
    peer = PeerCacheEntry(
        id=333,
        kind="user",
        username="visible-peer",
        phone="peer-phone-secret-sentinel",
        raw={"payload": "peer-raw-secret-sentinel"},
    )
    record = SessionRecord(
        dc_id=2,
        auth_key=auth_key,
        dc_options=(dc_option,),
        user=user,
        peers=(peer,),
        metadata={"session_key": "metadata-secret-sentinel"},
    )

    direct_reprs = (repr(auth_key), repr(dc_option), repr(user), repr(peer))
    record_repr = repr(record)
    for secret in (
        "auth-key-secret-sentinel",
        "dc-secret-sentinel",
        "phone-secret-sentinel",
        "peer-phone-secret-sentinel",
        "peer-raw-secret-sentinel",
        "metadata-secret-sentinel",
    ):
        assert all(secret not in rendered for rendered in direct_reprs)
        assert secret not in record_repr
    assert "dc_id=2" in record_repr
    assert "key_id=111" in record_repr
    assert "visible-user" in record_repr
    assert "visible-peer" in record_repr
    assert "id=333" in record_repr


def test_auth_key_exchange_result_repr_hides_auth_key() -> None:
    result = AuthKeyExchangeResult(
        auth_key=b"exchange-auth-key-secret-sentinel",
        auth_key_id=b"visible-key-id",
        server_salt=444,
        time_offset=1.5,
        dc_id=5,
    )

    rendered = repr(result)
    assert "exchange-auth-key-secret-sentinel" not in rendered
    assert "visible-key-id" in rendered
    assert "server_salt=444" in rendered
    assert "dc_id=5" in rendered


def test_repr_redaction_does_not_change_equality_or_session_serialization() -> None:
    first = AuthKey(dc_id=2, key=b"first-auth-key-secret")
    second = AuthKey(dc_id=2, key=b"second-auth-key-secret")
    record = SessionRecord(
        auth_key=first,
        user=UserIdentity(id=222, phone="serialized-phone-secret"),
        metadata={"session_key": "serialized-metadata-secret"},
    )

    assert first != second
    mapping = session_record_to_mapping(record)
    assert mapping["auth_key"]["key"] == b"first-auth-key-secret"
    assert mapping["user"]["phone"] == "serialized-phone-secret"
    assert mapping["metadata"]["session_key"] == "serialized-metadata-secret"


def test_safe_repr_summarizes_binary_payloads_without_dumping_contents() -> None:
    payload = (b"miniproto-live-media-limit:0000000000000404\n" * 8) + b"x" * 128
    request = functions.UploadSaveBigFilePart(file_id=1, file_part=2, file_total_parts=3, bytes=payload)
    rendered = str(RpcError("sender disconnected", request=request))
    assert "miniproto-live-media-limit" not in rendered
    assert "b'" not in rendered
    assert f"<bytes len={len(payload)}>" in rendered


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


def test_ambiguous_rpc_result_redacts_request_and_context_data() -> None:
    error = AmbiguousRpcResult(
        "uncertain password=do-not-leak",
        request={"api_hash": "hash-secret", "query": "visible"},
        context={"bot_token": "token-secret", "attempts": 1},
    )
    rendered = str(error)
    debug = repr(error)
    for secret in ("do-not-leak", "hash-secret", "token-secret"):
        assert secret not in rendered
        assert secret not in debug
    assert "visible" in rendered
    assert "attempts" in rendered


def test_protocol_validation_error_redacts_sensitive_context() -> None:
    error = ProtocolValidationError("msg_key", context={"auth_key": "key-secret", "msg_id": 123})
    rendered = str(error)
    debug = repr(error)
    assert error.reason == "msg_key"
    assert "key-secret" not in rendered
    assert "key-secret" not in debug
    assert "msg_id" in rendered


@pytest.mark.parametrize(
    ("raw_request", "credential"),
    [
        pytest.param(
            functions.AuthCheckRecoveryPassword(code="synthetic-check-18"), "synthetic-check-18", id="check-recovery"
        ),
        pytest.param(functions.AuthRecoverPassword(code="synthetic-recover-18"), "synthetic-recover-18", id="recover"),
        pytest.param(
            functions.AccountConfirmPasswordEmail(code="synthetic-confirm-18"),
            "synthetic-confirm-18",
            id="confirm-email",
        ),
        pytest.param(
            functions.AuthSignIn(
                phone_number="synthetic-phone-18",
                phone_code_hash="synthetic-hash-18",
                email_verification=types.EmailVerificationCode(code="synthetic-signin-18"),
            ),
            "synthetic-signin-18",
            id="signin-email",
        ),
        pytest.param(
            functions.AccountVerifyEmail(
                purpose=types.EmailVerifyPurposeLoginChange(),
                verification=types.EmailVerificationCode(code="synthetic-verify-18"),
            ),
            "synthetic-verify-18",
            id="verify-email",
        ),
    ],
)
def test_authentication_codes_are_redacted_in_rpc_and_timeout_diagnostics(
    raw_request: TLRequest, credential: str
) -> None:
    wire_before = raw_request.serialize()
    assert credential.encode() in wire_before
    with pytest.raises(RpcError) as caught:
        decode_rpc_response(RpcErrorBody(error_code=400, error_message="EMAIL_CODE_INVALID"), raw_request)
    timeout = wrap_transport_failure(TimeoutError("synthetic deadline"), raw_request, connected=True)

    assert isinstance(timeout, RequestTimeout)
    for error in (caught.value, timeout):
        assert error.request is raw_request
        for rendered in (str(error), repr(error), "".join(traceback.format_exception(error))):
            assert credential not in rendered
            assert REDACTED in rendered
            assert "synthetic-phone-18" not in rendered
            assert "synthetic-hash-18" not in rendered
    assert "[400] EMAIL_CODE_INVALID" in str(caught.value)
    assert "code=400" in repr(caught.value)
    assert raw_request.serialize() == wire_before


@pytest.mark.parametrize("connected", [True, False])
def test_connection_failure_wrappers_redact_recovery_codes(connected: bool) -> None:
    raw_request = functions.AuthRecoverPassword(code="synthetic-connection-18")
    error = wrap_transport_failure(ConnectionError("synthetic disconnect"), raw_request, connected=connected)

    assert type(error) is (RpcError if connected else ClientDisconnected)
    assert error.request is raw_request
    assert "synthetic-connection-18" not in str(error)
    assert "synthetic-connection-18" not in repr(error)
    assert "synthetic disconnect" in str(error)


@pytest.mark.parametrize("log_format", ["text", "json"])
def test_configured_exception_logging_redacts_nested_email_codes(
    log_format: LogFormat, monkeypatch: pytest.MonkeyPatch
) -> None:
    stream = io.StringIO()
    logger = get_logger()
    monkeypatch.setattr(logger, "handlers", [])
    monkeypatch.setattr(logger, "level", logger.level)
    monkeypatch.setattr(logger, "propagate", logger.propagate)
    configure_logging("ERROR", format=log_format, stream=stream)
    raw_request = functions.AccountVerifyEmail(
        purpose=types.EmailVerifyPurposeLoginChange(),
        verification=types.EmailVerificationCode(code="synthetic-logged-18"),
    )
    try:
        raise wrap_transport_failure(TimeoutError("synthetic deadline"), raw_request, connected=True)
    except RpcError:
        logger.exception(
            "verification failed",
            extra={
                "miniproto_event": {"event": "verification.failed", "request": raw_request, "code": "visible-status-18"}
            },
        )

    rendered = stream.getvalue()
    assert "synthetic-logged-18" not in rendered
    assert REDACTED in rendered
    assert "visible-status-18" in rendered
    assert "RequestTimeout" in rendered
    if log_format == "json":
        payload = json.loads(rendered)
        assert payload["request"]["verification"] == {"code": REDACTED}
        assert payload["code"] == "visible-status-18"


def test_semantic_redaction_keeps_ordinary_code_fields_and_existing_secret_controls() -> None:
    @dataclass
    class OrdinaryCode:
        code: str
        QUALNAME: ClassVar[str] = "emailVerificationCode"

    verification = types.EmailVerificationCode(code="synthetic-context-18")
    data = {
        "nested": [({"verification": verification},)],
        "ordinary": OrdinaryCode(code="visible-dataclass-18"),
        "code": "visible-mapping-18",
        "status": types.Error(code=503, text="visible status"),
        "phone_code": "synthetic-phone-code-18",
        "bot_token": "synthetic-bot-18",
        "payload": b"synthetic-binary-18",
    }

    assert redact_mapping(data) == {
        "nested": [({"verification": {"code": REDACTED}},)],
        "ordinary": {"code": "visible-dataclass-18"},
        "code": "visible-mapping-18",
        "status": {"code": 503, "text": "visible status"},
        "phone_code": REDACTED,
        "bot_token": REDACTED,
        "payload": "<bytes len=19>",
    }
    error = RpcError("synthetic failure", code=503, context=data)
    assert "synthetic-context-18" not in str(error)
    assert "synthetic-context-18" not in repr(error)
    assert "code=503" in repr(error)
    assert safe_repr(verification) == "{'code': '[redacted]'}"
    assert verification.code == "synthetic-context-18"

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

import miniproto.session.strings as session_strings
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    PeerCacheEntry,
    SessionEnvelopeError,
    SessionRecord,
    SessionString,
    UpdateState,
    UserIdentity,
    event_loop,
    export_session_string,
    import_session_string,
)
from miniproto.invoke import method_name_for_request
from miniproto.raw import types
from miniproto.security.redaction import safe_repr
from miniproto.session.models import session_record_from_mapping
from miniproto.session.strings import MAX_DC_OPTIONS, MAX_SESSION_STRING_CHARS

FIXTURES = json.loads(
    (Path(__file__).parent / "fixtures" / "session_strings" / "upstream.json").read_text(encoding="utf-8")
)
AUTH_KEY = bytes(range(256))
ROUND_TRIP_PASSPHRASE = "correct horse battery staple"  # noqa: S105 - deterministic test credential
CORRECT_PASSPHRASE = "correct passphrase"  # noqa: S105 - deterministic test credential
WRONG_PASSPHRASE = "wrong passphrase"  # noqa: S105 - deterministic test credential
PORTABLE_PASSPHRASE = "portable secret"  # noqa: S105 - deterministic test credential
UNSUPPORTED_PASSPHRASE = "not-supported"  # noqa: S105 - deterministic test credential
TEST_BOT_TOKEN = "123:token"  # noqa: S105 - deterministic test credential


def rich_record() -> SessionRecord:
    return SessionRecord(
        dc_id=2,
        auth_key=AuthKey(
            dc_id=2,
            key=AUTH_KEY,
            key_id=123,
            created_at=datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
            expires_at=datetime(2027, 1, 2, 3, 4, 5, tzinfo=UTC),
        ),
        dc_options=(
            DCOption(id=2, ip_address="149.154.167.51", port=443, static=True, secret=b"dc-secret"),
            DCOption(id=4, ip_address="2001:db8::4", port=80, ipv6=True, media_only=True),
        ),
        user=UserIdentity(
            id=42,
            access_hash=99,
            is_bot=False,
            username="alice",
            phone="+41000000000",
            first_name="Alice",
            last_name="Example",
        ),
        update_state=UpdateState(pts=10, qts=3, seq=7, date=datetime(2026, 2, 3, tzinfo=UTC)),
        peers=(
            PeerCacheEntry(
                id=42,
                kind="user",
                access_hash=99,
                username="alice",
                phone="+41000000000",
                updated_at=datetime(2026, 2, 4, tzinfo=UTC),
                raw={"min": False, "proof": b"peer-proof"},
            ),
        ),
        metadata={"server_salt": 456, "dc_auth": {"4": {"key": b"media-key", "salt": 789}}},
    )


def test_native_plain_session_string_preserves_the_complete_typed_record() -> None:
    exported = export_session_string(rich_record())

    assert isinstance(exported, SessionString)
    assert exported.startswith("mp1:")
    assert "=" not in exported
    assert import_session_string(exported) == rich_record()


def test_native_protected_session_string_round_trips_and_uses_random_salt_and_nonce() -> None:
    first = export_session_string(rich_record(), passphrase=ROUND_TRIP_PASSPHRASE)
    second = export_session_string(rich_record(), passphrase=ROUND_TRIP_PASSPHRASE)

    assert first != second
    assert import_session_string(first, passphrase=ROUND_TRIP_PASSPHRASE) == rich_record()
    assert import_session_string(second, passphrase=ROUND_TRIP_PASSPHRASE) == rich_record()


def test_native_plain_and_protected_vectors_are_stable_and_import_in_fresh_processes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plain = export_session_string(rich_record())
    native_fixture = FIXTURES["miniproto"]
    assert len(plain) == native_fixture["plain"]["length"]
    assert hashlib.sha256(plain.encode()).hexdigest() == native_fixture["plain"]["sha256"]

    random_values = [
        bytes.fromhex(native_fixture["protected"]["salt"]),
        bytes.fromhex(native_fixture["protected"]["nonce"]),
    ]
    monkeypatch.setattr(session_strings.os, "urandom", lambda _size: random_values.pop(0))
    protected = export_session_string(rich_record(), passphrase=native_fixture["protected"]["passphrase"])
    assert len(protected) == native_fixture["protected"]["length"]
    assert hashlib.sha256(protected.encode()).hexdigest() == native_fixture["protected"]["sha256"]

    script = """
import json
import sys
from miniproto import import_session_string

case = json.load(sys.stdin)
record = import_session_string(case["value"], passphrase=case["passphrase"])
assert record.dc_id == 2
assert record.auth_key is not None and record.auth_key.key == bytes(range(256))
assert record.user is not None and record.user.id == 42
assert record.update_state.pts == 10
assert len(record.peers) == 1
"""
    for value, passphrase in ((plain, None), (protected, native_fixture["protected"]["passphrase"])):
        subprocess.run(  # noqa: S603 - fixed interpreter and inline test program
            [sys.executable, "-c", script],
            input=json.dumps({"value": value, "passphrase": passphrase}),
            text=True,
            capture_output=True,
            check=True,
        )


def test_native_session_string_fails_closed_for_wrong_passphrase_and_tampering() -> None:
    protected = export_session_string(rich_record(), passphrase=CORRECT_PASSPHRASE)
    with pytest.raises(SessionEnvelopeError, match="authentication failed") as wrong_passphrase:
        import_session_string(protected, passphrase=WRONG_PASSPHRASE)
    assert protected not in str(wrong_passphrase.value)

    index = len(protected) // 2
    replacement = "A" if protected[index] != "A" else "B"
    tampered = protected[:index] + replacement + protected[index + 1 :]
    with pytest.raises(SessionEnvelopeError, match="authentication failed") as bad_ciphertext:
        import_session_string(tampered, passphrase=CORRECT_PASSPHRASE)
    assert tampered not in str(bad_ciphertext.value)

    plain = export_session_string(rich_record())
    index = len(plain) // 2
    replacement = "A" if plain[index] != "A" else "B"
    tampered_plain = plain[:index] + replacement + plain[index + 1 :]
    with pytest.raises(SessionEnvelopeError, match="checksum"):
        import_session_string(tampered_plain)


@pytest.mark.parametrize(
    "value, message",
    [("mp2:AAAA", "unsupported"), ("mp1:AAAA=", "base64"), ("mp1:not+urlsafe", "base64"), ("mp1:AAAA", "truncated")],
)
def test_native_session_string_rejects_unsupported_truncated_or_noncanonical_inputs(value: str, message: str) -> None:
    with pytest.raises(SessionEnvelopeError, match=message) as exc_info:
        import_session_string(value)
    assert value not in str(exc_info.value)


def test_native_session_string_rejects_oversized_input_before_base64_decoding() -> None:
    value = "mp1:" + "A" * (MAX_SESSION_STRING_CHARS + 1)
    with pytest.raises(SessionEnvelopeError, match="too large") as exc_info:
        import_session_string(value)
    assert value not in str(exc_info.value)


def test_session_string_repr_and_safe_repr_do_not_reveal_the_bearer_secret() -> None:
    exported = export_session_string(rich_record())

    assert exported not in repr(exported)
    assert exported not in safe_repr(exported)
    assert "redacted" in repr(exported).lower()
    assert "redacted" in safe_repr(exported).lower()


def test_native_session_export_rejects_excessive_collection_counts_before_encoding() -> None:
    option = DCOption(id=2, ip_address="149.154.167.51", port=443)
    record = SessionRecord(dc_id=2, dc_options=(option,) * (MAX_DC_OPTIONS + 1))

    with pytest.raises(SessionEnvelopeError, match="DC options"):
        export_session_string(record)


@pytest.mark.parametrize("case_name", ["ipv4", "ipv6"])
def test_telethon_v1_golden_strings_import_and_export_without_telethon(case_name: str) -> None:
    case = FIXTURES["telethon"]["cases"][case_name]
    record = import_session_string(case["value"], format="telethon")

    assert record.dc_id == case["dc_id"]
    assert record.auth_key is not None and record.auth_key.key == AUTH_KEY
    assert record.dc_options == (
        DCOption(
            id=case["dc_id"], ip_address=case["ip_address"], port=case["port"], ipv6=case_name == "ipv6", static=True
        ),
    )
    assert record.user is None
    assert record.metadata["session_import_format"] == "telethon-v1"
    assert record.metadata["update_state_bootstrap_required"] is True
    assert export_session_string(record, format="telethon") == case["value"]
    assert import_session_string(case["value"], format="auto").dc_id == case["dc_id"]


@pytest.mark.parametrize("case_name", ["modern", "legacy32", "legacy64"])
def test_pyrogram_golden_strings_import_current_and_legacy_layouts_without_pyrogram(case_name: str) -> None:
    case = FIXTURES["pyrogram"]["cases"][case_name]
    record = import_session_string(case["value"], format="pyrogram")

    assert record.dc_id == case["dc_id"]
    assert record.auth_key is not None and record.auth_key.key == AUTH_KEY
    assert record.user == UserIdentity(id=case["user_id"], is_bot=case["is_bot"])
    assert record.metadata["test_mode"] is case["test_mode"]
    assert record.metadata["session_import_format"].startswith("pyrogram-")
    assert record.metadata["update_state_bootstrap_required"] is True
    if case_name == "modern":
        assert record.metadata["api_id"] == case["api_id"]
        assert export_session_string(record, format="pyrogram") == case["value"]
    else:
        assert "api_id" not in record.metadata
    assert import_session_string(case["value"], format="auto").dc_id == case["dc_id"]


def test_foreign_session_exports_fail_when_required_fields_are_missing() -> None:
    with pytest.raises(SessionEnvelopeError, match="auth key"):
        export_session_string(SessionRecord(dc_id=2), format="telethon")
    with pytest.raises(SessionEnvelopeError, match="DC endpoint"):
        export_session_string(SessionRecord(dc_id=2, auth_key=AuthKey(dc_id=2, key=AUTH_KEY)), format="telethon")
    with pytest.raises(SessionEnvelopeError, match="API ID"):
        export_session_string(rich_record(), format="pyrogram")
    with pytest.raises(SessionEnvelopeError, match="passphrase"):
        export_session_string(rich_record(), format="telethon", passphrase=UNSUPPORTED_PASSPHRASE)


def test_client_session_string_conveniences_refuse_connected_or_implicit_overwrite() -> None:
    async def scenario() -> None:
        source_storage = InMemorySessionStorage(rich_record())
        source = Client(ClientConfig(api_id=12345, api_hash="hash", session_storage=source_storage))
        exported = await source.export_session_string(passphrase=PORTABLE_PASSPHRASE)

        target_storage = InMemorySessionStorage()
        target = Client(ClientConfig(api_id=12345, api_hash="hash", session_storage=target_storage))
        imported = await target.import_session_string(exported, passphrase=PORTABLE_PASSPHRASE)
        assert imported == rich_record()
        assert target_storage._data is not None

        with pytest.raises(ValueError, match="not empty"):
            await target.import_session_string(exported, passphrase=PORTABLE_PASSPHRASE)
        assert (
            await target.import_session_string(exported, passphrase=PORTABLE_PASSPHRASE, replace=True) == rich_record()
        )

        await target.connect()
        with pytest.raises(ConnectionError, match="disconnected"):
            await target.import_session_string(exported, passphrase=PORTABLE_PASSPHRASE, replace=True)

    event_loop.run(scenario())


def test_client_validates_pyrogram_api_test_mode_and_account_kind_with_explicit_override() -> None:
    async def scenario() -> None:
        modern = FIXTURES["pyrogram"]["cases"]["modern"]["value"]
        mismatched = Client(
            ClientConfig(api_id=54321, api_hash="hash", session_storage=InMemorySessionStorage(), test_mode=True)
        )
        with pytest.raises(ValueError, match="API ID"):
            await mismatched.import_session_string(modern, format="pyrogram")
        imported = await mismatched.import_session_string(modern, format="pyrogram", replace=True, allow_mismatch=True)
        assert imported.user is not None and imported.user.is_bot

        user = FIXTURES["pyrogram"]["cases"]["legacy32"]["value"]
        bot_config = Client(
            ClientConfig(
                api_id=12345,
                api_hash="hash",
                session_storage=InMemorySessionStorage(),
                test_mode=True,
                bot_token=TEST_BOT_TOKEN,
            )
        )
        with pytest.raises(ValueError, match="account kind"):
            await bot_config.import_session_string(user, format="pyrogram")
        assert (
            await bot_config.import_session_string(user, format="pyrogram", allow_mismatch=True)
        ).user == UserIdentity(id=123456789, is_bot=False)

    event_loop.run(scenario())


def test_client_imported_foreign_session_bootstraps_update_state_on_connect() -> None:
    class StateSender:
        def __init__(self) -> None:
            self.requests: list[object] = []
            self.is_connected = True

        async def request(
            self,
            body: bytes | object,
            *,
            content_related: bool = True,
            retry_safe: bool,
            request_timeout: float | None = None,
        ) -> object:
            del content_related, retry_safe, request_timeout
            self.requests.append(body)
            return types.UpdatesState(pts=101, qts=12, date=1_760_000_000, seq=33, unread_count=0).serialize()

        async def disconnect(self) -> None:
            self.is_connected = False

    async def scenario() -> None:
        storage = InMemorySessionStorage()
        client = Client(ClientConfig(api_id=12345, api_hash="hash", session_storage=storage))
        telethon = FIXTURES["telethon"]["cases"]["ipv4"]["value"]
        await client.import_session_string(telethon, format="telethon")
        sender = StateSender()
        client._sender = sender

        await client.connect()

        assert len(sender.requests) == 1
        assert method_name_for_request(sender.requests[0]) == "updates.getState"
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert (record.update_state.pts, record.update_state.qts, record.update_state.seq) == (101, 12, 33)
        assert "update_state_bootstrap_required" not in record.metadata
        assert record.metadata["session_import_format"] == "telethon-v1"
        await client.disconnect()

    event_loop.run(scenario())

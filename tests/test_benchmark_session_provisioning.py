from __future__ import annotations

import asyncio
from pathlib import Path

from tools.bench.provision_session import provision_sessions

from miniproto import AuthKey, SessionRecord, UserIdentity, export_session_string
from miniproto.session.models import session_record_from_mapping
from miniproto.session.storage import EncryptedSQLiteSessionStorage


def test_optional_string_session_provisions_encrypted_database_without_overwriting_existing(tmp_path: Path) -> None:
    record = SessionRecord(
        dc_id=4,
        auth_key=AuthKey(dc_id=4, key=b"a" * 256, key_id=123),
        user=UserIdentity(id=42, access_hash=84, is_bot=True),
    )
    value = str(export_session_string(record))
    env = {"MINIPROTO_SESSION_KEY": "a" * 32, "MINIPROTO_LIVE_BENCH_BOT_STRING_SESSION": value}

    async def scenario() -> None:
        provisioned = await provision_sessions(dc_id=4, env=env, root=tmp_path)
        assert provisioned == ("bot",)
        target = tmp_path / "miniproto-live-bench-bot-dc4.sqlite"
        loaded = await EncryptedSQLiteSessionStorage(target, key="a" * 32).load()
        assert loaded is not None
        assert session_record_from_mapping(loaded) == record

        replacement = str(
            export_session_string(
                SessionRecord(
                    dc_id=4,
                    auth_key=AuthKey(dc_id=4, key=b"b" * 256, key_id=456),
                    user=UserIdentity(id=43, access_hash=86, is_bot=True),
                )
            )
        )
        second = await provision_sessions(
            dc_id=4, env=env | {"MINIPROTO_LIVE_BENCH_BOT_STRING_SESSION": replacement}, root=tmp_path
        )
        assert second == ()
        preserved = await EncryptedSQLiteSessionStorage(target, key="a" * 32).load()
        assert preserved is not None
        assert session_record_from_mapping(preserved) == record

    asyncio.run(scenario())


def test_string_session_provisioning_does_not_claim_an_existing_empty_path(tmp_path: Path) -> None:
    target = tmp_path / "miniproto-live-bench-bot-dc4.sqlite"
    target.touch()
    record = SessionRecord(
        dc_id=4,
        auth_key=AuthKey(dc_id=4, key=b"a" * 256, key_id=123),
        user=UserIdentity(id=42, access_hash=84, is_bot=True),
    )
    env = {
        "MINIPROTO_SESSION_KEY": "a" * 32,
        "MINIPROTO_LIVE_BENCH_BOT_STRING_SESSION": str(export_session_string(record)),
    }

    provisioned = asyncio.run(provision_sessions(dc_id=4, env=env, root=tmp_path))

    assert provisioned == ()
    assert target.read_bytes() == b""

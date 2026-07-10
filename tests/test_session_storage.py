from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

import pytest

from miniproto import (
    AuthKey,
    DCOption,
    EncryptedSQLiteSessionStorage,
    InMemorySessionStorage,
    PeerCacheEntry,
    SessionRecord,
    UpdateState,
    UserIdentity,
    event_loop,
)
from miniproto.errors import SessionEnvelopeError
from miniproto.session.models import session_record_from_mapping
from miniproto.session.storage import deserialize_session_data, serialize_session_data


def run(coro):
    return event_loop.run(coro)


def sample_record() -> SessionRecord:
    return SessionRecord(
        dc_id=2,
        auth_key=AuthKey(dc_id=2, key=b"auth-key-bytes", key_id=123),
        dc_options=(DCOption(id=2, ip_address="149.154.167.51", port=443),),
        user=UserIdentity(id=42, access_hash=99, username="alice", phone="+12025550123"),
        update_state=UpdateState(pts=10, qts=3, seq=7, date=datetime(2026, 6, 30, tzinfo=UTC)),
        peers=(PeerCacheEntry(id=42, kind="user", access_hash=99, username="alice"),),
        metadata={"layer": 201, "note": "kept"},
    )


def test_in_memory_storage_preserves_mapping_payloads_and_copies() -> None:
    async def scenario() -> None:
        initial = {
            "auth_key": b"secret",
            "nested": {"created_at": datetime(2026, 6, 30, tzinfo=UTC)},
        }
        storage = InMemorySessionStorage(initial)
        loaded = await storage.load()
        assert loaded is not None
        assert loaded == initial
        assert loaded is not initial
        assert loaded["nested"] is not initial["nested"]
        await storage.save({"auth_key": b"new-secret"})
        assert await storage.load() == {"auth_key": b"new-secret"}
        await storage.clear()
        assert await storage.load() is None
        await storage.close()

    run(scenario())


def test_in_memory_storage_reuses_named_siblings() -> None:
    storage = InMemorySessionStorage()
    first = storage.sibling("download-1")
    assert first is storage.sibling("download-1")
    assert first is not storage.sibling("download-2")


def test_session_record_serialization_round_trips_dataclass_payload() -> None:
    record = sample_record()
    decoded = deserialize_session_data(serialize_session_data(record))
    restored = session_record_from_mapping(decoded)
    assert restored == record


def test_encrypted_sqlite_storage_requires_key(tmp_path) -> None:
    with pytest.raises(ValueError, match="requires a key"):
        EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite")


def test_encrypted_sqlite_storage_load_save_clear_close(tmp_path) -> None:
    async def scenario() -> None:
        storage = EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite", key="x" * 32)
        assert await storage.load() is None
        expected = sample_record()
        await storage.save(expected)
        loaded = await storage.load()
        assert loaded is not None
        assert loaded["auth_key"]["key"] == b"auth-key-bytes"
        assert loaded["update_state"]["pts"] == 10
        assert session_record_from_mapping(loaded) == expected
        await storage.clear()
        assert await storage.load() is None
        await storage.close()

    run(scenario())


def test_encrypted_sqlite_storage_uses_stable_sibling_paths_and_keys(tmp_path) -> None:
    async def scenario() -> None:
        storage = EncryptedSQLiteSessionStorage(tmp_path / "bot.sqlite", key="x" * 32)
        sibling = storage.sibling("download-1")
        assert sibling.path == tmp_path / "bot-download-1.sqlite"
        await sibling.save({"auth_key": b"auxiliary"})
        reopened = storage.sibling("download-1")
        assert reopened.path == sibling.path
        assert await reopened.load() == {"auth_key": b"auxiliary"}

    run(scenario())


@pytest.mark.parametrize("name", ["", ".", "../other", "download/1", "download\\1"])
def test_session_storage_rejects_unsafe_sibling_names(name) -> None:
    with pytest.raises(ValueError, match="sibling name"):
        InMemorySessionStorage().sibling(name)


def test_encrypted_sqlite_storage_splits_encrypted_rows_by_session_domain(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="x" * 32)
        expected = sample_record()
        await storage.save(expected)
        with sqlite3.connect(path) as connection:
            rows = connection.execute(
                "SELECT domain, envelope FROM session_domains ORDER BY domain"
            ).fetchall()
        assert [row[0] for row in rows] == ["auth", "metadata", "peers", "update_state"]
        assert all(isinstance(row[1], bytes) and row[1].startswith(b"{") for row in rows)
        loaded = await storage.load()
        assert loaded is not None
        assert session_record_from_mapping(loaded) == expected
        await storage.clear()
        with sqlite3.connect(path) as connection:
            count = connection.execute("SELECT count(*) FROM session_domains").fetchone()[0]
        assert count == 0

    run(scenario())


def test_encrypted_sqlite_storage_uses_environment_key(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        monkeypatch.setenv("MINIPROTO_SESSION_KEY", "env-key-material-that-is-long-enough")
        storage = EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite")
        await storage.save({"auth_key": b"from-env"})
        assert await storage.load() == {"auth_key": b"from-env"}

    run(scenario())


def test_encrypted_sqlite_storage_rejects_wrong_key(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        await storage.save({"auth_key": b"secret"})
        wrong = EncryptedSQLiteSessionStorage(path, key="b" * 32)
        with pytest.raises(SessionEnvelopeError, match="authentication failed"):
            await wrong.load()

    run(scenario())


def test_encrypted_sqlite_storage_rejects_corrupted_envelope(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        await storage.save({"auth_key": b"secret"})
        with sqlite3.connect(path) as connection:
            connection.execute(
                "UPDATE session_domains SET envelope = ? WHERE domain = ?", (b"not-json", "payload")
            )
        with pytest.raises(SessionEnvelopeError, match="not valid JSON"):
            await storage.load()

    run(scenario())


def test_encrypted_sqlite_storage_atomic_overwrite(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        await storage.save({"auth_key": b"old", "dc_id": 1})
        await storage.save({"auth_key": b"new", "dc_id": 2})
        assert await storage.load() == {"auth_key": b"new", "dc_id": 2}
        with sqlite3.connect(path) as connection:
            count = connection.execute(
                "SELECT count(*) FROM session_domains WHERE domain = ?", ("payload",)
            ).fetchone()[0]
        assert count == 1

    run(scenario())

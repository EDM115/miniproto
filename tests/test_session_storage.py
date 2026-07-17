from __future__ import annotations

import asyncio
import sqlite3
import threading
from dataclasses import replace
from datetime import UTC, datetime
from typing import Any, cast

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
from miniproto.client import _CachedSessionStorage
from miniproto.errors import SessionEnvelopeError, SessionStorageError
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


class PausingSQLiteStorage(EncryptedSQLiteSessionStorage):
    def __init__(self, path) -> None:
        super().__init__(path, key="a" * 32)
        self.paused_operation: str | None = None
        self.operation_started = threading.Event()
        self.operation_release = threading.Event()
        self.operation_failure: BaseException | None = None

    def pause(self, operation: str, *, failure: BaseException | None = None) -> None:
        self.paused_operation = operation
        self.operation_failure = failure
        self.operation_started.clear()
        self.operation_release.clear()

    def _wait_if_paused(self, operation: str) -> None:
        if self.paused_operation != operation:
            return
        self.operation_started.set()
        assert self.operation_release.wait(timeout=2)
        if self.operation_failure is not None:
            raise self.operation_failure

    def _save_sync(self, data) -> None:
        self._wait_if_paused("save")
        super()._save_sync(data)

    def _mutate_sync(self, transform):
        self._wait_if_paused("mutate")
        return super()._mutate_sync(transform)

    def _clear_sync(self) -> None:
        self._wait_if_paused("clear")
        super()._clear_sync()

    def _close_sync(self) -> None:
        self._wait_if_paused("close")
        super()._close_sync()


def test_in_memory_storage_preserves_mapping_payloads_and_copies() -> None:
    async def scenario() -> None:
        initial = {"auth_key": b"secret", "nested": {"created_at": datetime(2026, 6, 30, tzinfo=UTC)}}
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


def test_in_memory_mutate_is_atomic_isolated_and_tracks_changed_domains() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(sample_record())
        received: dict[str, object] = {}

        def transform(payload):
            assert payload is not None
            received["payload"] = payload
            record = session_record_from_mapping(payload)
            return replace(record, peers=(*record.peers, PeerCacheEntry(id=99, kind="channel", access_hash=999)))

        committed = await storage.mutate(transform)
        assert committed is not None
        assert committed is not received["payload"]
        assert session_record_from_mapping(committed).peers[-1].id == 99
        assert storage.domain_revisions() == {"auth": 0, "peers": 1, "update_state": 0, "metadata": 0, "payload": 0}

        mutable = dict(committed)
        mutable["dc_id"] = 5
        loaded = await storage.load()
        assert loaded is not None
        assert loaded["dc_id"] == 2

    run(scenario())


def test_in_memory_mutate_failure_and_unchanged_save_do_not_advance_revisions() -> None:
    async def scenario() -> None:
        initial = sample_record()
        storage = InMemorySessionStorage(initial)
        before = await storage.load()

        def fail(_payload):
            raise RuntimeError("transform failed")

        with pytest.raises(RuntimeError, match="transform failed"):
            await storage.mutate(fail)
        assert await storage.load() == before
        assert storage.domain_revisions() == {"auth": 0, "peers": 0, "update_state": 0, "metadata": 0, "payload": 0}
        assert before is not None
        await storage.save(initial)
        assert all(revision == 0 for revision in storage.domain_revisions().values())

    run(scenario())


def test_in_memory_close_is_idempotent_and_rejects_later_operations() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(sample_record())
        await storage.close()
        await storage.close()
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.load()
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.save(sample_record())
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.mutate(lambda payload: payload)
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.clear()

    run(scenario())


def test_in_memory_mutate_rejects_async_transform_without_changing_state() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage({"value": 1})

        async def async_transform(payload):
            return payload

        with pytest.raises(TypeError, match="synchronous"):
            await storage.mutate(cast(Any, async_transform))
        assert await storage.load() == {"value": 1}
        assert all(revision == 0 for revision in storage.domain_revisions().values())

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
            rows = connection.execute("SELECT domain, envelope FROM session_domains ORDER BY domain").fetchall()
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
            connection.execute("UPDATE session_domains SET envelope = ? WHERE domain = ?", (b"not-json", "payload"))
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


def test_encrypted_sqlite_mutate_rewrites_only_changed_domains(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        await storage.save(sample_record())
        with sqlite3.connect(path) as connection:
            before = dict(connection.execute("SELECT domain, envelope FROM session_domains").fetchall())
        revisions_before = dict(storage.domain_revisions())

        def add_peer(payload):
            assert payload is not None
            record = session_record_from_mapping(payload)
            return replace(record, peers=(*record.peers, PeerCacheEntry(id=100, kind="user", access_hash=1000)))

        committed = await storage.mutate(add_peer)
        assert committed is not None
        with sqlite3.connect(path) as connection:
            after = dict(connection.execute("SELECT domain, envelope FROM session_domains").fetchall())
        assert after["peers"] != before["peers"]
        assert after["auth"] == before["auth"]
        assert after["update_state"] == before["update_state"]
        assert after["metadata"] == before["metadata"]
        assert storage.domain_revisions() == {**revisions_before, "peers": revisions_before["peers"] + 1}

    run(scenario())


def test_encrypted_sqlite_mutate_rolls_back_all_domains_when_encryption_fails(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        await storage.save(sample_record())
        with sqlite3.connect(path) as connection:
            before = dict(connection.execute("SELECT domain, envelope FROM session_domains").fetchall())
        revisions_before = dict(storage.domain_revisions())
        encrypt = storage._encrypt
        calls = 0

        def fail_second_encryption(plaintext: bytes) -> bytes:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("encryption failed")
            return encrypt(plaintext)

        monkeypatch.setattr(storage, "_encrypt", fail_second_encryption)

        def change_two_domains(payload):
            assert payload is not None
            record = session_record_from_mapping(payload)
            metadata = dict(record.metadata)
            metadata["changed"] = True
            return replace(
                record, peers=(*record.peers, PeerCacheEntry(id=100, kind="user", access_hash=1000)), metadata=metadata
            )

        with pytest.raises(RuntimeError, match="encryption failed"):
            await storage.mutate(change_two_domains)
        with sqlite3.connect(path) as connection:
            after = dict(connection.execute("SELECT domain, envelope FROM session_domains").fetchall())
        assert after == before
        assert storage.domain_revisions() == revisions_before

    run(scenario())


def test_encrypted_sqlite_mutate_migrates_legacy_envelope(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "legacy.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        record = sample_record()
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as connection:
            connection.execute(
                """
                CREATE TABLE session_records (
                    name TEXT PRIMARY KEY,
                    envelope BLOB NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "INSERT INTO session_records (name, envelope, updated_at) VALUES (?, ?, ?)",
                ("default", storage._encrypt(serialize_session_data(record)), datetime.now(UTC).isoformat()),
            )

        committed = await storage.mutate(
            lambda payload: replace(
                session_record_from_mapping(payload or {}),
                peers=(PeerCacheEntry(id=100, kind="user", access_hash=1000),),
            )
        )
        assert committed is not None
        with sqlite3.connect(path) as connection:
            legacy_count = connection.execute("SELECT count(*) FROM session_records").fetchone()[0]
            domains = {row[0] for row in connection.execute("SELECT domain FROM session_domains").fetchall()}
        assert legacy_count == 0
        assert domains == {"auth", "peers", "update_state", "metadata"}
        assert session_record_from_mapping(committed).auth_key == record.auth_key
        assert storage.domain_revisions() == {"auth": 0, "peers": 1, "update_state": 0, "metadata": 0, "payload": 0}

    run(scenario())


def test_encrypted_sqlite_mutate_rolls_back_when_second_domain_write_fails(tmp_path) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key="a" * 32)
        await storage.save(sample_record())
        with sqlite3.connect(path) as connection:
            before = dict(connection.execute("SELECT domain, envelope FROM session_domains").fetchall())
            connection.execute(
                """
                CREATE TRIGGER fail_metadata_update
                BEFORE UPDATE ON session_domains
                WHEN NEW.domain = 'metadata'
                BEGIN
                    SELECT RAISE(FAIL, 'metadata write failed');
                END
                """
            )
        revisions_before = dict(storage.domain_revisions())

        def change_two_domains(payload):
            assert payload is not None
            record = session_record_from_mapping(payload)
            metadata = dict(record.metadata)
            metadata["changed"] = True
            return replace(
                record, peers=(*record.peers, PeerCacheEntry(id=100, kind="user", access_hash=1000)), metadata=metadata
            )

        with pytest.raises(SessionStorageError, match="mutate"):
            await storage.mutate(change_two_domains)
        with sqlite3.connect(path) as connection:
            after = dict(connection.execute("SELECT domain, envelope FROM session_domains").fetchall())
        assert after == before
        assert storage.domain_revisions() == revisions_before

    run(scenario())


def test_encrypted_sqlite_close_is_idempotent_and_rejects_later_operations(tmp_path) -> None:
    async def scenario() -> None:
        storage = EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite", key="a" * 32)
        await storage.close()
        await storage.close()
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.load()
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.save(sample_record())
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.mutate(lambda payload: payload)
        with pytest.raises(SessionStorageError, match="closed"):
            await storage.clear()

    run(scenario())


@pytest.mark.parametrize("backend", ["memory", "sqlite"])
def test_atomic_mutations_preserve_concurrent_auth_peer_update_and_metadata_changes(backend, tmp_path) -> None:
    async def scenario() -> None:
        initial = sample_record()
        storage = (
            InMemorySessionStorage(initial)
            if backend == "memory"
            else EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite", key="a" * 32)
        )
        if backend == "sqlite":
            await storage.save(initial)

        def add_peer(payload):
            assert payload is not None
            record = session_record_from_mapping(payload)
            return replace(record, peers=(*record.peers, PeerCacheEntry(id=100, kind="channel", access_hash=1000)))

        def advance_cursor(payload):
            assert payload is not None
            return replace(
                session_record_from_mapping(payload),
                update_state=UpdateState(pts=20, qts=4, seq=8, date=datetime(2026, 7, 1, tzinfo=UTC)),
            )

        def persist_salt(payload):
            assert payload is not None
            record = session_record_from_mapping(payload)
            metadata = dict(record.metadata)
            metadata["server_salt"] = 456
            return replace(record, metadata=metadata)

        def persist_dc_auth(payload):
            assert payload is not None
            record = session_record_from_mapping(payload)
            metadata = dict(record.metadata)
            metadata["dc_auth"] = {"4": {"key": b"m" * 32, "salt": 789}}
            return replace(record, metadata=metadata)

        await asyncio.gather(
            storage.mutate(add_peer),
            storage.mutate(advance_cursor),
            storage.mutate(persist_salt),
            storage.mutate(persist_dc_auth),
        )
        await asyncio.gather(
            storage.mutate(
                lambda payload: replace(session_record_from_mapping(payload or {}), auth_key=None, user=None)
            ),
            storage.mutate(add_peer),
        )
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key is None
        assert record.user is None
        assert record.update_state.pts == 20
        assert record.metadata["server_salt"] == 456
        assert record.metadata["dc_auth"]["4"]["salt"] == 789
        assert {peer.id for peer in record.peers} >= {42, 100}

    run(scenario())


def test_sqlite_mutation_queued_after_clear_receives_none(tmp_path) -> None:
    class PausingClearStorage(EncryptedSQLiteSessionStorage):
        def __init__(self, path) -> None:
            super().__init__(path, key="a" * 32)
            self.clear_acquired = threading.Event()
            self.clear_release = threading.Event()

        def _clear_sync(self) -> None:
            with self._lock:
                self.clear_acquired.set()
                assert self.clear_release.wait(timeout=2)
                super()._clear_sync()

    async def scenario() -> None:
        storage = PausingClearStorage(tmp_path / "session.sqlite")
        await storage.save(sample_record())
        clear_task = asyncio.create_task(storage.clear())
        assert await asyncio.to_thread(storage.clear_acquired.wait, 2)
        received = []
        mutation_task = asyncio.create_task(storage.mutate(lambda payload: received.append(payload) or payload))
        await asyncio.sleep(0)
        storage.clear_release.set()
        await clear_task
        assert await mutation_task is None
        assert received == [None]

    run(scenario())


def test_sqlite_close_commits_active_mutation_then_rejects_queued_mutation(tmp_path) -> None:
    class PausingCloseStorage(EncryptedSQLiteSessionStorage):
        def __init__(self, path) -> None:
            super().__init__(path, key="a" * 32)
            self.close_acquired = threading.Event()
            self.close_release = threading.Event()

        def _close_sync(self) -> None:
            with self._lock:
                self.close_acquired.set()
                assert self.close_release.wait(timeout=2)
                super()._close_sync()

    async def scenario() -> None:
        storage = PausingCloseStorage(tmp_path / "session.sqlite")
        await storage.save(sample_record())
        mutation_started = threading.Event()
        mutation_release = threading.Event()

        def active_mutation(payload):
            mutation_started.set()
            assert mutation_release.wait(timeout=2)
            assert payload is not None
            record = session_record_from_mapping(payload)
            metadata = dict(record.metadata)
            metadata["active_committed"] = True
            return replace(record, metadata=metadata)

        active_task = asyncio.create_task(storage.mutate(active_mutation))
        assert await asyncio.to_thread(mutation_started.wait, 2)
        close_task = asyncio.create_task(storage.close())
        await asyncio.sleep(0)
        mutation_release.set()
        committed = await active_task
        assert committed is not None
        assert committed["metadata"]["active_committed"] is True
        assert await asyncio.to_thread(storage.close_acquired.wait, 2)
        mutation_task = asyncio.create_task(storage.mutate(lambda payload: payload))
        await asyncio.sleep(0)
        storage.close_release.set()
        await close_task
        with pytest.raises(SessionStorageError, match="closed"):
            await mutation_task

    run(scenario())


@pytest.mark.parametrize("backend", ["memory", "sqlite"])
def test_arbitrary_mapping_mutation_stays_in_payload_domain(backend, tmp_path) -> None:
    async def scenario() -> None:
        initial = {"custom": {"bytes": b"\x00\x01", "items": [1, 2, 3]}, "created_at": datetime(2026, 7, 1, tzinfo=UTC)}
        storage = (
            InMemorySessionStorage(initial)
            if backend == "memory"
            else EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite", key="a" * 32)
        )
        if backend == "sqlite":
            await storage.save(initial)
        revisions_before = dict(storage.domain_revisions())
        committed = await storage.mutate(
            lambda payload: {**dict(payload or {}), "custom": {**dict((payload or {})["custom"]), "added": True}}
        )
        assert committed == {**initial, "custom": {**initial["custom"], "added": True}}
        revisions_after = storage.domain_revisions()
        assert revisions_after["payload"] == revisions_before["payload"] + 1
        assert all(
            revisions_after[domain] == revisions_before[domain]
            for domain in ("auth", "peers", "update_state", "metadata")
        )

    run(scenario())


def test_cached_sqlite_mutate_cancellation_waits_for_commit_and_reconciles_cache(tmp_path) -> None:
    async def scenario() -> None:
        backend = PausingSQLiteStorage(tmp_path / "session.sqlite")
        await backend.save({"value": 1})
        storage = _CachedSessionStorage(backend)
        assert await storage.load() == {"value": 1}

        backend.pause("mutate")
        mutation = asyncio.create_task(storage.mutate(lambda payload: {**dict(payload or {}), "value": 2}))
        assert await asyncio.to_thread(backend.operation_started.wait, 2)
        mutation.cancel()
        follower = asyncio.create_task(storage.load())
        await asyncio.sleep(0)
        try:
            assert not mutation.done()
            assert not follower.done()
        finally:
            backend.operation_release.set()

        with pytest.raises(asyncio.CancelledError):
            await mutation
        assert await follower == {"value": 2}
        assert storage.domain_revisions() == backend.domain_revisions()

    run(scenario())


def test_cached_sqlite_save_repeated_cancellation_preserves_first_cancellation_and_reconciles(tmp_path) -> None:
    async def scenario() -> None:
        backend = PausingSQLiteStorage(tmp_path / "session.sqlite")
        await backend.save({"value": 1})
        storage = _CachedSessionStorage(backend)
        assert await storage.load() == {"value": 1}

        backend.pause("save")
        save = asyncio.create_task(storage.save({"value": 2}))
        assert await asyncio.to_thread(backend.operation_started.wait, 2)
        save.cancel("first")
        await asyncio.sleep(0)
        assert not save.done()
        save.cancel("second")
        follower = asyncio.create_task(storage.load())
        await asyncio.sleep(0)
        try:
            assert not save.done()
            assert not follower.done()
        finally:
            backend.operation_release.set()

        with pytest.raises(asyncio.CancelledError) as cancelled:
            await save
        assert str(cancelled.value) == "first"
        assert await follower == {"value": 2}
        assert storage.domain_revisions() == backend.domain_revisions()

    run(scenario())


def test_cached_sqlite_clear_cancellation_waits_for_commit_and_reconciles_cache(tmp_path) -> None:
    async def scenario() -> None:
        backend = PausingSQLiteStorage(tmp_path / "session.sqlite")
        await backend.save({"value": 1})
        storage = _CachedSessionStorage(backend)
        assert await storage.load() == {"value": 1}

        backend.pause("clear")
        clear = asyncio.create_task(storage.clear())
        assert await asyncio.to_thread(backend.operation_started.wait, 2)
        clear.cancel()
        follower = asyncio.create_task(storage.load())
        await asyncio.sleep(0)
        try:
            assert not clear.done()
            assert not follower.done()
        finally:
            backend.operation_release.set()

        with pytest.raises(asyncio.CancelledError):
            await clear
        assert await follower is None
        assert storage.domain_revisions() == backend.domain_revisions()

    run(scenario())


def test_cached_sqlite_close_cancellation_waits_for_backend_and_marks_wrapper_closed(tmp_path) -> None:
    async def scenario() -> None:
        backend = PausingSQLiteStorage(tmp_path / "session.sqlite")
        await backend.save({"value": 1})
        storage = _CachedSessionStorage(backend)
        assert await storage.load() == {"value": 1}

        backend.pause("close")
        close = asyncio.create_task(storage.close())
        assert await asyncio.to_thread(backend.operation_started.wait, 2)
        close.cancel()
        follower = asyncio.create_task(storage.load())
        await asyncio.sleep(0)
        try:
            assert not close.done()
            assert not follower.done()
        finally:
            backend.operation_release.set()

        with pytest.raises(asyncio.CancelledError):
            await close
        with pytest.raises(SessionStorageError, match="closed"):
            await follower
        with pytest.raises(SessionStorageError, match="closed"):
            await backend.load()
        await storage.close()

    run(scenario())


def test_cached_sqlite_cancelled_failed_save_preserves_cache_and_propagates_cancellation(tmp_path) -> None:
    async def scenario() -> None:
        backend = PausingSQLiteStorage(tmp_path / "session.sqlite")
        await backend.save({"value": 1})
        storage = _CachedSessionStorage(backend)
        assert await storage.load() == {"value": 1}
        revisions_before = dict(storage.domain_revisions())

        backend.pause("save", failure=RuntimeError("save failed"))
        save = asyncio.create_task(storage.save({"value": 2}))
        assert await asyncio.to_thread(backend.operation_started.wait, 2)
        save.cancel("cancelled save")
        backend.operation_release.set()

        with pytest.raises(asyncio.CancelledError, match="cancelled save"):
            await save
        assert await storage.load() == {"value": 1}
        assert storage.domain_revisions() == revisions_before
        assert await backend.load() == {"value": 1}

    run(scenario())

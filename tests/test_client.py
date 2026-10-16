from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

import miniproto.client as client_module
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    EncryptedSQLiteSessionStorage,
    InMemorySessionStorage,
    Media,
    Message,
    NewMessage,
    Peer,
    PeerCacheEntry,
    SessionRecord,
    TransportConfig,
    Unauthorized,
    UpdateState,
    UserIdentity,
    event_loop,
    export_session_string,
)
from miniproto.connection.sender import MTProtoSender
from miniproto.errors import FloodWait, ProtocolValidationError, SessionStorageError
from miniproto.invoke import RawSender, build_sender_from_session, load_session_record
from miniproto.mtproto.codec import encode_message_body, gzip_pack
from miniproto.raw import functions, types
from miniproto.session.models import session_record_from_mapping
from miniproto.session.storage import SessionPayload
from miniproto.types import Update


def test_client_config_validates_api_id() -> None:
    with pytest.raises(ValueError, match="api_id"):
        ClientConfig(api_id=0, api_hash="hash")


def test_public_api_imports() -> None:
    config = ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage())
    client = Client(config)
    assert not client.is_connected


def test_client_invoke_forwards_quick_ack_options(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        captured: dict[str, object] = {}

        async def invoke_via_sender(raw_request: object, **kwargs: object) -> object:
            captured["raw_request"] = raw_request
            captured.update(kwargs)
            return b"result"

        monkeypatch.setattr(client, "_invoke_via_sender", invoke_via_sender)

        def callback(receipt: object) -> None:
            del receipt

        request = object()
        assert await client.invoke(request, quick_ack=True, quick_ack_callback=callback) == b"result"
        assert captured["raw_request"] is request
        assert captured["quick_ack"] is True
        assert captured["quick_ack_callback"] is callback

    event_loop.run(run())


def test_default_session_storage_requires_key_before_creating_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("MINIPROTO_SESSION_KEY", raising=False)
    session_path = tmp_path / "missing-key.sqlite"

    with pytest.raises(ValueError, match="requires a key"):
        Client(ClientConfig(api_id=1, api_hash="hash", session_path=session_path))

    assert not session_path.exists()


def test_default_session_storage_uses_encrypted_sqlite_from_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("MINIPROTO_SESSION_KEY", "a sufficiently long session key")
    session_path = tmp_path / "configured.sqlite"

    client = Client(ClientConfig(api_id=1, api_hash="hash", session_path=session_path))

    assert isinstance(client._session_storage_backend, EncryptedSQLiteSessionStorage)
    assert client._session_storage_backend.path == session_path
    assert not session_path.exists()


def test_default_client_construction_does_not_create_repository_session_artifact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MINIPROTO_SESSION_KEY", "a sufficiently long session key")
    default_path = Path.cwd() / "miniproto.session.sqlite"

    config = ClientConfig(api_id=1, api_hash="hash")
    client = Client(config)

    assert config.session_path == "miniproto.session.sqlite"
    assert isinstance(client._session_storage_backend, EncryptedSQLiteSessionStorage)
    assert client._session_storage_backend.path == Path("miniproto.session.sqlite")
    assert not default_path.exists()


def test_explicit_session_storage_takes_precedence_over_default(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("MINIPROTO_SESSION_KEY", raising=False)
    storage = InMemorySessionStorage()
    session_path = tmp_path / "must-not-be-created.sqlite"

    client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, session_path=session_path))

    assert client._session_storage_backend is storage
    assert not session_path.exists()


def test_default_session_storage_rejects_short_environment_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MINIPROTO_SESSION_KEY", "too-short")
    session_path = tmp_path / "short-key.sqlite"

    with pytest.raises(ValueError, match="at least 16 bytes"):
        Client(ClientConfig(api_id=1, api_hash="hash", session_path=session_path))

    assert not session_path.exists()


def test_default_session_storage_uses_stable_sibling_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MINIPROTO_SESSION_KEY", "a sufficiently long session key")
    client = Client(ClientConfig(api_id=1, api_hash="hash", session_path=tmp_path / "account.sqlite"))
    storage = client._session_storage_backend
    assert isinstance(storage, EncryptedSQLiteSessionStorage)

    sibling = storage.sibling("download-1")

    assert sibling.path == tmp_path / "account-download-1.sqlite"
    assert not sibling.path.exists()


def test_default_session_storage_survives_client_restart_with_all_domains(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    async def run() -> None:
        monkeypatch.setenv("MINIPROTO_SESSION_KEY", "a sufficiently long session key")
        session_path = tmp_path / "restart.sqlite"
        expected = SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=b"auth-key-bytes", key_id=123),
            dc_options=(DCOption(id=2, ip_address="149.154.167.51", port=443),),
            user=UserIdentity(id=42, access_hash=99, username="alice"),
            update_state=UpdateState(pts=10, qts=3, seq=7, date=datetime(2026, 7, 16, tzinfo=UTC)),
            peers=(PeerCacheEntry(id=42, kind="user", access_hash=99, username="alice"),),
            metadata={"server_salt": 456, "dc_auth": {"4": {"key": b"m" * 32, "salt": 789}}},
        )
        first = Client(ClientConfig(api_id=1, api_hash="hash", session_path=session_path))
        await first._storage.save(expected)
        await first._storage.close()

        second = Client(ClientConfig(api_id=1, api_hash="hash", session_path=session_path))
        loaded = await second._storage.load()
        await second._storage.close()

        assert loaded is not None
        assert session_record_from_mapping(loaded) == expected

    event_loop.run(run())


def test_client_lifecycle() -> None:
    async def run() -> None:
        async with Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage())) as client:
            assert client.is_connected
        assert not client.is_connected

    event_loop.run(run())


def test_authorization_uses_session_state() -> None:
    async def run() -> None:
        storage = InMemorySessionStorage({"auth_key": b"secret"})
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client.is_authorized()

    event_loop.run(run())


def test_concurrent_sender_initialization_is_single_flight() -> None:
    async def run() -> None:
        class FakeRawSender:
            @property
            def is_connected(self) -> bool:
                return True

            async def request(
                self,
                body: bytes | object,
                *,
                content_related: bool = True,
                retry_safe: bool,
                request_timeout: float | None = None,
            ) -> object:
                del body, content_related, retry_safe, request_timeout
                return b"ok"

            async def disconnect(self) -> None:
                return None

        created = 0

        async def factory(record: object) -> FakeRawSender:
            nonlocal created
            del record
            created += 1
            await asyncio.sleep(0)
            return FakeRawSender()

        storage = InMemorySessionStorage({"auth_key": b"secret"})
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender_factory = factory
        senders = await asyncio.gather(*(client._ensure_sender() for _ in range(10)))
        assert created == 1
        assert len({id(sender) for sender in senders}) == 1

    event_loop.run(run())


def test_get_me_requires_authorized_session() -> None:
    async def run() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        with pytest.raises(Unauthorized):
            await client.get_me()

    event_loop.run(run())


def test_update_dispatch_and_iteration() -> None:
    async def run() -> None:
        peer = Peer(id=123, kind="user", access_hash=456)
        message = Message(id=1, peer=peer, text="hello", date=datetime.now(UTC))
        update = NewMessage(message=message)
        seen: list[NewMessage] = []
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))

        @client.on(NewMessage)
        def handle_new_message(event: NewMessage) -> None:
            seen.append(event)

        iterator = client.iter_updates()
        pending = asyncio.create_task(anext(iterator))
        await asyncio.sleep(0)
        await client._emit_new_message(update)
        queued = await pending
        assert queued == update
        assert seen == [update]
        await iterator.aclose()

    event_loop.run(run())


@pytest.mark.parametrize("operation", ["invoke", "media_authorization"])
@pytest.mark.parametrize("limit_delta", [-1, 0])
def test_client_result_decoding_honors_configured_gzip_limit(operation: str, limit_delta: int) -> None:
    async def run() -> None:
        expected = (
            types.NearestDc(country="FR", this_dc=2, nearest_dc=2)
            if operation == "invoke"
            else types.AuthAuthorization(user=types.User(id=42, first_name="Alice"))
        )
        limit = len(expected.serialize()) + limit_delta

        class CompressedSender:
            is_connected = True

            async def request(
                self,
                body: bytes | object,
                *,
                content_related: bool = True,
                retry_safe: bool,
                request_timeout: float | None = None,
            ) -> object:
                del body, content_related, retry_safe, request_timeout
                return gzip_pack(expected)

            async def disconnect(self) -> None:
                return None

        sender = CompressedSender()
        client = Client(
            ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=InMemorySessionStorage(),
                transport=TransportConfig(max_payload_size=limit),
            )
        )
        client._sender = sender
        await client.connect()

        async def decode() -> object:
            if operation == "invoke":
                return await client.invoke(functions.HelpGetNearestDc())
            return await client._import_exported_authorization(
                sender, types.AuthExportedAuthorization(id=123, bytes=b"synthetic export"), 4
            )

        try:
            if limit_delta < 0:
                with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
                    await decode()
            else:
                result = await decode()
                assert result == (expected if operation == "invoke" else None)
        finally:
            await client.disconnect()

    event_loop.run(run())


@pytest.mark.parametrize("limit_delta", [-1, 0])
def test_decode_pushed_payload_honors_expansion_limit(limit_delta: int) -> None:
    update = types.UpdateShortMessage(id=1, user_id=42, message="hello", pts=1, pts_count=1, date=100)
    payload = encode_message_body(gzip_pack(update))
    limit = len(update.serialize()) + limit_delta
    if limit_delta < 0:
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            client_module._decode_pushed_payload(payload, max_output_size=limit)
    else:
        assert client_module._decode_pushed_payload(payload, max_output_size=limit) == update


@pytest.mark.parametrize("wrappers", [16, 17])
def test_decode_pushed_payload_bounds_nested_wrappers(wrappers: int) -> None:
    update = types.UpdateShortMessage(id=1, user_id=42, message="hello", pts=1, pts_count=1, date=100)
    wrapped = update
    for _ in range(wrappers):
        wrapped = gzip_pack(wrapped)
    payload = encode_message_body(wrapped)
    if wrappers > 16:
        with pytest.raises(ProtocolValidationError, match="gzip_wrapper_depth"):
            client_module._decode_pushed_payload(payload)
    else:
        assert client_module._decode_pushed_payload(payload) == update


@pytest.mark.parametrize("limit_delta", [-1, 0])
def test_receive_dispatch_applies_the_configured_gzip_limit(limit_delta: int) -> None:
    async def run() -> None:
        update = types.UpdateShortMessage(id=1, user_id=42, message="hello", pts=1, pts_count=1, date=100)
        payload = encode_message_body(gzip_pack(update))
        client = Client(
            ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=InMemorySessionStorage(),
                transport=TransportConfig(max_payload_size=len(update.serialize()) + limit_delta),
            )
        )

        class OneUpdateSender:
            received = False

            async def recv_message(self) -> object:
                if self.received:
                    raise EOFError("test sender exhausted")
                self.received = True
                return SimpleNamespace(body=payload)

        try:
            with pytest.raises(EOFError, match="test sender exhausted"):
                await client._receive_dispatch_loop(cast(RawSender, OneUpdateSender()))
            queue = client._update_manager._raw_updates
            if limit_delta < 0:
                assert queue.empty()
            else:
                assert queue.get_nowait() == update
                assert queue.empty()
        finally:
            await client.disconnect()

    event_loop.run(run())


OLD_KEY = b"a" * 256


NEW_KEY = b"b" * 256


OLD_FOREIGN_KEY = b"c" * 256


NEW_FOREIGN_KEY = b"d" * 256


OLD_CDN_KEY = b"e" * 256


def account_record(*, old: bool) -> SessionRecord:
    return SessionRecord(
        dc_id=2,
        auth_key=AuthKey(dc_id=2, key=OLD_KEY if old else NEW_KEY, created_at=datetime(2026, 1, 1, tzinfo=UTC)),
        update_state=UpdateState(date=datetime(2026, 1, 1, tzinfo=UTC)),
        user=UserIdentity(id=41 if old else 93),
        dc_options=(
            DCOption(id=2, ip_address="127.0.0.2", port=443),
            DCOption(id=4, ip_address="127.0.0.4", port=443),
            DCOption(id=5, ip_address="127.0.0.5", port=443, cdn=True),
        ),
        metadata={
            "server_salt": 11 if old else 37,
            "dc_auth": {"4": {"key": OLD_FOREIGN_KEY if old else NEW_FOREIGN_KEY, "salt": 19 if old else 43}},
        },
    )


def client_for(storage: InMemorySessionStorage) -> Client:
    return Client(
        ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage, media_idle_close=None),
        _updates_enabled=False,
    )


class AccountSender:
    def __init__(self, record: SessionRecord, *, block_close: bool = False, fail_close: bool = False) -> None:
        assert record.auth_key is not None
        self.key = record.auth_key.key
        self.is_connected = True
        self.closed = False
        self.fail_close = fail_close
        self.close_started = asyncio.Event()
        self.close_release = asyncio.Event()
        if not block_close:
            self.close_release.set()

    async def request(
        self, body: object, *, content_related: bool = True, retry_safe: bool, request_timeout: float | None = None
    ) -> object:
        del body, content_related, retry_safe, request_timeout
        return types.UploadFile(type=types.StorageFileUnknown(), mtime=0, bytes=self.key[:3])

    async def disconnect(self) -> None:
        self.close_started.set()
        await self.close_release.wait()
        self.closed = True
        self.is_connected = False
        if self.fail_close:
            raise OSError("synthetic sender close failure")


async def download(client: Client, interface: str) -> bytes:
    media = Media(
        id=1,
        size=3,
        dc_id=2,
        location=types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"synthetic", thumb_size=""),
    )
    options: dict[str, Any] = {"media_lanes": 1, "concurrency": 1, "part_size": 4096, "limit": 3}
    if interface == "download":
        result = await client.download_media(media, **options)
        assert result.data is not None
        return result.data
    iterator = client.iter_download(media, **options)
    try:
        return b"".join([chunk async for chunk in iterator])
    finally:
        await iterator.aclose()


@pytest.mark.parametrize("interface", ["download", "stream"])
def test_disconnected_media_cannot_capture_old_account_before_replacement(interface: str) -> None:
    async def scenario() -> None:
        client = client_for(InMemorySessionStorage(account_record(old=True)))
        built: list[AccountSender] = []

        def factory(record: SessionRecord) -> AccountSender:
            sender = AccountSender(record)
            built.append(sender)
            return sender

        client._sender_factory = factory
        with pytest.raises(ConnectionError, match="connected"):
            await download(client, interface)
        assert built == []
        assert client._media_pools == {}
        await client.import_session_string(export_session_string(account_record(old=False)), replace=True)
        await client.connect()
        try:
            assert await download(client, interface) == b"bbb"
            assert [sender.key for sender in built] == [NEW_KEY]
        finally:
            await client.disconnect()

    asyncio.run(scenario())


def test_replacement_discards_cached_credentials_and_ignores_old_salt_callbacks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(account_record(old=True))
        client = client_for(storage)

        async def skip_export(sender: object, dc_id: int) -> None:
            del sender, dc_id

        monkeypatch.setattr(client, "_import_media_authorization", skip_export)
        main = await client._ensure_sender()
        download_pool = await client._get_media_pool(kind="download", lane_count=1, dc_id=2)
        upload_pool = await client._get_media_pool(kind="upload", lane_count=1, dc_id=4)
        await download_pool.prewarm()
        await upload_pool.prewarm()
        same_dc = download_pool._lanes[0]._sender
        foreign = upload_pool._lanes[0]._sender
        cdn = await build_sender_from_session(
            client.config,
            client._storage,
            dc_id_override=5,
            auth_key_override=OLD_CDN_KEY,
            server_salt_override=23,
            require_cdn=True,
        )
        client._cdn_senders[5] = cdn
        client._cdn_auth_cache[5] = (OLD_CDN_KEY, 23)
        client._app_config_hash = 123
        client._upload_limit_parts_cache = 555
        client._media_schedulers.configure_download_limits(small_limit=1, large_limit=1)
        client._method_flood_wait_cache.remember(
            functions.HelpGetNearestDc(), FloodWait(123, message="FLOOD_WAIT_123", code=420)
        )
        assert isinstance(main, MTProtoSender)
        assert isinstance(same_dc, MTProtoSender)
        assert isinstance(foreign, MTProtoSender)
        assert isinstance(cdn, MTProtoSender)
        assert main.on_salt_change is not None
        assert same_dc.on_salt_change is not None
        assert foreign.on_salt_change is not None
        old_callbacks = (main.on_salt_change, same_dc.on_salt_change, foreign.on_salt_change)
        old_callbacks[0](71)
        old_salt_task = client._salt_persist_task
        assert old_salt_task is not None
        replacement = account_record(old=False)

        await client.import_session_string(export_session_string(replacement), replace=True)

        assert all(not sender.is_usable for sender in (main, same_dc, foreign, cdn))
        assert old_salt_task.done()
        assert client._sender is None
        assert client._media_pools == {}
        assert client._cdn_senders == {}
        assert client._dc_auth_cache == {}
        assert client._cdn_auth_cache == {}
        assert client._latest_server_salt is None
        assert client._app_config_hash == 0
        assert client._upload_limit_parts_cache is None
        assert client._method_flood_wait_cache.get(functions.HelpGetNearestDc()) is None
        rebuilt_foreign = await client._build_foreign_media_sender(4)
        rebuilt_main = await client._ensure_sender()
        assert isinstance(rebuilt_foreign, MTProtoSender)
        assert isinstance(rebuilt_main, MTProtoSender)
        assert rebuilt_foreign.state.auth_key == NEW_FOREIGN_KEY
        assert rebuilt_foreign.state.server_salt == 43
        assert rebuilt_main.state.auth_key == NEW_KEY
        assert rebuilt_main.state.server_salt == 37
        for callback in old_callbacks:
            callback(999)
        assert client._latest_server_salt is None
        assert client._dc_auth_cache[4] == (NEW_FOREIGN_KEY, 43)
        assert client._salt_persist_task is None
        assert load_session_record(await storage.load(), 2) == replacement
        await rebuilt_foreign.disconnect()
        await client.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("outcome", ["cancel", "failure"])
def test_replacement_drains_all_old_lanes_before_unlocking_lifecycle(outcome: str) -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(account_record(old=True))
        client = client_for(storage)
        pool = await client._get_media_pool(kind="download", lane_count=2, dc_id=2)
        first = AccountSender(account_record(old=True), fail_close=outcome == "failure")
        blocked = AccountSender(account_record(old=True), block_close=True)
        pool._lanes[0]._sender = first
        pool._lanes[1]._sender = blocked
        operation = asyncio.create_task(
            client.import_session_string(export_session_string(account_record(old=False)), replace=True)
        )
        await blocked.close_started.wait()
        if outcome == "cancel":
            operation.cancel("first cancellation")
            await asyncio.sleep(0)
            operation.cancel("second cancellation")
        connecting = asyncio.create_task(client.connect())
        await asyncio.sleep(0)
        assert not operation.done()
        assert not connecting.done()
        assert not client.is_connected
        assert load_session_record(await storage.load(), 2) == account_record(old=True)
        blocked.close_release.set()
        if outcome == "cancel":
            with pytest.raises(asyncio.CancelledError, match="first cancellation"):
                await operation
        else:
            with pytest.raises(OSError, match="synthetic sender close failure"):
                await operation
        await connecting
        assert first.closed and blocked.closed
        assert load_session_record(await storage.load(), 2) == account_record(old=True)
        await client.disconnect()

    asyncio.run(scenario())


class CommitBlockedStorage(InMemorySessionStorage):
    def __init__(self, record: SessionRecord) -> None:
        super().__init__(record)
        self.committed = asyncio.Event()
        self.release = asyncio.Event()

    async def mutate(
        self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]
    ) -> Mapping[str, Any] | None:
        result = await super().mutate(transform)
        self.committed.set()
        await self.release.wait()
        return result


def test_cancelled_committed_import_connects_only_after_cache_reconciliation() -> None:
    async def scenario() -> None:
        storage = CommitBlockedStorage(account_record(old=True))
        client = client_for(storage)
        old_sender = AccountSender(account_record(old=True))
        client._sender = old_sender
        built: list[AccountSender] = []

        def factory(record: SessionRecord) -> AccountSender:
            sender = AccountSender(record)
            built.append(sender)
            return sender

        client._sender_factory = factory
        operation = asyncio.create_task(
            client.import_session_string(export_session_string(account_record(old=False)), replace=True)
        )
        await storage.committed.wait()
        assert old_sender.closed
        operation.cancel("cancelled after commit")
        connecting = asyncio.create_task(client.connect())
        await asyncio.sleep(0)
        assert not operation.done()
        assert not connecting.done()
        assert not client.is_connected
        storage.release.set()
        with pytest.raises(asyncio.CancelledError, match="cancelled after commit"):
            await operation
        await connecting
        try:
            assert await download(client, "download") == b"bbb"
            assert [sender.key for sender in built] == [NEW_KEY]
        finally:
            await client.disconnect()

    asyncio.run(scenario())


def test_refused_implicit_replacement_keeps_existing_resources() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(account_record(old=True))
        client = client_for(storage)
        sender = AccountSender(account_record(old=True))
        client._sender = sender
        with pytest.raises(ValueError, match="not empty"):
            await client.import_session_string(export_session_string(account_record(old=False)))
        assert client._sender is sender
        assert not sender.closed
        assert load_session_record(await storage.load(), 2) == account_record(old=True)
        await client.disconnect()

    asyncio.run(scenario())


def test_terminal_disconnect_rejects_import_and_closes_old_media() -> None:
    async def scenario() -> None:
        client = client_for(InMemorySessionStorage(account_record(old=True)))
        senders: list[AccountSender] = []

        def factory(record: SessionRecord) -> AccountSender:
            sender = AccountSender(record)
            senders.append(sender)
            return sender

        client._sender_factory = factory
        await client.connect()
        assert await download(client, "download") == b"aaa"
        await client.disconnect()
        with pytest.raises(SessionStorageError, match="closed"):
            await client.import_session_string(export_session_string(account_record(old=False)), replace=True)
        assert all(sender.closed for sender in senders)
        assert not client.is_connected

    asyncio.run(scenario())


def test_failed_bootstrap_replacement_reloads_cursor_and_preserves_subscribers() -> None:
    class FailedBootstrapSender(AccountSender):
        async def request(
            self, body: object, *, content_related: bool = True, retry_safe: bool, request_timeout: float | None = None
        ) -> object:
            del body, content_related, retry_safe, request_timeout
            raise RuntimeError("synthetic bootstrap failure")

    async def scenario() -> None:
        source = account_record(old=True)
        source = replace(
            source,
            update_state=replace(source.update_state, pts=10),
            metadata={
                **source.metadata,
                "update_state_bootstrap_required": True,
                "updates": {"recent_update_keys": ["old-event"]},
            },
        )
        target = account_record(old=False)
        target = replace(
            target,
            update_state=replace(target.update_state, pts=300),
            metadata={**target.metadata, "updates": {"recent_update_keys": ["new-event"]}},
        )
        storage = InMemorySessionStorage(source)
        client = Client(ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage))
        client._sender_factory = FailedBootstrapSender
        received: list[Update] = []
        client.on(Update, received.append)
        iterator = client.iter_updates()
        first = asyncio.create_task(anext(iterator))
        await asyncio.sleep(0)
        await client._emit_update(Update(raw="already-delivered"))
        assert (await first).raw == "already-delivered"
        with pytest.raises(RuntimeError, match="synthetic bootstrap failure"):
            await client.connect()
        manager = client._update_manager
        assert manager._cursor is not None and manager._cursor.pts == 10
        assert manager._duplicates.keys() == ("old-event",)
        await client._emit_update(Update(raw="old-queued"))
        await client._feed_raw_update(
            types.UpdateShortMessage(id=11, user_id=41, message="old", pts=11, pts_count=1, date=100)
        )
        public_queue = manager._updates
        raw_queue = manager._raw_updates
        assert not public_queue.empty() and not raw_queue.empty()

        await client.import_session_string(export_session_string(target), replace=True)

        assert client._update_manager is manager
        assert manager._updates is public_queue and manager._raw_updates is raw_queue
        assert public_queue.empty() and raw_queue.empty()
        assert manager._iterator_count == 1
        assert manager._duplicates.keys() == ()
        await client.connect()
        assert manager._cursor is not None and manager._cursor.pts == 300
        assert manager._duplicates.keys() == ("new-event",)
        pending = asyncio.create_task(anext(iterator))
        await client._feed_raw_update(
            types.UpdateShortMessage(id=42, user_id=93, message="new", pts=301, pts_count=1, date=200)
        )
        try:
            update = await asyncio.wait_for(pending, 1)
            assert isinstance(update, NewMessage)
            assert update.message is not None and update.message.id == 42
            assert received[-1] is update
            assert len(received) == 3
            assert load_session_record(await storage.load(), 2).update_state.pts == 301
        finally:
            await iterator.aclose()
            await client.disconnect()

    asyncio.run(scenario())

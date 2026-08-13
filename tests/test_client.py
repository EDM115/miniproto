from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    EncryptedSQLiteSessionStorage,
    InMemorySessionStorage,
    Message,
    NewMessage,
    Peer,
    PeerCacheEntry,
    SessionRecord,
    Unauthorized,
    UpdateState,
    UserIdentity,
    event_loop,
)
from miniproto.session.models import session_record_from_mapping


def test_client_config_validates_api_id() -> None:
    with pytest.raises(ValueError, match="api_id"):
        ClientConfig(api_id=0, api_hash="hash")


def test_client_config_hides_bot_token_from_repr() -> None:
    config = ClientConfig(api_id=1, api_hash="hash", bot_token="123:secret")  # noqa: S106
    assert "123:secret" not in repr(config)


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

        await client._emit_new_message(update)
        iterator = client.iter_updates()
        queued = await anext(iterator)
        assert queued == update
        assert seen == [update]

    event_loop.run(run())

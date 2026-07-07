from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Peer,
    SessionRecord,
    UserIdentity,
    event_loop,
)
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, session_record_from_mapping

AUTH_KEY = b"p" * 256


@dataclass(slots=True)
class FakeSender:
    responses: list[object]
    requests: list[object] = field(default_factory=list)
    is_connected: bool = True

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        self.requests.append(body)
        if not self.responses:
            raise AssertionError("fake sender has no queued response")
        return self.responses.pop(0)

    async def disconnect(self) -> None:
        self.is_connected = False


def run(coro):
    return event_loop.run(coro)


def storage_with_record() -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
        )
    )


def inner_request(wrapped: object) -> object:
    if isinstance(wrapped, functions.InvokeWithoutUpdates):
        wrapped = wrapped.query
    if isinstance(wrapped, functions.InvokeWithLayer):
        assert isinstance(wrapped.query, functions.InitConnection)
        return wrapped.query.query
    return wrapped


def test_get_me_fetches_generated_users_get_users_and_persists_self_identity() -> None:
    async def scenario() -> None:
        storage = storage_with_record()
        sender = FakeSender(
            [
                (
                    types.User(
                        self_=True, id=42, access_hash=9900, username="alice", first_name="Alice"
                    ),
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        me = await client.get_me()
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.UsersGetUsers)
        assert isinstance(request.id[0], types.InputUserSelf)
        assert me.id == 42
        assert me.peer == Peer(id=42, kind="self", access_hash=9900)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.user == UserIdentity(
            id=42, access_hash=9900, username="alice", first_name="Alice"
        )
        assert record.peers[0].kind == "self"
        assert record.peers[0].username == "alice"

    run(scenario())


def test_get_me_uses_cached_identity_without_raw_request() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(user=UserIdentity(id=42, access_hash=9900, username="alice"))
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        me = await client.get_me()
        assert me.username == "alice"
        assert me.peer == Peer(id=42, kind="self", access_hash=9900)

    run(scenario())


def test_resolve_peer_fills_missing_access_hash_from_cache() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),)
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        resolved = await client.resolve_peer(Peer(id=7, kind="user"))
        assert resolved == Peer(id=7, kind="user", access_hash=77)

    run(scenario())


def test_resolve_username_uses_case_insensitive_cache() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(
                        id=7,
                        kind="user",
                        access_hash=77,
                        username="Alice",
                        raw={"usernames": ["AliceAlt"]},
                    ),
                )
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client.resolve_peer("@alicealt") == Peer(id=7, kind="user", access_hash=77)

    run(scenario())


def test_resolve_username_fetches_contacts_resolve_username_and_caches_access_hash() -> None:
    async def scenario() -> None:
        storage = storage_with_record()
        sender = FakeSender(
            [
                types.ContactsResolvedPeer(
                    peer=types.PeerUser(user_id=8),
                    users=(types.User(id=8, access_hash=88, username="Bob"),),
                    chats=(),
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        resolved = await client.resolve_peer("https://t.me/Bob")
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.ContactsResolveUsername)
        assert request.username == "bob"
        assert resolved == Peer(id=8, kind="user", access_hash=88)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.peers[0].username == "Bob"
        assert record.peers[0].access_hash == 88

    run(scenario())


def test_resolve_numeric_peer_seeds_dialog_cache_when_missing() -> None:
    async def scenario() -> None:
        storage = storage_with_record()
        sender = FakeSender(
            [
                types.MessagesDialogs(
                    dialogs=(),
                    messages=(),
                    chats=(),
                    users=(types.User(id=854158484, access_hash=484, username="EDM115"),),
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        resolved = await client.resolve_peer("854158484")
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesGetDialogs)
        assert isinstance(request.offset_peer, types.InputPeerEmpty)
        assert request.limit == 100
        assert resolved == Peer(id=854158484, kind="user", access_hash=484)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.peers[0].id == 854158484
        assert record.peers[0].access_hash == 484

    run(scenario())


def test_resolve_phone_and_encoded_channel_id_from_cache() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=9, kind="user", access_hash=99, phone="+1 555 0100"),
                    PeerCacheEntry(id=1234567890, kind="channel", access_hash=44),
                )
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client.resolve_peer("+15550100") == Peer(id=9, kind="user", access_hash=99)
        assert await client.resolve_peer(-1001234567890) == Peer(
            id=1234567890, kind="channel", access_hash=44
        )

    run(scenario())


def test_resolve_peer_requires_cached_access_hash_for_users_and_channels() -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash"))
        with pytest.raises(Exception, match="access hash"):
            await client.resolve_peer(Peer(id=1, kind="user"))

    run(scenario())

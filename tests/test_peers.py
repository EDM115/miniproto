from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

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
from miniproto.peers import PeerCache, _merge_entries
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, UpdateState, session_record_from_mapping
from miniproto.session.storage import SessionPayload

AUTH_KEY = b"p" * 256


class MutationOnlySessionStorage(InMemorySessionStorage):
    async def save(self, data: SessionPayload) -> None:
        del data
        raise AssertionError("peer persistence must use atomic mutate")


class CountingSessionStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionRecord) -> None:
        super().__init__(initial)
        self.load_count = 0

    async def load(self):
        self.load_count += 1
        return await super().load()


class PostCommitCancellationStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionRecord) -> None:
        super().__init__(initial)
        self.committed = asyncio.Event()

    async def mutate(self, transform):
        committed = await super().mutate(transform)
        self.committed.set()
        await asyncio.Event().wait()
        return committed


class InterleavingPeerStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionRecord) -> None:
        super().__init__(initial)
        self.external_entry: PeerCacheEntry | None = None

    async def mutate(self, transform):
        external = self.external_entry
        self.external_entry = None
        if external is not None:

            def add_external(payload):
                record = session_record_from_mapping(payload or {})
                return SessionRecord(
                    dc_id=record.dc_id,
                    auth_key=record.auth_key,
                    dc_options=record.dc_options,
                    user=record.user,
                    update_state=record.update_state,
                    peers=(*record.peers, external),
                    metadata=record.metadata,
                )

            await super().mutate(add_external)
        return await super().mutate(transform)


class PausingLoadStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionRecord) -> None:
        super().__init__(initial)
        self.load_started = asyncio.Event()
        self.release_load = asyncio.Event()
        self.pause_next_load = True

    async def load(self):
        if self.pause_next_load:
            self.pause_next_load = False
            self.load_started.set()
            await self.release_load.wait()
        return await super().load()


class FailingMutationStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionRecord) -> None:
        super().__init__(initial)
        self.fail_mutation = False

    async def mutate(self, transform):
        if self.fail_mutation:
            raise RuntimeError("injected pre-commit failure")
        return await super().mutate(transform)


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
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
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
        sender = FakeSender([(types.User(self_=True, id=42, access_hash=9900, username="alice", first_name="Alice"),)])
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
        assert record.user == UserIdentity(id=42, access_hash=9900, username="alice", first_name="Alice")
        assert record.peers[0].kind == "self"
        assert record.peers[0].username == "alice"

    run(scenario())


def test_peer_cache_persists_with_atomic_mutation_and_preserves_unrelated_domains() -> None:
    async def scenario() -> None:
        storage = MutationOnlySessionStorage(
            SessionRecord(dc_id=2, update_state=UpdateState(pts=17), metadata={"server_salt": 123})
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client._peer_cache.remember_raw_entities(types.User(id=42, access_hash=9000, username="alice"))
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 17
        assert record.metadata["server_salt"] == 123
        assert record.peers[0].id == 42

    run(scenario())


def test_get_me_uses_cached_identity_without_raw_request() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(user=UserIdentity(id=42, access_hash=9900, username="alice")))
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        me = await client.get_me()
        assert me.username == "alice"
        assert me.peer == Peer(id=42, kind="self", access_hash=9900)

    run(scenario())


def test_resolve_peer_fills_missing_access_hash_from_cache() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),))
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
                        id=7, kind="user", access_hash=77, username="Alice", raw={"usernames": ["AliceAlt"]}
                    ),
                )
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client.resolve_peer("@alicealt") == Peer(id=7, kind="user", access_hash=77)

    run(scenario())


def test_resolve_username_refreshes_stale_cached_usernames() -> None:
    async def scenario() -> None:
        old = datetime.now(UTC) - timedelta(days=2)
        storage = InMemorySessionStorage(
            SessionRecord(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="Alice", updated_at=old),))
        )
        sender = FakeSender(
            [
                types.ContactsResolvedPeer(
                    peer=types.PeerUser(user_id=8),
                    users=(types.User(id=8, access_hash=88, username="Alice"),),
                    chats=(),
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        assert await client.resolve_peer("@alice") == Peer(id=8, kind="user", access_hash=88)
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.ContactsResolveUsername)

    run(scenario())


def test_resolve_username_fetches_contacts_resolve_username_and_caches_access_hash() -> None:
    async def scenario() -> None:
        storage = storage_with_record()
        sender = FakeSender(
            [
                types.ContactsResolvedPeer(
                    peer=types.PeerUser(user_id=8), users=(types.User(id=8, access_hash=88, username="Bob"),), chats=()
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


def test_min_user_and_channel_entities_do_not_poison_cached_access_hashes() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage()
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client._peer_cache.remember_raw_entities(
            types.ContactsResolvedPeer(
                peer=types.PeerUser(user_id=7),
                users=(types.User(id=7, access_hash=77, min=True, username="alice"),),
                chats=(
                    types.Channel(
                        id=123,
                        access_hash=999,
                        min=True,
                        title="Channel",
                        photo=types.ChatPhotoEmpty(),
                        date=1_700_000_000,
                        username="channel",
                    ),
                ),
            )
        )
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert any(peer.id == 7 and peer.access_hash is None for peer in record.peers)
        assert any(peer.id == 123 and peer.access_hash is None for peer in record.peers)
        await client._peer_cache.remember_raw_entities(
            types.ContactsResolvedPeer(
                peer=types.PeerUser(user_id=7),
                users=(types.User(id=7, access_hash=78, username="alice"),),
                chats=(
                    types.Channel(
                        id=123,
                        access_hash=1000,
                        title="Channel",
                        photo=types.ChatPhotoEmpty(),
                        date=1_700_000_001,
                        username="channel",
                    ),
                ),
            )
        )
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert any(peer.id == 7 and peer.access_hash == 78 for peer in record.peers)
        assert any(peer.id == 123 and peer.access_hash == 1000 for peer in record.peers)

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
        assert await client.resolve_peer(-1001234567890) == Peer(id=1234567890, kind="channel", access_hash=44)

    run(scenario())


def test_resolve_peer_requires_cached_access_hash_for_users_and_channels() -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        with pytest.raises(Exception, match="access hash"):
            await client.resolve_peer(Peer(id=1, kind="user"))

    run(scenario())


def test_numeric_index_preserves_duplicate_kind_and_self_precedence() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                user=UserIdentity(id=7, access_hash=700),
                peers=(
                    PeerCacheEntry(id=7, kind="self", access_hash=70),
                    PeerCacheEntry(id=7, kind="user", access_hash=71),
                    PeerCacheEntry(id=7, kind="chat"),
                    PeerCacheEntry(id=7, kind="channel", access_hash=72),
                ),
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(7) == Peer(id=7, kind="self", access_hash=70)
        assert await cache.resolve_peer(Peer(id=7, kind="user")) == Peer(id=7, kind="user", access_hash=71)
        assert await cache.resolve_peer(-7) == Peer(id=7, kind="chat")
        assert await cache.resolve_peer(-1_000_000_000_007) == Peer(id=7, kind="channel", access_hash=72)

    run(scenario())


def test_partial_same_key_merge_advances_updated_at_and_preserves_fields() -> None:
    old = datetime.now(UTC) - timedelta(days=2)
    new = datetime.now(UTC)
    current = PeerCacheEntry(
        id=7,
        kind="user",
        access_hash=77,
        username="Alice",
        phone="+1 555 0100",
        updated_at=old,
        raw={"first_name": "Alice", "usernames": ["AliceAlt"]},
    )
    partial = PeerCacheEntry(id=7, kind="user", updated_at=new, raw={"last_name": "Example"})
    assert _merge_entries((current,), (partial,)) == (
        PeerCacheEntry(
            id=7,
            kind="user",
            access_hash=77,
            username="Alice",
            phone="+1 555 0100",
            updated_at=new,
            raw={"first_name": "Alice", "usernames": ["AliceAlt"], "last_name": "Example"},
        ),
    )


def test_username_conflict_skips_stale_first_owner_and_returns_later_fresh_without_network() -> None:
    async def scenario() -> None:
        old = datetime.now(UTC) - timedelta(days=2)
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=1, kind="user", access_hash=11, username="shared", updated_at=old),
                    PeerCacheEntry(id=2, kind="user", access_hash=22, username="shared"),
                )
            )
        )
        requests: list[object] = []

        def invoke(request: object) -> object:
            requests.append(request)
            raise AssertionError("fresh later owner must avoid network resolution")

        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, invoke)
        assert await cache.resolve_peer("@shared") == Peer(id=2, kind="user", access_hash=22)
        assert requests == []

    run(scenario())


def test_username_conflict_all_stale_resolves_network_once() -> None:
    async def scenario() -> None:
        old = datetime.now(UTC) - timedelta(days=2)
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=1, kind="user", access_hash=11, username="shared", updated_at=old),
                    PeerCacheEntry(id=2, kind="user", access_hash=22, username="shared", updated_at=old),
                )
            )
        )
        requests: list[object] = []

        def invoke(request: object) -> object:
            requests.append(request)
            return types.ContactsResolvedPeer(
                peer=types.PeerUser(user_id=2), users=(types.User(id=2, access_hash=222, username="shared"),), chats=()
            )

        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, invoke)
        assert await cache.resolve_peer("@shared") == Peer(id=2, kind="user", access_hash=222)
        assert await cache.resolve_peer("@shared") == Peer(id=2, kind="user", access_hash=222)
        assert len(requests) == 1

    run(scenario())


def test_warm_kind_username_phone_and_numeric_lookups_do_not_reload_or_scan() -> None:
    async def scenario() -> None:
        storage = CountingSessionStorage(
            SessionRecord(
                peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="Alice", phone="+1 555 0100"),)
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(Peer(id=7, kind="user")) == Peer(id=7, kind="user", access_hash=77)
        warm_loads = storage.load_count
        warm_stats = cache.index_stats
        for reference in (7, "@alice", "+15550100", Peer(id=7, kind="user")):
            assert await cache.resolve_peer(reference) == Peer(id=7, kind="user", access_hash=77)
        assert storage.load_count == warm_loads
        assert cache.index_stats["rebuilds"] == warm_stats["rebuilds"]
        assert cache.index_stats["canonical_tuple_visits"] == warm_stats["canonical_tuple_visits"]

    run(scenario())


def test_committed_direct_merge_updates_indexes_without_full_rebuild() -> None:
    async def scenario() -> None:
        storage = CountingSessionStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        warm_stats = cache.index_stats
        await cache.remember_raw_entities(types.User(id=2, access_hash=22, username="second", phone="+12025550102"))
        assert await cache.resolve_peer("@second") == Peer(id=2, kind="user", access_hash=22)
        assert cache.index_stats["rebuilds"] == warm_stats["rebuilds"]
        assert cache.index_stats["incremental_reconciliations"] == warm_stats["incremental_reconciliations"] + 1

    run(scenario())


def test_multi_entry_direct_merge_preserves_canonical_new_owner_order() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="chat"),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="chat")
        incoming = tuple(
            PeerCacheEntry(id=peer_id, kind="user", access_hash=peer_id, username="shared") for peer_id in range(2, 22)
        )
        await cache._save_entries(incoming)
        assert await cache.resolve_peer("@shared") == Peer(id=2, kind="user", access_hash=2)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert tuple(entry.id for entry in record.peers[1:]) == tuple(range(2, 22))

    run(scenario())


def test_same_id_self_then_user_incremental_merge_matches_canonical_order() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(PeerCacheEntry(id=7, kind="user", access_hash=700, username="previous", phone="+12025550700"),)
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(7) == Peer(id=7, kind="user", access_hash=700)
        warm = dict(cache.index_stats)

        await cache._save_entries(
            (
                PeerCacheEntry(id=7, kind="self", access_hash=70, username="shared", phone="+12025550100"),
                PeerCacheEntry(id=7, kind="user", access_hash=71, username="shared", phone="+12025550100"),
            )
        )

        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert tuple((entry.kind, entry.id) for entry in record.peers) == (("self", 7), ("user", 7))
        assert await cache.resolve_peer("@shared") == Peer(id=7, kind="self", access_hash=70)
        assert await cache.resolve_peer("+12025550100") == Peer(id=7, kind="self", access_hash=70)
        assert await cache.resolve_peer(7) == Peer(id=7, kind="self", access_hash=70)
        assert await cache.resolve_peer(Peer(id=7, kind="user")) == Peer(id=7, kind="user", access_hash=71)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"]
        assert cache.index_stats["canonical_tuple_visits"] == warm["canonical_tuple_visits"]

    run(scenario())


def test_same_id_user_then_self_incremental_merge_removes_user_canonically() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="chat"),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="chat")
        warm = dict(cache.index_stats)

        await cache._save_entries(
            (
                PeerCacheEntry(id=7, kind="user", access_hash=71, username="shared", phone="+12025550100"),
                PeerCacheEntry(id=7, kind="self", access_hash=70, username="shared", phone="+12025550100"),
            )
        )

        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert tuple((entry.kind, entry.id) for entry in record.peers) == (("chat", 1), ("self", 7))
        assert await cache.resolve_peer("@shared") == Peer(id=7, kind="self", access_hash=70)
        assert await cache.resolve_peer("+12025550100") == Peer(id=7, kind="self", access_hash=70)
        assert await cache.resolve_peer(7) == Peer(id=7, kind="self", access_hash=70)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"]
        assert cache.index_stats["canonical_tuple_visits"] == warm["canonical_tuple_visits"]

    run(scenario())


def test_username_owner_drop_promotes_next_durable_owner() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=1, kind="user", access_hash=11, username="shared"),
                    PeerCacheEntry(id=2, kind="user", access_hash=22, username="shared"),
                )
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer("@shared") == Peer(id=1, kind="user", access_hash=11)
        warm = cache.index_stats
        await cache._save_entries(
            (PeerCacheEntry(id=1, kind="user", access_hash=11, username="renamed", raw={"usernames": ["renamed-alt"]}),)
        )
        assert await cache.resolve_peer("@shared") == Peer(id=2, kind="user", access_hash=22)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"]
        assert cache.index_stats["canonical_tuple_visits"] == warm["canonical_tuple_visits"]

    run(scenario())


def test_phone_owner_change_promotes_next_durable_owner() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=1, kind="user", access_hash=11, phone="+1 202 555 0100"),
                    PeerCacheEntry(id=2, kind="user", access_hash=22, phone="12025550100"),
                )
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer("+12025550100") == Peer(id=1, kind="user", access_hash=11)
        warm = cache.index_stats
        await cache._save_entries((PeerCacheEntry(id=1, kind="user", access_hash=11, phone="+1 202 555 0199"),))
        assert await cache.resolve_peer("+12025550100") == Peer(id=2, kind="user", access_hash=22)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"]
        assert cache.index_stats["canonical_tuple_visits"] == warm["canonical_tuple_visits"]

    run(scenario())


def test_earlier_durable_key_acquiring_existing_alias_takes_precedence() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=1, kind="user", access_hash=11, username="first"),
                    PeerCacheEntry(id=2, kind="user", access_hash=22, username="shared"),
                )
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer("@shared") == Peer(id=2, kind="user", access_hash=22)
        warm = dict(cache.index_stats)
        await cache._save_entries((PeerCacheEntry(id=1, kind="user", access_hash=11, username="shared"),))
        assert await cache.resolve_peer("@shared") == Peer(id=1, kind="user", access_hash=11)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"]
        assert cache.index_stats["canonical_tuple_visits"] == warm["canonical_tuple_visits"]

    run(scenario())


def test_legacy_benchmark_username_lookup_skips_stale_duplicate_alias_owner() -> None:
    from tools.bench.benchmark_runtime_paths import _legacy_username_lookup

    now = datetime.now(UTC)
    record = SessionRecord(
        peers=(
            PeerCacheEntry(
                id=1, kind="user", access_hash=11, updated_at=now - timedelta(days=2), raw={"usernames": ["shared"]}
            ),
            PeerCacheEntry(id=2, kind="user", access_hash=22, updated_at=now, raw={"usernames": ["shared"]}),
        )
    )
    assert run(_legacy_username_lookup(record, "@shared")) == Peer(id=2, kind="user", access_hash=22)


def test_raw_username_strings_preserve_current_alias_semantics() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                peers=(
                    PeerCacheEntry(id=7, kind="user", access_hash=77, raw={"usernames": ["persisted-inactive-alias"]}),
                )
            )
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer("@persisted-inactive-alias") == Peer(id=7, kind="user", access_hash=77)

    run(scenario())


def test_update_state_and_metadata_revisions_do_not_rebuild_peer_indexes() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(7) == Peer(id=7, kind="user", access_hash=77)
        warm = cache.index_stats

        def update_unrelated(payload):
            record = session_record_from_mapping(payload or {})
            return SessionRecord(
                dc_id=record.dc_id,
                auth_key=record.auth_key,
                dc_options=record.dc_options,
                user=record.user,
                update_state=UpdateState(pts=1),
                peers=record.peers,
                metadata={"updated": True},
            )

        await storage.mutate(update_unrelated)
        assert await cache.resolve_peer(7) == Peer(id=7, kind="user", access_hash=77)
        assert cache.index_stats == warm

    run(scenario())


def test_external_peer_and_auth_domain_mutations_rebuild_once() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        warm = cache.index_stats

        def add_peer(payload):
            record = session_record_from_mapping(payload or {})
            return SessionRecord(
                dc_id=record.dc_id,
                auth_key=record.auth_key,
                dc_options=record.dc_options,
                user=record.user,
                update_state=record.update_state,
                peers=(*record.peers, PeerCacheEntry(id=2, kind="user", access_hash=22)),
                metadata=record.metadata,
            )

        await storage.mutate(add_peer)
        assert await cache.resolve_peer(2) == Peer(id=2, kind="user", access_hash=22)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"] + 1
        after_peer = cache.index_stats

        def add_identity(payload):
            record = session_record_from_mapping(payload or {})
            return SessionRecord(
                dc_id=record.dc_id,
                auth_key=record.auth_key,
                dc_options=record.dc_options,
                user=UserIdentity(id=9, access_hash=99),
                update_state=record.update_state,
                peers=record.peers,
                metadata=record.metadata,
            )

        await storage.mutate(add_identity)
        assert (await cache.get_me()).id == 9
        assert cache.index_stats["rebuilds"] == after_peer["rebuilds"] + 1
        after_auth = cache.index_stats
        assert (await cache.get_me()).id == 9
        assert cache.index_stats == after_auth

    run(scenario())


def test_external_peer_commit_queued_between_ensure_and_direct_mutate_cannot_be_hidden() -> None:
    async def scenario() -> None:
        storage = InterleavingPeerStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        warm = cache.index_stats
        storage.external_entry = PeerCacheEntry(id=2, kind="user", access_hash=22)
        await cache._save_entries((PeerCacheEntry(id=3, kind="user", access_hash=33),))
        assert await cache.resolve_peer(2) == Peer(id=2, kind="user", access_hash=22)
        assert await cache.resolve_peer(3) == Peer(id=3, kind="user", access_hash=33)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"] + 1
        assert cache.index_stats["incremental_reconciliations"] == warm["incremental_reconciliations"]

    run(scenario())


def test_cancelled_post_commit_peer_merge_marks_indexes_stale_then_rebuilds() -> None:
    async def scenario() -> None:
        storage = PostCommitCancellationStorage(
            SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),))
        )
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        warm = cache.index_stats
        task = asyncio.create_task(cache._save_entries((PeerCacheEntry(id=2, kind="user", access_hash=22),)))
        await storage.committed.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert cache.index_stats == warm
        assert await cache.resolve_peer(2) == Peer(id=2, kind="user", access_hash=22)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"] + 1
        assert await cache.resolve_peer(2) == Peer(id=2, kind="user", access_hash=22)
        assert cache.index_stats["rebuilds"] == warm["rebuilds"] + 1

    run(scenario())


def test_warm_client_peer_lookups_never_call_cached_storage_load() -> None:
    async def scenario() -> None:
        backend = InMemorySessionStorage(
            SessionRecord(
                peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice", phone="+12025550100"),)
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=backend))
        storage = client._storage
        original_load = storage.load
        calls = 0

        async def counting_load():
            nonlocal calls
            calls += 1
            return await original_load()

        storage_handle: Any = storage
        storage_handle.load = counting_load
        assert await client.resolve_peer(7) == Peer(id=7, kind="user", access_hash=77)
        warm_calls = calls
        for reference in ("@alice", "+12025550100", Peer(id=7, kind="user"), 7):
            assert await client.resolve_peer(reference) == Peer(id=7, kind="user", access_hash=77)
        assert calls == warm_calls == 1

    run(scenario())


def test_concurrent_cold_lookup_and_merge_publish_one_consistent_index() -> None:
    async def scenario() -> None:
        storage = PausingLoadStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        lookup = asyncio.create_task(cache.resolve_peer(1))
        await storage.load_started.wait()
        merge = asyncio.create_task(
            cache._save_entries(
                (PeerCacheEntry(id=2, kind="user", access_hash=22, username="second", phone="+12025550102"),)
            )
        )
        await asyncio.sleep(0)
        storage.release_load.set()
        assert await lookup == Peer(id=1, kind="user", access_hash=11)
        await merge
        assert await cache.resolve_peer(2) == Peer(id=2, kind="user", access_hash=22)
        assert await cache.resolve_peer("@second") == Peer(id=2, kind="user", access_hash=22)
        assert await cache.resolve_peer("+12025550102") == Peer(id=2, kind="user", access_hash=22)

    run(scenario())


def test_failed_peer_mutation_does_not_publish_incoming_indexes() -> None:
    async def scenario() -> None:
        storage = FailingMutationStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),)))
        cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, lambda _: ())
        assert await cache.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        warm = cache.index_stats
        storage.fail_mutation = True
        with pytest.raises(RuntimeError, match="pre-commit"):
            await cache._save_entries((PeerCacheEntry(id=2, kind="user", access_hash=22),))
        with pytest.raises(Exception, match="access hash"):
            await cache.resolve_peer(Peer(id=2, kind="user"))
        assert await cache.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        assert cache.index_stats == warm

    run(scenario())

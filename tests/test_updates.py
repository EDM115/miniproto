from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Literal

import pytest
from tools.bench.fake_mtproto import FakeMTProtoServer

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    EncryptedSQLiteSessionStorage,
    InMemorySessionStorage,
    NewMessage,
    SessionRecord,
    TransportConfig,
    encode_file_id,
    event_loop,
)
from miniproto.config import UpdateQueueOverflowPolicy
from miniproto.errors import NotFound
from miniproto.mtproto.codec import MessageContainer, MessageContainerItem, RpcResult
from miniproto.peers import PeerCache
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, UpdateState, session_record_from_mapping
from miniproto.session.storage import SessionPayload
from miniproto.types import Message, Peer, Update
from miniproto.updates.manager import UpdateManager
from miniproto.updates.state import EntityReference, UpdateCursor, merge_peer_cache_entries

AUTH_KEY = b"u" * 256


class MutationOnlySessionStorage(InMemorySessionStorage):
    async def save(self, data: SessionPayload) -> None:
        del data
        raise AssertionError("update persistence must use atomic mutate")


def run(coro):
    return event_loop.run(coro)


class FakeUpdateClient(Client):
    def __init__(self, config: ClientConfig, responses: list[object] | None = None) -> None:
        super().__init__(config)
        self.responses = responses or []
        self.update_requests: list[object] = []

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
        quick_ack: bool = False,
        quick_ack_callback: object | None = None,
    ) -> object:
        del quick_ack, quick_ack_callback
        self.update_requests.append(raw_request)
        if not self.responses:
            raise AssertionError("fake update client has no queued invoke response")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def storage_with_state(*, pts: int = 0, qts: int = 0, seq: int = 0, date: int = 1) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(update_state=UpdateState(pts=pts, qts=qts, seq=seq, date=datetime.fromtimestamp(date, UTC)))
    )


def storage_with_channel_state(*, channel_id: int = 123, pts: int = 10) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            peers=(PeerCacheEntry(id=channel_id, kind="channel", access_hash=999),),
            metadata={
                "updates": {
                    "channels": {str(channel_id): {"pts": pts, "date": datetime.fromtimestamp(50, UTC).isoformat()}}
                }
            },
        )
    )


def raw_message(message_id: int, text: str, *, user_id: int = 42, date: int = 100) -> types.Message:
    return types.Message(id=message_id, peer_id=types.PeerUser(user_id=user_id), date=date, message=text)


def raw_channel_message(message_id: int, text: str, *, channel_id: int = 123, date: int = 100) -> types.Message:
    return types.Message(id=message_id, peer_id=types.PeerChannel(channel_id=channel_id), date=date, message=text)


def short_message(
    message_id: int, text: str, *, user_id: int = 42, pts: int = 1, pts_count: int = 1, date: int = 100
) -> types.UpdateShortMessage:
    return types.UpdateShortMessage(
        id=message_id, user_id=user_id, message=text, pts=pts, pts_count=pts_count, date=date
    )


def public_message(text: str, *, message_id: int = 1) -> NewMessage:
    return NewMessage(
        message=Message(id=message_id, peer=Peer(id=42, kind="user"), text=text, date=datetime.fromtimestamp(100, UTC))
    )


def test_short_update_normalization_persists_state_and_duplicate_window() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10, qts=3, seq=7, date=50)
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client.connect()
        await client._handle_raw_update(short_message(101, "hello", pts=11, date=101))
        iterator = client.iter_updates()
        event = await anext(iterator)
        assert isinstance(event, NewMessage)
        assert event.message is not None
        assert event.message.text == "hello"
        assert event.message.peer == Peer(id=42, kind="user")
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 11
        assert record.update_state.qts == 3
        assert record.update_state.seq == 7
        assert record.metadata["updates"]["recent_update_keys"]
        await client.disconnect()

    run(scenario())


def test_update_manager_persists_with_atomic_mutation_and_preserves_auth() -> None:
    async def scenario() -> None:
        auth_key = AuthKey(dc_id=2, key=AUTH_KEY, key_id=123)
        storage = MutationOnlySessionStorage(SessionRecord(dc_id=2, auth_key=auth_key, metadata={"kept": True}))
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client._update_manager.handle_raw_update(short_message(101, "hello", pts=1, date=101))
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key == auth_key
        assert record.metadata["kept"] is True
        assert record.update_state.pts == 1

    run(scenario())


def test_duplicate_updates_are_not_emitted_twice() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client.connect()
        raw_update = short_message(101, "once", pts=11, date=101)
        iterator = client.iter_updates()
        await client._handle_raw_update(raw_update)
        first = await anext(iterator)
        assert isinstance(first, NewMessage)
        await client._handle_raw_update(raw_update)
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(anext(iterator), timeout=0.01)
        await client.disconnect()

    run(scenario())


# fmt: off
@pytest.mark.parametrize("difference", [False, True])
def test_channel_message_duplicate_keys_keep_independent_message_boxes(difference: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        storage = InMemorySessionStorage(SessionRecord(update_state=UpdateState(pts=10), peers=(PeerCacheEntry(id=123, kind="channel", access_hash=100), PeerCacheEntry(id=456, kind="channel", access_hash=200))))
        messages = (raw_channel_message(7, "first", channel_id=123), raw_channel_message(7, "second", channel_id=456))
        responses: list[object] = [types.UpdatesChannelDifference(final=True, pts=2, new_messages=(message,), other_updates=(), chats=(), users=()) for message in messages] if difference else []
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), responses)
        manager = client._update_manager
        delivered: list[NewMessage] = []
        manager.on(NewMessage, delivered.append)
        if difference:
            updates = tuple(types.UpdateDeleteChannelMessages(channel_id=channel_id, messages=(55,), pts=3, pts_count=1) for channel_id in (123, 456))
        else:
            updates = (types.Updates(updates=tuple(types.UpdateNewChannelMessage(message=message, pts=1, pts_count=1) for message in messages), chats=(), users=(), date=100, seq=0),)

        for update in updates:
            await manager.handle_raw_update(update)
            await manager.handle_raw_update(update)

        assert len(delivered) == 2
        received = []
        for event in delivered:
            assert isinstance(event, NewMessage)
            assert event.message is not None
            received.append((event.message.peer.id, event.message.id, event.message.text))
        assert received == [(123, 7, "first"), (456, 7, "second")]
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 10
        assert {key: value["pts"] for key, value in record.metadata["updates"]["channels"].items()} == {"123": 3 if difference else 1, "456": 3 if difference else 1}
        if difference:
            assert len(client.update_requests) == 2
            for request, channel_id in zip(client.update_requests, (123, 456), strict=True):
                assert isinstance(request, functions.UpdatesGetChannelDifference)
                assert request.channel.channel_id == channel_id
                assert request.pts == 0
        else:
            assert client.update_requests == []

    run(scenario())


def test_channel_identity_alone_does_not_deduplicate_unordered_updates() -> None:
    async def scenario() -> None:
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_state()))
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)
        updates = (types.UpdateChannel(channel_id=123), types.UpdateChannel(channel_id=123))
        for update in updates:
            await manager.handle_raw_update(update)
        assert [event.raw for event in delivered] == list(updates)

    run(scenario())


def test_zero_count_pts_updates_preserve_payload_identity_and_persist_before_delivery() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(update_state=UpdateState(pts=10), metadata={"updates": {"recent_update_keys": ["UpdateReadHistoryInbox|pts:10"]}}))
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        manager = client._update_manager
        delivered: list[Update] = []

        async def receive(event: Update) -> None:
            loaded = await storage.load()
            assert loaded is not None
            record = session_record_from_mapping(loaded)
            assert record.update_state.pts == 10
            assert len(record.metadata["updates"]["recent_update_keys"]) == len(delivered) + 2
            delivered.append(event)

        manager.on(Update, receive)
        updates = tuple(types.UpdateReadHistoryInbox(peer=types.PeerUser(user_id=user_id), max_id=max_id, still_unread_count=unread, pts=10, pts_count=0) for user_id, max_id, unread in ((42, 8, 2), (77, 8, 2), (42, 9, 1), (42, 9, 0)))
        for update in updates:
            await manager.handle_raw_update(update)
            await manager.handle_raw_update(types.UpdateReadHistoryInbox.deserialize(update.serialize()))

        assert [event.raw for event in delivered] == list(updates)
        persisted = await storage.load()
        reopened = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(persisted)))
        replayed: list[Update] = []
        reopened._update_manager.on(Update, replayed.append)
        await reopened._update_manager.handle_raw_update(types.UpdateReadHistoryInbox.deserialize(updates[0].serialize()))
        fresh = types.UpdateReadHistoryInbox(peer=types.PeerUser(user_id=42), max_id=10, still_unread_count=0, pts=10, pts_count=0)
        await reopened._update_manager.handle_raw_update(fresh)
        assert [event.raw for event in replayed] == [fresh]
        assert client.update_requests == reopened.update_requests == []

    run(scenario())


@pytest.mark.parametrize("pts", [9, 10, 11])
def test_channel_read_updates_default_missing_pts_count_to_zero(pts: int, monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        storage = storage_with_channel_state(pts=10)
        responses: list[object] = [types.UpdatesChannelDifferenceEmpty(final=True, pts=11)] if pts == 11 else []
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), responses)
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)
        updates = tuple(types.UpdateReadChannelInbox(channel_id=123, max_id=max_id, still_unread_count=unread, pts=pts) for max_id, unread in ((7, 1), (8, 0)))

        for update in updates:
            await manager.handle_raw_update(update)
            await manager.handle_raw_update(types.UpdateReadChannelInbox.deserialize(update.serialize()))

        assert [event.raw for event in delivered] == (list(updates) if pts >= 10 else [])
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 0
        assert record.metadata["updates"]["channels"]["123"]["pts"] == max(10, pts)
        if pts == 11:
            assert len(client.update_requests) == 1
            request = client.update_requests[0]
            assert isinstance(request, functions.UpdatesGetChannelDifference)
            assert request.pts == 10
        else:
            assert client.update_requests == []

    run(scenario())


@pytest.mark.parametrize(("origin", "notification_pts", "stored_pts"), [("direct", None, 10), ("container", 12, 10), ("difference", 10, 10), ("recovery", 12, None), ("direct", 12, 0), ("mixed", 12, None)])
def test_channel_too_long_requests_recovery_instead_of_applying_pts(origin: str, notification_pts: int | None, stored_pts: int | None, monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        storage = storage_with_channel_state(pts=stored_pts) if stored_pts is not None else InMemorySessionStorage(SessionRecord(peers=(PeerCacheEntry(id=123, kind="channel", access_hash=999),)))
        notification = types.UpdateChannelTooLong(channel_id=123, pts=notification_pts)
        difference = types.UpdatesDifference(new_messages=(), new_encrypted_messages=(), other_updates=(notification,), chats=(), users=(), state=types.UpdatesState(pts=0, qts=0, date=100, seq=0, unread_count=0))
        recovered_message = raw_channel_message(7, "recovered")
        channel_difference = types.UpdatesChannelDifference(final=True, pts=13, new_messages=(recovered_message,), other_updates=(), chats=(), users=())
        responses: list[object] = [difference, channel_difference] if origin == "recovery" else [channel_difference]
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), responses)
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)
        trailing_read = types.UpdateReadChannelInbox(channel_id=123, max_id=7, still_unread_count=0, pts=13)
        if origin == "direct":
            raw = notification
        elif origin in {"container", "mixed"}:
            raw = types.Updates(updates=(notification, trailing_read) if origin == "mixed" else (notification,), chats=(), users=(), date=100, seq=0)
        elif origin == "difference":
            raw = difference
        else:
            raw = types.UpdatesTooLong()

        await manager.handle_raw_update(raw)

        assert [event.raw for event in delivered] == ([recovered_message, trailing_read] if origin == "mixed" else [recovered_message])
        requests = [request for request in client.update_requests if isinstance(request, functions.UpdatesGetChannelDifference)]
        assert len(requests) == 1
        assert requests[0].channel.channel_id == 123
        assert requests[0].pts == (stored_pts if stored_pts is not None else notification_pts)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 0
        assert record.metadata["updates"]["channels"]["123"]["pts"] == 13

    run(scenario())


@pytest.mark.parametrize("channel_id", [None, 123])
@pytest.mark.parametrize(("pts", "pts_count", "applied"), [(9, 0, False), (10, 0, True), (10, 1, False), (11, 2, False), (12, 2, True)])
def test_pts_comparison_uses_count_for_stale_equal_and_next_ranges(channel_id: int | None, pts: int, pts_count: int, applied: bool) -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10) if channel_id is None else storage_with_channel_state(channel_id=channel_id, pts=10)
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)
        update = types.UpdateDeleteMessages(messages=(55,), pts=pts, pts_count=pts_count) if channel_id is None else types.UpdateDeleteChannelMessages(channel_id=channel_id, messages=(55,), pts=pts, pts_count=pts_count)

        await manager.handle_raw_update(update)
        await manager.handle_raw_update(update)

        assert [event.raw for event in delivered] == ([update] if applied else [])
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        expected_pts = pts if applied else 10
        if channel_id is None:
            assert record.update_state.pts == expected_pts
        else:
            assert record.metadata["updates"]["channels"][str(channel_id)]["pts"] == expected_pts
            assert record.update_state.pts == 0
        assert client.update_requests == []

    run(scenario())


@pytest.mark.parametrize(("qts", "applied"), [(7, False), (8, False), (9, True)])
def test_qts_comparison_ignores_stale_updates_and_applies_next(qts: int, applied: bool) -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10, qts=8)
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)
        update = types.UpdateBotDeleteBusinessMessage(connection_id="business", peer=types.PeerUser(user_id=42), messages=(7,), qts=qts)

        await manager.handle_raw_update(update)
        await manager.handle_raw_update(update)

        assert [event.raw for event in delivered] == ([update] if applied else [])
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 10
        assert record.update_state.qts == (qts if applied else 8)
        assert client.update_requests == []

    run(scenario())


@pytest.mark.parametrize("sequence", ["pts", "channel_pts", "channel_read", "qts"])
def test_unresolved_update_gap_keeps_unit_retryable(sequence: str, monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        if sequence in {"channel_pts", "channel_read"}:
            storage = storage_with_channel_state(pts=10)
            behind = types.UpdatesChannelDifferenceEmpty(final=True, pts=10)
            caught_up = types.UpdatesChannelDifferenceEmpty(final=True, pts=13 if sequence == "channel_read" else 12)
            update = types.UpdateReadChannelInbox(channel_id=123, max_id=7, still_unread_count=0, pts=13) if sequence == "channel_read" else types.UpdateDeleteChannelMessages(channel_id=123, messages=(55,), pts=13, pts_count=1)
        else:
            storage = storage_with_state(pts=10, qts=8)
            behind = types.UpdatesDifference(new_messages=(), new_encrypted_messages=(), other_updates=(), chats=(), users=(), state=types.UpdatesState(pts=10, qts=8, date=100, seq=0, unread_count=0))
            caught_up = types.UpdatesDifference(new_messages=(), new_encrypted_messages=(), other_updates=(), chats=(), users=(), state=types.UpdatesState(pts=12 if sequence == "pts" else 10, qts=10 if sequence == "qts" else 8, date=101, seq=0, unread_count=0))
            update = types.UpdateDeleteMessages(messages=(55,), pts=13, pts_count=1) if sequence == "pts" else types.UpdateBotDeleteBusinessMessage(connection_id="business", peer=types.PeerUser(user_id=42), messages=(7,), qts=11)
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [behind, behind, caught_up])
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)

        await manager.handle_raw_update(update)

        assert delivered == []
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.metadata["updates"]["recent_update_keys"] == []
        if sequence in {"channel_pts", "channel_read"}:
            assert record.metadata["updates"]["channels"]["123"]["pts"] == 10
            assert record.update_state.pts == 0
        else:
            assert record.update_state.pts == 10
            assert record.update_state.qts == 8

        await manager.handle_raw_update(update)

        assert [event.raw for event in delivered] == [update]
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        if sequence in {"channel_pts", "channel_read"}:
            assert record.metadata["updates"]["channels"]["123"]["pts"] == 13
            assert record.update_state.pts == 0
        else:
            assert record.update_state.pts == (13 if sequence == "pts" else 10)
            assert record.update_state.qts == (11 if sequence == "qts" else 8)
        assert len(client.update_requests) == 3

    run(scenario())


def test_difference_updates_apply_after_messages_without_individual_pts() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        read = types.UpdateReadHistoryInbox(peer=types.PeerUser(user_id=42), max_id=8, still_unread_count=0, pts=13, pts_count=1)
        difference = types.UpdatesDifference(new_messages=(raw_message(7, "first missing", date=100), raw_message(8, "second missing", date=101)), new_encrypted_messages=(), other_updates=(read,), chats=(), users=(), state=types.UpdatesState(pts=13, qts=0, date=102, seq=0, unread_count=0))
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [difference])
        manager = client._update_manager
        delivered: list[Update] = []
        manager.on(Update, delivered.append)
        current = short_message(9, "current", pts=14, date=103)

        await manager.handle_raw_update(current)

        assert [event.raw for event in delivered] == [*difference.new_messages, read, current]
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 14
        assert len(client.update_requests) == 1

    run(scenario())
# fmt: on


def test_gap_recovery_fetches_difference_before_emitting_current_update() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10, qts=0, seq=0, date=50)
        difference = types.UpdatesDifference(
            new_messages=(raw_message(111, "missing", date=100),),
            new_encrypted_messages=(),
            other_updates=(),
            chats=(),
            users=(types.User(id=42, access_hash=9000, first_name="Alice", username="alice"),),
            state=types.UpdatesState(pts=12, qts=0, date=100, seq=0, unread_count=0),
        )
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [difference])
        await client.connect()
        iterator = client.iter_updates()
        await client._handle_raw_update(short_message(112, "current", pts=13, date=101))
        first = await anext(iterator)
        second = await anext(iterator)
        assert isinstance(first, NewMessage)
        assert isinstance(second, NewMessage)
        assert first.message is not None
        assert second.message is not None
        assert [first.message.text, second.message.text] == ["missing", "current"]
        assert len(client.update_requests) == 1
        request = client.update_requests[0]
        assert isinstance(request, functions.UpdatesGetDifference)
        assert request.pts == 10
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 13
        assert any(peer.id == 42 and peer.access_hash == 9000 for peer in record.peers)
        await client.disconnect()

    run(scenario())


def test_channel_gap_recovery_uses_channel_difference_and_persists_channel_cursor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        channel_id = 123
        storage = storage_with_channel_state(channel_id=channel_id, pts=10)
        difference = types.UpdatesChannelDifference(
            final=True,
            pts=12,
            new_messages=(raw_channel_message(111, "missing", channel_id=channel_id, date=100),),
            other_updates=(),
            chats=(
                types.Channel(
                    id=channel_id, access_hash=999, title="Channel", photo=types.ChatPhotoEmpty(), date=1_700_000_000
                ),
            ),
            users=(),
        )
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [difference])
        await client.connect()
        iterator = client.iter_updates()
        await client._handle_raw_update(
            types.UpdateNewChannelMessage(
                message=raw_channel_message(112, "current", channel_id=channel_id, date=101), pts=13, pts_count=1
            )
        )
        first = await anext(iterator)
        second = await anext(iterator)
        assert isinstance(first, NewMessage)
        assert isinstance(second, NewMessage)
        assert first.message is not None
        assert second.message is not None
        assert [first.message.text, second.message.text] == ["missing", "current"]
        assert len(client.update_requests) == 1
        request = client.update_requests[0]
        assert isinstance(request, functions.UpdatesGetChannelDifference)
        assert isinstance(request.channel, types.InputChannel)
        assert request.channel.channel_id == channel_id
        assert request.channel.access_hash == 999
        assert isinstance(request.filter, types.ChannelMessagesFilterEmpty)
        assert request.pts == 10
        loaded = await storage.load()
        assert loaded is not None
        channels = loaded["metadata"]["updates"]["channels"]
        assert channels[str(channel_id)]["pts"] == 13
        await client.disconnect()

    run(scenario())


def test_channel_difference_too_long_persists_dialog_pts_between_rounds(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        channel_id = 123
        storage = storage_with_channel_state(channel_id=channel_id, pts=10)
        responses: list[object] = [
            types.UpdatesChannelDifferenceTooLong(
                final=False, dialog=SimpleNamespace(pts=40), messages=(), chats=(), users=()
            ),
            types.UpdatesChannelDifferenceEmpty(final=True, pts=41),
        ]
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), responses)
        await client.connect()

        await client._update_manager._recover_channel_gap(channel_id)

        requests = [
            request for request in client.update_requests if isinstance(request, functions.UpdatesGetChannelDifference)
        ]
        assert [request.pts for request in requests] == [10, 40]
        assert client._update_manager._current_cursor().channel_cursor(channel_id).pts == 41
        await client.disconnect()

    run(scenario())


def test_channel_gap_without_access_hash_does_not_apply_or_advance_gapped_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        channel_id = 123
        storage = storage_with_state()
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client.connect()

        events = await client._update_manager._process_raw_update(
            types.UpdateNewChannelMessage(
                message=raw_channel_message(112, "current", channel_id=channel_id, date=101), pts=13, pts_count=1
            )
        )

        assert events == []
        assert client._update_manager._current_cursor().channel_cursor(channel_id).pts == 0
        assert client.update_requests == []
        await client.disconnect()

    run(scenario())


def test_qts_gap_triggers_global_difference_recovery() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10, qts=3, date=50)
        difference = types.UpdatesDifference(
            new_messages=(),
            new_encrypted_messages=(),
            other_updates=(),
            chats=(),
            users=(),
            state=types.UpdatesState(pts=10, qts=5, date=100, seq=0, unread_count=0),
        )
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [difference])
        await client.connect()

        await client._update_manager.handle_raw_update(SimpleNamespace(qts=6))

        assert isinstance(client.update_requests[0], functions.UpdatesGetDifference)
        assert client.update_requests[0].qts == 3
        assert client._update_manager._current_cursor().qts == 6
        await client.disconnect()

    run(scenario())


def test_identityless_updates_are_not_collapsed_by_type_name() -> None:
    async def scenario() -> None:
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_state()))
        await client.connect()

        first = await client._update_manager._process_raw_update(SimpleNamespace(value="first"))
        second = await client._update_manager._process_raw_update(SimpleNamespace(value="second"))

        assert len(first) == 1
        assert len(second) == 1
        await client.disconnect()

    run(scenario())


# fmt: off
def test_layer230_identityless_wallet_updates_preserve_distinct_raw_states() -> None:
    async def scenario() -> None:
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_state()))
        first_raw = types.UpdateWalletState.deserialize(bytes.fromhex("aaf2c36a ecb2b99c 01000000"))
        second_raw = types.UpdateWalletState.deserialize(bytes.fromhex("aaf2c36a 6b34c595 05000000 03616263 02102000 0807060504030201"))
        await client.connect()
        try:
            first = await client._update_manager._process_raw_update(first_raw)
            second = await client._update_manager._process_raw_update(second_raw)
            assert [type(event) for event in first + second] == [Update, Update]
            assert first[0].raw is first_raw
            assert second[0].raw is second_raw
            assert first_raw.state == types.WalletStateEmpty(creating=True)
            assert second_raw.state == types.WalletState(backup_enabled=True, can_enable_backup=True, address="abc", public_key=b"\x10\x20", balance=0x0102030405060708)
        finally:
            await client.disconnect()

    run(scenario())
# fmt: on


def test_zero_global_cursors_detect_missing_initial_ranges() -> None:
    async def scenario() -> None:
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_state()))
        await client.connect()
        manager = client._update_manager

        assert manager._pts_gap(short_message(100, "late", pts=2, date=100))
        assert manager._qts_gap(SimpleNamespace(qts=2))
        assert manager._sequence_gap(SimpleNamespace(seq=2, seq_start=2))

        await client.disconnect()

    run(scenario())


def test_updates_container_advances_pts_without_false_gap_recovery() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        container = types.Updates(
            updates=(
                types.UpdateNewMessage(message=raw_message(501, "first", date=501), pts=11, pts_count=1),
                types.UpdateNewMessage(message=raw_message(502, "second", date=502), pts=12, pts_count=1),
            ),
            users=(),
            chats=(),
            date=502,
            seq=1,
        )
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client.connect()
        iterator = client.iter_updates()
        await client._handle_raw_update(container)
        first = await anext(iterator)
        second = await anext(iterator)
        assert isinstance(first, NewMessage)
        assert isinstance(second, NewMessage)
        assert first.message is not None
        assert second.message is not None
        assert [first.message.text, second.message.text] == ["first", "second"]
        assert client.update_requests == []
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 12
        assert record.update_state.seq == 1
        await client.disconnect()

    run(scenario())


def test_update_short_wrapper_normalizes_inner_update() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        raw_update = types.UpdateShort(
            update=types.UpdateNewMessage(message=raw_message(201, "wrapped", date=201), pts=11, pts_count=1), date=201
        )
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        await client.connect()
        await client._handle_raw_update(raw_update)
        event = await anext(client.iter_updates())
        assert isinstance(event, NewMessage)
        assert event.message is not None
        assert event.message.text == "wrapped"
        await client.disconnect()

    run(scenario())


def test_pushed_updates_from_real_sender_reach_iter_updates() -> None:
    async def scenario() -> None:
        pushed = types.UpdateShortMessage(id=901, user_id=42, message="pushed", pts=11, pts_count=1, date=901)

        def handle(message):
            if message.seq_no % 2 == 0:
                return None
            return MessageContainer(
                messages=(
                    MessageContainerItem(msg_id=message.msg_id + 1, seq_no=1, body=pushed.serialize()),
                    MessageContainerItem(
                        msg_id=message.msg_id + 5,
                        seq_no=3,
                        body=RpcResult(
                            req_msg_id=message.msg_id,
                            result=types.NearestDc(country="US", this_dc=2, nearest_dc=2).serialize(),
                        ),
                    ),
                )
            )

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            endpoint = server.endpoint
            storage = InMemorySessionStorage(
                SessionRecord(
                    dc_id=2,
                    auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
                    dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),),
                    update_state=UpdateState(pts=10, qts=0, seq=0, date=datetime.fromtimestamp(1, UTC)),
                )
            )
            client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, transport=transport))
            await client.connect()
            await client.invoke(functions.HelpGetNearestDc())
            event = await asyncio.wait_for(anext(client.iter_updates()), timeout=2.0)
            assert isinstance(event, NewMessage)
            assert event.message is not None
            assert event.message.text == "pushed"
            await client.disconnect()

    run(scenario())


def test_update_queue_drop_oldest_overflow_policy_keeps_latest_update() -> None:
    async def scenario() -> None:
        client = Client(
            ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=InMemorySessionStorage(),
                update_queue_size=1,
                update_queue_overflow="drop_oldest",
            )
        )
        await client._emit_new_message(public_message("old", message_id=1))
        await client._emit_new_message(public_message("new", message_id=2))
        event = await anext(client.iter_updates())
        assert isinstance(event, NewMessage)
        assert event.message is not None
        assert event.message.text == "new"

    run(scenario())


def test_update_queue_drop_newest_overflow_policy_keeps_existing_update() -> None:
    async def scenario() -> None:
        seen: list[str] = []
        client = Client(
            ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=InMemorySessionStorage(),
                update_queue_size=1,
                update_queue_overflow="drop_newest",
            )
        )

        @client.on(NewMessage)
        def handle(event: NewMessage) -> None:
            if event.message is not None:
                seen.append(event.message.text)

        iterator = client.iter_updates()
        pending = asyncio.create_task(anext(iterator))
        await asyncio.sleep(0)
        await client._emit_new_message(public_message("old", message_id=1))
        await client._emit_new_message(public_message("new", message_id=2))
        event = await pending
        assert isinstance(event, NewMessage)
        assert event.message is not None
        assert event.message.text == "old"
        assert seen == ["old"]
        await iterator.aclose()

    run(scenario())


def test_reconnect_reuses_persisted_duplicate_window() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        first_client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        raw_update = short_message(301, "persisted", pts=11, date=301)
        await first_client.connect()
        await first_client._handle_raw_update(raw_update)
        event = await anext(first_client.iter_updates())
        assert isinstance(event, NewMessage)
        persisted = await storage.load()
        assert persisted is not None
        await first_client.disconnect()
        reopened = InMemorySessionStorage(persisted)
        second_client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=reopened))
        await second_client.connect()
        iterator = second_client.iter_updates()
        await second_client._handle_raw_update(raw_update)
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(anext(iterator), timeout=0.01)
        await second_client.disconnect()

    run(scenario())


def test_background_update_task_surfaces_handler_exceptions_on_disconnect() -> None:
    async def scenario() -> None:
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))

        @client.on(NewMessage)
        def fail(_: NewMessage) -> None:
            raise RuntimeError("handler exploded")

        await client.connect()
        await client._feed_raw_update(short_message(401, "boom", pts=1, date=401))
        await asyncio.sleep(0.05)
        with pytest.raises(RuntimeError, match="handler exploded"):
            await client.disconnect()

    run(scenario())


def test_update_config_validates_overflow_policy_and_duplicate_window() -> None:
    invalid_policy: Any = "invalid"
    with pytest.raises(ValueError, match="update_queue_overflow"):
        ClientConfig(api_id=1, api_hash="hash", update_queue_overflow=invalid_policy)
    with pytest.raises(ValueError, match="update_duplicate_window"):
        ClientConfig(api_id=1, api_hash="hash", update_duplicate_window=0)


def test_min_update_entity_cannot_poison_full_cached_access_hash() -> None:
    full = PeerCacheEntry(
        id=123, kind="channel", access_hash=999, username="full-channel", raw={"title": "Full channel"}
    )
    partial = EntityReference(id=123, kind="channel", updated_at=datetime.now(UTC))
    assert merge_peer_cache_entries((full,), (partial,)) == (
        PeerCacheEntry(
            id=123,
            kind="channel",
            access_hash=999,
            username="full-channel",
            updated_at=partial.updated_at,
            raw={"title": "Full channel"},
            username_observed_at=full.username_observed_at,
        ),
    )


def test_min_update_preserves_live_cursor_channel_access_hash() -> None:
    full = EntityReference(id=123, kind="channel", access_hash=999, username="full-channel", title="Full channel")
    partial = EntityReference(id=123, kind="channel", updated_at=datetime.now(UTC))
    cursor = UpdateCursor(entities=(full,)).with_entities((partial,))
    assert cursor.entities == (
        EntityReference(
            id=123,
            kind="channel",
            access_hash=999,
            username="full-channel",
            title="Full channel",
            updated_at=partial.updated_at,
            username_observed_at={"full-channel": full.updated_at},
        ),
    )


def test_update_delivered_entity_invalidates_warm_peer_index_once() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(peers=(PeerCacheEntry(id=1, kind="user", access_hash=11),)))
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client.resolve_peer(1) == Peer(id=1, kind="user", access_hash=11)
        warm = client._peer_cache.index_stats
        await client._update_manager.handle_raw_update(
            types.Updates(
                updates=(), users=(types.User(id=2, access_hash=22, username="delivered"),), chats=(), date=100, seq=0
            )
        )
        assert await client.resolve_peer("@delivered") == Peer(id=2, kind="user", access_hash=22)
        assert client._peer_cache.index_stats["rebuilds"] == warm["rebuilds"] + 1
        after = client._peer_cache.index_stats
        assert await client.resolve_peer(2) == Peer(id=2, kind="user", access_hash=22)
        assert client._peer_cache.index_stats == after

    run(scenario())


def client_with_queue(size: int = 1000, policy: UpdateQueueOverflowPolicy = "raise") -> Client:
    return Client(ClientConfig(api_id=1, api_hash="synthetic-update-queue", session_storage=InMemorySessionStorage(), update_queue_size=size, update_queue_overflow=policy))  # fmt: skip


def _queued_message(number: int) -> NewMessage:
    date = datetime.fromtimestamp(100, UTC)
    return NewMessage(date=date, message=Message(id=number, peer=Peer(id=42, kind="user"), text=str(number), date=date))


def _queued_raw_message(number: int) -> types.UpdateShortMessage:
    return types.UpdateShortMessage(id=number, user_id=42, message=str(number), pts=number, pts_count=1, date=100 + number)  # fmt: skip


@pytest.mark.parametrize(("policy", "size"), [("raise", 1000), ("drop_newest", 2), ("drop_oldest", 2)])
def test_callback_only_delivery_exceeds_queue_capacity(policy: UpdateQueueOverflowPolicy, size: int) -> None:
    async def scenario() -> None:
        client = client_with_queue(size=size, policy=policy)
        seen: list[int] = []
        delivered = asyncio.Event()

        @client.on(NewMessage)
        def receive(update: NewMessage) -> None:
            assert update.message is not None
            seen.append(update.message.id)
            delivered.set()

        await client.connect()
        waiter = asyncio.create_task(client.wait_for_updates())
        try:
            for number in range(1, client.config.update_queue_size + 8):
                delivered.clear()
                await client._feed_raw_update(_queued_raw_message(number))
                await asyncio.wait_for(delivered.wait(), timeout=1)
                await client._emit_update(Update(raw=number))
            assert seen == list(range(1, size + 8))
            assert client._update_manager._updates.empty()
            assert not waiter.done()
            stored = await client._storage.load()
            assert session_record_from_mapping(stored or {}).update_state.pts == size + 7
        finally:
            await client.disconnect()
            await waiter

    event_loop.run(scenario())


@pytest.mark.parametrize("callbacks", [False, True])
@pytest.mark.parametrize("policy", ["raise", "drop_newest", "drop_oldest"])
def test_active_iterator_preserves_overflow(callbacks: bool, policy: UpdateQueueOverflowPolicy) -> None:
    async def scenario() -> None:
        client = client_with_queue(size=2, policy=policy)
        seen: list[int] = []

        if callbacks:

            @client.on(NewMessage)
            def receive(update: NewMessage) -> None:
                assert update.message is not None
                seen.append(update.message.id)

        iterator = client.iter_updates()
        first = asyncio.create_task(anext(iterator))
        await asyncio.sleep(0)
        await client._emit_update(_queued_message(7))
        assert await first == _queued_message(7)
        await client._emit_update(_queued_message(31))
        await client._emit_update(_queued_message(12))
        if policy == "raise":
            with pytest.raises(asyncio.QueueFull):
                await client._emit_update(_queued_message(99))
        else:
            await client._emit_update(_queued_message(99))
        expected = [12, 99] if policy == "drop_oldest" else [31, 12]
        received = [await anext(iterator), await anext(iterator)]
        assert [event.message.id for event in received if isinstance(event, NewMessage) and event.message] == expected
        expected_callbacks = [7, 31, 12, 99] if policy == "drop_oldest" else [7, 31, 12]
        assert seen == (expected_callbacks if callbacks else [])
        await iterator.aclose()

    event_loop.run(scenario())


def test_callback_awaiting_iterator_observes_queue_admission_first() -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        consumed = asyncio.Event()
        order: list[str] = []

        @client.on(NewMessage)
        async def receive(_: NewMessage) -> None:
            await asyncio.wait_for(consumed.wait(), timeout=1)
            order.append("callback")

        iterator = client.iter_updates()

        async def consume() -> None:
            assert await anext(iterator) == _queued_message(23)
            order.append("iterator")
            consumed.set()

        consumer = asyncio.create_task(consume())
        await asyncio.sleep(0)
        await client._emit_update(_queued_message(23))
        await consumer
        assert order == ["iterator", "callback"]
        await iterator.aclose()

    event_loop.run(scenario())


@pytest.mark.parametrize("cancel", [False, True], ids=["close", "cancel"])
def test_last_iterator_releases_callback_only_delivery_without_retaining_new_copies(cancel: bool) -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        seen: list[NewMessage] = []
        client.on(NewMessage, seen.append)
        iterator = client.iter_updates()
        pending = asyncio.create_task(anext(iterator))
        await asyncio.sleep(0)
        if cancel:
            pending.cancel()
            with pytest.raises(asyncio.CancelledError):
                await pending
        else:
            await client._emit_update(_queued_message(4))
            assert await pending == _queued_message(4)
            await iterator.aclose()
        for number in [17, 6, 29]:
            await client._emit_update(_queued_message(number))
        assert seen == [_queued_message(number) for number in ([17, 6, 29] if cancel else [4, 17, 6, 29])]
        assert client._update_manager._updates.empty()

    event_loop.run(scenario())


def test_competing_iterators_keep_queue_owned_until_last_closes() -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        seen: list[NewMessage] = []
        client.on(NewMessage, seen.append)
        first = client.iter_updates()
        second = client.iter_updates()
        pending_first = asyncio.create_task(anext(first))
        pending_second = asyncio.create_task(anext(second))
        await asyncio.sleep(0)
        await client._emit_update(_queued_message(8))
        assert await pending_first == _queued_message(8)
        await first.aclose()
        await client._emit_update(_queued_message(3))
        assert await pending_second == _queued_message(3)
        await client._emit_update(_queued_message(19))
        with pytest.raises(asyncio.QueueFull):
            await client._emit_update(_queued_message(27))
        assert await anext(second) == _queued_message(19)
        await second.aclose()
        await client._emit_update(_queued_message(41))
        await client._emit_update(_queued_message(56))
        assert seen == [_queued_message(number) for number in [8, 3, 19, 41, 56]]
        assert client._update_manager._updates.empty()

    event_loop.run(scenario())


def test_callback_history_is_not_replayed_and_empty_handler_lists_keep_iterator_buffering() -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        client.on(NewMessage, lambda _: None)
        unopened = client.iter_updates()
        await client._emit_update(_queued_message(14))
        await client._emit_update(_queued_message(9))
        pending = asyncio.create_task(anext(unopened))
        await asyncio.sleep(0)
        assert not pending.done()
        await client._emit_update(_queued_message(22))
        assert await pending == _queued_message(22)
        await unopened.aclose()
        client._update_manager.handlers[NewMessage].clear()
        await client._emit_update(_queued_message(64))
        iterator = client.iter_updates()
        assert await anext(iterator) == _queued_message(64)
        await iterator.aclose()

    event_loop.run(scenario())


def test_background_iterator_failure_is_public_and_cursor_commits_before_delivery() -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        await client._handle_raw_update(_queued_raw_message(1))
        await client.connect()
        waiter = asyncio.create_task(client.wait_for_updates())
        await client._feed_raw_update(_queued_raw_message(2))
        with pytest.raises(asyncio.QueueFull):
            await asyncio.wait_for(waiter, timeout=1)
        assert client.is_connected
        stored = await client._storage.load()
        assert session_record_from_mapping(stored or {}).update_state.pts == 2
        with pytest.raises(asyncio.QueueFull):
            await client._feed_raw_update(_queued_raw_message(3))
        assert client._update_manager._raw_updates.empty()
        iterator = client.iter_updates()
        first = await anext(iterator)
        assert isinstance(first, NewMessage) and first.message is not None and first.message.id == 1
        await client.connect()
        recovered_waiter = asyncio.create_task(client.wait_for_updates())
        await client._handle_raw_update(_queued_raw_message(2))
        assert client._update_manager._updates.empty()
        await client._feed_raw_update(_queued_raw_message(3))
        recovered = await asyncio.wait_for(anext(iterator), timeout=1)
        assert isinstance(recovered, NewMessage) and recovered.message is not None and recovered.message.id == 3
        await iterator.aclose()
        await client.disconnect()
        await recovered_waiter

    event_loop.run(scenario())


def test_handler_failure_reaches_public_waiter_and_subsequent_raw_intake() -> None:
    async def scenario() -> None:
        client = client_with_queue()

        @client.on(NewMessage)
        def fail(_: NewMessage) -> None:
            raise RuntimeError("synthetic handler failure")

        await client.connect()
        waiter = asyncio.create_task(client.wait_for_updates())
        await client._feed_raw_update(_queued_raw_message(1))
        with pytest.raises(RuntimeError, match="synthetic handler failure"):
            await asyncio.wait_for(waiter, timeout=1)
        with pytest.raises(RuntimeError, match="synthetic handler failure"):
            await client._feed_raw_update(_queued_raw_message(2))
        assert client._update_manager._raw_updates.empty()
        assert client._update_manager._updates.empty()
        with pytest.raises(RuntimeError, match="synthetic handler failure"):
            await client.disconnect()

    event_loop.run(scenario())


def test_waiter_cancellation_leaves_drainer_running_and_disconnect_completes_new_waiter() -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        delivered = asyncio.Event()
        client.on(NewMessage, lambda _: delivered.set())
        with pytest.raises(RuntimeError, match="not running"):
            await client.wait_for_updates()
        await client.connect()
        cancelled_waiter = asyncio.create_task(client.wait_for_updates())
        await asyncio.sleep(0)
        cancelled_waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await cancelled_waiter
        await client._feed_raw_update(_queued_raw_message(1))
        await asyncio.wait_for(delivered.wait(), timeout=1)
        waiter = asyncio.create_task(client.wait_for_updates())
        await asyncio.sleep(0)
        await client.disconnect()
        await asyncio.wait_for(waiter, timeout=1)

    event_loop.run(scenario())


def test_slow_callback_still_exposes_real_raw_queue_backpressure() -> None:
    async def scenario() -> None:
        client = client_with_queue(size=1)
        started = asyncio.Event()
        release = asyncio.Event()
        finished = asyncio.Event()
        seen: list[int] = []

        @client.on(NewMessage)
        async def receive(update: NewMessage) -> None:
            assert update.message is not None
            seen.append(update.message.id)
            if update.message.id == 1:
                started.set()
                await release.wait()
            else:
                finished.set()

        await client.connect()
        await client._feed_raw_update(_queued_raw_message(1))
        await asyncio.wait_for(started.wait(), timeout=1)
        await client._feed_raw_update(_queued_raw_message(2))
        with pytest.raises(asyncio.QueueFull):
            await client._feed_raw_update(_queued_raw_message(3))
        release.set()
        await asyncio.wait_for(finished.wait(), timeout=1)
        assert seen == [1, 2]
        assert client._update_manager._updates.empty()
        await client.disconnect()

    event_loop.run(scenario())


UPDATE_ALIAS_STORAGE_KEY = b"offline-update-alias-fixture-key"


UPDATE_OLD_PHONE = "+15550103300"


# fmt: off
def raw_entity(kind: Literal["user", "self", "channel"], *, replacement: bool, minimal: bool = False) -> types.User | types.Channel:
    usernames = (
        types.Username(username="oldsecondary", active=False),
        types.Username(username="newsecondary", active=True),
        types.Username(username="othersecondary", active=True),
        types.Username(username="inactive", active=False),
    ) if replacement else None
    username = "newprimary" if replacement else None
    if kind in {"user", "self"}:
        return types.User(id=71, self_=kind == "self", access_hash=999 if minimal else 717, first_name="Observed", username=username, usernames=usernames, min=minimal)
    return types.Channel(id=71, access_hash=999 if minimal else 717, title="Observed channel", photo=types.ChatPhotoEmpty(), date=100, username=username, usernames=usernames, min=minimal)


def container(entity: types.User | types.Channel, source: str) -> object:
    users = (entity,) if isinstance(entity, types.User) else ()
    chats = (entity,) if isinstance(entity, types.Channel) else ()
    if source == "difference":
        return types.UpdatesDifference(new_messages=(), new_encrypted_messages=(), other_updates=(), users=users, chats=chats, state=types.UpdatesState(pts=0, qts=0, date=100, seq=0, unread_count=0))
    return types.Updates(updates=(), users=users, chats=chats, date=100, seq=0)


@pytest.mark.parametrize("kind", ["user", "self", "channel"])
@pytest.mark.parametrize("source", ["push", "difference"])
@pytest.mark.parametrize("replacement", [False, True], ids=["remove", "replace"])
def test_full_update_replaces_aliases_in_warm_and_reloaded_storage(tmp_path: Path, kind: Literal["user", "self", "channel"], source: str, replacement: bool) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key=UPDATE_ALIAS_STORAGE_KEY)
        initial = SessionRecord(peers=(PeerCacheEntry(id=71, kind=kind, access_hash=710, username="oldprimary", phone=UPDATE_OLD_PHONE if kind in {"user", "self"} else None, raw={"_miniproto_complete": True, "usernames": ["oldsecondary"]}),))
        await storage.save(initial)
        requests: list[str] = []

        async def remote(request: object) -> object:
            assert isinstance(request, functions.ContactsResolveUsername)
            requests.append(request.username)
            if request.username == "oldprimary":
                return types.ContactsResolvedPeer(peer=types.PeerUser(user_id=99), users=(types.User(id=99, access_hash=990, username="oldprimary"),), chats=())
            raise NotFound("alias requires remote resolution")

        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)
        cache = PeerCache(config, storage, remote)
        manager = UpdateManager(config, storage, remote)
        try:
            assert await cache.resolve_peer("@oldprimary") == Peer(id=71, kind=kind, access_hash=710)
            assert await cache.resolve_peer("@oldsecondary") == Peer(id=71, kind=kind, access_hash=710)
            if kind in {"user", "self"}:
                assert await cache.resolve_peer(UPDATE_OLD_PHONE) == Peer(id=71, kind=kind, access_hash=710)
            await manager.handle_raw_update(container(raw_entity(kind, replacement=replacement), source))
            record = session_record_from_mapping(await storage.load() or {})
            assert len(record.peers) == 1
            peer = record.peers[0]
            assert peer.username == ("newprimary" if replacement else None)
            assert peer.phone is None
            assert peer.access_hash == 717

            async def check_aliases(candidate: PeerCache) -> None:
                before = len(requests)
                if replacement:
                    for alias in ("newprimary", "newsecondary", "othersecondary"):
                        assert await candidate.resolve_peer(f"@{alias}") == Peer(id=71, kind=kind, access_hash=717)
                assert len(requests) == before
                for alias in ("oldsecondary", "inactive"):
                    with pytest.raises(NotFound, match="alias requires remote resolution"):
                        await candidate.resolve_peer(f"@{alias}")
                assert requests[before:] == ["oldsecondary", "inactive"]
                if kind in {"user", "self"}:
                    with pytest.raises(NotFound, match="phone peer is not cached"):
                        await candidate.resolve_peer(UPDATE_OLD_PHONE)
                assert await candidate.resolve_peer("@oldprimary") == Peer(id=99, kind="user", access_hash=990)

            await check_aliases(cache)
            direct = PeerCache(config, InMemorySessionStorage(initial), remote)
            await direct.remember_raw_entities(raw_entity(kind, replacement=replacement))
            await check_aliases(direct)
            await storage.close()
            reloaded = EncryptedSQLiteSessionStorage(path, key=UPDATE_ALIAS_STORAGE_KEY)
            try:
                await check_aliases(PeerCache(config, reloaded, remote))
                reloaded_manager = UpdateManager(config, reloaded, remote)
                await reloaded_manager.handle_raw_update(types.UpdateShort(update=types.UpdateUserStatus(user_id=71, status=types.UserStatusEmpty()), date=101))
                await check_aliases(PeerCache(config, reloaded, remote))
            finally:
                await reloaded.close()
        finally:
            await storage.close()

    event_loop.run(scenario())


@pytest.mark.parametrize("kind", ["user", "self", "channel"])
def test_min_update_preserves_omitted_cached_aliases_and_usable_hash(tmp_path: Path, kind: Literal["user", "self", "channel"]) -> None:
    async def scenario() -> None:
        storage = EncryptedSQLiteSessionStorage(tmp_path / "session.sqlite", key=UPDATE_ALIAS_STORAGE_KEY)
        await storage.save(SessionRecord(peers=(PeerCacheEntry(id=71, kind=kind, access_hash=710, username="oldprimary", phone=UPDATE_OLD_PHONE if kind in {"user", "self"} else None, raw={"_miniproto_complete": True, "usernames": ["oldsecondary"]}),)))

        async def no_remote(request: object) -> object:
            raise AssertionError(f"unexpected remote request: {type(request).__name__}")

        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)
        try:
            await UpdateManager(config, storage, no_remote).handle_raw_update(container(raw_entity(kind, replacement=False, minimal=True), "push"))
            cache = PeerCache(config, storage, no_remote)
            for alias in ("oldprimary", "oldsecondary"):
                assert await cache.resolve_peer(f"@{alias}") == Peer(id=71, kind=kind, access_hash=710)
            record = session_record_from_mapping(await storage.load() or {})
            assert record.peers[0].access_hash == 710
            if kind in {"user", "self"}:
                assert record.peers[0].phone == UPDATE_OLD_PHONE
                assert await cache.resolve_peer(UPDATE_OLD_PHONE) == Peer(id=71, kind=kind, access_hash=710)
        finally:
            await storage.close()

    event_loop.run(scenario())


OBSERVATION_STORAGE_KEY = b"offline-peer-observation-fixture-key"


OBSERVATION_OLD_PHONE = "+15550103400"


OBSERVATION_NEW_PHONE = "+15550103499"


# fmt: off
def original_peer(peer_id: int = 71) -> PeerCacheEntry:
    return PeerCacheEntry(id=peer_id, kind="user", access_hash=710, username="oldprimary", phone=OBSERVATION_OLD_PHONE, raw={"_miniproto_complete": True, "usernames": ["oldsecondary"]})


def pushed(entity: types.User, *, seq: int = 0) -> types.Updates:
    return types.Updates(updates=(), users=(entity,), chats=(), date=100, seq=seq)


def unrelated_update() -> types.UpdateShort:
    return types.UpdateShort(update=types.UpdateUserStatus(user_id=99, status=types.UserStatusEmpty()), date=101)


@pytest.mark.parametrize("route", ["history", "message", "media"])
@pytest.mark.parametrize("replace_username", [False, True], ids=["remove", "replace"])
def test_rpc_correction_survives_cursor_persistence_and_reload(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, route: str, replace_username: bool) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
        await storage.save(SessionRecord(peers=(original_peer(),)))
        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)
        client = Client(config)
        corrected_username = "corrected" if replace_username else None
        correction = types.User(id=71, access_hash=717, username=corrected_username, usernames=(types.Username(username="correctedsecondary", active=True),) if replace_username else None)
        requests: list[object] = []

        async def remote(request: object, **kwargs: object) -> object:
            del kwargs
            requests.append(request)
            if isinstance(request, functions.ContactsResolveUsername):
                raise NotFound("alias needs remote resolution")
            if isinstance(request, functions.UpdatesGetState):
                return types.UpdatesState(pts=0, qts=0, date=102, seq=0, unread_count=0)
            if isinstance(request, functions.MessagesGetHistory):
                return types.MessagesMessages(messages=(), users=(correction,), chats=(), topics=())
            assert isinstance(request, functions.MessagesSendMessage | functions.MessagesSendMedia)
            return pushed(correction)

        monkeypatch.setattr(client, "_invoke_via_sender", remote)

        async def assert_correction(cache: PeerCache) -> None:
            expected = Peer(id=71, kind="user", access_hash=717)
            assert await cache.resolve_peer(71) == expected
            if corrected_username is not None:
                assert await cache.resolve_peer(f"@{corrected_username}") == expected
                assert await cache.resolve_peer("@correctedsecondary") == expected
            for alias in ("oldprimary", "oldsecondary"):
                with pytest.raises(NotFound, match="alias needs remote resolution"):
                    await cache.resolve_peer(f"@{alias}")
            with pytest.raises(NotFound, match="phone peer is not cached"):
                await cache.resolve_peer(OBSERVATION_OLD_PHONE)

        try:
            await client.connect()
            assert await client.resolve_peer("@oldprimary") == Peer(id=71, kind="user", access_hash=710)
            assert await client.resolve_peer(OBSERVATION_OLD_PHONE) == Peer(id=71, kind="user", access_hash=710)
            destination = Peer(id=71, kind="user", access_hash=710)
            if route == "history":
                await client.get_history(destination)
            elif route == "message":
                await client.send_message(destination, "offline fixture", random_id=34)
            else:
                document = types.Document(id=340, access_hash=341, file_reference=b"offline-reference", date=100, mime_type="application/octet-stream", size=1, dc_id=2, attributes=())
                await client.send_file(destination, encode_file_id(document), caption="offline fixture", random_id=34)
            assert isinstance(requests[0], {"history": functions.MessagesGetHistory, "message": functions.MessagesSendMessage, "media": functions.MessagesSendMedia}[route])
            await assert_correction(client._peer_cache)
            corrected_record = session_record_from_mapping(await storage.load() or {})
            corrected_peer = corrected_record.peers[0]
            assert corrected_peer.username == corrected_username
            assert corrected_peer.phone is None
            peers_revision = client._storage.domain_revisions()["peers"]

            await client._handle_raw_update(unrelated_update())
            await client._update_manager.sync_state()

            assert session_record_from_mapping(await storage.load() or {}).peers == (corrected_peer,)
            assert client._storage.domain_revisions()["peers"] == peers_revision
            await assert_correction(client._peer_cache)
            reloaded = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
            try:
                assert session_record_from_mapping(await reloaded.load() or {}).peers == (corrected_peer,)
                await assert_correction(PeerCache(config, reloaded, remote))
            finally:
                await reloaded.close()

            await client._handle_raw_update(pushed(types.User(id=71, min=True, access_hash=999, first_name="Partial")))
            await assert_correction(client._peer_cache)
            newer = types.User(id=71, access_hash=719, username="newest", phone=OBSERVATION_NEW_PHONE, usernames=(types.Username(username="newestsecondary", active=True),))
            await client._handle_raw_update(pushed(newer))
            expected = Peer(id=71, kind="user", access_hash=719)
            for alias in ("@newest", "@newestsecondary", OBSERVATION_NEW_PHONE):
                assert await client.resolve_peer(alias) == expected
            with pytest.raises(NotFound, match="alias needs remote resolution"):
                await client.resolve_peer("@correctedsecondary")
            await client.disconnect()
            reloaded = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
            try:
                cache = PeerCache(config, reloaded, remote)
                for alias in ("@newest", "@newestsecondary", OBSERVATION_NEW_PHONE):
                    assert await cache.resolve_peer(alias) == expected
            finally:
                await reloaded.close()
        finally:
            await client.disconnect()

    event_loop.run(scenario())


@pytest.mark.parametrize("rpc_peer_id", [71, 72], ids=["same-peer", "unrelated-peer"])
def test_rpc_correction_during_recovery_only_supersedes_matching_pending_peer(rpc_peer_id: int) -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(SessionRecord(peers=(original_peer(71), original_peer(72))))
        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)

        async def remote(request: object) -> object:
            if isinstance(request, functions.ContactsResolveUsername):
                raise NotFound("older pending alias is no longer authoritative")
            assert isinstance(request, functions.UpdatesGetDifference)
            await cache.remember_raw_entities(types.User(id=rpc_peer_id, access_hash=800, username="rpc-corrected"))
            return types.UpdatesDifferenceEmpty(date=102, seq=2)

        cache = PeerCache(config, storage, remote)
        manager = UpdateManager(config, storage, remote)
        await manager.handle_raw_update(pushed(types.User(id=71, access_hash=711, username="envelope"), seq=2))

        peers = {peer.id: peer for peer in session_record_from_mapping(await storage.load() or {}).peers}
        assert peers[71].username == ("rpc-corrected" if rpc_peer_id == 71 else "envelope")
        assert peers[71].access_hash == (800 if rpc_peer_id == 71 else 711)
        assert peers[rpc_peer_id].username == "rpc-corrected"
        assert peers[rpc_peer_id].phone is None
        if rpc_peer_id == 71:
            with pytest.raises(NotFound, match="older pending alias is no longer authoritative"):
                await cache.resolve_peer("@envelope")
        await manager.handle_raw_update(unrelated_update())
        assert session_record_from_mapping(await storage.load() or {}).peers == tuple(peers.values())
        await manager.handle_raw_update(pushed(types.User(id=71, access_hash=719, username="newest")))
        assert await cache.resolve_peer("@newest") == Peer(id=71, kind="user", access_hash=719)

    event_loop.run(scenario())


@pytest.mark.parametrize("channel_difference", [False, True], ids=["global", "channel"])
def test_newer_difference_entity_wins_over_envelope_with_shared_baseline(monkeypatch: pytest.MonkeyPatch, channel_difference: bool) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        storage = InMemorySessionStorage(SessionRecord(peers=(original_peer(), PeerCacheEntry(id=8, kind="channel", access_hash=88))))
        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)
        newest = types.User(id=71, access_hash=719, username="difference", phone=OBSERVATION_NEW_PHONE)

        async def remote(request: object) -> object:
            if channel_difference:
                assert isinstance(request, functions.UpdatesGetChannelDifference)
                return types.UpdatesChannelDifference(final=True, pts=2, new_messages=(), other_updates=(), chats=(), users=(newest,))
            assert isinstance(request, functions.UpdatesGetDifference)
            return types.UpdatesDifference(new_messages=(), new_encrypted_messages=(), other_updates=(), chats=(), users=(newest,), state=types.UpdatesState(pts=0, qts=0, date=102, seq=2, unread_count=0))

        manager = UpdateManager(config, storage, remote)
        updates = (types.UpdateChannelTooLong(channel_id=8, pts=1),) if channel_difference else ()
        envelope = types.Updates(updates=updates, users=(types.User(id=71, access_hash=711, username="envelope"),), chats=(), date=100, seq=0 if channel_difference else 2)
        await manager.handle_raw_update(envelope)
        cache = PeerCache(config, storage, remote)
        expected = Peer(id=71, kind="user", access_hash=719)
        assert await cache.resolve_peer("@difference") == expected
        assert await cache.resolve_peer(OBSERVATION_NEW_PHONE) == expected
        peer = next(peer for peer in session_record_from_mapping(await storage.load() or {}).peers if peer.id == 71)
        assert peer.username == "difference"
        assert peer.phone == OBSERVATION_NEW_PHONE
        assert peer.raw is not None and peer.raw["_miniproto_complete"] is True

    event_loop.run(scenario())


@pytest.mark.parametrize("partial_field", ["name", "phone", "username"])
def test_partial_observation_during_recovery_does_not_block_independent_alias_removals(tmp_path: Path, partial_field: str) -> None:
    async def scenario() -> None:
        path = tmp_path / "partial.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
        await storage.save(SessionRecord(peers=(original_peer(),)))
        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)

        async def remote(request: object) -> object:
            if isinstance(request, functions.ContactsResolveUsername):
                raise NotFound("retired alias requires remote resolution")
            assert isinstance(request, functions.UpdatesGetDifference)
            if partial_field == "name":
                await cache.remember_raw_entities(types.User(id=71, min=True, access_hash=999, first_name="Newer partial"))
            elif partial_field == "phone":
                await cache.remember_raw_entities(types.User(id=71, min=True, phone=OBSERVATION_NEW_PHONE))
            else:
                await UpdateManager(config, storage, remote).handle_raw_update(pushed(types.User(id=71, min=True, username="partialprimary")))
            return types.UpdatesDifferenceEmpty(date=102, seq=2)

        cache = PeerCache(config, storage, remote)

        async def check(candidate: PeerCache) -> None:
            assert await candidate.resolve_peer(71) == Peer(id=71, kind="user", access_hash=711)
            for alias in ("oldprimary", "oldsecondary"):
                with pytest.raises(NotFound, match="retired alias requires remote resolution"):
                    await candidate.resolve_peer(f"@{alias}")
            with pytest.raises(NotFound, match="phone peer is not cached"):
                await candidate.resolve_peer(OBSERVATION_OLD_PHONE)
            if partial_field == "phone":
                assert await candidate.resolve_peer(OBSERVATION_NEW_PHONE) == Peer(id=71, kind="user", access_hash=711)
            if partial_field == "username":
                assert await candidate.resolve_peer("@partialprimary") == Peer(id=71, kind="user", access_hash=711)

        try:
            assert await cache.resolve_peer("@oldsecondary") == Peer(id=71, kind="user", access_hash=710)
            manager = UpdateManager(config, storage, remote)
            await manager.handle_raw_update(pushed(types.User(id=71, access_hash=711, first_name="Older full"), seq=2))
            record = session_record_from_mapping(await storage.load() or {})
            peer = record.peers[0]
            assert peer.username == ("partialprimary" if partial_field == "username" else None)
            assert peer.phone == (OBSERVATION_NEW_PHONE if partial_field == "phone" else None)
            assert peer.access_hash == 711
            if partial_field == "name":
                assert peer.raw is not None and peer.raw["first_name"] == "Newer partial"
                assert peer.raw.get("title") != "Older full"
            await check(cache)
            await storage.close()
            reloaded = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
            try:
                assert session_record_from_mapping(await reloaded.load() or {}).peers == (peer,)
                await check(PeerCache(config, reloaded, remote))
            finally:
                await reloaded.close()
        finally:
            await storage.close()

    event_loop.run(scenario())


@pytest.mark.parametrize("concurrent", ["partial", "full", "full-then-partial"])
def test_first_full_peer_survives_concurrent_partial_insert(tmp_path: Path, concurrent: str) -> None:
    async def scenario() -> None:
        path = tmp_path / "first-peer.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
        await storage.save(SessionRecord())
        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)
        concurrent_peer: PeerCacheEntry | None = None
        recovery_requests = 0

        async def remote(request: object) -> object:
            nonlocal concurrent_peer, recovery_requests
            if isinstance(request, functions.ContactsResolveUsername):
                raise NotFound("alias absent from newer full observation")
            assert isinstance(request, functions.UpdatesGetDifference)
            recovery_requests += 1
            assert not session_record_from_mapping(await storage.load() or {}).peers
            if concurrent != "partial":
                await cache.remember_raw_entities(types.User(id=71, access_hash=800, first_name="Newer full"))
            if concurrent != "full":
                await cache.remember_raw_entities(types.User(id=71, min=True, access_hash=999, first_name="Partial"))
            concurrent_peer = session_record_from_mapping(await storage.load() or {}).peers[0]
            return types.UpdatesDifferenceEmpty(date=102, seq=2)

        cache = PeerCache(config, storage, remote)

        async def check(candidate: PeerCache) -> None:
            access_hash = 717 if concurrent == "partial" else 800
            expected = Peer(id=71, kind="user", access_hash=access_hash)
            assert await candidate.resolve_peer(71) == expected
            assert await candidate.resolve_input_peer(71) == types.InputPeerUser(user_id=71, access_hash=access_hash)
            for alias in ("@newprimary", "@newsecondary"):
                if concurrent == "partial":
                    assert await candidate.resolve_peer(alias) == expected
                else:
                    with pytest.raises(NotFound, match="alias absent from newer full observation"):
                        await candidate.resolve_peer(alias)
            if concurrent == "partial":
                assert await candidate.resolve_peer(OBSERVATION_NEW_PHONE) == expected

        try:
            manager = UpdateManager(config, storage, remote)
            full = types.User(id=71, access_hash=717, first_name="Admitted full", username="newprimary", phone=OBSERVATION_NEW_PHONE, usernames=(types.Username(username="newsecondary", active=True),))  # fmt: skip
            await manager.handle_raw_update(pushed(full, seq=2))
            assert recovery_requests == 1
            record = session_record_from_mapping(await storage.load() or {})
            assert record.update_state is not None and record.update_state.seq == 2
            assert len(record.peers) == 1
            peer = record.peers[0]
            if concurrent == "partial":
                assert peer.access_hash == 717
                assert peer.username == "newprimary"
                assert peer.raw is not None and peer.raw["_miniproto_complete"] is True
                assert peer.raw["first_name"] == "Partial"
            else:
                assert peer == concurrent_peer
            await check(cache)
            await storage.close()
            reloaded = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
            try:
                assert session_record_from_mapping(await reloaded.load() or {}).peers == record.peers
                await check(PeerCache(config, reloaded, remote))
            finally:
                await reloaded.close()
        finally:
            await storage.close()

    event_loop.run(scenario())


@pytest.mark.parametrize("full_source", ["rpc", "push"])
@pytest.mark.parametrize("partial_count", [1, 3])
def test_full_alias_absence_authority_survives_later_partials_and_reload(tmp_path: Path, full_source: str, partial_count: int) -> None:
    async def scenario() -> None:
        path = tmp_path / "full-then-partial.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
        await storage.save(SessionRecord(peers=(original_peer(),)))
        config = ClientConfig(api_id=1, api_hash="offline", session_storage=storage)
        authoritative: PeerCacheEntry | None = None

        async def remote(request: object) -> object:
            nonlocal authoritative
            if isinstance(request, functions.ContactsResolveUsername):
                raise NotFound("alias absent from newer full observation")
            assert isinstance(request, functions.UpdatesGetDifference)
            full = types.User(id=71, access_hash=800, username="rpc-corrected")
            if full_source == "rpc":
                await cache.remember_raw_entities(full)
            else:
                await UpdateManager(config, storage, remote).handle_raw_update(pushed(full))
            partials = (types.User(id=71, min=True, first_name="Later partial"), types.User(id=71, min=True, username="partial-alias"), types.User(id=71, min=True, phone=OBSERVATION_NEW_PHONE))
            for partial in partials[:partial_count]:
                await cache.remember_raw_entities(partial)
            authoritative = session_record_from_mapping(await storage.load() or {}).peers[0]
            return types.UpdatesDifferenceEmpty(date=102, seq=2)

        cache = PeerCache(config, storage, remote)

        async def check(candidate: PeerCache) -> None:
            for alias in ("envelope", "oldprimary", "oldsecondary"):
                with pytest.raises(NotFound, match="alias absent from newer full observation"):
                    await candidate.resolve_peer(f"@{alias}")
            active = "rpc-corrected" if partial_count == 1 else "partial-alias"
            assert await candidate.resolve_peer(f"@{active}") == Peer(id=71, kind="user", access_hash=800)
            if partial_count == 3:
                assert await candidate.resolve_peer(OBSERVATION_NEW_PHONE) == Peer(id=71, kind="user", access_hash=800)

        try:
            manager = UpdateManager(config, storage, remote)
            await manager.handle_raw_update(pushed(types.User(id=71, access_hash=711, username="envelope"), seq=2))
            await check(cache)
            assert authoritative is not None
            assert authoritative.raw is not None and authoritative.raw["first_name"] == "Later partial"
            assert session_record_from_mapping(await storage.load() or {}).peers == (authoritative,)
            await storage.close()
            reloaded = EncryptedSQLiteSessionStorage(path, key=OBSERVATION_STORAGE_KEY)
            try:
                assert session_record_from_mapping(await reloaded.load() or {}).peers == (authoritative,)
                await check(PeerCache(config, reloaded, remote))
            finally:
                await reloaded.close()
        finally:
            await storage.close()

    event_loop.run(scenario())

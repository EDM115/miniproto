from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any

import pytest
from tests.support.fake_mtproto import FakeMTProtoServer

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    NewMessage,
    SessionRecord,
    TransportConfig,
    event_loop,
)
from miniproto.mtproto.codec import MessageContainer, MessageContainerItem, RpcResult
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, UpdateState, session_record_from_mapping
from miniproto.types import Message, Peer

AUTH_KEY = b"u" * 256


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
    ) -> object:
        self.update_requests.append(raw_request)
        if not self.responses:
            raise AssertionError("fake update client has no queued invoke response")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def storage_with_state(
    *, pts: int = 0, qts: int = 0, seq: int = 0, date: int = 1
) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            update_state=UpdateState(
                pts=pts, qts=qts, seq=seq, date=datetime.fromtimestamp(date, UTC)
            )
        )
    )


def storage_with_channel_state(*, channel_id: int = 123, pts: int = 10) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            peers=(PeerCacheEntry(id=channel_id, kind="channel", access_hash=999),),
            metadata={
                "updates": {
                    "channels": {
                        str(channel_id): {
                            "pts": pts,
                            "date": datetime.fromtimestamp(50, UTC).isoformat(),
                        }
                    }
                }
            },
        )
    )


def raw_message(message_id: int, text: str, *, user_id: int = 42, date: int = 100) -> types.Message:
    return types.Message(
        id=message_id, peer_id=types.PeerUser(user_id=user_id), date=date, message=text
    )


def raw_channel_message(
    message_id: int, text: str, *, channel_id: int = 123, date: int = 100
) -> types.Message:
    return types.Message(
        id=message_id, peer_id=types.PeerChannel(channel_id=channel_id), date=date, message=text
    )


def short_message(
    message_id: int,
    text: str,
    *,
    user_id: int = 42,
    pts: int = 1,
    pts_count: int = 1,
    date: int = 100,
) -> types.UpdateShortMessage:
    return types.UpdateShortMessage(
        id=message_id, user_id=user_id, message=text, pts=pts, pts_count=pts_count, date=date
    )


def public_message(text: str, *, message_id: int = 1) -> NewMessage:
    return NewMessage(
        message=Message(
            id=message_id,
            peer=Peer(id=42, kind="user"),
            text=text,
            date=datetime.fromtimestamp(100, UTC),
        )
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
        client = FakeUpdateClient(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [difference]
        )
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
                    id=channel_id,
                    access_hash=999,
                    title="Channel",
                    photo=types.ChatPhotoEmpty(),
                    date=1_700_000_000,
                ),
            ),
            users=(),
        )
        client = FakeUpdateClient(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage), [difference]
        )
        await client.connect()
        iterator = client.iter_updates()
        await client._handle_raw_update(
            types.UpdateNewChannelMessage(
                message=raw_channel_message(112, "current", channel_id=channel_id, date=101),
                pts=13,
                pts_count=1,
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


def test_updates_container_advances_pts_without_false_gap_recovery() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        container = types.Updates(
            updates=(
                types.UpdateNewMessage(
                    message=raw_message(501, "first", date=501), pts=11, pts_count=1
                ),
                types.UpdateNewMessage(
                    message=raw_message(502, "second", date=502), pts=12, pts_count=1
                ),
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
            update=types.UpdateNewMessage(
                message=raw_message(201, "wrapped", date=201), pts=11, pts_count=1
            ),
            date=201,
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
        pushed = types.UpdateShortMessage(
            id=901, user_id=42, message="pushed", pts=11, pts_count=1, date=901
        )

        def handle(message):
            if message.seq_no % 2 == 0:
                return None
            return MessageContainer(
                messages=(
                    MessageContainerItem(
                        msg_id=message.msg_id + 4, seq_no=1, body=pushed.serialize()
                    ),
                    MessageContainerItem(
                        msg_id=message.msg_id + 8,
                        seq_no=3,
                        body=RpcResult(
                            req_msg_id=message.msg_id,
                            result=types.NearestDc(
                                country="US", this_dc=2, nearest_dc=2
                            ).serialize(),
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
                    update_state=UpdateState(
                        pts=10, qts=0, seq=0, date=datetime.fromtimestamp(1, UTC)
                    ),
                )
            )
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=storage, transport=transport
                )
            )
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
                api_id=1, api_hash="hash", update_queue_size=1, update_queue_overflow="drop_oldest"
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
                api_id=1, api_hash="hash", update_queue_size=1, update_queue_overflow="drop_newest"
            )
        )

        @client.on(NewMessage)
        def handle(event: NewMessage) -> None:
            if event.message is not None:
                seen.append(event.message.text)

        await client._emit_new_message(public_message("old", message_id=1))
        await client._emit_new_message(public_message("new", message_id=2))
        event = await anext(client.iter_updates())
        assert isinstance(event, NewMessage)
        assert event.message is not None
        assert event.message.text == "old"
        assert seen == ["old"]

    run(scenario())


def test_reconnect_reuses_persisted_duplicate_window() -> None:
    async def scenario() -> None:
        storage = storage_with_state(pts=10)
        first_client = FakeUpdateClient(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage)
        )
        raw_update = short_message(301, "persisted", pts=11, date=301)
        await first_client.connect()
        await first_client._handle_raw_update(raw_update)
        event = await anext(first_client.iter_updates())
        assert isinstance(event, NewMessage)
        await first_client.disconnect()
        second_client = FakeUpdateClient(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage)
        )
        await second_client.connect()
        iterator = second_client.iter_updates()
        await second_client._handle_raw_update(raw_update)
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(anext(iterator), timeout=0.01)
        await second_client.disconnect()

    run(scenario())


def test_background_update_task_surfaces_handler_exceptions_on_disconnect() -> None:
    async def scenario() -> None:
        client = FakeUpdateClient(ClientConfig(api_id=1, api_hash="hash"))

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

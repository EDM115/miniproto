from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Message,
    Peer,
    SessionRecord,
    event_loop,
)
from miniproto.errors import TransportFlood
from miniproto.mtproto.codec import RpcErrorBody, encode_message_body
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, UserIdentity, session_record_from_mapping

AUTH_KEY = b"m" * 256


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


def storage_with_auth(
    *, peers: tuple[PeerCacheEntry, ...] = (), user: UserIdentity | None = None
) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
            user=user,
            peers=peers,
        )
    )


def inner_request(wrapped: object) -> object:
    assert isinstance(wrapped, functions.InvokeWithLayer)
    assert isinstance(wrapped.query, functions.InitConnection)
    return wrapped.query.query


def rpc_error(code: int, text: str) -> bytes:
    return encode_message_body(RpcErrorBody(error_code=code, error_message=text))


def test_send_message_uses_cached_input_peer_and_generated_send_request() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),)
        )
        sender = FakeSender(
            [types.UpdateShortSentMessage(id=123, pts=1, pts_count=1, date=1_700_000_000)]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        message = await client.send_message("@alice", "hello")
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesSendMessage)
        assert isinstance(request.peer, types.InputPeerUser)
        assert request.peer.user_id == 7
        assert request.peer.access_hash == 77
        assert request.message == "hello"
        assert request.entities is None
        assert request.random_id > 0
        assert message.id == 123
        assert message.peer == Peer(id=7, kind="user", access_hash=77)
        assert message.text == "hello"

    run(scenario())


def test_send_message_parses_markdown_lite_entities() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(user=UserIdentity(id=42, access_hash=9900, username="alice"))
        sender = FakeSender(
            [types.UpdateShortSentMessage(id=124, pts=1, pts_count=1, date=1_700_000_000)]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        message = await client.send_message(
            "me", "hi **bold** and `x`", parse_mode="markdown-lite", random_id=99
        )
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesSendMessage)
        assert isinstance(request.peer, types.InputPeerSelf)
        assert request.message == "hi bold and x"
        assert request.random_id == 99
        assert request.entities == (
            types.MessageEntityBold(offset=3, length=4),
            types.MessageEntityCode(offset=12, length=1),
        )
        assert message.entities == request.entities

    run(scenario())


def test_send_message_plain_text_keeps_markdown_markers_without_parse_mode() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(user=UserIdentity(id=42, access_hash=9900, username="alice"))
        sender = FakeSender(
            [types.UpdateShortSentMessage(id=125, pts=1, pts_count=1, date=1_700_000_000)]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        await client.send_message("self", "**not parsed**")
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesSendMessage)
        assert request.message == "**not parsed**"
        assert request.entities is None

    run(scenario())


def test_send_message_normalizes_message_from_updates_container_and_remembers_entities() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),)
        )
        raw_message = types.Message(
            id=77, peer_id=types.PeerUser(user_id=7), date=1_700_000_001, message="server text"
        )
        sender = FakeSender(
            [
                types.Updates(
                    updates=(types.UpdateNewMessage(message=raw_message, pts=2, pts_count=1),),
                    users=(types.User(id=7, access_hash=70, username="alice2"),),
                    chats=(),
                    date=1_700_000_001,
                    seq=1,
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        message = await client.send_message(Peer(id=7, kind="user", access_hash=77), "client text")
        assert message.id == 77
        assert message.text == "server text"
        assert message.peer == Peer(id=7, kind="user", access_hash=77)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.peers[0].username == "alice2"
        assert record.peers[0].access_hash == 70

    run(scenario())


def test_send_message_surfaces_flood_wait_errors_from_raw_invoke() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(user=UserIdentity(id=42, access_hash=9900, username="alice"))
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5")])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        with pytest.raises(TransportFlood) as exc_info:
            await client.send_message("me", "hello")
        assert exc_info.value.seconds == 5

    run(scenario())


def test_get_history_returns_normalized_messages_and_remembers_entities() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),)
        )
        raw_message = types.Message(
            id=77, peer_id=types.PeerUser(user_id=7), date=1_700_000_001, message="history text"
        )
        sender = FakeSender(
            [
                types.MessagesMessages(
                    messages=(raw_message,),
                    chats=(),
                    users=(types.User(id=7, access_hash=99, username="alice2"),),
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        messages = await client.get_history("@alice", limit=10, offset_id=5)
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesGetHistory)
        assert isinstance(request.peer, types.InputPeerUser)
        assert request.limit == 10
        assert request.offset_id == 5
        assert messages == (
            Message(
                id=77,
                peer=Peer(id=7, kind="user", access_hash=77),
                text="history text",
                date=messages[0].date,
                raw=raw_message,
            ),
        )
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.peers[0].username == "alice2"
        assert record.peers[0].access_hash == 99

    run(scenario())


def test_edit_message_sends_generated_edit_request_and_normalizes_result() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),)
        )
        raw_message = types.Message(
            id=77,
            peer_id=types.PeerUser(user_id=7),
            date=1_700_000_002,
            message="edited bold",
            entities=(types.MessageEntityBold(offset=7, length=4),),
        )
        sender = FakeSender(
            [
                types.Updates(
                    updates=(types.UpdateEditMessage(message=raw_message, pts=2, pts_count=1),),
                    users=(),
                    chats=(),
                    date=1_700_000_002,
                    seq=1,
                )
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        message = await client.edit_message("@alice", 77, "edited **bold**", parse_mode="md")
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesEditMessage)
        assert request.id == 77
        assert request.message == "edited bold"
        assert request.entities == (types.MessageEntityBold(offset=7, length=4),)
        assert message.id == 77
        assert message.text == "edited bold"
        assert message.entities == request.entities

    run(scenario())


def test_delete_messages_uses_messages_delete_for_non_channels() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),)
        )
        sender = FakeSender([types.MessagesAffectedMessages(pts=2, pts_count=2)])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        result = await client.delete_messages("@alice", [77, 78], revoke=False)
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.MessagesDeleteMessages)
        assert request.revoke is False
        assert request.id == (77, 78)
        assert isinstance(result, types.MessagesAffectedMessages)
        assert result.pts_count == 2

    run(scenario())


def test_delete_messages_uses_channels_delete_for_channels() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            peers=(PeerCacheEntry(id=8, kind="channel", access_hash=88, username="channel"),)
        )
        sender = FakeSender([types.MessagesAffectedMessages(pts=3, pts_count=1)])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        await client.delete_messages("@channel", 99)
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.ChannelsDeleteMessages)
        assert isinstance(request.channel, types.InputChannel)
        assert request.channel.channel_id == 8
        assert request.channel.access_hash == 88
        assert request.id == (99,)

    run(scenario())


def test_send_message_rejects_unknown_parse_mode_and_options() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(user=UserIdentity(id=42, access_hash=9900, username="alice"))
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        with pytest.raises(ValueError, match="parse mode"):
            await client.send_message("me", "hello", parse_mode="html")
        with pytest.raises(TypeError, match="unsupported send_message options"):
            await client.send_message("me", "hello", unsupported=True)

    run(scenario())

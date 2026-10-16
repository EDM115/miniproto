from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

import pytest

import miniproto.messages as messages
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Message,
    Peer,
    SessionRecord,
    encode_file_id,
    event_loop,
)
from miniproto.errors import FloodWait
from miniproto.messages import message_from_update_result
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
    if isinstance(wrapped, functions.InvokeWithoutUpdates):
        wrapped = wrapped.query
    if isinstance(wrapped, functions.InvokeWithLayer):
        assert isinstance(wrapped.query, functions.InitConnection)
        return wrapped.query.query
    return wrapped


def rpc_error(code: int, text: str) -> bytes:
    return encode_message_body(RpcErrorBody(error_code=code, error_message=text))


def test_send_message_uses_cached_input_peer_and_generated_send_request() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),))
        sender = FakeSender([types.UpdateShortSentMessage(id=123, pts=1, pts_count=1, date=1_700_000_000)])
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
        sender = FakeSender([types.UpdateShortSentMessage(id=124, pts=1, pts_count=1, date=1_700_000_000)])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender = sender
        await client.connect()
        message = await client.send_message("me", "hi **bold** and `x`", parse_mode="markdown-lite", random_id=99)
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
        sender = FakeSender([types.UpdateShortSentMessage(id=125, pts=1, pts_count=1, date=1_700_000_000)])
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
        storage = storage_with_auth(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),))
        raw_message = types.Message(id=77, peer_id=types.PeerUser(user_id=7), date=1_700_000_001, message="server text")
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
        with pytest.raises(FloodWait) as exc_info:
            await client.send_message("me", "hello")
        assert exc_info.value.seconds == 5

    run(scenario())


def test_get_history_returns_normalized_messages_and_remembers_entities() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),))
        raw_message = types.Message(
            id=77, peer_id=types.PeerUser(user_id=7), date=1_700_000_001, message="history text"
        )
        sender = FakeSender(
            [
                types.MessagesMessages(
                    messages=(raw_message,),
                    chats=(),
                    users=(types.User(id=7, access_hash=99, username="alice2"),),
                    topics=(),
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
                date=datetime.fromtimestamp(1_700_000_001, UTC),
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
        storage = storage_with_auth(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),))
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


@pytest.mark.parametrize("update_type", [types.UpdateEditMessage, types.UpdateEditChannelMessage])
def test_message_normalization_unwraps_edit_inside_update_short(
    update_type: type[types.UpdateEditMessage] | type[types.UpdateEditChannelMessage],
) -> None:
    raw_message = types.Message(id=77, peer_id=types.PeerUser(user_id=7), date=1_700_000_002, message="edited")
    result = types.UpdateShort(update=update_type(message=raw_message, pts=2, pts_count=1), date=1_700_000_002)

    message = message_from_update_result(result, fallback_peer=Peer(id=7, kind="user"), fallback_text="fallback")

    assert message.id == 77
    assert message.text == "edited"


def test_delete_messages_uses_messages_delete_for_non_channels() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),))
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
        storage = storage_with_auth(peers=(PeerCacheEntry(id=8, kind="channel", access_hash=88, username="channel"),))
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


@pytest.mark.parametrize("parse_mode", ["markdown", "markdown-lite", "md", " MARKDOWN_LITE "])
def test_markdown_offsets_count_rendered_utf16_units(parse_mode: str) -> None:
    parsed = messages.parse_message_text("A😀\\* **é🦊**__e\u0301__`λ🚀` ```py\nZ🐈```!", parse_mode)

    assert parsed.text == "A😀* é🦊e\u0301λ🚀 py\nZ🐈!"
    assert parsed.entities == (
        types.MessageEntityBold(offset=5, length=3),
        types.MessageEntityItalic(offset=8, length=2),
        types.MessageEntityCode(offset=10, length=3),
        types.MessageEntityPre(offset=14, length=6, language=""),
    )


def test_empty_spans_do_not_advance_offsets_or_create_entities() -> None:
    parsed = messages.parse_message_text("😀****____``**q**``````__x__", "md")

    assert parsed.text == "😀qx"
    assert parsed.entities == (types.MessageEntityBold(offset=2, length=1), types.MessageEntityItalic(offset=3, length=1))  # fmt: skip


def test_span_contents_preserve_nested_markers_and_backslashes() -> None:
    parsed = messages.parse_message_text("**a__β__\\*🦊**__b`c`__", "md")

    assert parsed.text == "a__β__\\*🦊b`c`"
    assert parsed.entities == (types.MessageEntityBold(offset=0, length=10), types.MessageEntityItalic(offset=10, length=4))  # fmt: skip


def test_backslash_inside_span_does_not_escape_closing_delimiter() -> None:
    parsed = messages.parse_message_text("**x\\**tail", "md")

    assert parsed.text == "x\\tail"
    assert parsed.entities == (types.MessageEntityBold(offset=0, length=2),)


def test_escaped_astral_character_counts_as_two_utf16_units() -> None:
    parsed = messages.parse_message_text("\\🦊**x**", "md")

    assert parsed.text == "🦊x"
    assert parsed.entities == (types.MessageEntityBold(offset=2, length=1),)


def test_unmatched_delimiters_and_trailing_escape_remain_in_offsets() -> None:
    parsed = messages.parse_message_text("😀***x __q__ \\", "md")

    assert parsed.text == "😀***x q \\"
    assert parsed.entities == (types.MessageEntityItalic(offset=7, length=1),)


def test_unmatched_triple_backticks_retain_single_character_fallback() -> None:
    parsed = messages.parse_message_text("```open", "md")

    assert parsed.text == "`open"
    assert parsed.entities == ()


@pytest.mark.parametrize("text", ["\ud800", "**x**\ud800", "\\\ud800"])
def test_surrogates_after_last_span_are_not_measured(text: str) -> None:
    parsed = messages.parse_message_text(text, "md")

    assert parsed.text == ("x\ud800" if text.startswith("**") else "\ud800")


@pytest.mark.parametrize("text", ["\ud800****", "**\ud800**", "**x**\ud800__y__", "\\\ud800__x__"])
def test_surrogates_in_measured_prefixes_and_spans_still_raise(text: str) -> None:
    with pytest.raises(UnicodeEncodeError):
        messages.parse_message_text(text, "md")


@pytest.mark.parametrize("parse_mode", [None, "", "plain", "text", "none"])
def test_plain_modes_preserve_markers_escapes_and_surrogates(parse_mode: str | None) -> None:
    text = "\ud800\\* **😀**"

    parsed = messages.parse_message_text(text, parse_mode)

    assert parsed.text == text
    assert parsed.entities == ()


@pytest.mark.parametrize("repeat_count", [128, 256])
def test_utf16_accounting_work_is_bounded_by_rendered_text(monkeypatch: pytest.MonkeyPatch, repeat_count: int) -> None:
    measured_characters = 0
    utf16_length = messages._utf16_length

    def measure(value: str) -> int:
        nonlocal measured_characters
        measured_characters += len(value)
        return utf16_length(value)

    monkeypatch.setattr(messages, "_utf16_length", measure)

    parsed = messages.parse_message_text("p😀\\*__λ__**🦊**" * repeat_count, "md")

    assert parsed.text == "p😀*λ🦊" * repeat_count
    assert parsed.entities == tuple(entity for index in range(repeat_count) for entity in (types.MessageEntityItalic(offset=7 * index + 4, length=1), types.MessageEntityBold(offset=7 * index + 5, length=2)))  # fmt: skip
    assert 0 < measured_characters <= len(parsed.text)


@pytest.mark.parametrize("operation", ["send", "edit", "caption"])
@pytest.mark.parametrize("formatting", ["markdown", "plain", "explicit", "empty-explicit"])
def test_public_message_and_caption_callers_preserve_formatting(monkeypatch: pytest.MonkeyPatch, operation: str, formatting: str) -> None:  # fmt: skip
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        requests: list[object] = []

        async def invoke(request: object, **kwargs: object) -> object:
            requests.append(request)
            return types.Updates(updates=(), users=(), chats=(), date=1_700_000_000, seq=1)

        monkeypatch.setattr(client, "invoke", invoke)
        source = "😀 \\* **x🦊**"
        explicit = (types.MessageEntityCode(offset=0, length=2),)
        if formatting == "markdown":
            parse_mode = "md"
            entities = None
            expected_text = "😀 * x🦊"
            expected_entities = (types.MessageEntityBold(offset=5, length=3),)
        elif formatting == "plain":
            parse_mode = None
            entities = None
            expected_text = source
            expected_entities = ()
        else:
            expected_entities = explicit if formatting == "explicit" else ()
            parse_mode = "html"
            entities = expected_entities
            expected_text = source
        peer = Peer(id=7, kind="user", access_hash=77)
        if operation == "send":
            result = await client.send_message(peer, source, parse_mode=parse_mode, entities=entities)
            expected_request_type = functions.MessagesSendMessage
        elif operation == "edit":
            result = await client.edit_message(peer, 21, source, parse_mode=parse_mode, entities=entities)
            expected_request_type = functions.MessagesEditMessage
        else:
            location = types.InputDocumentFileLocation(id=17, access_hash=37, file_reference=b"offline", thumb_size="")
            result = await client.send_file(peer, encode_file_id(location), caption=source, parse_mode=parse_mode, entities=entities)  # fmt: skip
            expected_request_type = functions.MessagesSendMedia

        assert len(requests) == 1
        request = requests[0]
        assert isinstance(request, expected_request_type)
        assert request.message == expected_text
        assert request.entities == (expected_entities or None)
        assert result.text == expected_text
        assert result.entities == expected_entities

    event_loop.run(scenario())

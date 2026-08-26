"""Parse lightweight message markup and normalize Telegram message responses."""

from __future__ import annotations

import secrets
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

from miniproto.media.download import media_from_raw
from miniproto.raw import types
from miniproto.types import Message, Peer
from miniproto.updates.state import coerce_update_datetime, utc_now

MessageParseMode = Literal["markdown", "markdown-lite", "md", "plain", "text", "none"]


@dataclass(frozen=True, slots=True)
class ParsedMessageText:
    """Rendered message text and UTF-16-indexed MTProto entities.

    Attributes:
        text: Rendered text after supported delimiters and escapes are removed.
        entities: Immutable entities whose offsets and lengths are UTF-16 code units.
    """

    text: str
    entities: tuple[object, ...] = ()


def parse_message_text(text: str, parse_mode: str | None = None) -> ParsedMessageText:
    """Render the supported lightweight Markdown delimiters into MTProto entities.

    Args:
        text: Source message text, with backslashes escaping the next character.
        parse_mode: ``markdown``/``markdown-lite``/``md`` enables parsing;
            ``None``, ``plain``, ``text`` and ``none`` preserve text verbatim.

    Returns:
        Rendered text and entities whose offsets and lengths use UTF-16 code units.

    Raises:
        ValueError: If ``parse_mode`` is not a supported spelling.
    """
    mode = _normalize_parse_mode(parse_mode)
    if mode is None:
        return ParsedMessageText(text=text)
    output: list[str] = []
    entities: list[object] = []
    index = 0
    while index < len(text):
        if text[index] == "\\" and index + 1 < len(text):
            output.append(text[index + 1])
            index += 2
            continue
        parsed = _parse_delimited_entity(text, index, output)
        if parsed is not None:
            next_index, entity = parsed
            if entity is not None:
                entities.append(entity)
            index = next_index
            continue
        output.append(text[index])
        index += 1
    return ParsedMessageText(text="".join(output), entities=tuple(entities))


def make_random_id() -> int:
    """Return a non-zero random 63-bit client message identifier."""
    return secrets.randbits(63) or 1


def message_from_send_result(result: object, *, peer: Peer, text: str, entities: Iterable[object] = ()) -> Message:
    """Normalize a send response, retaining supplied values when Telegram omits a message.

    Args:
        result: Raw send result or update container.
        peer: Destination peer used as the fallback message peer.
        text: Submitted text used if no raw message is present.
        entities: Submitted entities used if Telegram did not return entities.

    Returns:
        The sent message, with a zero ID and current UTC time only for incomplete responses.
    """
    parsed_entities = tuple(entities)
    if isinstance(result, types.UpdateShortSentMessage):
        return Message(
            id=result.id,
            peer=peer,
            text=text,
            date=coerce_update_datetime(result.date),
            media=media_from_raw(result.media),
            entities=tuple(result.entities or parsed_entities),
            raw=result,
        )
    raw_message = _find_message_result(result)
    if raw_message is not None:
        return _message_from_raw(raw_message, fallback_peer=peer, fallback_entities=parsed_entities)
    return Message(id=0, peer=peer, text=text, date=utc_now(), entities=parsed_entities, raw=result)


def message_from_raw(raw: types.Message, *, fallback_peer: Peer) -> Message:
    """Convert a raw Telegram message using ``fallback_peer`` for unknown peer forms.

    Args:
        raw: Concrete Telegram message object.
        fallback_peer: Destination peer retained when raw peer form is unknown or richer.
    """
    return _message_from_raw(raw, fallback_peer=fallback_peer, fallback_entities=())


def message_from_update_result(
    result: object, *, fallback_peer: Peer, fallback_text: str, entities: Iterable[object] = ()
) -> Message:
    """Normalize an update response or create a fallback message when none is present.

    The fallback has ID ``0`` and the current UTC time, preserving submitted text
    and entities for response forms that do not carry a message object.

    Args:
        result: Raw update or response container to inspect.
        fallback_peer: Peer used when no concrete message is found.
        fallback_text: Submitted text used by the synthetic fallback.
        entities: Submitted entities used when a concrete message omits entities.
    """
    parsed_entities = tuple(entities)
    raw_message = _find_message_result(result)
    if raw_message is None:
        return Message(
            id=0, peer=fallback_peer, text=fallback_text, date=utc_now(), entities=parsed_entities, raw=result
        )
    return _message_from_raw(raw_message, fallback_peer=fallback_peer, fallback_entities=parsed_entities)


def messages_from_history_result(result: object, *, fallback_peer: Peer) -> tuple[Message, ...]:
    """Convert only concrete raw messages from a history result in source order.

    Args:
        result: Raw history response with an optional ``messages`` sequence.
        fallback_peer: Peer used for unknown raw peer representations.
    """
    raw_messages = tuple(getattr(result, "messages", ()) or ())
    return tuple(
        _message_from_raw(raw, fallback_peer=fallback_peer, fallback_entities=())
        for raw in raw_messages
        if isinstance(raw, types.Message)
    )


def _parse_delimited_entity(text: str, index: int, output: list[str]) -> tuple[int, object | None] | None:
    """Parse one closed delimiter at ``index`` and append its rendered content.

    Args:
        text: Original unrendered message text.
        index: Character offset where a delimiter may begin.
        output: Rendered text fragments emitted before and including this entity.
    """
    for delimiter, kind in (("```", "pre"), ("**", "bold"), ("__", "italic"), ("`", "code")):
        if not text.startswith(delimiter, index):
            continue
        content_start = index + len(delimiter)
        content_end = text.find(delimiter, content_start)
        if content_end < 0:
            return None
        content = text[content_start:content_end]
        offset = _utf16_length("".join(output))
        output.append(content)
        length = _utf16_length(content)
        entity = _entity(kind, offset, length) if length > 0 else None
        return content_end + len(delimiter), entity
    return None


def _entity(kind: str, offset: int, length: int) -> object:
    """Create the MTProto entity for a supported lightweight markup kind.

    Args:
        kind: Supported delimiter kind: bold, italic, code or pre.
        offset: UTF-16 start offset in the rendered text.
        length: UTF-16 entity length.
    """
    if kind == "bold":
        return types.MessageEntityBold(offset=offset, length=length)
    if kind == "italic":
        return types.MessageEntityItalic(offset=offset, length=length)
    if kind == "code":
        return types.MessageEntityCode(offset=offset, length=length)
    return types.MessageEntityPre(offset=offset, length=length, language="")


def _normalize_parse_mode(parse_mode: str | None) -> str | None:
    """Map public parse-mode aliases to parser modes or plain-text ``None``.

    Args:
        parse_mode: Optional public mode spelling supplied by the caller.
    """
    if parse_mode is None:
        return None
    normalized = parse_mode.strip().casefold().replace("_", "-")
    if normalized in {"", "none", "plain", "text"}:
        return None
    if normalized in {"markdown", "markdown-lite", "md"}:
        return normalized
    raise ValueError(f"unsupported parse mode: {parse_mode}")


def _find_message_result(result: object) -> types.Message | None:
    """Recursively find the first concrete message in supported update containers.

    Args:
        result: Raw message or supported update/result container.
    """
    if isinstance(result, types.Message):
        return result
    if isinstance(result, types.UpdateNewMessage | types.UpdateNewChannelMessage) and isinstance(
        result.message, types.Message
    ):
        return result.message
    if isinstance(result, types.UpdateEditMessage | types.UpdateEditChannelMessage) and isinstance(
        result.message, types.Message
    ):
        return result.message
    if isinstance(result, types.UpdateShort) and isinstance(
        result.update,
        types.UpdateNewMessage
        | types.UpdateNewChannelMessage
        | types.UpdateEditMessage
        | types.UpdateEditChannelMessage,
    ):
        return _find_message_result(result.update)
    if isinstance(result, types.Updates | types.UpdatesCombined):
        for update in result.updates:
            found = _find_message_result(update)
            if found is not None:
                return found
    return None


def _message_from_raw(raw: types.Message, *, fallback_peer: Peer, fallback_entities: tuple[object, ...]) -> Message:
    """Build a message model while preserving raw media, date and entity defaults.

    Args:
        raw: Concrete Telegram message object.
        fallback_peer: Peer used when raw peer conversion cannot identify a kind.
        fallback_entities: Submitted entities used only when raw entities are absent.
    """
    return Message(
        id=raw.id,
        peer=_peer_from_raw(raw.peer_id, fallback_peer),
        text=raw.message,
        date=coerce_update_datetime(raw.date),
        media=media_from_raw(raw.media),
        entities=tuple(raw.entities or fallback_entities),
        raw=raw,
    )


def _peer_from_raw(raw_peer: object, fallback: Peer) -> Peer:
    """Convert supported raw peer IDs, retaining richer matching fallback metadata.

    Args:
        raw_peer: Raw Telegram peer identifier to convert.
        fallback: Submitted peer retained for matching IDs or unsupported forms.
    """
    if isinstance(raw_peer, types.PeerUser):
        if fallback.kind in {"self", "user"} and fallback.id == raw_peer.user_id:
            return fallback
        return Peer(id=raw_peer.user_id, kind="user")
    if isinstance(raw_peer, types.PeerChat):
        if fallback.kind == "chat" and fallback.id == raw_peer.chat_id:
            return fallback
        return Peer(id=raw_peer.chat_id, kind="chat")
    if isinstance(raw_peer, types.PeerChannel):
        if fallback.kind == "channel" and fallback.id == raw_peer.channel_id:
            return fallback
        return Peer(id=raw_peer.channel_id, kind="channel")
    return fallback


def _utf16_length(value: str) -> int:
    """Return a string length in Telegram entity UTF-16 code units.

    Args:
        value: Text whose code-unit length is required.
    """
    return len(value.encode("utf-16-le")) // 2


__all__ = [
    "MessageParseMode",
    "ParsedMessageText",
    "make_random_id",
    "message_from_raw",
    "message_from_send_result",
    "message_from_update_result",
    "messages_from_history_result",
    "parse_message_text",
]

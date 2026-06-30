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
    text: str
    entities: tuple[object, ...] = ()


def parse_message_text(text: str, parse_mode: str | None = None) -> ParsedMessageText:
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
    return secrets.randbits(63) or 1


def message_from_send_result(
    result: object, *, peer: Peer, text: str, entities: Iterable[object] = ()
) -> Message:
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


def _parse_delimited_entity(
    text: str, index: int, output: list[str]
) -> tuple[int, object | None] | None:
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
    if kind == "bold":
        return types.MessageEntityBold(offset=offset, length=length)
    if kind == "italic":
        return types.MessageEntityItalic(offset=offset, length=length)
    if kind == "code":
        return types.MessageEntityCode(offset=offset, length=length)
    return types.MessageEntityPre(offset=offset, length=length, language="")


def _normalize_parse_mode(parse_mode: str | None) -> str | None:
    if parse_mode is None:
        return None
    normalized = parse_mode.strip().casefold().replace("_", "-")
    if normalized in {"", "none", "plain", "text"}:
        return None
    if normalized in {"markdown", "markdown-lite", "md"}:
        return normalized
    raise ValueError(f"unsupported parse mode: {parse_mode}")


def _find_message_result(result: object) -> types.Message | None:
    if isinstance(result, types.Message):
        return result
    if isinstance(result, types.UpdateNewMessage | types.UpdateNewChannelMessage) and isinstance(
        result.message, types.Message
    ):
        return result.message
    if isinstance(result, types.UpdateShort) and isinstance(
        result.update, types.UpdateNewMessage | types.UpdateNewChannelMessage
    ):
        return _find_message_result(result.update)
    if isinstance(result, types.Updates | types.UpdatesCombined):
        for update in result.updates:
            found = _find_message_result(update)
            if found is not None:
                return found
    return None


def _message_from_raw(
    raw: types.Message, *, fallback_peer: Peer, fallback_entities: tuple[object, ...]
) -> Message:
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
    return len(value.encode("utf-16-le")) // 2


__all__ = [
    "MessageParseMode",
    "ParsedMessageText",
    "make_random_id",
    "message_from_send_result",
    "parse_message_text",
]

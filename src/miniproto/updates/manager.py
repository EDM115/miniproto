from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Literal, TypeVar, cast, overload

from miniproto.config import ClientConfig
from miniproto.raw import functions, types
from miniproto.session.models import SessionRecord, session_record_from_mapping
from miniproto.session.storage import SessionStorage
from miniproto.types import Message, NewMessage, Peer, Update
from miniproto.updates.state import (
    DuplicateTracker,
    EntityReference,
    UpdateCursor,
    coerce_update_datetime,
    merge_peer_cache_entries,
    metadata_with_duplicate_keys,
)

UpdateQueueOverflowPolicy = Literal["raise", "drop_oldest", "drop_newest"]
UpdateT = TypeVar("UpdateT", bound=Update)
UpdateHandler = Callable[[UpdateT], Awaitable[None] | None]
UpdateInvoker = Callable[[object], Awaitable[object]]
_MAX_DIFFERENCE_ROUNDS = 10


@dataclass(frozen=True, slots=True)
class RawUpdateUnit:
    raw: object
    date: object | None = None


class UpdateManager:
    def __init__(
        self, config: ClientConfig, storage: SessionStorage, invoke: UpdateInvoker
    ) -> None:
        self._config = config
        self._storage = storage
        self._invoke = invoke
        self._updates: asyncio.Queue[Update] = asyncio.Queue(maxsize=config.update_queue_size)
        self._raw_updates: asyncio.Queue[object] = asyncio.Queue(maxsize=config.update_queue_size)
        self._handlers: dict[type[Update], list[UpdateHandler[Any]]] = {}
        self._task: asyncio.Task[None] | None = None
        self._state_lock = asyncio.Lock()
        self._cursor: UpdateCursor | None = None
        self._duplicates = DuplicateTracker(max_size=config.update_duplicate_window)

    @property
    def handlers(self) -> dict[type[Update], list[UpdateHandler[Any]]]:
        return self._handlers

    async def start(self) -> None:
        await self._ensure_loaded()
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._drain_raw_updates())

    async def stop(self) -> None:
        task = self._task
        self._task = None
        if task is None:
            return
        if task.done():
            exc = task.exception()
            if exc is not None:
                raise exc
            return
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    async def feed_raw_update(self, raw_update: object) -> None:
        if not self._offer_queue(self._raw_updates, raw_update):
            return

    async def handle_raw_update(self, raw_update: object) -> None:
        async with self._state_lock:
            await self._ensure_loaded()
            events = await self._process_raw_update(raw_update)
            await self._persist_cursor()
        for event in events:
            await self.emit_update(event)

    async def emit_update(self, update: Update) -> None:
        if not self._offer_queue(self._updates, update):
            return
        await self._dispatch_handlers(update)

    async def iter_updates(self) -> AsyncIterator[Update]:
        while True:
            yield await self._updates.get()

    @overload
    def on(
        self, update_type: type[UpdateT]
    ) -> Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]: ...

    @overload
    def on(
        self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT]
    ) -> UpdateHandler[UpdateT]: ...

    def on(
        self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT] | None = None
    ) -> UpdateHandler[UpdateT] | Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]:
        def register(candidate: UpdateHandler[UpdateT]) -> UpdateHandler[UpdateT]:
            self._handlers.setdefault(update_type, []).append(candidate)
            return candidate

        if handler is None:
            return register
        return register(handler)

    async def sync_state(self) -> UpdateCursor:
        result = await self._invoke(functions.UpdatesGetState())
        if not isinstance(result, types.UpdatesState):
            raise TypeError("updates.getState returned a non-updates.State result")
        async with self._state_lock:
            await self._ensure_loaded()
            self._set_cursor(
                self._current_cursor().with_state(
                    pts=result.pts, qts=result.qts, seq=result.seq, date=result.date
                )
            )
            await self._persist_cursor()
            return self._current_cursor()

    async def _drain_raw_updates(self) -> None:
        while True:
            raw_update = await self._raw_updates.get()
            await self.handle_raw_update(raw_update)

    async def _ensure_loaded(self) -> None:
        if self._cursor is not None:
            return
        payload = await self._storage.load()
        record = session_record_from_mapping(payload or {})
        self._cursor = UpdateCursor.from_record(
            record, duplicate_window=self._config.update_duplicate_window
        )
        self._duplicates = DuplicateTracker(
            self._cursor.duplicate_keys, max_size=self._config.update_duplicate_window
        )

    async def _persist_cursor(self) -> None:
        cursor = self._current_cursor().with_duplicate_keys(self._duplicates.keys())
        self._cursor = cursor
        payload = await self._storage.load()
        record = session_record_from_mapping(payload or {})
        updated = SessionRecord(
            dc_id=record.dc_id,
            auth_key=record.auth_key,
            dc_options=record.dc_options,
            user=record.user,
            update_state=cursor.to_update_state(),
            peers=merge_peer_cache_entries(record.peers, cursor.entities),
            metadata=metadata_with_duplicate_keys(record.metadata, cursor.duplicate_keys),
        )
        await self._storage.save(updated)

    async def _process_raw_update(self, raw_update: object) -> list[Update]:
        self._remember_entities(_extract_entity_references(raw_update))
        if isinstance(
            raw_update,
            types.UpdatesDifferenceEmpty
            | types.UpdatesDifference
            | types.UpdatesDifferenceSlice
            | types.UpdatesDifferenceTooLong,
        ):
            return self._apply_difference(raw_update)
        if isinstance(raw_update, types.UpdatesTooLong):
            return await self._recover_gap()
        events: list[Update] = []
        if self._sequence_gap(raw_update) or self._pts_gap(raw_update):
            events.extend(await self._recover_gap())
        for unit in _iter_update_units(raw_update):
            if self._pts_gap(unit.raw):
                events.extend(await self._recover_gap())
            events.extend(self._apply_update_unit(unit))
        self._apply_sequence(raw_update)
        self._remember_entities(_extract_entity_references(raw_update))
        return events

    async def _recover_gap(self) -> list[Update]:
        recovered: list[Update] = []
        for _ in range(_MAX_DIFFERENCE_ROUNDS):
            cursor = self._current_cursor()
            difference = await self._invoke(
                functions.UpdatesGetDifference(
                    pts=cursor.pts, date=int(cursor.date.timestamp()), qts=cursor.qts
                )
            )
            if not isinstance(
                difference,
                types.UpdatesDifferenceEmpty
                | types.UpdatesDifference
                | types.UpdatesDifferenceSlice
                | types.UpdatesDifferenceTooLong,
            ):
                raise TypeError("updates.getDifference returned a non-updates.Difference result")
            recovered.extend(self._apply_difference(difference))
            if not isinstance(difference, types.UpdatesDifferenceSlice):
                return _ordered_events(recovered)
        raise RuntimeError("updates.getDifference did not converge")

    def _apply_difference(self, difference: object) -> list[Update]:
        self._remember_entities(_extract_entity_references(difference))
        if isinstance(difference, types.UpdatesDifferenceEmpty):
            self._set_cursor(
                self._current_cursor().with_state(seq=difference.seq, date=difference.date)
            )
            return []
        if isinstance(difference, types.UpdatesDifferenceTooLong):
            self._set_cursor(self._current_cursor().with_state(pts=difference.pts))
            return []
        if isinstance(difference, types.UpdatesDifference | types.UpdatesDifferenceSlice):
            events: list[Update] = []
            for message in difference.new_messages:
                events.extend(self._apply_update_unit(RawUpdateUnit(raw=message)))
            for update in difference.other_updates:
                events.extend(self._apply_update_unit(RawUpdateUnit(raw=update)))
            state = (
                difference.intermediate_state
                if isinstance(difference, types.UpdatesDifferenceSlice)
                else difference.state
            )
            if isinstance(state, types.UpdatesState):
                self._set_cursor(
                    self._current_cursor().with_state(
                        pts=state.pts, qts=state.qts, seq=state.seq, date=state.date
                    )
                )
            return _ordered_events(events)
        return []

    def _apply_update_unit(self, unit: RawUpdateUnit) -> list[Update]:
        raw = unit.raw
        key = _raw_update_key(raw)
        cursor = self._current_cursor()
        pts = _optional_int_attr(raw, "pts")
        if pts is not None and pts <= cursor.pts:
            self._duplicates.add(key)
            return []
        if key in self._duplicates:
            return []
        events = _public_updates_from_raw(raw, unit.date)
        self._duplicates.add(key)
        qts = _optional_int_attr(raw, "qts")
        date = _raw_date(raw, unit.date)
        next_cursor = cursor
        if pts is not None and pts > next_cursor.pts:
            next_cursor = next_cursor.with_state(pts=pts, date=date)
        if qts is not None and qts > next_cursor.qts:
            next_cursor = next_cursor.with_state(qts=qts, date=date)
        self._set_cursor(next_cursor)
        self._remember_entities(_extract_entity_references(raw))
        return events

    def _pts_gap(self, raw_update: object) -> bool:
        cursor = self._current_cursor()
        expected_pts = cursor.pts
        for unit in _iter_update_units(raw_update):
            pts = _optional_int_attr(unit.raw, "pts")
            pts_count = _optional_int_attr(unit.raw, "pts_count")
            if pts is None or pts_count is None:
                continue
            if expected_pts == 0:
                expected_pts = max(expected_pts, pts)
                continue
            if pts > expected_pts + pts_count:
                return True
            if pts > expected_pts:
                expected_pts = pts
        return False

    def _sequence_gap(self, raw_update: object) -> bool:
        cursor = self._current_cursor()
        if cursor.seq == 0:
            return False
        seq = _optional_int_attr(raw_update, "seq")
        if seq is None:
            return False
        seq_start = _optional_int_attr(raw_update, "seq_start") or seq
        return seq_start > cursor.seq + 1

    def _apply_sequence(self, raw_update: object) -> None:
        seq = _optional_int_attr(raw_update, "seq")
        if seq is None:
            return
        cursor = self._current_cursor()
        if seq > cursor.seq:
            self._set_cursor(cursor.with_state(seq=seq, date=_raw_date(raw_update, None)))

    def _remember_entities(self, entities: Iterable[EntityReference]) -> None:
        collected = tuple(entities)
        if not collected:
            return
        self._set_cursor(self._current_cursor().with_entities(collected))

    def _offer_queue(self, queue: asyncio.Queue[Any], item: Any) -> bool:
        try:
            queue.put_nowait(item)
            return True
        except asyncio.QueueFull:
            policy = self._config.update_queue_overflow
            if policy == "drop_newest":
                return False
            if policy == "drop_oldest":
                with suppress(asyncio.QueueEmpty):
                    queue.get_nowait()
                queue.put_nowait(item)
                return True
            raise

    async def _dispatch_handlers(self, update: Update) -> None:
        for update_type, handlers in self._handlers.items():
            if isinstance(update, update_type):
                for handler in handlers:
                    result = handler(update)
                    if result is not None:
                        await result

    def _current_cursor(self) -> UpdateCursor:
        if self._cursor is None:
            raise RuntimeError("update state has not been loaded")
        return self._cursor

    def _set_cursor(self, cursor: UpdateCursor) -> None:
        self._cursor = cursor.with_duplicate_keys(self._duplicates.keys())


def _iter_update_units(raw_update: object) -> tuple[RawUpdateUnit, ...]:
    if isinstance(raw_update, types.UpdateShort):
        return (RawUpdateUnit(raw=raw_update.update, date=raw_update.date),)
    if isinstance(raw_update, types.Updates | types.UpdatesCombined):
        return tuple(
            RawUpdateUnit(raw=update, date=raw_update.date) for update in raw_update.updates
        )
    if isinstance(
        raw_update,
        types.UpdateShortMessage | types.UpdateShortChatMessage | types.UpdateShortSentMessage,
    ):
        return (RawUpdateUnit(raw=raw_update, date=raw_update.date),)
    return (RawUpdateUnit(raw=raw_update),)


def _public_updates_from_raw(raw: object, fallback_date: object | None = None) -> list[Update]:
    date = _raw_date(raw, fallback_date)
    if isinstance(raw, types.UpdateShortMessage):
        peer = Peer(id=raw.user_id, kind="user")
        message = Message(id=raw.id, peer=peer, text=raw.message, date=date, raw=raw)
        return [NewMessage(date=date, raw=raw, message=message, metadata=_metadata(raw))]
    if isinstance(raw, types.UpdateShortChatMessage):
        peer = Peer(id=raw.chat_id, kind="chat")
        message = Message(id=raw.id, peer=peer, text=raw.message, date=date, raw=raw)
        return [
            NewMessage(
                date=date, raw=raw, message=message, metadata=_metadata(raw, from_id=raw.from_id)
            )
        ]
    if isinstance(raw, types.UpdateNewMessage | types.UpdateNewChannelMessage):
        return _public_updates_from_message(raw.message, raw)
    if isinstance(raw, types.Message):
        return _public_updates_from_message(raw, raw)
    return [Update(date=date, raw=raw)]


def _public_updates_from_message(raw_message: object, raw_update: object) -> list[Update]:
    if not isinstance(raw_message, types.Message):
        return [Update(date=_raw_date(raw_update, None), raw=raw_update)]
    date = _raw_date(raw_message, None)
    peer = _peer_from_raw_peer(raw_message.peer_id)
    message = Message(
        id=raw_message.id,
        peer=peer,
        text=raw_message.message,
        date=date,
        media=raw_message.media,
        raw=raw_message,
    )
    return [NewMessage(date=date, raw=raw_update, message=message, metadata=_metadata(raw_update))]


def _peer_from_raw_peer(raw_peer: object) -> Peer:
    if isinstance(raw_peer, types.PeerUser):
        return Peer(id=raw_peer.user_id, kind="user")
    if isinstance(raw_peer, types.PeerChat):
        return Peer(id=raw_peer.chat_id, kind="chat")
    if isinstance(raw_peer, types.PeerChannel):
        return Peer(id=raw_peer.channel_id, kind="channel")
    return Peer(id=0, kind="self")


def _extract_entity_references(raw: object) -> tuple[EntityReference, ...]:
    entities: list[EntityReference] = []
    for user in _iter_attr_tuple(raw, "users"):
        if isinstance(user, types.User):
            entities.append(
                EntityReference(
                    id=user.id,
                    kind="user",
                    access_hash=user.access_hash,
                    username=user.username,
                    phone=user.phone,
                    title=" ".join(part for part in (user.first_name, user.last_name) if part)
                    or None,
                )
            )
    for chat in _iter_attr_tuple(raw, "chats"):
        if isinstance(chat, types.Chat):
            entities.append(EntityReference(id=chat.id, kind="chat", title=chat.title))
        elif isinstance(chat, types.Channel):
            entities.append(
                EntityReference(
                    id=chat.id,
                    kind="channel",
                    access_hash=chat.access_hash,
                    username=chat.username,
                    title=chat.title,
                )
            )
    if isinstance(raw, types.UpdatesDifference | types.UpdatesDifferenceSlice):
        for update in raw.other_updates:
            entities.extend(_extract_entity_references(update))
    if isinstance(raw, types.Updates | types.UpdatesCombined):
        for update in raw.updates:
            entities.extend(_extract_entity_references(update))
    return tuple(entities)


def _iter_attr_tuple(raw: object, attr: str) -> tuple[object, ...]:
    value = getattr(raw, attr, ())
    if isinstance(value, tuple):
        return cast("tuple[object, ...]", value)
    if isinstance(value, list):
        return tuple(value)
    return ()


def _raw_date(raw: object, fallback: object | None) -> Any:
    value = getattr(raw, "date", fallback)
    return coerce_update_datetime(cast("Any", value))


def _metadata(raw: object, **extra: object) -> dict[str, object]:
    values: dict[str, object] = {"raw_type": type(raw).__name__}
    values.update(extra)
    return values


def _ordered_events(events: Iterable[Update]) -> list[Update]:
    return [
        event for _, event in sorted(enumerate(events), key=lambda item: (item[1].date, item[0]))
    ]


def _raw_update_key(raw: object) -> str:
    parts = [type(raw).__name__]
    for attr in ("pts", "qts", "seq", "date", "id"):
        value = getattr(raw, attr, None)
        if isinstance(value, int | str):
            parts.append(f"{attr}:{value}")
    nested_message = getattr(raw, "message", None)
    if not isinstance(nested_message, str):
        nested_id = getattr(nested_message, "id", None)
        if isinstance(nested_id, int):
            parts.append(f"message:{nested_id}")
    return "|".join(parts)


def _optional_int_attr(raw: object, attr: str) -> int | None:
    value = getattr(raw, attr, None)
    if value is None:
        return None
    return int(value)

"""Asynchronous update ingestion with persistent cursors, duplicate filtering, and bounded gap recovery."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Literal, TypeVar, cast, overload

from miniproto.config import ClientConfig
from miniproto.observability import emit_event, get_logger, record_metric
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
_MAX_CHANNEL_DIFFERENCE_ROUNDS = 10
POSSIBLE_GAP_GRACE_SECONDS = 0.5
_LOGGER = get_logger("updates")


@dataclass(frozen=True, slots=True)
class RawUpdateUnit:
    """One raw update paired with an optional enclosing-container timestamp.

    Attributes:
        raw: Decoded Telegram update, message, or envelope payload.
        date: Optional date inherited from an enclosing update container.
    """

    raw: object
    date: object | None = None


class UpdateManager:
    """Process Telegram updates into public events while persisting recovery state.

    Args:
        config: Client configuration defining queue capacities, overflow policy, and duplicate-window size.
        storage: Session storage used to load and atomically persist update cursors and discovered entities.
        invoke: Async raw-RPC invoker used for ``updates.getState`` and difference recovery.

    Lifecycle:
        ``start`` restores state and launches a raw-update drainer. ``stop`` cancels that drainer but does not close or sentinel the public queue; consumers of ``iter_updates`` remain blocked until cancellation or a future event.

    Persistence:
        Raw update processing holds a state lock, applies cursor/entity/duplicate changes, and persists them before emitted public events are queued and handlers are called. Persisted state is therefore ahead of, or equal to, observable delivery; it does not provide application-level exactly-once handling.
    """

    def __init__(self, config: ClientConfig, storage: SessionStorage, invoke: UpdateInvoker) -> None:
        """Initialize bounded raw/public queues and uninitialized persistent cursor state.

        Args:
            config: Client queue capacities, overflow policy, and duplicate-window settings.
            storage: Session storage used to load and atomically persist cursor state.
            invoke: Async raw-RPC callable used for state and difference recovery.
        """
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
        """Return the mutable mapping of registered update types to handlers."""
        return self._handlers

    async def start(self) -> None:
        """Restore persistent state and start draining queued raw updates.

        Repeated calls retain the existing drainer when it is still running. A failed load propagates and no new drainer is started.
        """
        started = time.perf_counter()
        await self._ensure_loaded()
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._drain_raw_updates())
        _emit_update_event(
            "updates.start",
            started,
            outcome="success",
            queue_size=self._config.update_queue_size,
            overflow=self._config.update_queue_overflow,
        )

    async def stop(self) -> None:
        """Cancel and await the raw-update drainer without closing either queue.

        Cancellation while a raw item is being processed can interrupt that processing. If an already-completed drainer failed, this method re-raises its exception.

        Raises:
            Exception: The completed drainer's exception, if any.
        """
        started = time.perf_counter()
        task = self._task
        self._task = None
        if task is None:
            _emit_update_event("updates.stop", started, outcome="success", had_task=False)
            return
        if task.done():
            exc = task.exception()
            if exc is not None:
                _emit_update_event(
                    "updates.stop", started, outcome="error", error_type=type(exc).__name__, had_task=True
                )
                raise exc
            _emit_update_event("updates.stop", started, outcome="success", had_task=True)
            return
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        _emit_update_event("updates.stop", started, outcome="success", had_task=True)

    async def feed_raw_update(self, raw_update: object) -> None:
        """Offer a raw Telegram update to the bounded background-processing queue.

        Queue-full behavior is controlled by ``ClientConfig.update_queue_overflow``: ``"raise"`` propagates ``asyncio.QueueFull``, ``"drop_newest"`` discards this update, and ``"drop_oldest"`` replaces the oldest queued update.

        Args:
            raw_update: Decoded Telegram update or update-container object to enqueue.
        """
        if not self._offer_queue(self._raw_updates, raw_update):
            return

    async def handle_raw_update(self, raw_update: object) -> None:
        """Process one raw update synchronously, persist resulting state, then emit its public events.

        Gap recovery and cursor mutation are serialized under the manager's state lock. Recovered events are date-ordered within a difference response; callers should not infer global ordering guarantees across independent input calls.

        Args:
            raw_update: Decoded Telegram update or update-container object to process.

        Raises:
            Exception: Propagates storage, RPC, gap-recovery, queue, and handler failures.
        """
        started = time.perf_counter()
        async with self._state_lock:
            await self._ensure_loaded()
            events = await self._process_raw_update(raw_update)
            await self._persist_cursor()
        for event in events:
            await self.emit_update(event)
        _emit_update_event(
            "updates.handle_raw", started, outcome="success", raw_type=type(raw_update).__name__, emitted=len(events)
        )

    async def emit_update(self, update: Update) -> None:
        """Offer a normalized update to consumers, then invoke matching handlers sequentially.

        If the public queue rejects the item under a dropping overflow policy, handlers are not invoked. Matching registered types are visited in registration-mapping order, and each handler is awaited before the next one when it returns an awaitable.

        Args:
            update: Normalized public update to queue and dispatch.

        Raises:
            asyncio.QueueFull: If the public queue is full and policy is ``"raise"``.
            Exception: Propagates a matching handler failure.
        """
        if not self._offer_queue(self._updates, update):
            record_metric(
                "updates.queue_dropped", 1, attributes={"queue": "public", "policy": self._config.update_queue_overflow}
            )
            return
        await self._dispatch_handlers(update)

    async def iter_updates(self) -> AsyncIterator[Update]:
        """Yield normalized public updates from the FIFO queue until the consumer is cancelled.

        Yields:
            Updates accepted by the public queue. Dropped updates and items never processed due to drainer cancellation are not yielded.

        Cancellation:
            Stopping the manager does not end this iterator or wake a waiting consumer.
        """
        while True:
            yield await self._updates.get()

    @overload
    def on(self, update_type: type[UpdateT]) -> Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]:
        """Return a decorator that registers a handler for ``update_type``.

        Args:
            update_type: Normalized update subclass the decorator's handler receives.
        """
        ...

    @overload
    def on(self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT]) -> UpdateHandler[UpdateT]:
        """Register and return ``handler`` for ``update_type``.

        Args:
            update_type: Normalized update subclass matched with ``isinstance``.
            handler: Synchronous or asynchronous callback to register.
        """
        ...

    def on(
        self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT] | None = None
    ) -> UpdateHandler[UpdateT] | Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]:
        """Register a handler directly or return a decorator for one update subtype.

        Args:
            update_type: Normalized update subclass to match with ``isinstance``.
            handler: Optional synchronous or asynchronous callback.

        Returns:
            The registered handler, or a decorator that registers a supplied handler.
        """

        def register(candidate: UpdateHandler[UpdateT]) -> UpdateHandler[UpdateT]:
            """Append ``candidate`` while preserving handler registration order.

            Args:
                candidate: Synchronous or asynchronous handler to append.
            """
            self._handlers.setdefault(update_type, []).append(candidate)
            return candidate

        if handler is None:
            return register
        return register(handler)

    async def sync_state(self) -> UpdateCursor:
        """Fetch Telegram's current global update state and persist it atomically.

        Returns:
            The loaded cursor after replacing its global PTS, QTS, sequence, and date fields.

        Raises:
            TypeError: If ``updates.getState`` does not return ``updates.State``.
            Exception: Propagates RPC and session-storage failures.
        """
        result = await self._invoke(functions.UpdatesGetState())
        if not isinstance(result, types.UpdatesState):
            raise TypeError("updates.getState returned a non-updates.State result")
        async with self._state_lock:
            await self._ensure_loaded()
            self._set_cursor(
                self._current_cursor().with_state(pts=result.pts, qts=result.qts, seq=result.seq, date=result.date)
            )
            await self._persist_cursor()
            return self._current_cursor()

    async def _drain_raw_updates(self) -> None:
        """Continuously process raw queue entries until the task is cancelled or fails."""
        while True:
            raw_update = await self._raw_updates.get()
            await self.handle_raw_update(raw_update)

    async def _ensure_loaded(self) -> None:
        """Load cursor, cached entities, and bounded duplicate keys from session storage once."""
        if self._cursor is not None:
            return
        payload = await self._storage.load()
        record = session_record_from_mapping(payload or {})
        self._cursor = UpdateCursor.from_record(record, duplicate_window=self._config.update_duplicate_window)
        self._duplicates = DuplicateTracker(self._cursor.duplicate_keys, max_size=self._config.update_duplicate_window)

    async def _persist_cursor(self) -> None:
        """Atomically persist the current cursor, duplicate window, and merged peer entities."""
        cursor = self._current_cursor().with_duplicate_keys(self._duplicates.keys())
        self._cursor = cursor

        def persist(payload):
            """Rebuild the session record with the manager's current persisted update state.

            Args:
                payload: Latest stored session mapping supplied by ``storage.mutate``.
            """
            record = session_record_from_mapping(payload or {})
            return SessionRecord(
                dc_id=record.dc_id,
                auth_key=record.auth_key,
                dc_options=record.dc_options,
                user=record.user,
                update_state=cursor.to_update_state(),
                peers=merge_peer_cache_entries(record.peers, cursor.entities),
                metadata=metadata_with_duplicate_keys(record.metadata, cursor.duplicate_keys, cursor.channel_cursors),
            )

        await self._storage.mutate(persist)

    async def _process_raw_update(self, raw_update: object) -> list[Update]:
        """Detect gaps, recover when needed, apply units, and return normalized events.

        Args:
            raw_update: Decoded Telegram update or container to inspect and apply.
        """
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
        channel_gaps = self._channel_pts_gaps(raw_update)
        if self._sequence_gap(raw_update) or self._pts_gap(raw_update):
            events.extend(await self._recover_gap())
        for channel_id in channel_gaps:
            events.extend(await self._recover_channel_gap(channel_id))
        for unit in _iter_update_units(raw_update):
            unit_channel_gaps = self._channel_pts_gaps(unit.raw)
            if unit_channel_gaps:
                for channel_id in unit_channel_gaps:
                    events.extend(await self._recover_channel_gap(channel_id))
            elif self._pts_gap(unit.raw):
                events.extend(await self._recover_gap())
            events.extend(self._apply_update_unit(unit))
        self._apply_sequence(raw_update)
        self._remember_entities(_extract_entity_references(raw_update))
        return events

    async def _recover_gap(self) -> list[Update]:
        """Recover a global PTS/sequence gap through at most ten difference RPC rounds.

        Returns:
            Recovered events ordered by timestamp while preserving ties' original order.

        Raises:
            TypeError: If Telegram returns an unexpected difference type.
            RuntimeError: If ten ``updates.getDifference`` rounds do not converge.
        """
        started = time.perf_counter()
        record_metric("updates.gaps", 1)
        recovered: list[Update] = []
        for _ in range(_MAX_DIFFERENCE_ROUNDS):
            cursor = self._current_cursor()
            difference = await self._invoke(
                functions.UpdatesGetDifference(pts=cursor.pts, date=int(cursor.date.timestamp()), qts=cursor.qts)
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
                events = _ordered_events(recovered)
                _emit_update_event("updates.recover_gap", started, outcome="success", rounds=_ + 1, emitted=len(events))
                return events
        _emit_update_event("updates.recover_gap", started, outcome="error", error_type="NoConvergence")
        raise RuntimeError("updates.getDifference did not converge")

    async def _recover_channel_gap(self, channel_id: int) -> list[Update]:
        """Recover one channel PTS gap when a cached access hash permits the RPC.

        The method waits the configured possible-gap grace interval before polling and returns no events when the channel access hash is unavailable. Recovery stops after ten non-final rounds.

        Args:
            channel_id: Telegram channel identifier whose PTS gap is recovered.

        Raises:
            TypeError: If Telegram returns an unexpected channel-difference type.
            RuntimeError: If ten channel-difference rounds do not converge.
        """
        started = time.perf_counter()
        input_channel = self._input_channel_for_channel(channel_id)
        if input_channel is None:
            _emit_update_event(
                "updates.recover_channel_gap",
                started,
                outcome="error",
                error_type="MissingChannelAccessHash",
                channel_id=channel_id,
            )
            return []
        if POSSIBLE_GAP_GRACE_SECONDS > 0:
            await asyncio.sleep(POSSIBLE_GAP_GRACE_SECONDS)
        record_metric("updates.channel_gaps", 1)
        recovered: list[Update] = []
        for round_index in range(_MAX_CHANNEL_DIFFERENCE_ROUNDS):
            cursor = self._current_cursor().channel_cursor(channel_id)
            difference = await self._invoke(
                functions.UpdatesGetChannelDifference(
                    channel=input_channel, filter=types.ChannelMessagesFilterEmpty(), pts=cursor.pts, limit=100
                )
            )
            if not isinstance(
                difference,
                types.UpdatesChannelDifferenceEmpty
                | types.UpdatesChannelDifference
                | types.UpdatesChannelDifferenceTooLong,
            ):
                raise TypeError("updates.getChannelDifference returned a non-channel difference result")
            recovered.extend(self._apply_channel_difference(channel_id, difference))
            if getattr(difference, "final", True):
                events = _ordered_events(recovered)
                _emit_update_event(
                    "updates.recover_channel_gap",
                    started,
                    outcome="success",
                    channel_id=channel_id,
                    rounds=round_index + 1,
                    emitted=len(events),
                )
                return events
        _emit_update_event(
            "updates.recover_channel_gap", started, outcome="error", error_type="NoConvergence", channel_id=channel_id
        )
        raise RuntimeError("updates.getChannelDifference did not converge")

    def _apply_difference(self, difference: object) -> list[Update]:
        """Apply a global difference response and update cursor/entity state.

        Args:
            difference: Decoded result of ``updates.getDifference``.
        """
        self._remember_entities(_extract_entity_references(difference))
        if isinstance(difference, types.UpdatesDifferenceEmpty):
            self._set_cursor(self._current_cursor().with_state(seq=difference.seq, date=difference.date))
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
                    self._current_cursor().with_state(pts=state.pts, qts=state.qts, seq=state.seq, date=state.date)
                )
            return _ordered_events(events)
        return []

    def _apply_channel_difference(self, channel_id: int, difference: object) -> list[Update]:
        """Apply one channel difference response and update that channel's cursor.

        Args:
            channel_id: Channel whose cursor is updated.
            difference: Decoded result of ``updates.getChannelDifference``.
        """
        self._remember_entities(_extract_entity_references(difference))
        if isinstance(difference, types.UpdatesChannelDifferenceEmpty):
            self._set_cursor(self._current_cursor().with_channel_state(channel_id, pts=difference.pts))
            return []
        if isinstance(difference, types.UpdatesChannelDifference):
            events: list[Update] = []
            for message in difference.new_messages:
                events.extend(self._apply_update_unit(RawUpdateUnit(raw=message)))
            for update in difference.other_updates:
                events.extend(self._apply_update_unit(RawUpdateUnit(raw=update)))
            self._set_cursor(self._current_cursor().with_channel_state(channel_id, pts=difference.pts))
            return _ordered_events(events)
        if isinstance(difference, types.UpdatesChannelDifferenceTooLong):
            events = [
                event
                for message in difference.messages
                for event in self._apply_update_unit(RawUpdateUnit(raw=message))
            ]
            return _ordered_events(events)
        return []

    def _apply_update_unit(self, unit: RawUpdateUnit) -> list[Update]:
        """Drop duplicate/stale units or convert a new unit while advancing cursor state.

        Args:
            unit: Raw update paired with any enclosing-container timestamp.
        """
        raw = unit.raw
        key = _raw_update_key(raw)
        cursor = self._current_cursor()
        pts = _optional_int_attr(raw, "pts")
        channel_id = _channel_id_from_update(raw)
        comparison_pts = cursor.channel_cursor(channel_id).pts if channel_id is not None else cursor.pts
        if pts is not None and pts <= comparison_pts:
            self._duplicates.add(key)
            return []
        if key in self._duplicates:
            return []
        events = _public_updates_from_raw(raw, unit.date)
        self._duplicates.add(key)
        qts = _optional_int_attr(raw, "qts")
        date = _raw_date(raw, unit.date)
        next_cursor = cursor
        if pts is not None and channel_id is not None and pts > comparison_pts:
            next_cursor = next_cursor.with_channel_state(channel_id, pts=pts, date=date)
        elif pts is not None and pts > next_cursor.pts:
            next_cursor = next_cursor.with_state(pts=pts, date=date)
        if qts is not None and qts > next_cursor.qts:
            next_cursor = next_cursor.with_state(qts=qts, date=date)
        self._set_cursor(next_cursor)
        self._remember_entities(_extract_entity_references(raw))
        return events

    def _pts_gap(self, raw_update: object) -> bool:
        """Return whether non-channel update units skip beyond the expected global PTS.

        Args:
            raw_update: Raw update or container whose non-channel PTS values are inspected.
        """
        cursor = self._current_cursor()
        expected_pts = cursor.pts
        for unit in _iter_update_units(raw_update):
            if _channel_id_from_update(unit.raw) is not None:
                continue
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

    def _channel_pts_gaps(self, raw_update: object) -> tuple[int, ...]:
        """Return unique channel IDs whose update units skip their expected PTS.

        Args:
            raw_update: Raw update or container whose channel PTS values are inspected.
        """
        gaps: list[int] = []
        expected_by_channel: dict[int, int] = {}
        for unit in _iter_update_units(raw_update):
            channel_id = _channel_id_from_update(unit.raw)
            if channel_id is None:
                continue
            pts = _optional_int_attr(unit.raw, "pts")
            pts_count = _optional_int_attr(unit.raw, "pts_count")
            if pts is None or pts_count is None:
                continue
            expected_pts = expected_by_channel.get(channel_id, self._current_cursor().channel_cursor(channel_id).pts)
            if expected_pts == 0:
                expected_by_channel[channel_id] = max(expected_pts, pts)
                continue
            if pts > expected_pts + pts_count:
                gaps.append(channel_id)
            if pts > expected_pts:
                expected_by_channel[channel_id] = pts
        return tuple(dict.fromkeys(gaps))

    def _sequence_gap(self, raw_update: object) -> bool:
        """Return whether a container sequence starts after the current global sequence.

        Args:
            raw_update: Raw update container whose sequence fields are inspected.
        """
        cursor = self._current_cursor()
        if cursor.seq == 0:
            return False
        seq = _optional_int_attr(raw_update, "seq")
        if seq is None:
            return False
        seq_start = _optional_int_attr(raw_update, "seq_start") or seq
        return seq_start > cursor.seq + 1

    def _apply_sequence(self, raw_update: object) -> None:
        """Advance global sequence state when the raw container carries a newer value.

        Args:
            raw_update: Raw update container supplying optional sequence/date fields.
        """
        seq = _optional_int_attr(raw_update, "seq")
        if seq is None:
            return
        cursor = self._current_cursor()
        if seq > cursor.seq:
            self._set_cursor(cursor.with_state(seq=seq, date=_raw_date(raw_update, None)))

    def _remember_entities(self, entities: Iterable[EntityReference]) -> None:
        """Merge observed entities into cursor state when the iterable is nonempty.

        Args:
            entities: Entity references extracted from raw update data.
        """
        collected = tuple(entities)
        if not collected:
            return
        self._set_cursor(self._current_cursor().with_entities(collected))

    def _offer_queue(self, queue: asyncio.Queue[Any], item: Any) -> bool:
        """Put an item according to the configured bounded-queue overflow policy.

        Returns:
            ``True`` when the queue accepted the item and ``False`` for ``drop_newest``.

        Raises:
            asyncio.QueueFull: If the queue is full and policy is ``"raise"``.

        Args:
            queue: Raw or public bounded queue receiving the item.
            item: Update object to enqueue under the configured overflow policy.
        """
        try:
            queue.put_nowait(item)
            record_metric("updates.queue_depth", queue.qsize(), attributes={"max_size": queue.maxsize})
            return True
        except asyncio.QueueFull:
            policy = self._config.update_queue_overflow
            if policy == "drop_newest":
                record_metric(
                    "updates.queue_dropped", 1, attributes={"policy": policy, "item_type": type(item).__name__}
                )
                return False
            if policy == "drop_oldest":
                with suppress(asyncio.QueueEmpty):
                    queue.get_nowait()
                queue.put_nowait(item)
                record_metric(
                    "updates.queue_dropped", 1, attributes={"policy": policy, "item_type": type(item).__name__}
                )
                return True
            raise

    async def _dispatch_handlers(self, update: Update) -> None:
        """Run every matching registered handler sequentially, awaiting awaitable results.

        Args:
            update: Public update passed to handlers whose registered type matches it.
        """
        for update_type, handlers in self._handlers.items():
            if isinstance(update, update_type):
                for handler in handlers:
                    result = handler(update)
                    if result is not None:
                        await result

    def _current_cursor(self) -> UpdateCursor:
        """Return loaded cursor state or fail when a caller bypasses initialization.

        Raises:
            RuntimeError: If state has not been loaded from session storage.
        """
        if self._cursor is None:
            raise RuntimeError("update state has not been loaded")
        return self._cursor

    def _set_cursor(self, cursor: UpdateCursor) -> None:
        """Set cursor state after replacing its persisted duplicate keys from the tracker.

        Args:
            cursor: Replacement cursor state before duplicate keys are synchronized.
        """
        self._cursor = cursor.with_duplicate_keys(self._duplicates.keys())

    def _input_channel_for_channel(self, channel_id: int) -> object | None:
        """Build an input channel from retained entity data, or return ``None`` without an access hash.

        Args:
            channel_id: Telegram channel identifier to convert for recovery RPCs.
        """
        for entity in self._current_cursor().entities:
            if entity.kind == "channel" and entity.id == channel_id and entity.access_hash is not None:
                return types.InputChannel(channel_id=channel_id, access_hash=entity.access_hash)
        return None


def _iter_update_units(raw_update: object) -> tuple[RawUpdateUnit, ...]:
    """Expand short and container update envelopes into timestamp-associated units.

    Args:
        raw_update: Decoded Telegram update or envelope to expand.
    """
    if isinstance(raw_update, types.UpdateShort):
        return (RawUpdateUnit(raw=raw_update.update, date=raw_update.date),)
    if isinstance(raw_update, types.Updates | types.UpdatesCombined):
        return tuple(RawUpdateUnit(raw=update, date=raw_update.date) for update in raw_update.updates)
    if isinstance(raw_update, types.UpdateShortMessage | types.UpdateShortChatMessage | types.UpdateShortSentMessage):
        return (RawUpdateUnit(raw=raw_update, date=raw_update.date),)
    return (RawUpdateUnit(raw=raw_update),)


def _public_updates_from_raw(raw: object, fallback_date: object | None = None) -> list[Update]:
    """Convert supported raw updates to normalized public updates, preserving raw payloads.

    Args:
        raw: Decoded Telegram update/message to convert.
        fallback_date: Enclosing timestamp used when ``raw`` carries no date.
    """
    date = _raw_date(raw, fallback_date)
    if isinstance(raw, types.UpdateShortMessage):
        peer = Peer(id=raw.user_id, kind="user")
        message = Message(id=raw.id, peer=peer, text=raw.message, date=date, raw=raw)
        return [NewMessage(date=date, raw=raw, message=message, metadata=_metadata(raw))]
    if isinstance(raw, types.UpdateShortChatMessage):
        peer = Peer(id=raw.chat_id, kind="chat")
        message = Message(id=raw.id, peer=peer, text=raw.message, date=date, raw=raw)
        return [NewMessage(date=date, raw=raw, message=message, metadata=_metadata(raw, from_id=raw.from_id))]
    if isinstance(raw, types.UpdateNewMessage | types.UpdateNewChannelMessage):
        return _public_updates_from_message(raw.message, raw)
    if isinstance(raw, types.Message):
        return _public_updates_from_message(raw, raw)
    return [Update(date=date, raw=raw)]


def _public_updates_from_message(raw_message: object, raw_update: object) -> list[Update]:
    """Convert a raw message to ``NewMessage`` or retain an opaque update fallback.

    Args:
        raw_message: Candidate decoded Telegram message.
        raw_update: Outer raw update retained by the public event.
    """
    if not isinstance(raw_message, types.Message):
        return [Update(date=_raw_date(raw_update, None), raw=raw_update)]
    date = _raw_date(raw_message, None)
    peer = _peer_from_raw_peer(raw_message.peer_id)
    message = Message(
        id=raw_message.id, peer=peer, text=raw_message.message, date=date, media=raw_message.media, raw=raw_message
    )
    return [NewMessage(date=date, raw=raw_update, message=message, metadata=_metadata(raw_update))]


def _peer_from_raw_peer(raw_peer: object) -> Peer:
    """Normalize a raw peer variant, falling back to a self peer for unknown shapes.

    Args:
        raw_peer: Decoded raw peer variant from a Telegram message.
    """
    if isinstance(raw_peer, types.PeerUser):
        return Peer(id=raw_peer.user_id, kind="user")
    if isinstance(raw_peer, types.PeerChat):
        return Peer(id=raw_peer.chat_id, kind="chat")
    if isinstance(raw_peer, types.PeerChannel):
        return Peer(id=raw_peer.channel_id, kind="channel")
    return Peer(id=0, kind="self")


def _channel_id_from_update(raw: object) -> int | None:
    """Extract a channel ID from direct update data or a nested message peer.

    Args:
        raw: Raw update or message whose channel fields are inspected.
    """
    direct_channel_id = getattr(raw, "channel_id", None)
    if isinstance(direct_channel_id, int):
        return direct_channel_id
    raw_message = getattr(raw, "message", raw)
    peer_id = getattr(raw_message, "peer_id", None)
    if isinstance(peer_id, types.PeerChannel):
        return peer_id.channel_id
    return None


def _extract_entity_references(raw: object) -> tuple[EntityReference, ...]:
    """Collect users and chats carried by raw update/difference containers recursively.

    Args:
        raw: Raw update or difference container carrying users/chats and nested updates.
    """
    entities: list[EntityReference] = []
    for user in _iter_attr_tuple(raw, "users"):
        if isinstance(user, types.User):
            entities.append(
                EntityReference(
                    id=user.id,
                    kind="user",
                    access_hash=None if user.min else user.access_hash,
                    username=user.username,
                    phone=user.phone,
                    title=" ".join(part for part in (user.first_name, user.last_name) if part) or None,
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
                    access_hash=None if chat.min else chat.access_hash,
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
    """Return a tuple view of a raw object's list or tuple attribute.

    Args:
        raw: Object carrying the optional collection attribute.
        attr: Attribute name expected to hold a list or tuple.
    """
    value = getattr(raw, attr, ())
    if isinstance(value, tuple):
        return cast("tuple[object, ...]", value)
    if isinstance(value, list):
        return tuple(value)
    return ()


def _raw_date(raw: object, fallback: object | None) -> Any:
    """Extract and coerce a raw object's date, using ``fallback`` when absent.

    Args:
        raw: Raw object whose optional ``date`` attribute is read.
        fallback: Date-like value used when the raw object omits ``date``.
    """
    value = getattr(raw, "date", fallback)
    return coerce_update_datetime(cast("Any", value))


def _metadata(raw: object, **extra: object) -> dict[str, object]:
    """Build public update metadata with raw type plus caller-supplied fields.

    Args:
        raw: Raw Telegram object whose type name is recorded.
        **extra: Additional metadata fields to merge after the raw type.
    """
    values: dict[str, object] = {"raw_type": type(raw).__name__}
    values.update(extra)
    return values


def _ordered_events(events: Iterable[Update]) -> list[Update]:
    """Sort events by timestamp while preserving input order for equal timestamps.

    Args:
        events: Public updates to order by their datetime values.
    """
    return [event for _, event in sorted(enumerate(events), key=lambda item: (item[1].date, item[0]))]


def _raw_update_key(raw: object) -> str:
    """Build a best-effort duplicate key from raw type and selected identity fields.

    Args:
        raw: Raw Telegram update/message from which identity attributes are read.
    """
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
    """Return an attribute coerced to ``int``, or ``None`` when it is absent.

    Args:
        raw: Object carrying the optional scalar attribute.
        attr: Attribute name to read and coerce.
    """
    value = getattr(raw, attr, None)
    if value is None:
        return None
    return int(value)


def _emit_update_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    """Emit structured update timing telemetry and an outcome-dependent log event.

    Args:
        event: Stable update event name used for telemetry.
        started: Monotonic start timestamp used to calculate milliseconds elapsed.
        outcome: Operation outcome used for log severity and metric attributes.
        **fields: Additional non-secret structured telemetry fields.
    """
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.DEBUG,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        **fields,
    )

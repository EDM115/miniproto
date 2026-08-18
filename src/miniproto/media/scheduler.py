"""Coordinate fair, byte-bounded media transfers per data centre and direction."""

from __future__ import annotations

import asyncio
import itertools
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from miniproto.observability import record_metric

type MediaDirection = Literal["download", "upload"]
type MediaPriority = Literal["foreground", "background"]
type MediaSizeClass = Literal["small", "large"]

MEDIA_SCHEDULER_UNIT = 64 * 1024
MEDIA_LARGE_FILE_THRESHOLD = 20 * 1024 * 1024
DEFAULT_DOWNLOAD_SMALL_LIMIT = 5
DEFAULT_DOWNLOAD_LARGE_LIMIT = 2
_BACKGROUND_GRANT_INTERVAL = 8


@dataclass(frozen=True, slots=True)
class MediaSchedulerSnapshot:
    """Immutable byte and operation measurements for one DC/direction scheduler.

    Attributes:
        max_bytes: Per-data-centre and direction byte ceiling in bytes.
        active_bytes: Charged bytes reserved by unreleased permits.
        queued_bytes: Charged bytes waiting for a permit.
        active_transfers: Transfers with at least one live permit.
        queued_transfers: Transfers with at least one queued acquire.
        grants: Total permits granted by this scheduler since creation.
        grants_by_transfer: Copy of total grants keyed by transfer identifier.
    """

    max_bytes: int
    active_bytes: int
    queued_bytes: int
    active_transfers: int
    queued_transfers: int
    grants: int
    grants_by_transfer: dict[str, int]


@dataclass(slots=True)
class _Waiter:
    """A queued charged-byte request and the future that receives its permit.

    Attributes:
        charged_bytes: 64 KiB-rounded reservation size in bytes.
        priority: Scheduling priority for this individual acquire.
        queued_at: Monotonic enqueue timestamp used for wait metrics.
        future: Future completed with the resulting permit or cancelled on close.
        scheduler: Scheduler that currently owns this queued request.
        state: Transfer state that currently contains this queued request.
    """

    charged_bytes: int
    priority: MediaPriority
    queued_at: float
    future: asyncio.Future[MediaPermit]
    scheduler: _MediaScheduler
    state: _TransferState


@dataclass(slots=True)
class _TransferState:
    """Private deficit-round-robin state for a single logical transfer.

    Attributes:
        transfer_id: Registry-generated identifier used for fairness metrics.
        size_class: Small or large operation-cap class.
        priority: Default request priority for this transfer.
        pending: FIFO acquire waiters not yet granted.
        active_permits: Number of unreleased permits.
        deficit_bytes: Accumulated 64 KiB scheduling quantum credit.
        closing: Whether new acquires are rejected and pending work is draining.
    """

    transfer_id: str
    size_class: MediaSizeClass
    priority: MediaPriority
    pending: deque[_Waiter] = field(default_factory=deque)
    active_permits: int = 0
    deficit_bytes: int = 0
    closing: bool = False


class MediaPermit:
    """A charged scheduler reservation that must eventually be released.

    Use as an async context manager or call :meth:`release`. The first release
    returns capacity; repeated releases are harmless and return capacity at most
    once. Holding a permit keeps its charged bytes and transfer operation slot
    active, even after transfer closure, until it is released.
    """

    __slots__ = ("_charged_bytes", "_released", "_scheduler", "_state")

    def __init__(self, scheduler: _MediaScheduler, state: _TransferState, charged_bytes: int) -> None:
        """Bind a newly granted charge to its scheduler and transfer state.

        Args:
            scheduler: Private owner that accounts for release capacity.
            state: Registered transfer state whose live-permit count is updated.
            charged_bytes: Already rounded reservation size in bytes.
        """
        self._scheduler = scheduler
        self._state = state
        self._charged_bytes = charged_bytes
        self._released = False

    @property
    def charged_bytes(self) -> int:
        """Return the allocation rounded up to the scheduler unit."""
        return self._charged_bytes

    @property
    def released(self) -> bool:
        """Return whether this permit has already returned its allocation."""
        return self._released

    def release(self) -> None:
        """Return the allocation to the scheduler; subsequent calls do nothing."""
        if self._released:
            return
        self._released = True
        self._scheduler._release(self._state, self._charged_bytes)

    async def __aenter__(self) -> MediaPermit:
        """Return this live permit for ``async with`` use."""
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: object | None
    ) -> None:
        """Release the reservation when an ``async with`` block exits.

        Args:
            exc_type: Exception type from the body, if any.
            exc: Exception instance from the body, if any.
            traceback: Traceback object from the body, if any.
        """
        del exc_type, exc, traceback
        self.release()


class _MediaScheduler:
    """Schedule one DC/direction using byte capacity and deficit round robin."""

    def __init__(
        self,
        *,
        dc_id: int,
        direction: MediaDirection,
        max_bytes: int,
        small_limit: int | None,
        large_limit: int | None,
        on_idle: Callable[[_MediaScheduler], None],
    ) -> None:
        """Initialise private queues, capacity limits, metrics, and idle cleanup.

        Args:
            dc_id: Data-centre key shared only by this scheduler instance.
            direction: Upload or download key paired with ``dc_id``.
            max_bytes: Per-key charged-byte ceiling in bytes.
            small_limit: Maximum active small download transfers, or no cap.
            large_limit: Maximum active large download transfers, or no cap.
            on_idle: Callback used to evict this scheduler after complete drain.
        """
        self.dc_id = dc_id
        self.direction = direction
        self.max_bytes = max_bytes
        self.small_limit = small_limit
        self.large_limit = large_limit
        self._on_idle = on_idle
        self._states: list[_TransferState] = []
        self._cursor = 0
        self._last_granted_state: _TransferState | None = None
        self._active_bytes = 0
        self._queued_bytes = 0
        self._grants = 0
        self._grants_by_transfer: dict[str, int] = {}
        self._foreground_grants_since_background = 0

    @property
    def idle(self) -> bool:
        """Return whether no registered, active, or queued transfer remains."""
        return not self._states and self._active_bytes == 0 and self._queued_bytes == 0

    def register(self, *, transfer_id: str, size_class: MediaSizeClass, priority: MediaPriority) -> _TransferState:
        """Register a transfer and return its private scheduling state.

        Args:
            transfer_id: Unique logical transfer identifier.
            size_class: Operation-cap class determined from total size.
            priority: Default priority used unless an acquire overrides it.
        """
        state = _TransferState(transfer_id=transfer_id, size_class=size_class, priority=priority)
        self._states.append(state)
        self._record_queue_state()
        record_metric(
            "media.scheduler.transfers_registered",
            1,
            attributes={
                "dc_id": self.dc_id,
                "direction": self.direction,
                "size_class": size_class,
                "priority": priority,
            },
        )
        return state

    async def acquire(
        self, state: _TransferState, requested_bytes: int, priority: MediaPriority | None = None
    ) -> MediaPermit:
        """Wait for and return a reservation for a charged request.

        Cancellation removes a still-queued request or releases a just-granted
        permit, so it cannot leak byte capacity.

        Args:
            state: Registered transfer requesting capacity.
            requested_bytes: Positive unrounded payload size in bytes.
            priority: Per-request priority, defaulting to the transfer priority.

        Raises:
            RuntimeError: If the transfer is closed or no longer registered.
            ValueError: If a non-positive or over-capacity request is supplied.
        """
        if state.closing or state not in self._states:
            raise RuntimeError("media transfer is closed")
        charged_bytes = _charged_bytes(requested_bytes)
        if charged_bytes > self.max_bytes:
            raise ValueError(f"media request charge {charged_bytes} exceeds the per-DC byte limit {self.max_bytes}")
        loop = asyncio.get_running_loop()
        waiter = _Waiter(
            charged_bytes=charged_bytes,
            priority=state.priority if priority is None else priority,
            queued_at=time.monotonic(),
            future=loop.create_future(),
            scheduler=self,
            state=state,
        )
        state.pending.append(waiter)
        self._queued_bytes += charged_bytes
        record_metric(
            "media.scheduler.queued_bytes",
            self._queued_bytes,
            unit="bytes",
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )
        self._dispatch()
        try:
            return await waiter.future
        except asyncio.CancelledError:
            removed = False
            if waiter.future.done() and not waiter.future.cancelled():
                waiter.future.result().release()
            else:
                if not waiter.future.done():
                    waiter.future.cancel()
                removed = waiter.scheduler._remove_waiter(waiter.state, waiter)
            record_metric(
                "media.scheduler.cancellations",
                1,
                attributes={"dc_id": waiter.scheduler.dc_id, "direction": waiter.scheduler.direction},
            )
            if removed:
                waiter.scheduler._dispatch()
            raise

    def move_pending(self, state: _TransferState, target: _MediaScheduler, target_state: _TransferState) -> None:
        """Move queued waiters during a transfer rebind without changing order.

        Args:
            state: Closing source transfer state.
            target: Newly bound scheduler receiving queued charges.
            target_state: Registered destination transfer state.
        """
        while state.pending:
            waiter = state.pending.popleft()
            self._queued_bytes -= waiter.charged_bytes
            waiter.scheduler = target
            waiter.state = target_state
            target_state.pending.append(waiter)
            target._queued_bytes += waiter.charged_bytes
        state.closing = True
        self._remove_if_drained(state)
        self._record_queue_state()
        target._record_queue_state()
        target._dispatch()

    def unregister(self, state: _TransferState) -> None:
        """Close a transfer, cancel pending waiters, and retain live permits.

        Args:
            state: Transfer state to close. Its live permits remain charged until
                their owners release them.
        """
        state.closing = True
        while state.pending:
            waiter = state.pending.popleft()
            self._queued_bytes -= waiter.charged_bytes
            waiter.future.cancel()
        self._remove_if_drained(state)
        self._record_queue_state()
        self._dispatch()

    def close(self) -> None:
        """Close every registered transfer and cancel its pending requests."""
        for state in tuple(self._states):
            self.unregister(state)

    def configure_limits(self, *, small_limit: int | None, large_limit: int | None) -> None:
        """Replace operation limits and promptly dispatch newly unblocked work.

        Args:
            small_limit: Active small-transfer cap, or ``None`` for no cap.
            large_limit: Active large-transfer cap, or ``None`` for no cap.
        """
        self.small_limit = small_limit
        self.large_limit = large_limit
        record_metric(
            "media.scheduler.effective_small_limit",
            small_limit or 0,
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )
        record_metric(
            "media.scheduler.effective_large_limit",
            large_limit or 0,
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )
        self._dispatch()

    def snapshot(self) -> MediaSchedulerSnapshot:
        """Return a copy-safe snapshot of capacity, queues, and grant counts."""
        queued_transfers = sum(bool(state.pending) for state in self._states)
        active_transfers = sum(state.active_permits > 0 for state in self._states)
        return MediaSchedulerSnapshot(
            max_bytes=self.max_bytes,
            active_bytes=self._active_bytes,
            queued_bytes=self._queued_bytes,
            active_transfers=active_transfers,
            queued_transfers=queued_transfers,
            grants=self._grants,
            grants_by_transfer=dict(self._grants_by_transfer),
        )

    def _dispatch(self) -> None:
        """Grant work until no eligible request fits current limits."""
        self._discard_done_waiters()
        while self._states and self._queued_bytes > 0:
            priorities = self._priority_order()
            granted = False
            for priority in priorities:
                granted = self._grant_one(priority)
                if granted:
                    break
            if not granted:
                return

    def _discard_done_waiters(self) -> None:
        """Remove cancelled or externally completed waiters before charging capacity."""
        removed = False
        for state in tuple(self._states):
            retained: deque[_Waiter] = deque()
            for waiter in state.pending:
                if waiter.future.done():
                    self._queued_bytes -= waiter.charged_bytes
                    removed = True
                else:
                    retained.append(waiter)
            if len(retained) != len(state.pending):
                state.pending = retained
                self._remove_if_drained(state)
        if removed:
            self._record_queue_state()

    def _priority_order(self) -> tuple[MediaPriority, ...]:
        """Prefer foreground work while forcing every eighth eligible grant background."""
        has_foreground = any(state.pending and state.pending[0].priority == "foreground" for state in self._states)
        has_background = any(state.pending and state.pending[0].priority == "background" for state in self._states)
        if has_background and self._foreground_grants_since_background >= _BACKGROUND_GRANT_INTERVAL:
            return ("background", "foreground") if has_foreground else ("background",)
        if has_foreground:
            return ("foreground", "background") if has_background else ("foreground",)
        return ("background",) if has_background else ()

    def _grant_one(self, priority: MediaPriority) -> bool:
        """Grant one eligible request with rotating deficit-round-robin fairness.

        Args:
            priority: Queue priority to select for this grant attempt.
        """
        count = len(self._states)
        if count == 0:
            return False
        last_granted = self._last_granted_state
        if last_granted is None:
            start_index = self._cursor % count
        else:
            try:
                start_index = (self._states.index(last_granted) + 1) % count
            except ValueError:
                start_index = self._cursor % count
        # A 1 MiB request needs sixteen 64 KiB deficit turns. Grow deficits in
        # bounded passes only while capacity is otherwise idle; when active
        # bytes are the blocker, wait for release rather than spinning.
        max_passes = max(1, self.max_bytes // MEDIA_SCHEDULER_UNIT)
        for _ in range(max_passes):
            saw_candidate = False
            for step in range(count):
                index = (start_index + step) % count
                state = self._states[index]
                if not state.pending or state.pending[0].priority != priority or state.closing:
                    continue
                saw_candidate = True
                state.deficit_bytes += MEDIA_SCHEDULER_UNIT
                waiter = state.pending[0]
                if waiter.charged_bytes > state.deficit_bytes:
                    continue
                if self._active_bytes + waiter.charged_bytes > self.max_bytes:
                    continue
                if state.active_permits == 0 and not self._has_transfer_slot(state.size_class):
                    continue
                state.pending.popleft()
                state.deficit_bytes -= waiter.charged_bytes
                state.active_permits += 1
                self._active_bytes += waiter.charged_bytes
                self._queued_bytes -= waiter.charged_bytes
                self._cursor = (index + 1) % max(1, len(self._states))
                self._last_granted_state = state
                self._grants += 1
                self._grants_by_transfer[state.transfer_id] = self._grants_by_transfer.get(state.transfer_id, 0) + 1
                if priority == "background":
                    self._foreground_grants_since_background = 0
                else:
                    self._foreground_grants_since_background += 1
                wait_s = max(0.0, time.monotonic() - waiter.queued_at)
                record_metric(
                    "media.scheduler.wait_seconds",
                    wait_s,
                    unit="s",
                    attributes={
                        "dc_id": self.dc_id,
                        "direction": self.direction,
                        "priority": priority,
                        "size_class": state.size_class,
                    },
                )
                record_metric(
                    "media.scheduler.grants",
                    1,
                    attributes={
                        "dc_id": self.dc_id,
                        "direction": self.direction,
                        "priority": priority,
                        "size_class": state.size_class,
                        "transfer_id": state.transfer_id,
                    },
                )
                self._record_queue_state()
                waiter.future.set_result(MediaPermit(self, state, waiter.charged_bytes))
                return True
            if not saw_candidate:
                return False
        return False

    def _has_transfer_slot(self, size_class: MediaSizeClass) -> bool:
        """Return whether another transfer of ``size_class`` may become active.

        Args:
            size_class: Small or large class whose active-transfer cap is checked.
        """
        limit = self.small_limit if size_class == "small" else self.large_limit
        if limit is None:
            return True
        active = sum(state.size_class == size_class and state.active_permits > 0 for state in self._states)
        return active < limit

    def _release(self, state: _TransferState, charged_bytes: int) -> None:
        """Return capacity from a permit and dispatch any work it unblocks.

        Args:
            state: Transfer state whose live permit count is decremented.
            charged_bytes: Charged reservation to remove from active-byte usage.
        """
        if state.active_permits <= 0:
            return
        state.active_permits -= 1
        self._active_bytes = max(0, self._active_bytes - charged_bytes)
        record_metric(
            "media.scheduler.active_bytes",
            self._active_bytes,
            unit="bytes",
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )
        self._remove_if_drained(state)
        self._dispatch()

    def _remove_waiter(self, state: _TransferState, waiter: _Waiter) -> bool:
        """Remove one cancelled waiter and report whether it was still queued.

        Args:
            state: Transfer queue that might still contain the waiter.
            waiter: Specific acquire request cancelled by its caller.
        """
        try:
            state.pending.remove(waiter)
        except ValueError:
            return False
        self._queued_bytes = max(0, self._queued_bytes - waiter.charged_bytes)
        self._record_queue_state()
        self._remove_if_drained(state)
        return True

    def _remove_if_drained(self, state: _TransferState) -> None:
        """Forget a closed transfer once it has no pending or active work.

        Args:
            state: Closing transfer whose queues and live permits are inspected.
        """
        if not state.closing or state.pending or state.active_permits:
            return
        try:
            index = self._states.index(state)
        except ValueError:
            return
        self._states.pop(index)
        if self._states:
            self._cursor %= len(self._states)
        else:
            self._cursor = 0
        if self.idle:
            self._on_idle(self)

    def _record_queue_state(self) -> None:
        """Publish current aggregate queue and active-byte metrics."""
        record_metric(
            "media.scheduler.queued_transfers",
            sum(bool(state.pending) for state in self._states),
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )
        record_metric(
            "media.scheduler.queued_bytes",
            self._queued_bytes,
            unit="bytes",
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )
        record_metric(
            "media.scheduler.active_bytes",
            self._active_bytes,
            unit="bytes",
            attributes={"dc_id": self.dc_id, "direction": self.direction},
        )


class MediaTransfer:
    """A caller-owned transfer registration that can acquire fair media permits."""

    def __init__(
        self,
        registry: MediaSchedulerRegistry,
        *,
        transfer_id: str,
        dc_id: int,
        direction: MediaDirection,
        total_size: int | None,
        priority: MediaPriority,
    ) -> None:
        """Register this transfer using its direction, priority, and size class.

        Args:
            registry: Registry that owns the selected scheduler.
            transfer_id: Unique registry-generated transfer name.
            dc_id: Initial data-centre binding.
            direction: Upload or download scheduler direction.
            total_size: Known total bytes, or ``None`` to classify as large.
            priority: Default foreground or background request priority.
        """
        self._registry = registry
        self.transfer_id = transfer_id
        self.dc_id = dc_id
        self.direction = direction
        self.total_size = total_size
        self.priority = priority
        self.size_class: MediaSizeClass = (
            "large" if total_size is None or total_size >= MEDIA_LARGE_FILE_THRESHOLD else "small"
        )
        self._scheduler = registry._get_scheduler(dc_id, direction)
        self._state = self._scheduler.register(
            transfer_id=self.transfer_id, size_class=self.size_class, priority=self.priority
        )
        self._bindings: list[tuple[_MediaScheduler, _TransferState]] = [(self._scheduler, self._state)]
        self._closed = False

    @property
    def scheduler_snapshot(self) -> MediaSchedulerSnapshot:
        """Return current metrics for this transfer's currently bound scheduler."""
        return self._scheduler.snapshot()

    async def acquire(self, requested_bytes: int, *, priority: MediaPriority | None = None) -> MediaPermit:
        """Acquire a charged byte reservation, optionally overriding request priority.

        Args:
            requested_bytes: Positive payload size charged in 64 KiB units.
            priority: Per-request foreground/background override, if needed.

        Raises:
            RuntimeError: If this transfer has been closed.
            ValueError: If the request cannot fit its scheduler's byte limit.
        """
        if self._closed:
            raise RuntimeError("media transfer is closed")
        return await self._scheduler.acquire(self._state, requested_bytes, priority)

    async def rebind(self, dc_id: int) -> None:
        """Move future queued work to ``dc_id`` while live permits drain in place.

        Args:
            dc_id: Destination data-centre identifier.

        Raises:
            RuntimeError: If this transfer has been closed.
        """
        if self._closed:
            raise RuntimeError("media transfer is closed")
        if dc_id == self.dc_id:
            return
        old_scheduler = self._scheduler
        old_state = self._state
        new_scheduler = self._registry._get_scheduler(dc_id, self.direction)
        new_state = new_scheduler.register(
            transfer_id=self.transfer_id, size_class=self.size_class, priority=self.priority
        )
        old_scheduler.move_pending(old_state, new_scheduler, new_state)
        self.dc_id = dc_id
        self._scheduler = new_scheduler
        self._state = new_state
        self._bindings.append((new_scheduler, new_state))
        record_metric(
            "media.scheduler.transfer_rebinds", 1, attributes={"direction": self.direction, "target_dc_id": dc_id}
        )

    async def close(self) -> None:
        """Close the transfer and cancel all still-pending acquires."""
        if self._closed:
            return
        self._closed = True
        for scheduler, state in self._bindings:
            scheduler.unregister(state)


class MediaSchedulerRegistry:
    """Own lazy per-DC schedulers and create lifecycle-managed media transfers."""

    def __init__(
        self,
        *,
        download_max_bytes: int,
        upload_max_bytes: int,
        download_small_limit: int = DEFAULT_DOWNLOAD_SMALL_LIMIT,
        download_large_limit: int = DEFAULT_DOWNLOAD_LARGE_LIMIT,
    ) -> None:
        """Configure byte caps and download operation limits.

        Args:
            download_max_bytes: Per-DC download charged-byte ceiling in bytes.
            upload_max_bytes: Per-DC upload charged-byte ceiling in bytes.
            download_small_limit: Concurrent small download-transfer cap.
            download_large_limit: Concurrent large download-transfer cap.

        Raises:
            ValueError: If a byte cap is below one scheduler unit or an
                operation limit is not positive.
        """
        _validate_limit("download_max_bytes", download_max_bytes)
        _validate_limit("upload_max_bytes", upload_max_bytes)
        _validate_operation_limit("download_small_limit", download_small_limit)
        _validate_operation_limit("download_large_limit", download_large_limit)
        self.download_max_bytes = download_max_bytes
        self.upload_max_bytes = upload_max_bytes
        self.download_small_limit = download_small_limit
        self.download_large_limit = download_large_limit
        self._schedulers: dict[tuple[int, MediaDirection], _MediaScheduler] = {}
        self._ids = itertools.count(1)
        record_metric("media.scheduler.configured_download_bytes", download_max_bytes, unit="bytes")
        record_metric("media.scheduler.configured_upload_bytes", upload_max_bytes, unit="bytes")

    @property
    def scheduler_count(self) -> int:
        """Return the number of lazily created schedulers currently retained."""
        return len(self._schedulers)

    def open_transfer(
        self, *, dc_id: int, direction: MediaDirection, total_size: int | None, priority: MediaPriority = "foreground"
    ) -> MediaTransfer:
        """Open a transfer with foreground priority by default.

        Args:
            dc_id: Positive Telegram data-centre identifier.
            direction: Whether requests upload or download.
            total_size: Known size, or ``None`` to conservatively classify it as large.
            priority: ``foreground`` by default; background still receives periodic grants.

        Raises:
            ValueError: If the DC, direction, size, or priority is invalid.
        """
        if dc_id <= 0:
            raise ValueError("media transfer dc_id must be positive")
        if direction not in {"download", "upload"}:
            raise ValueError("media transfer direction must be download or upload")
        if total_size is not None and total_size < 0:
            raise ValueError("media transfer total_size must not be negative")
        if priority not in {"foreground", "background"}:
            raise ValueError("media transfer priority must be foreground or background")
        transfer_id = f"{direction}-{next(self._ids)}"
        return MediaTransfer(
            self, transfer_id=transfer_id, dc_id=dc_id, direction=direction, total_size=total_size, priority=priority
        )

    def configure_download_limits(self, *, small_limit: int, large_limit: int) -> None:
        """Update limits for future and existing download schedulers.

        Args:
            small_limit: Positive concurrent small-download transfer cap.
            large_limit: Positive concurrent large-download transfer cap.

        Raises:
            ValueError: If either concurrent-transfer limit is not positive.
        """
        _validate_operation_limit("small_limit", small_limit)
        _validate_operation_limit("large_limit", large_limit)
        self.download_small_limit = small_limit
        self.download_large_limit = large_limit
        for (_dc_id, direction), scheduler in self._schedulers.items():
            if direction == "download":
                scheduler.configure_limits(small_limit=small_limit, large_limit=large_limit)

    async def close(self) -> None:
        """Close all schedulers, cancel their queues, and discard the registry map."""
        schedulers = tuple(self._schedulers.values())
        for scheduler in schedulers:
            scheduler.close()
        self._schedulers.clear()

    def _get_scheduler(self, dc_id: int, direction: MediaDirection) -> _MediaScheduler:
        """Return the lazy scheduler for a DC/direction pair.

        Args:
            dc_id: Data-centre component of the scheduler key.
            direction: Upload or download component of the scheduler key.
        """
        key = (dc_id, direction)
        scheduler = self._schedulers.get(key)
        if scheduler is not None:
            return scheduler

        def remove_if_idle(candidate: _MediaScheduler) -> None:
            """Evict this exact scheduler only after it becomes fully idle.

            Args:
                candidate: Scheduler that notified the registry about idleness.
            """
            if candidate.idle and self._schedulers.get(key) is candidate:
                self._schedulers.pop(key, None)

        scheduler = _MediaScheduler(
            dc_id=dc_id,
            direction=direction,
            max_bytes=self.download_max_bytes if direction == "download" else self.upload_max_bytes,
            small_limit=self.download_small_limit if direction == "download" else None,
            large_limit=self.download_large_limit if direction == "download" else None,
            on_idle=remove_if_idle,
        )
        self._schedulers[key] = scheduler
        return scheduler


def _charged_bytes(requested_bytes: int) -> int:
    """Round a positive request up to one 64 KiB scheduler allocation unit.

    Args:
        requested_bytes: Positive unrounded payload size in bytes.

    Raises:
        ValueError: If ``requested_bytes`` is not positive.
    """
    if requested_bytes <= 0:
        raise ValueError("media request bytes must be positive")
    return ((requested_bytes + MEDIA_SCHEDULER_UNIT - 1) // MEDIA_SCHEDULER_UNIT) * MEDIA_SCHEDULER_UNIT


def _validate_limit(name: str, value: int) -> None:
    """Require a byte limit large enough to hold one charged request.

    Args:
        name: User-facing configuration field name for errors.
        value: Candidate byte limit in bytes.
    """
    if value < MEDIA_SCHEDULER_UNIT:
        raise ValueError(f"{name} must be at least {MEDIA_SCHEDULER_UNIT} bytes")


def _validate_operation_limit(name: str, value: int) -> None:
    """Require a positive concurrent-transfer limit.

    Args:
        name: User-facing configuration field name for errors.
        value: Candidate concurrent-transfer operation cap.
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive")


__all__ = [
    "DEFAULT_DOWNLOAD_LARGE_LIMIT",
    "DEFAULT_DOWNLOAD_SMALL_LIMIT",
    "MEDIA_LARGE_FILE_THRESHOLD",
    "MEDIA_SCHEDULER_UNIT",
    "MediaDirection",
    "MediaPermit",
    "MediaPriority",
    "MediaSchedulerRegistry",
    "MediaSchedulerSnapshot",
    "MediaSizeClass",
    "MediaTransfer",
]

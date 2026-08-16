"""Mutable MTProto session state for IDs, sequencing, replay checks, and acknowledgements."""

from __future__ import annotations

import secrets
import time
from collections import OrderedDict
from collections.abc import Collection
from dataclasses import dataclass, field

from miniproto.crypto.mtproto import auth_key_id
from miniproto.errors import ProtocolValidationError

MAX_SERVER_MSG_ID_FUTURE_SKEW = 30
MAX_SERVER_MSG_ID_PAST_SKEW = 300
_SERVER_MSG_ID_PARITY = 1


@dataclass(slots=True)
class MTProtoState:
    """Track one authorization key's MTProto session, timing, and acknowledgement state.

    Attributes:
        auth_key: Required 256-byte MTProto authorization key.
        server_salt: Current masked 64-bit server salt, defaulting to ``0``.
        session_id: Current random 64-bit session ID.
        time_offset: Server-time offset applied while allocating message IDs.
        duplicate_window: Maximum retained incoming IDs, defaulting to ``8192``.
        _last_msg_id: Last locally allocated message ID used to preserve monotonicity.
        _content_related_count: Count used to allocate content-related sequence numbers.
        _seen_msg_ids: Retained incoming IDs used for duplicate and replay checks.
        _pending_acks: Incoming content-related IDs awaiting acknowledgement.
        _time_trusted: Whether an accepted incoming ID has established server time.
    """

    auth_key: bytes
    server_salt: int = 0
    session_id: int = field(default_factory=lambda: secrets.randbits(64))
    time_offset: float = 0.0
    duplicate_window: int = 8192
    _last_msg_id: int = 0
    _content_related_count: int = 0
    _seen_msg_ids: OrderedDict[int, None] = field(default_factory=OrderedDict)
    _pending_acks: OrderedDict[int, float] = field(default_factory=OrderedDict)
    _time_trusted: bool = False

    def __post_init__(self) -> None:
        """Normalize fixed-width fields and validate construction invariants.

        Raises:
            ValueError: If the authorization key is not 256 bytes or the duplicate window is nonpositive.
        """
        self.auth_key = bytes(self.auth_key)
        if len(self.auth_key) != 256:
            raise ValueError("MTProto auth_key must be 256 bytes")
        self.server_salt &= 0xFFFFFFFFFFFFFFFF
        self.session_id &= 0xFFFFFFFFFFFFFFFF
        if self.duplicate_window <= 0:
            raise ValueError("duplicate_window must be positive")

    @property
    def auth_key_id(self) -> bytes:
        """Return the MTProto auth-key fingerprint derived from the session key."""
        return auth_key_id(self.auth_key)

    def next_msg_id(self) -> int:
        """Allocate a strictly increasing client MTProto message ID.

        Returns:
            Timestamp-derived, client-parity message ID advancing in steps of four.
        """
        candidate = int((time.time() + self.time_offset) * 2**32) & ~3
        if candidate <= self._last_msg_id:
            candidate = self._last_msg_id + 4
        self._last_msg_id = candidate
        return candidate

    def next_seq_no(self, *, content_related: bool) -> int:
        """Allocate the next MTProto sequence number.

        Args:
            content_related: Whether this message advances the content-related counter.

        Returns:
            Even non-content or odd content-related sequence number.
        """
        seq_no = self._content_related_count * 2 + (1 if content_related else 0)
        if content_related:
            self._content_related_count += 1
        return seq_no

    def observe_server_msg_id(self, msg_id: int) -> None:
        """Update the time offset from the timestamp carried by a server message ID.

        Args:
            msg_id: Server-generated MTProto message ID.
        """
        server_time = msg_id >> 32
        if server_time > 0:
            self.time_offset = server_time - time.time()

    @property
    def time_trusted(self) -> bool:
        """Return whether an accepted incoming message has established the session clock."""
        return self._time_trusted

    def validate_incoming(
        self,
        msg_id: int,
        *,
        session_id: int,
        now: float | None = None,
        provisional_time_offset: float | None = None,
        provisional_seen_msg_ids: Collection[int] = (),
    ) -> None:
        """Validate an incoming envelope before permanently recording it.

        Args:
            msg_id: Server-generated message ID to validate.
            session_id: Envelope session ID, which must match this state.
            now: Optional wall-clock time for deterministic validation.
            provisional_time_offset: Optional transactional offset to use for time-window checks.
            provisional_seen_msg_ids: Additional IDs already staged in the current transaction.

        Raises:
            ProtocolValidationError: If session, parity, duplicate, replay-window, or trusted time checks fail.
        """
        if session_id != self.session_id:
            raise ProtocolValidationError("session_id", context={"msg_id": msg_id})
        if msg_id % 4 != _SERVER_MSG_ID_PARITY:
            raise ProtocolValidationError("msg_id_parity", context={"msg_id": msg_id})
        if msg_id in self._seen_msg_ids or msg_id in provisional_seen_msg_ids:
            raise ProtocolValidationError("duplicate_msg_id", context={"msg_id": msg_id})
        replay_window = (*self._seen_msg_ids, *provisional_seen_msg_ids)
        if replay_window and len(replay_window) >= self.duplicate_window and msg_id <= min(replay_window):
            raise ProtocolValidationError("replay_floor", context={"msg_id": msg_id})
        if self._time_trusted or provisional_time_offset is not None:
            offset = self.time_offset if provisional_time_offset is None else provisional_time_offset
            current_time = (time.time() if now is None else now) + offset
            server_time = msg_id >> 32
            if server_time > current_time + MAX_SERVER_MSG_ID_FUTURE_SKEW:
                raise ProtocolValidationError("msg_id_future", context={"msg_id": msg_id})
            if server_time < current_time - MAX_SERVER_MSG_ID_PAST_SKEW:
                raise ProtocolValidationError("msg_id_past", context={"msg_id": msg_id})

    def commit_incoming(self, msg_id: int, *, content_related: bool = True, now: float | None = None) -> None:
        """Permanently record an already validated incoming message.

        Args:
            msg_id: Validated server message ID.
            content_related: Queue an acknowledgement when ``True`` (the default).
            now: Optional wall-clock time used when initially trusting the server clock.
        """
        self._seen_msg_ids[msg_id] = None
        while len(self._seen_msg_ids) > self.duplicate_window:
            self._seen_msg_ids.pop(min(self._seen_msg_ids))
        if content_related:
            self._pending_acks[msg_id] = time.monotonic()
        if not self._time_trusted:
            server_time = msg_id >> 32
            if server_time > 0:
                self.time_offset = server_time - (time.time() if now is None else now)
            self._time_trusted = True

    def record_incoming(self, msg_id: int, *, content_related: bool = True) -> bool:
        """Record a server message unless it is already known.

        Args:
            msg_id: Server message ID.
            content_related: Queue an acknowledgement when ``True`` (the default).

        Returns:
            ``True`` for a newly recorded ID, otherwise ``False``.
        """
        if msg_id in self._seen_msg_ids:
            return False
        self._seen_msg_ids[msg_id] = None
        self._seen_msg_ids.move_to_end(msg_id)
        while len(self._seen_msg_ids) > self.duplicate_window:
            self._seen_msg_ids.popitem(last=False)
        if content_related:
            self._pending_acks[msg_id] = time.monotonic()
        self.observe_server_msg_id(msg_id)
        return True

    def queue_ack(self, msg_id: int) -> None:
        """Queue one message ID for a future ``msgs_ack`` body.

        Args:
            msg_id: Server message ID to acknowledge.
        """
        self._pending_acks[msg_id] = time.monotonic()

    @property
    def pending_ack_count(self) -> int:
        """Return the number of unique message IDs awaiting acknowledgement."""
        return len(self._pending_acks)

    def oldest_pending_ack_age(self, now: float | None = None) -> float:
        """Return the age of the oldest queued acknowledgement.

        Args:
            now: Optional monotonic timestamp for deterministic measurement.

        Returns:
            Nonnegative age in seconds, or ``0.0`` when the queue is empty.
        """
        if not self._pending_acks:
            return 0.0
        oldest = next(iter(self._pending_acks.values()))
        return max(0.0, (time.monotonic() if now is None else now) - oldest)

    def pop_pending_acks(self, *, limit: int | None = None) -> tuple[int, ...]:
        """Remove the oldest queued acknowledgement IDs.

        Args:
            limit: Maximum IDs to remove; ``None`` (default) removes all queued IDs.

        Returns:
            Removed IDs in acknowledgement order.
        """
        if limit is None:
            limit = len(self._pending_acks)
        msg_ids: list[int] = []
        for _ in range(min(limit, len(self._pending_acks))):
            msg_id, _value = self._pending_acks.popitem(last=False)
            msg_ids.append(msg_id)
        return tuple(msg_ids)

    def requeue_acks(self, msg_ids: tuple[int, ...]) -> None:
        """Restore acknowledgement IDs after an unsent batch fails.

        Args:
            msg_ids: IDs to queue unless already pending.
        """
        now = time.monotonic()
        for msg_id in msg_ids:
            if msg_id not in self._pending_acks:
                self._pending_acks[msg_id] = now

    def apply_server_salt(self, server_salt: int) -> None:
        """Replace the current server salt after masking it to 64 bits.

        Args:
            server_salt: New server-supplied salt.
        """
        self.server_salt = server_salt & 0xFFFFFFFFFFFFFFFF

    def correct_time_offset_from_msg_id(self, msg_id: int) -> None:
        """Refresh the server-time offset and restart client message-ID monotonicity.

        Args:
            msg_id: Server message ID supplying the authoritative timestamp.
        """
        self.observe_server_msg_id(msg_id)
        self._last_msg_id = 0

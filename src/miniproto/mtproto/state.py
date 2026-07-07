from __future__ import annotations

import secrets
import time
from collections import OrderedDict
from dataclasses import dataclass, field

from miniproto.crypto.mtproto import auth_key_id


@dataclass(slots=True)
class MTProtoState:
    auth_key: bytes
    server_salt: int = 0
    session_id: int = field(default_factory=lambda: secrets.randbits(64))
    time_offset: float = 0.0
    duplicate_window: int = 8192
    _last_msg_id: int = 0
    _content_related_count: int = 0
    _seen_msg_ids: OrderedDict[int, None] = field(default_factory=OrderedDict)
    _pending_acks: OrderedDict[int, float] = field(default_factory=OrderedDict)

    def __post_init__(self) -> None:
        self.auth_key = bytes(self.auth_key)
        if len(self.auth_key) != 256:
            raise ValueError("MTProto auth_key must be 256 bytes")
        self.server_salt &= 0xFFFFFFFFFFFFFFFF
        self.session_id &= 0xFFFFFFFFFFFFFFFF
        if self.duplicate_window <= 0:
            raise ValueError("duplicate_window must be positive")

    @property
    def auth_key_id(self) -> bytes:
        return auth_key_id(self.auth_key)

    def next_msg_id(self) -> int:
        candidate = int((time.time() + self.time_offset) * 2**32) & ~3
        if candidate <= self._last_msg_id:
            candidate = self._last_msg_id + 4
        self._last_msg_id = candidate
        return candidate

    def next_seq_no(self, *, content_related: bool) -> int:
        seq_no = self._content_related_count * 2 + (1 if content_related else 0)
        if content_related:
            self._content_related_count += 1
        return seq_no

    def observe_server_msg_id(self, msg_id: int) -> None:
        server_time = msg_id >> 32
        if server_time > 0:
            self.time_offset = server_time - time.time()

    def record_incoming(self, msg_id: int, *, content_related: bool = True) -> bool:
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
        self._pending_acks[msg_id] = time.monotonic()

    @property
    def pending_ack_count(self) -> int:
        return len(self._pending_acks)

    def oldest_pending_ack_age(self, now: float | None = None) -> float:
        if not self._pending_acks:
            return 0.0
        oldest = next(iter(self._pending_acks.values()))
        return max(0.0, (time.monotonic() if now is None else now) - oldest)

    def pop_pending_acks(self, *, limit: int | None = None) -> tuple[int, ...]:
        if limit is None:
            limit = len(self._pending_acks)
        msg_ids: list[int] = []
        for _ in range(min(limit, len(self._pending_acks))):
            msg_id, _value = self._pending_acks.popitem(last=False)
            msg_ids.append(msg_id)
        return tuple(msg_ids)

    def requeue_acks(self, msg_ids: tuple[int, ...]) -> None:
        now = time.monotonic()
        for msg_id in msg_ids:
            if msg_id not in self._pending_acks:
                self._pending_acks[msg_id] = now

    def apply_server_salt(self, server_salt: int) -> None:
        self.server_salt = server_salt & 0xFFFFFFFFFFFFFFFF

    def correct_time_offset_from_msg_id(self, msg_id: int) -> None:
        self.observe_server_msg_id(msg_id)
        self._last_msg_id = 0

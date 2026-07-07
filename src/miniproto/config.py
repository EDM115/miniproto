from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from miniproto.session.storage import SessionStorage

TransportMode = Literal["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"]
UpdateQueueOverflowPolicy = Literal["raise", "drop_oldest", "drop_newest"]


@dataclass(slots=True, frozen=True)
class TransportConfig:
    mode: TransportMode = "tcp_abridged"
    connect_timeout: float = 10.0
    read_timeout: float = 30.0
    write_timeout: float = 30.0
    reconnect_backoff_initial: float = 0.25
    reconnect_backoff_max: float = 5.0
    max_payload_size: int = 16 * 1024 * 1024
    proxy: str | None = None

    def __post_init__(self) -> None:
        if self.connect_timeout <= 0:
            raise ValueError("connect_timeout must be positive")
        if self.read_timeout <= 0:
            raise ValueError("read_timeout must be positive")
        if self.write_timeout <= 0:
            raise ValueError("write_timeout must be positive")
        if self.reconnect_backoff_initial < 0:
            raise ValueError("reconnect_backoff_initial must not be negative")
        if self.reconnect_backoff_max < self.reconnect_backoff_initial:
            raise ValueError(
                "reconnect_backoff_max must be greater than or equal to reconnect_backoff_initial"
            )
        if self.max_payload_size <= 0:
            raise ValueError("max_payload_size must be positive")


@dataclass(slots=True, frozen=True)
class DeviceInfo:
    device_model: str = "miniproto"
    system_version: str = "unknown"
    app_version: str = "0.1.0"
    lang_code: str = "en"
    system_lang_code: str = "en"


@dataclass(slots=True, frozen=True)
class ClientConfig:
    api_id: int
    api_hash: str
    session_storage: SessionStorage | None = None
    transport: TransportConfig = field(default_factory=TransportConfig)
    device: DeviceInfo = field(default_factory=DeviceInfo)
    update_queue_size: int = 1000
    update_queue_overflow: UpdateQueueOverflowPolicy = "raise"
    update_duplicate_window: int = 2048
    dc_id: int = 2
    test_mode: bool = False
    request_timeout: float = 30.0
    max_request_retries: int = 2
    max_reconnect_attempts: int | None = None
    max_pending_rpcs: int = 512
    flood_sleep_threshold: int | None = None
    media_concurrency: int | None = None
    media_max_buffer_size: int | None = None

    def __post_init__(self) -> None:
        if self.api_id <= 0:
            raise ValueError("api_id must be a positive integer")
        if not self.api_hash:
            raise ValueError("api_hash must not be empty")
        if self.update_queue_size <= 0:
            raise ValueError("update_queue_size must be positive")
        if self.update_queue_overflow not in {"raise", "drop_oldest", "drop_newest"}:
            raise ValueError("update_queue_overflow must be raise, drop_oldest, or drop_newest")
        if self.update_duplicate_window <= 0:
            raise ValueError("update_duplicate_window must be positive")
        if self.dc_id <= 0:
            raise ValueError("dc_id must be a positive integer")
        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be positive")
        if self.max_request_retries < 0:
            raise ValueError("max_request_retries must not be negative")
        if self.max_reconnect_attempts is not None and self.max_reconnect_attempts <= 0:
            raise ValueError("max_reconnect_attempts must be positive when set")
        if self.max_pending_rpcs <= 0:
            raise ValueError("max_pending_rpcs must be positive")
        if self.flood_sleep_threshold is not None and self.flood_sleep_threshold < 0:
            raise ValueError("flood_sleep_threshold must not be negative")
        if self.media_concurrency is not None and self.media_concurrency <= 0:
            raise ValueError("media_concurrency must be positive when set")
        if self.media_max_buffer_size is not None and self.media_max_buffer_size <= 0:
            raise ValueError("media_max_buffer_size must be positive when set")

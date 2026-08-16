"""Immutable configuration models for client connections, updates, and media transfers."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal

from miniproto.session.storage import SessionStorage

TransportMode = Literal["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"]
UpdateQueueOverflowPolicy = Literal["raise", "drop_oldest", "drop_newest"]
_MEDIA_SCHEDULER_MIN_BYTES = 64 * 1024


@dataclass(slots=True, frozen=True)
class TransportConfig:
    """Connection transport settings with validated timeouts and payload limits.

    Attributes:
        mode: TCP framing mode; defaults to ``"tcp_abridged"``.
        connect_timeout: Maximum seconds allowed to establish a connection.
        read_timeout: Maximum seconds allowed for a transport read.
        write_timeout: Maximum seconds allowed for a transport write.
        reconnect_backoff_initial: Initial reconnect delay in seconds.
        reconnect_backoff_max: Maximum reconnect delay in seconds.
        max_payload_size: Largest accepted transport payload in bytes.
        proxy: Optional proxy URL, omitted from representations to avoid exposing credentials.
    """

    mode: TransportMode = "tcp_abridged"
    connect_timeout: float = 10.0
    read_timeout: float = 30.0
    write_timeout: float = 30.0
    reconnect_backoff_initial: float = 0.25
    reconnect_backoff_max: float = 5.0
    max_payload_size: int = 16 * 1024 * 1024
    proxy: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate positive timeouts and payload size plus ordered reconnect bounds.

        Raises:
            ValueError: If a timeout or payload limit is non-positive, the initial reconnect delay is negative, or the maximum delay is smaller than the initial delay.
        """
        if self.connect_timeout <= 0:
            raise ValueError("connect_timeout must be positive")
        if self.read_timeout <= 0:
            raise ValueError("read_timeout must be positive")
        if self.write_timeout <= 0:
            raise ValueError("write_timeout must be positive")
        if self.reconnect_backoff_initial < 0:
            raise ValueError("reconnect_backoff_initial must not be negative")
        if self.reconnect_backoff_max < self.reconnect_backoff_initial:
            raise ValueError("reconnect_backoff_max must be greater than or equal to reconnect_backoff_initial")
        if self.max_payload_size <= 0:
            raise ValueError("max_payload_size must be positive")


@dataclass(slots=True, frozen=True)
class DeviceInfo:
    """Application and device identity sent when initializing a Telegram session.

    Defaults identify this library without probing the host system; callers may supply platform-specific values when Telegram-facing metadata must be customized.

    Attributes:
        device_model: Human-readable device model sent in Telegram initialization, defaulting to ``"miniproto"``.
        system_version: Operating-system version label sent to Telegram, defaulting to ``"unknown"``.
        app_version: Application version label sent to Telegram, defaulting to ``"0.1.0"``.
        lang_code: Preferred interface language code, defaulting to ``"en"``.
        system_lang_code: Device system language code, defaulting to ``"en"``.
    """

    device_model: str = "miniproto"
    system_version: str = "unknown"
    app_version: str = "0.1.0"
    lang_code: str = "en"
    system_lang_code: str = "en"


@dataclass(slots=True, frozen=True)
class ClientConfig:
    """Immutable client configuration for authentication, session storage, RPCs, updates, and media.

    Args:
        api_id: Positive Telegram application identifier.
        api_hash: Telegram application secret; excluded from representations.
        session_storage: Optional session backend. When omitted, the client uses encrypted SQLite storage at ``session_path``.
        session_path: Path for the default encrypted SQLite session, defaulting to ``"miniproto.session.sqlite"``.
        transport: TCP transport configuration.
        device: Telegram-facing device metadata.
        update_queue_size: Bounded number of pending updates, defaulting to 1000.
        update_queue_overflow: Overflow action: ``"raise"``, ``"drop_oldest"``, or ``"drop_newest"``.
        update_duplicate_window: Number of recent updates retained for duplicate suppression.
        dc_id: Initial Telegram datacenter identifier, defaulting to 2.
        test_mode: Select Telegram's test environment when true.
        request_timeout: Default per-request timeout in seconds.
        max_request_retries: Maximum automatic retries for eligible RPCs.
        max_reconnect_attempts: Optional cap for transport reconnections.
        max_pending_rpcs: Maximum concurrently pending RPCs.
        flood_sleep_threshold: Maximum flood-wait duration to sleep automatically; ``None`` uses the default retry policy.
        method_flood_cache_size: Number of method flood-wait entries to remember.
        media_concurrency: Optional default concurrent media requests.
        media_max_buffer_size: Optional media buffering cap in bytes.
        media_download_max_in_flight_bytes_per_dc: Per-DC download scheduler byte budget.
        media_upload_max_in_flight_bytes_per_dc: Per-DC upload scheduler byte budget.
        media_download_small_queue_limit: Optional small-download queue limit.
        media_download_large_queue_limit: Optional large-download queue limit.
        media_idle_close: Seconds before unused media lanes close; ``None`` keeps them open for the client lifetime.
        bot_token: Optional bot token, excluded from representations.

    Raises:
        ValueError: If required identifiers or secrets are empty, limits are invalid, or a media scheduler budget is below 64 KiB.

    Security:
        ``api_hash``, ``bot_token``, and the supplied storage backend are hidden from the dataclass representation, but callers remain responsible for protecting configuration values and session storage.
    """

    api_id: int
    api_hash: str = field(repr=False)
    session_storage: SessionStorage | None = field(default=None, repr=False)
    session_path: str | os.PathLike[str] = "miniproto.session.sqlite"
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
    method_flood_cache_size: int = 512
    media_concurrency: int | None = None
    media_max_buffer_size: int | None = None
    media_download_max_in_flight_bytes_per_dc: int = 16 * 1024 * 1024
    media_upload_max_in_flight_bytes_per_dc: int = 8 * 1024 * 1024
    media_download_small_queue_limit: int | None = None
    media_download_large_queue_limit: int | None = None
    # Media lanes idle-close after this many seconds without requests (mtcute
    # closes at 60 s); keepalive pings keep them warm until then. None keeps
    # lanes open for the client's whole lifetime.
    media_idle_close: float | None = 120.0
    bot_token: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate client, update, RPC, and media resource limits.

        Raises:
            ValueError: If an identifier, timeout, queue size, retry count, or configured resource bound violates its documented constraint.
        """
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
        if self.method_flood_cache_size <= 0:
            raise ValueError("method_flood_cache_size must be positive")
        if self.media_concurrency is not None and self.media_concurrency <= 0:
            raise ValueError("media_concurrency must be positive when set")
        if self.media_max_buffer_size is not None and self.media_max_buffer_size <= 0:
            raise ValueError("media_max_buffer_size must be positive when set")
        if self.media_download_max_in_flight_bytes_per_dc < _MEDIA_SCHEDULER_MIN_BYTES:
            raise ValueError(
                f"media_download_max_in_flight_bytes_per_dc must be at least {_MEDIA_SCHEDULER_MIN_BYTES} bytes"
            )
        if self.media_upload_max_in_flight_bytes_per_dc < _MEDIA_SCHEDULER_MIN_BYTES:
            raise ValueError(
                f"media_upload_max_in_flight_bytes_per_dc must be at least {_MEDIA_SCHEDULER_MIN_BYTES} bytes"
            )
        if self.media_download_small_queue_limit is not None and self.media_download_small_queue_limit <= 0:
            raise ValueError("media_download_small_queue_limit must be positive when set")
        if self.media_download_large_queue_limit is not None and self.media_download_large_queue_limit <= 0:
            raise ValueError("media_download_large_queue_limit must be positive when set")
        if self.media_idle_close is not None and self.media_idle_close <= 0:
            raise ValueError("media_idle_close must be positive when set")
        if self.bot_token is not None and not self.bot_token:
            raise ValueError("bot_token must not be empty when set")

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from miniproto.session.storage import SessionStorage

TransportMode = Literal["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"]


@dataclass(slots=True, frozen=True)
class TransportConfig:
    mode: TransportMode = "tcp_abridged"
    connect_timeout: float = 10.0
    read_timeout: float = 30.0
    reconnect_backoff_initial: float = 0.25
    reconnect_backoff_max: float = 5.0
    proxy: str | None = None


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

    def __post_init__(self) -> None:
        if self.api_id <= 0:
            raise ValueError("api_id must be a positive integer")
        if not self.api_hash:
            raise ValueError("api_hash must not be empty")
        if self.update_queue_size <= 0:
            raise ValueError("update_queue_size must be positive")

"""Public API for miniproto."""

from miniproto.client import Client
from miniproto.config import ClientConfig, DeviceInfo, TransportConfig
from miniproto.errors import FloodWait, RpcError, Unauthorized
from miniproto.session.storage import (
    EncryptedSQLiteSessionStorage,
    InMemorySessionStorage,
    SessionStorage,
)
from miniproto.types import Media, Message, NewMessage, Peer, Update

__all__ = [
    "Client",
    "ClientConfig",
    "DeviceInfo",
    "EncryptedSQLiteSessionStorage",
    "FloodWait",
    "InMemorySessionStorage",
    "Media",
    "Message",
    "NewMessage",
    "Peer",
    "RpcError",
    "SessionStorage",
    "TransportConfig",
    "Unauthorized",
    "Update",
]

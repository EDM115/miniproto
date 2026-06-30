"""Public API for miniproto."""

from miniproto.client import Client
from miniproto.config import ClientConfig, DeviceInfo, TransportConfig
from miniproto.errors import (
    FloodWait,
    RpcError,
    SessionEnvelopeError,
    SessionStorageError,
    Unauthorized,
)
from miniproto.session.models import (
    AuthKey,
    DCOption,
    PeerCacheEntry,
    SessionRecord,
    UpdateState,
    UserIdentity,
)
from miniproto.session.storage import (
    EncryptedSQLiteSessionStorage,
    InMemorySessionStorage,
    SessionStorage,
)
from miniproto.types import Media, Message, NewMessage, Peer, Update

__all__ = [
    "AuthKey",
    "Client",
    "ClientConfig",
    "DCOption",
    "DeviceInfo",
    "EncryptedSQLiteSessionStorage",
    "FloodWait",
    "InMemorySessionStorage",
    "Media",
    "Message",
    "NewMessage",
    "Peer",
    "PeerCacheEntry",
    "RpcError",
    "SessionEnvelopeError",
    "SessionRecord",
    "SessionStorage",
    "SessionStorageError",
    "TransportConfig",
    "Unauthorized",
    "Update",
    "UpdateState",
    "UserIdentity",
]

"""Public API for miniproto."""

from miniproto import event_loop
from miniproto.auth import AuthKeyExchange, AuthKeyExchangeResult, AuthService
from miniproto.client import Client
from miniproto.config import ClientConfig, DeviceInfo, TransportConfig
from miniproto.errors import (
    AuthError,
    AuthKeyNotFound,
    AuthKeyRegenerationRequired,
    DatacenterMigration,
    FloodWait,
    InvalidCode,
    InvalidDatacenter,
    PasswordInvalid,
    PasswordRequired,
    RpcError,
    SessionEnvelopeError,
    SessionStorageError,
    SignUpRequired,
    TransportFlood,
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
    "AuthError",
    "AuthKey",
    "AuthKeyExchange",
    "AuthKeyExchangeResult",
    "AuthKeyNotFound",
    "AuthKeyRegenerationRequired",
    "AuthService",
    "Client",
    "ClientConfig",
    "DCOption",
    "DatacenterMigration",
    "DeviceInfo",
    "EncryptedSQLiteSessionStorage",
    "FloodWait",
    "InMemorySessionStorage",
    "InvalidCode",
    "InvalidDatacenter",
    "Media",
    "Message",
    "NewMessage",
    "PasswordInvalid",
    "PasswordRequired",
    "Peer",
    "PeerCacheEntry",
    "RpcError",
    "SessionEnvelopeError",
    "SessionRecord",
    "SessionStorage",
    "SessionStorageError",
    "SignUpRequired",
    "TransportConfig",
    "TransportFlood",
    "Unauthorized",
    "Update",
    "UpdateState",
    "UserIdentity",
    "event_loop",
]

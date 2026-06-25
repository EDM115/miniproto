from __future__ import annotations

import os
from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SessionStorage(Protocol):
    async def load(self) -> Mapping[str, Any] | None: ...

    async def save(self, data: Mapping[str, Any]) -> None: ...

    async def clear(self) -> None: ...

    async def close(self) -> None: ...


class InMemorySessionStorage:
    def __init__(self, initial: Mapping[str, Any] | None = None) -> None:
        self._data: MutableMapping[str, Any] | None = dict(initial) if initial is not None else None

    async def load(self) -> Mapping[str, Any] | None:
        return dict(self._data) if self._data is not None else None

    async def save(self, data: Mapping[str, Any]) -> None:
        self._data = dict(data)

    async def clear(self) -> None:
        self._data = None

    async def close(self) -> None:
        return None


class EncryptedSQLiteSessionStorage:
    """Fail-closed placeholder for encrypted SQLite session persistence."""

    def __init__(self, path: str | os.PathLike[str], key: bytes | str | None = None) -> None:
        resolved_key = key or os.environ.get("MINIPROTO_SESSION_KEY")
        if not resolved_key:
            raise ValueError(
                "EncryptedSQLiteSessionStorage requires a key or MINIPROTO_SESSION_KEY"
            )
        self.path = Path(path)
        self._key = resolved_key.encode() if isinstance(resolved_key, str) else bytes(resolved_key)

    async def load(self) -> Mapping[str, Any] | None:
        raise NotImplementedError("encrypted SQLite session loading is not implemented yet")

    async def save(self, data: Mapping[str, Any]) -> None:
        raise NotImplementedError("encrypted SQLite session saving is not implemented yet")

    async def clear(self) -> None:
        raise NotImplementedError("encrypted SQLite session clearing is not implemented yet")

    async def close(self) -> None:
        return None

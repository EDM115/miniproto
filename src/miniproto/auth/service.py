from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Iterable, Mapping
from dataclasses import replace
from typing import Any, Protocol, runtime_checkable

from miniproto.auth.dc import dc_options_from_raw, select_dc_option
from miniproto.auth.password import compute_check_password
from miniproto.config import ClientConfig
from miniproto.errors import (
    DatacenterMigration,
    InvalidDatacenter,
    PasswordRequired,
    RpcError,
    SignUpRequired,
    classify_rpc_error,
)
from miniproto.raw import functions, types
from miniproto.session.models import (
    DCOption,
    PeerCacheEntry,
    SessionRecord,
    UpdateState,
    UserIdentity,
    session_record_from_mapping,
)
from miniproto.session.storage import SessionStorage

Callback0 = Callable[[], Awaitable[str] | str]
RawInvoker = Callable[[object], Awaitable[object] | object]


@runtime_checkable
class SupportsInvoke(Protocol):
    async def invoke(self, raw_request: object) -> object: ...


class AuthService:
    def __init__(self, config: ClientConfig, storage: SessionStorage, invoker: RawInvoker) -> None:
        self.config = config
        self.storage = storage
        self._invoke = invoker

    async def sign_in_phone(
        self, phone: str, code_callback: Callback0, password_callback: Callback0 | None = None
    ) -> object:
        sent = await self._invoke_auth(
            functions.AuthSendCode(
                phone_number=phone,
                api_id=self.config.api_id,
                api_hash=self.config.api_hash,
                settings=types.CodeSettings(),
            )
        )
        if isinstance(sent, types.AuthSentCodeSuccess):
            await self._persist_authorization(sent.authorization, phone=phone, is_bot=False)
            return sent.authorization
        if not isinstance(sent, types.AuthSentCode):
            raise RpcError("auth.sendCode returned an unexpected result", request="auth.sendCode")
        code = await _resolve_callback(code_callback)
        try:
            authorization = await self._invoke_auth(
                functions.AuthSignIn(
                    phone_number=phone, phone_code_hash=sent.phone_code_hash, phone_code=code
                )
            )
        except PasswordRequired:
            authorization = await self._sign_in_password(password_callback)
        if isinstance(authorization, types.AuthAuthorizationSignUpRequired):
            raise SignUpRequired("phone number requires sign-up before sign-in")
        if not isinstance(authorization, types.AuthAuthorization):
            raise RpcError("auth.signIn returned an unexpected result", request="auth.signIn")
        await self._persist_authorization(authorization, phone=phone, is_bot=False)
        return authorization

    async def sign_in_bot(self, token: str) -> object:
        authorization = await self._invoke_auth(
            functions.AuthImportBotAuthorization(
                flags=0,
                api_id=self.config.api_id,
                api_hash=self.config.api_hash,
                bot_auth_token=token,
            )
        )
        if not isinstance(authorization, types.AuthAuthorization):
            raise RpcError(
                "auth.importBotAuthorization returned an unexpected result",
                request="auth.importBotAuthorization",
            )
        await self._persist_authorization(authorization, phone=None, is_bot=True)
        return authorization

    async def export_authorization(self, dc_id: int) -> types.AuthExportedAuthorization:
        exported = await self._invoke_auth(functions.AuthExportAuthorization(dc_id=dc_id))
        if not isinstance(exported, types.AuthExportedAuthorization):
            raise RpcError(
                "auth.exportAuthorization returned an unexpected result",
                request="auth.exportAuthorization",
            )
        return exported

    async def import_authorization(self, exported: types.AuthExportedAuthorization) -> object:
        authorization = await self._invoke_auth(
            functions.AuthImportAuthorization(id=exported.id, bytes=exported.bytes)
        )
        if isinstance(authorization, types.AuthAuthorization):
            await self._persist_authorization(
                authorization, phone=None, is_bot=bool(getattr(authorization.user, "bot", False))
            )
        return authorization

    async def persist_dc_options(self, raw_config: object) -> tuple[DCOption, ...]:
        raw_options = getattr(raw_config, "dc_options", ())
        dc_options = dc_options_from_raw(raw_options if isinstance(raw_options, Iterable) else ())
        current = await self._load_record()
        await self.storage.save(
            replace(
                current,
                dc_id=int(getattr(raw_config, "this_dc", current.dc_id or self.config.dc_id)),
                dc_options=dc_options,
            )
        )
        return dc_options

    async def select_current_dc(self) -> DCOption:
        record = await self._load_record()
        dc_id = record.dc_id or self.config.dc_id
        if not record.dc_options:
            raise InvalidDatacenter(f"no DC options stored for dc_id={dc_id}")
        return select_dc_option(record.dc_options, dc_id)

    async def handle_dc_migration(
        self, error: DatacenterMigration
    ) -> types.AuthExportedAuthorization | None:
        record = await self._load_record()
        if record.dc_id == error.dc_id:
            raise InvalidDatacenter(f"already on migrated dc_id={error.dc_id}")
        if record.user is None:
            await self.storage.save(replace(record, dc_id=error.dc_id))
            return None
        exported = await self.export_authorization(error.dc_id)
        await self.storage.save(replace(record, dc_id=error.dc_id))
        return exported

    async def _sign_in_password(self, password_callback: Callback0 | None) -> object:
        if password_callback is None:
            raise PasswordRequired("account requires a 2FA password callback")
        password = await _resolve_callback(password_callback)
        password_state = await self._invoke_auth(functions.AccountGetPassword())
        if not isinstance(password_state, types.AccountPassword):
            raise RpcError(
                "account.getPassword returned an unexpected result", request="account.getPassword"
            )
        check = compute_check_password(password, password_state)
        return await self._invoke_auth(functions.AuthCheckPassword(password=check))

    async def _invoke_auth(self, request: object) -> object:
        try:
            result = self._invoke(request)
            return await result if inspect.isawaitable(result) else result
        except RpcError as exc:
            raise classify_rpc_error(exc) from exc

    async def _persist_authorization(
        self, authorization: types.AuthAuthorization, *, phone: str | None, is_bot: bool
    ) -> None:
        record = await self._load_record()
        user = _identity_from_authorization(authorization, phone=phone, is_bot=is_bot)
        peers = _upsert_self_peer(record.peers, user)
        metadata = dict(record.metadata)
        future_auth_token = getattr(authorization, "future_auth_token", None)
        if isinstance(future_auth_token, bytes):
            metadata["future_auth_token"] = future_auth_token
        await self.storage.save(
            replace(
                record,
                dc_id=record.dc_id or self.config.dc_id,
                user=user,
                peers=peers,
                update_state=record.update_state or UpdateState(),
                metadata=metadata,
            )
        )

    async def _load_record(self) -> SessionRecord:
        loaded = await self.storage.load()
        if loaded is None:
            return SessionRecord(dc_id=self.config.dc_id)
        if _looks_like_phase2_record(loaded):
            return session_record_from_mapping(loaded)
        return _record_from_legacy_mapping(loaded, self.config.dc_id)


def _identity_from_authorization(
    authorization: types.AuthAuthorization, *, phone: str | None, is_bot: bool
) -> UserIdentity:
    user = authorization.user
    return UserIdentity(
        id=int(user.id),
        access_hash=_optional_int(getattr(user, "access_hash", None)),
        is_bot=bool(getattr(user, "bot", False)) or is_bot,
        username=_optional_str(getattr(user, "username", None)),
        phone=_optional_str(getattr(user, "phone", None)) or phone,
        first_name=_optional_str(getattr(user, "first_name", None)),
        last_name=_optional_str(getattr(user, "last_name", None)),
    )


def _upsert_self_peer(
    peers: tuple[PeerCacheEntry, ...], user: UserIdentity
) -> tuple[PeerCacheEntry, ...]:
    entry = PeerCacheEntry(
        id=user.id,
        kind="self",
        access_hash=user.access_hash,
        username=user.username,
        phone=user.phone,
        raw={"is_bot": user.is_bot},
    )
    remaining = tuple(peer for peer in peers if not (peer.kind == "self" or peer.id == user.id))
    return (entry, *remaining)


def _record_from_legacy_mapping(data: Mapping[str, Any], dc_id: int) -> SessionRecord:
    payload = dict(data)
    record_data: dict[str, Any] = {
        "version": 1,
        "dc_id": _optional_int(payload.get("dc_id")) or dc_id,
        "auth_key": payload.get("auth_key")
        if isinstance(payload.get("auth_key"), Mapping)
        else None,
        "dc_options": payload.get("dc_options", ()),
        "user": payload.get("user") if isinstance(payload.get("user"), Mapping) else None,
        "update_state": payload.get("update_state"),
        "peers": payload.get("peers", ()),
        "metadata": {
            key: value
            for key, value in payload.items()
            if key not in {"dc_id", "auth_key", "dc_options", "user", "update_state", "peers"}
        },
    }
    if isinstance(payload.get("auth_key"), bytes):
        record_data["auth_key"] = {
            "dc_id": record_data["dc_id"],
            "key": payload["auth_key"],
            "key_id": None,
        }
    return session_record_from_mapping(record_data)


def _looks_like_phase2_record(data: Mapping[str, Any]) -> bool:
    return "version" in data and any(
        key in data for key in ("dc_options", "user", "update_state", "peers", "metadata")
    )


async def _resolve_callback(callback: Callback0) -> str:
    value = callback()
    resolved = await value if inspect.isawaitable(value) else value
    return str(resolved)


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str | bytes | bytearray):
        return int(value)
    return int(str(value))


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)

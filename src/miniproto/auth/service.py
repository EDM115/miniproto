"""High-level Telegram authorization flows and their session persistence."""

from __future__ import annotations

import inspect
import logging
import time
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
from miniproto.observability import emit_event, get_logger, record_metric
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
_LOGGER = get_logger("auth")


@runtime_checkable
class SupportsInvoke(Protocol):
    """Object capable of sending a raw Telegram request."""

    async def invoke(self, raw_request: object) -> object:
        """Invoke ``raw_request`` and return its decoded Telegram result.

        Args:
            raw_request: Constructor-backed Telegram request object to send.
        """


class AuthService:
    """Run sign-in and data-center authorization flows for one client session.

    Args:
        config: Client credentials and default data-center configuration.
        storage: Session storage receiving successful authorization state.
        invoker: Callable that sends raw Telegram requests, synchronously or asynchronously.
    """

    def __init__(self, config: ClientConfig, storage: SessionStorage, invoker: RawInvoker) -> None:
        """Bind the client configuration, session storage, and raw-request invoker.

        Args:
            config: Client credentials and default data-center configuration.
            storage: Mutable session storage for authorization state.
            invoker: Callable that returns or awaits raw Telegram RPC results.
        """
        self.config = config
        self.storage = storage
        self._invoke = invoker

    async def sign_in_phone(
        self, phone: str, code_callback: Callback0, password_callback: Callback0 | None = None
    ) -> object:
        """Sign in a phone-number account, requesting a code and optional 2FA password.

        Args:
            phone: Account phone number sent to ``auth.sendCode``.
            code_callback: Callable that returns or awaits the verification code.
            password_callback: Callable used only when Telegram requires two-factor authentication.

        Returns:
            The successful Telegram authorization object.

        Raises:
            PasswordRequired: If the account needs 2FA and no password callback was provided.
            SignUpRequired: If the number has no Telegram account.
            RpcError: If Telegram returns an unexpected result for an authorization request.
        """
        started = time.perf_counter()
        try:
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
                _emit_auth_event("auth.sign_in_phone", started, outcome="success", path="sent_code_success")
                return sent.authorization
            if not isinstance(sent, types.AuthSentCode):
                raise RpcError("auth.sendCode returned an unexpected result", request="auth.sendCode")
            code = await _resolve_callback(code_callback)
            try:
                authorization = await self._invoke_auth(
                    functions.AuthSignIn(phone_number=phone, phone_code_hash=sent.phone_code_hash, phone_code=code)
                )
            except PasswordRequired:
                authorization = await self._sign_in_password(password_callback)
            if isinstance(authorization, types.AuthAuthorizationSignUpRequired):
                raise SignUpRequired("phone number requires sign-up before sign-in")
            if not isinstance(authorization, types.AuthAuthorization):
                raise RpcError("auth.signIn returned an unexpected result", request="auth.signIn")
            await self._persist_authorization(authorization, phone=phone, is_bot=False)
        except BaseException as exc:
            _emit_auth_event("auth.sign_in_phone", started, outcome="error", error_type=type(exc).__name__)
            raise
        _emit_auth_event("auth.sign_in_phone", started, outcome="success", path="code")
        return authorization

    async def sign_in_bot(self, token: str) -> object:
        """Authorize a bot token and persist the authenticated bot identity.

        Args:
            token: Bot authorization token supplied by BotFather.

        Returns:
            The successful Telegram authorization object.

        Raises:
            RpcError: If Telegram does not return an authorization object.
        """
        started = time.perf_counter()
        try:
            authorization = await self._invoke_auth(
                functions.AuthImportBotAuthorization(
                    flags=0, api_id=self.config.api_id, api_hash=self.config.api_hash, bot_auth_token=token
                )
            )
            if not isinstance(authorization, types.AuthAuthorization):
                raise RpcError(
                    "auth.importBotAuthorization returned an unexpected result", request="auth.importBotAuthorization"
                )
            await self._persist_authorization(authorization, phone=None, is_bot=True)
        except BaseException as exc:
            _emit_auth_event("auth.sign_in_bot", started, outcome="error", error_type=type(exc).__name__)
            raise
        _emit_auth_event("auth.sign_in_bot", started, outcome="success")
        return authorization

    async def export_authorization(self, dc_id: int) -> types.AuthExportedAuthorization:
        """Export the current user authorization for import at another data center.

        Args:
            dc_id: Target data-center identifier.

        Returns:
            Telegram's short-lived exported authorization payload.

        Raises:
            RpcError: If Telegram returns an unexpected export response.
        """
        exported = await self._invoke_auth(functions.AuthExportAuthorization(dc_id=dc_id))
        if not isinstance(exported, types.AuthExportedAuthorization):
            raise RpcError("auth.exportAuthorization returned an unexpected result", request="auth.exportAuthorization")
        return exported

    async def import_authorization(self, exported: types.AuthExportedAuthorization) -> object:
        """Import an exported authorization and persist it when it includes user data.

        Args:
            exported: Authorization previously exported for this data center.

        Returns:
            Telegram's import result, which may or may not include an authorization object.
        """
        authorization = await self._invoke_auth(functions.AuthImportAuthorization(id=exported.id, bytes=exported.bytes))
        if isinstance(authorization, types.AuthAuthorization):
            await self._persist_authorization(
                authorization, phone=None, is_bot=bool(getattr(authorization.user, "bot", False))
            )
        return authorization

    async def persist_dc_options(self, raw_config: object) -> tuple[DCOption, ...]:
        """Normalize ``help.Config`` DC options and atomically store them in the session.

        Args:
            raw_config: Telegram configuration result exposing ``dc_options`` and optional ``this_dc``.

        Returns:
            The normalized, persisted data-center options.
        """
        raw_options = getattr(raw_config, "dc_options", ())
        dc_options = dc_options_from_raw(raw_options if isinstance(raw_options, Iterable) else ())
        raw_dc_id = getattr(raw_config, "this_dc", None)

        def persist(payload: Mapping[str, Any] | None) -> SessionRecord:
            """Merge the fetched DC configuration into the latest stored session record.

            Args:
                payload: Latest stored session mapping supplied by ``storage.mutate``.
            """
            current = _session_record_from_payload(payload, self.config.dc_id)
            return replace(current, dc_id=int(raw_dc_id or current.dc_id or self.config.dc_id), dc_options=dc_options)

        await self.storage.mutate(persist)
        return dc_options

    async def select_current_dc(self) -> DCOption:
        """Return the preferred non-media endpoint for the persisted current DC.

        Raises:
            InvalidDatacenter: If the session has no saved endpoint for its current DC.
        """
        record = await self._load_record()
        dc_id = record.dc_id or self.config.dc_id
        if not record.dc_options:
            raise InvalidDatacenter(f"no DC options stored for dc_id={dc_id}")
        return select_dc_option(record.dc_options, dc_id)

    async def handle_dc_migration(self, error: DatacenterMigration) -> types.AuthExportedAuthorization | None:
        """Persist Telegram's requested DC migration and export user authorization when needed.

        An unauthenticated session only changes its target DC. An authenticated session also
        obtains an exported authorization, which the caller must import through a sender for
        the target DC.

        Args:
            error: Classified Telegram migration response with the target ``dc_id``.

        Returns:
            An exported authorization for authenticated sessions, otherwise ``None``.

        Raises:
            InvalidDatacenter: If Telegram requests the already-selected DC.
        """
        started = time.perf_counter()
        record = await self._load_record()
        if record.dc_id == error.dc_id:
            raise InvalidDatacenter(f"already on migrated dc_id={error.dc_id}")
        if record.user is None:
            await self.storage.mutate(
                lambda payload: replace(_session_record_from_payload(payload, self.config.dc_id), dc_id=error.dc_id)
            )
            _emit_auth_event("auth.dc_migration", started, outcome="success", target_dc_id=error.dc_id, exported=False)
            return None
        exported = await self.export_authorization(error.dc_id)
        await self.storage.mutate(
            lambda payload: replace(_session_record_from_payload(payload, self.config.dc_id), dc_id=error.dc_id)
        )
        _emit_auth_event("auth.dc_migration", started, outcome="success", target_dc_id=error.dc_id, exported=True)
        return exported

    async def _sign_in_password(self, password_callback: Callback0 | None) -> object:
        """Resolve a 2FA callback, construct its SRP proof, and submit it to Telegram.

        Args:
            password_callback: Optional callable producing the user's plain-text 2FA password.
        """
        if password_callback is None:
            raise PasswordRequired("account requires a 2FA password callback")
        password = await _resolve_callback(password_callback)
        password_state = await self._invoke_auth(functions.AccountGetPassword())
        if not isinstance(password_state, types.AccountPassword):
            raise RpcError("account.getPassword returned an unexpected result", request="account.getPassword")
        check = compute_check_password(password, password_state)
        return await self._invoke_auth(functions.AuthCheckPassword(password=check))

    async def _invoke_auth(self, request: object) -> object:
        """Invoke one authorization request and classify Telegram RPC failures.

        Args:
            request: Raw Telegram authorization request to pass to the configured invoker.
        """
        try:
            result = self._invoke(request)
            return await result if inspect.isawaitable(result) else result
        except RpcError as exc:
            raise classify_rpc_error(exc) from exc

    async def _persist_authorization(
        self, authorization: types.AuthAuthorization, *, phone: str | None, is_bot: bool
    ) -> None:
        """Persist the authenticated identity, self peer, and optional future auth token.

        Args:
            authorization: Successful Telegram authorization result to persist.
            phone: Phone number supplied during user sign-in, if one was supplied.
            is_bot: Whether the authorization flow authenticated a bot token.
        """
        user = _identity_from_authorization(authorization, phone=phone, is_bot=is_bot)
        future_auth_token = getattr(authorization, "future_auth_token", None)

        def persist(payload: Mapping[str, Any] | None) -> SessionRecord:
            """Merge an authorization result with the latest session record.

            Args:
                payload: Latest stored session mapping supplied by ``storage.mutate``.
            """
            record = _session_record_from_payload(payload, self.config.dc_id)
            peers = _upsert_self_peer(record.peers, user)
            metadata = dict(record.metadata)
            if isinstance(future_auth_token, bytes):
                metadata["future_auth_token"] = future_auth_token
            return replace(
                record,
                dc_id=record.dc_id or self.config.dc_id,
                user=user,
                peers=peers,
                update_state=record.update_state or UpdateState(),
                metadata=metadata,
            )

        await self.storage.mutate(persist)

    async def _load_record(self) -> SessionRecord:
        """Load the persisted session as the current structured record."""
        return _session_record_from_payload(await self.storage.load(), self.config.dc_id)


def _identity_from_authorization(
    authorization: types.AuthAuthorization, *, phone: str | None, is_bot: bool
) -> UserIdentity:
    """Extract a durable user identity from Telegram's successful authorization result.

    Args:
        authorization: Telegram response supplying the authenticated raw user.
        phone: User-entered phone fallback when Telegram omits it from the raw user.
        is_bot: Bot-flow fallback when Telegram's raw flag is absent.
    """
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


def _session_record_from_payload(loaded: Mapping[str, Any] | None, dc_id: int) -> SessionRecord:
    """Load current or legacy session mappings into a structured record.

    Args:
        loaded: Persisted mapping or ``None`` for an empty session.
        dc_id: Default data-center ID used for empty and legacy records.
    """
    if loaded is None:
        return SessionRecord(dc_id=dc_id)
    if _looks_like_phase2_record(loaded):
        return session_record_from_mapping(loaded)
    return _record_from_legacy_mapping(loaded, dc_id)


def _upsert_self_peer(peers: tuple[PeerCacheEntry, ...], user: UserIdentity) -> tuple[PeerCacheEntry, ...]:
    """Replace stale self-peer entries with an entry derived from ``user``.

    Args:
        peers: Existing cached peer entries.
        user: Authenticated identity from which to build the self-peer entry.
    """
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
    """Convert a pre-record session mapping to the current session-record schema.

    Args:
        data: Legacy persisted session mapping.
        dc_id: Default data-center ID when the legacy mapping omits one.
    """
    payload = dict(data)
    record_data: dict[str, Any] = {
        "version": 1,
        "dc_id": _optional_int(payload.get("dc_id")) or dc_id,
        "auth_key": payload.get("auth_key") if isinstance(payload.get("auth_key"), Mapping) else None,
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
        record_data["auth_key"] = {"dc_id": record_data["dc_id"], "key": payload["auth_key"], "key_id": None}
    return session_record_from_mapping(record_data)


def _looks_like_phase2_record(data: Mapping[str, Any]) -> bool:
    """Return whether a mapping contains fields of the structured session format.

    Args:
        data: Candidate persisted session mapping.
    """
    return "version" in data and any(key in data for key in ("dc_options", "user", "update_state", "peers", "metadata"))


async def _resolve_callback(callback: Callback0) -> str:
    """Resolve synchronous or asynchronous credential callbacks to text.

    Args:
        callback: Callable returning or awaiting a credential-like value.
    """
    value = callback()
    resolved = await value if inspect.isawaitable(value) else value
    return str(resolved)


def _optional_int(value: object) -> int | None:
    """Convert a supported scalar to an integer while preserving ``None``.

    Args:
        value: Optional scalar session field to convert.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str | bytes | bytearray):
        return int(value)
    return int(str(value))


def _optional_str(value: object) -> str | None:
    """Convert a value to text while preserving ``None``.

    Args:
        value: Optional value to convert using :class:`str`.
    """
    return None if value is None else str(value)


def _emit_auth_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    """Record a duration metric and structured authorization lifecycle event.

    Args:
        event: Stable authorization event name used for metrics and logs.
        started: Monotonic start timestamp used to derive duration in milliseconds.
        outcome: Event outcome, used to choose log severity and metric attributes.
        **fields: Additional non-secret structured fields emitted with the event.
    """
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.INFO,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        **fields,
    )

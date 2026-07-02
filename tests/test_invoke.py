from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    SessionRecord,
    UserIdentity,
)
from miniproto.connection.transport import TransportClosed, TransportError
from miniproto.errors import (
    AuthKeyNotFound,
    ClientDisconnected,
    FloodPremiumWait,
    InvalidCode,
    ResultTypeMismatch,
    RpcError,
    TransportFlood,
)
from miniproto.invoke import RawSender, decode_result_payload
from miniproto.mtproto.codec import RpcErrorBody, encode_message_body
from miniproto.raw import functions, types
from miniproto.session.models import session_record_from_mapping

AUTH_KEY = b"k" * 256


def run(coro):
    return asyncio.run(coro)


@dataclass(slots=True)
class FakeSender:
    responses: list[object]
    requests: list[object] = field(default_factory=list)
    disconnected: int = 0
    is_connected: bool = True

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        self.requests.append(body)
        if not self.responses:
            raise AssertionError("fake sender has no queued response")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response

    async def disconnect(self) -> None:
        self.disconnected += 1
        self.is_connected = False


class BlockingSender:
    def __init__(self) -> None:
        self.requests: list[object] = []
        self.started = asyncio.Event()
        self.pending = 0
        self.is_connected = True

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        self.requests.append(body)
        self.pending += 1
        self.started.set()
        try:
            await asyncio.Future()
        finally:
            self.pending -= 1

    async def disconnect(self) -> None:
        self.is_connected = False


class DisconnectingSender:
    def __init__(self) -> None:
        self.requests: list[object] = []
        self.started = asyncio.Event()
        self.future: asyncio.Future[object] | None = None
        self.is_connected = True

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        self.requests.append(body)
        self.future = asyncio.get_running_loop().create_future()
        self.started.set()
        return await self.future

    async def disconnect(self) -> None:
        self.is_connected = False
        if self.future is not None and not self.future.done():
            self.future.set_exception(TransportClosed("sender disconnected"))


def nearest_dc() -> types.NearestDc:
    return types.NearestDc(country="US", this_dc=2, nearest_dc=2)


def rpc_error(code: int, text: str) -> bytes:
    return encode_message_body(RpcErrorBody(error_code=code, error_message=text))


def storage_with_auth(
    *, dc_id: int = 2, user: UserIdentity | None = None
) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=dc_id,
            auth_key=AuthKey(dc_id=dc_id, key=AUTH_KEY, key_id=123),
            dc_options=(
                DCOption(id=2, ip_address="127.0.0.1", port=443),
                DCOption(id=4, ip_address="127.0.0.1", port=444),
            ),
            user=user,
        )
    )


async def connected_client(
    sender: RawSender,
    storage: InMemorySessionStorage | None = None,
    *,
    config: ClientConfig | None = None,
) -> Client:
    client = Client(
        config
        or ClientConfig(
            api_id=1, api_hash="hash", session_storage=storage or InMemorySessionStorage()
        )
    )
    client._sender = sender
    await client.connect()
    return client


def test_invoke_wraps_request_with_layer_and_init_connection_then_decodes_result() -> None:
    async def scenario() -> None:
        request = functions.HelpGetNearestDc()
        result_object = nearest_dc()
        sender = FakeSender([result_object.serialize()])
        client = await connected_client(sender)
        result = await client.invoke(request)
        assert result == result_object
        assert len(sender.requests) == 1
        wrapped = sender.requests[0]
        assert isinstance(wrapped, functions.InvokeWithLayer)
        assert wrapped.layer == 214
        assert isinstance(wrapped.query, functions.InitConnection)
        assert wrapped.query.api_id == 1
        assert isinstance(wrapped.query.query, functions.HelpGetNearestDc)

    run(scenario())


def test_decode_result_payload_accepts_namespaced_abstract_result_type() -> None:
    user = types.User(id=42, access_hash=99, first_name="miniproto test")
    authorization = types.AuthAuthorization(user=user)
    assert decode_result_payload(authorization.serialize(), "auth.Authorization") == authorization


def test_invoke_rejects_decoded_result_that_does_not_match_request_result_type() -> None:
    async def scenario() -> None:
        client = await connected_client(FakeSender([types.BoolTrue().serialize()]))
        with pytest.raises(ResultTypeMismatch, match="NearestDc"):
            await client.invoke(functions.HelpGetNearestDc())

    run(scenario())


def test_invoke_maps_rpc_error_payloads_to_specific_public_exception_classes() -> None:
    async def scenario() -> None:
        request = functions.HelpGetNearestDc()
        client = await connected_client(FakeSender([rpc_error(400, "PHONE_CODE_INVALID")]))
        with pytest.raises(InvalidCode) as exc_info:
            await client.invoke(request)
        assert type(exc_info.value).__name__ == "PhoneCodeInvalid"
        assert exc_info.value.request is request

    run(scenario())


def test_invoke_exposes_all_generated_telegram_errors_including_flood_premium_wait() -> None:
    async def scenario() -> None:
        client = await connected_client(FakeSender([rpc_error(420, "FLOOD_PREMIUM_WAIT_7")]))
        with pytest.raises(FloodPremiumWait) as exc_info:
            await client.invoke(functions.HelpGetNearestDc())
        assert exc_info.value.seconds == 7
        assert isinstance(exc_info.value, FloodPremiumWait)

    run(scenario())


def test_invoke_sleeps_for_bounded_flood_wait_only_when_allowed() -> None:
    async def scenario() -> None:
        request = functions.HelpGetNearestDc()
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_0"), nearest_dc().serialize()])
        client = await connected_client(
            sender, config=ClientConfig(api_id=1, api_hash="hash", max_request_retries=1)
        )
        result = await client.invoke(request, flood_sleep_threshold=0)
        assert result == nearest_dc()
        assert len(sender.requests) == 2

    run(scenario())


def test_invoke_raises_flood_wait_by_default_without_sleeping() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5")])
        client = await connected_client(sender)
        with pytest.raises(TransportFlood) as exc_info:
            await client.invoke(functions.HelpGetNearestDc())
        assert exc_info.value.seconds == 5
        assert len(sender.requests) == 1

    run(scenario())


def test_invoke_retries_retryable_transport_failures_for_read_requests() -> None:
    async def scenario() -> None:
        sender = FakeSender([TransportError("temporary"), nearest_dc().serialize()])
        client = Client(ClientConfig(api_id=1, api_hash="hash", max_request_retries=1))
        client._sender_factory = lambda _record: sender
        await client.connect()
        result = await client.invoke(functions.HelpGetNearestDc())
        assert result == nearest_dc()
        assert len(sender.requests) == 2
        assert sender.disconnected == 1

    run(scenario())


def test_invoke_retries_retryable_rpc_timeout_errors_for_read_requests() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(-503, "MSG_WAIT_TIMEOUT"), nearest_dc().serialize()])
        client = Client(ClientConfig(api_id=1, api_hash="hash", max_request_retries=1))
        client._sender_factory = lambda _record: sender
        await client.connect()
        result = await client.invoke(functions.HelpGetNearestDc())
        assert result == nearest_dc()
        assert len(sender.requests) == 2

    run(scenario())


def test_invoke_does_not_retry_unsafe_requests_after_transport_failure() -> None:
    async def scenario() -> None:
        sender = FakeSender([TransportError("after send")])
        client = Client(ClientConfig(api_id=1, api_hash="hash", max_request_retries=1))
        client._sender_factory = lambda _record: sender
        await client.connect()
        request = functions.MessagesSendMessage(
            peer=types.InputPeerSelf(), message="hi", random_id=1
        )
        with pytest.raises(RpcError, match="after send"):
            await client.invoke(request)
        assert len(sender.requests) == 1

    run(scenario())


def test_invoke_handles_dc_migration_and_retries_safe_request_with_new_sender() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(dc_id=2)
        first = FakeSender([rpc_error(303, "USER_MIGRATE_4")])
        second = FakeSender([nearest_dc().serialize()])
        senders = [first, second]
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage, max_request_retries=1)
        )
        client._sender_factory = lambda _record: senders.pop(0)
        await client.connect()
        result = await client.invoke(functions.HelpGetNearestDc())
        assert result == nearest_dc()
        loaded = await storage.load()
        assert loaded is not None
        assert session_record_from_mapping(loaded).dc_id == 4
        assert first.disconnected == 1
        assert len(second.requests) == 1

    run(scenario())


def test_invoke_clears_invalid_auth_key_when_telegram_rejects_it() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(
            user=UserIdentity(id=42, access_hash=9000, username="alice", phone="+9996621234")
        )
        sender = FakeSender([rpc_error(401, "AUTH_KEY_UNREGISTERED")])
        client = await connected_client(sender, storage)
        with pytest.raises(AuthKeyNotFound):
            await client.invoke(functions.HelpGetNearestDc())
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key is None
        assert record.user is None

    run(scenario())


def test_invoke_cancellation_does_not_leave_fake_sender_pending() -> None:
    async def scenario() -> None:
        sender = BlockingSender()
        client = await connected_client(sender)
        task = asyncio.create_task(client.invoke(functions.HelpGetNearestDc()))
        await sender.started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert sender.pending == 0

    run(scenario())


def test_disconnect_surfaces_deterministic_exception_to_pending_invoke() -> None:
    async def scenario() -> None:
        sender = DisconnectingSender()
        client = await connected_client(sender)
        task = asyncio.create_task(client.invoke(functions.HelpGetNearestDc()))
        await sender.started.wait()
        await client.disconnect()
        with pytest.raises(ClientDisconnected):
            await task

    run(scenario())

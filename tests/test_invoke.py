from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, cast

import pytest
from tests.support.fake_mtproto import FakeMTProtoServer

import miniproto.invoke as invoke_module
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    SessionRecord,
    TransportConfig,
    UserIdentity,
    event_loop,
)
from miniproto.connection.sender import MTProtoSender
from miniproto.connection.transport import TransportClosed, TransportError
from miniproto.errors import (
    AuthKeyNotFound,
    AuthKeyRegenerationRequired,
    ClientDisconnected,
    FloodPremiumWait,
    FloodWait,
    InvalidCode,
    ResultTypeMismatch,
    RpcError,
)
from miniproto.invoke import (
    TELEGRAM_LAYER,
    RawSender,
    build_sender_from_session,
    decode_result_payload,
    is_retryable_request,
)
from miniproto.mtproto.codec import BadServerSalt, RpcErrorBody, RpcResult, encode_message_body
from miniproto.raw import functions, types
from miniproto.session.models import session_record_from_mapping
from miniproto.session.storage import SessionPayload

AUTH_KEY = b"k" * 256


def run(coro):
    return event_loop.run(coro)


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
            if isinstance(response, TransportClosed):
                self.is_connected = False
            raise response
        return response

    async def disconnect(self) -> None:
        self.disconnected += 1
        self.is_connected = False


class InitTrackingSender:
    """Fake sender exposing connection_initialized like the real MTProtoSender."""

    def __init__(self, responses: list[object]) -> None:
        self.responses = responses
        self.requests: list[object] = []
        self.connection_initialized = False
        self.is_connected = True
        self.disconnected = 0

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, request_timeout
        self.requests.append(body)
        if not self.responses:
            raise AssertionError("init tracking sender has no queued response")
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


class GateFailSender:
    def __init__(self, exc: Exception) -> None:
        self.requests: list[object] = []
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.exc = exc
        self.is_connected = True
        self.disconnected = 0

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, request_timeout
        self.requests.append(body)
        self.started.set()
        await self.release.wait()
        raise self.exc

    async def disconnect(self) -> None:
        self.disconnected += 1
        self.is_connected = False


class CountingSessionStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionPayload | None = None) -> None:
        super().__init__(initial)
        self.loads = 0

    async def load(self):
        self.loads += 1
        return await super().load()


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
        assert wrapped.layer == TELEGRAM_LAYER
        assert isinstance(wrapped.query, functions.InitConnection)
        assert wrapped.query.api_id == 1
        assert isinstance(wrapped.query.query, functions.HelpGetNearestDc)

    run(scenario())


def test_invoke_wraps_only_the_first_request_on_an_initializable_sender() -> None:
    async def scenario() -> None:
        sender = InitTrackingSender([nearest_dc().serialize(), nearest_dc().serialize()])
        client = await connected_client(sender)
        await client.invoke(functions.HelpGetNearestDc())
        await client.invoke(functions.HelpGetNearestDc())
        assert len(sender.requests) == 2
        first, second = sender.requests
        assert isinstance(first, functions.InvokeWithLayer)
        assert isinstance(first.query, functions.InitConnection)
        assert isinstance(first.query.query, functions.HelpGetNearestDc)
        # The connection is initialized after the first successful request; subsequent
        # requests must go out unwrapped.
        assert isinstance(second, functions.HelpGetNearestDc)

    run(scenario())


def test_invoke_rewraps_after_sender_reports_reconnect() -> None:
    async def scenario() -> None:
        sender = InitTrackingSender([nearest_dc().serialize(), nearest_dc().serialize()])
        client = await connected_client(sender)
        await client.invoke(functions.HelpGetNearestDc())
        sender.connection_initialized = False  # simulates a sender-side reconnect
        await client.invoke(functions.HelpGetNearestDc())
        assert all(isinstance(request, functions.InvokeWithLayer) for request in sender.requests)

    run(scenario())


def test_retryable_request_classification_is_cached_per_request_class() -> None:
    class CountingQualName:
        def __init__(self) -> None:
            self.calls = 0

        def __str__(self) -> str:
            self.calls += 1
            return "help.getNearestDc"

    class DummyRequest:
        QUALNAME = CountingQualName()

    assert is_retryable_request(DummyRequest())
    assert is_retryable_request(DummyRequest())
    assert DummyRequest.QUALNAME.calls == 1


def test_client_session_storage_loads_are_cached_and_invalidated_on_save() -> None:
    async def scenario() -> None:
        storage = CountingSessionStorage(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client._current_dc_id() == 2
        assert await client._current_dc_id() == 2
        assert storage.loads == 1

        await client._storage.save(
            SessionRecord(
                dc_id=4,
                auth_key=AuthKey(dc_id=4, key=AUTH_KEY, key_id=123),
                dc_options=(DCOption(id=4, ip_address="127.0.0.1", port=444),),
            )
        )
        assert await client._current_dc_id() == 4
        assert storage.loads == 1

    run(scenario())


def test_media_lane_wraps_first_request_in_invoke_without_updates() -> None:
    async def scenario() -> None:
        sender = InitTrackingSender([nearest_dc().serialize(), nearest_dc().serialize()])
        client = await connected_client(sender)

        async def ensure_sender() -> RawSender:
            return sender

        async def drop_sender(_sender: RawSender) -> None:
            return None

        await client._invoke_via_sender(
            functions.HelpGetNearestDc(),
            ensure_sender=ensure_sender,
            drop_sender=drop_sender,
            without_updates=True,
        )
        await client._invoke_via_sender(
            functions.HelpGetNearestDc(),
            ensure_sender=ensure_sender,
            drop_sender=drop_sender,
            without_updates=True,
        )
        first, second = sender.requests
        assert isinstance(first, functions.InvokeWithoutUpdates)
        assert isinstance(first.query, functions.InvokeWithLayer)
        assert isinstance(first.query.query, functions.InitConnection)
        assert isinstance(first.query.query.query, functions.HelpGetNearestDc)
        assert isinstance(second, functions.HelpGetNearestDc)

    run(scenario())


def fake_server_storage(server: FakeMTProtoServer) -> InMemorySessionStorage:
    endpoint = server.endpoint
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),),
        )
    )


def test_invoke_against_real_sender_inits_once_and_serializes_once() -> None:
    async def scenario() -> None:
        constructor_ids: list[int] = []

        def handle(message):
            constructor_ids.append(int.from_bytes(message.body[:4], "little"))
            return RpcResult(req_msg_id=message.msg_id, result=nearest_dc().serialize())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            config = ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=fake_server_storage(server),
                transport=transport,
            )
            client = Client(config)
            await client.connect()
            serialize_calls = 0
            original_serialize = functions.InvokeWithLayer.serialize

            def counting_serialize(self: Any) -> bytes:
                nonlocal serialize_calls
                serialize_calls += 1
                return original_serialize(self)

            cast(Any, functions.InvokeWithLayer).serialize = counting_serialize
            try:
                assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
                assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
            finally:
                cast(Any, functions.InvokeWithLayer).serialize = original_serialize
            assert constructor_ids == [
                functions.InvokeWithLayer.CONSTRUCTOR_ID,
                functions.HelpGetNearestDc.CONSTRUCTOR_ID,
            ]
            # The wrapped first request is serialized exactly once (no throwaway
            # validation serialization).
            assert serialize_calls == 1
            await client.disconnect()

    run(scenario())


def test_bad_server_salt_is_persisted_and_used_by_new_senders() -> None:
    async def scenario() -> None:
        new_salt = 0x0102030405060708
        content_messages = 0

        def handle(message):
            nonlocal content_messages
            if message.seq_no % 2 == 0:
                return None
            content_messages += 1
            if content_messages == 1:
                return BadServerSalt(
                    bad_msg_id=message.msg_id,
                    bad_msg_seq_no=message.seq_no,
                    error_code=48,
                    new_server_salt=new_salt,
                )
            return RpcResult(req_msg_id=message.msg_id, result=nearest_dc().serialize())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            storage = fake_server_storage(server)
            config = ClientConfig(
                api_id=1, api_hash="hash", session_storage=storage, transport=transport
            )
            client = Client(config)
            await client.connect()
            assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
            await client.disconnect()
            loaded = await storage.load()
            assert loaded is not None
            record = session_record_from_mapping(loaded)
            assert record.metadata["server_salt"] == new_salt
            rebuilt = await build_sender_from_session(config, storage)
            assert isinstance(rebuilt, MTProtoSender)
            assert rebuilt.state.server_salt == new_salt

    run(scenario())


def test_build_sender_uses_fresh_session_id_while_preserving_server_salt(monkeypatch) -> None:
    async def scenario() -> None:
        storage = storage_with_auth()
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        await storage.save(
            SessionRecord(
                dc_id=record.dc_id,
                auth_key=record.auth_key,
                dc_options=record.dc_options,
                metadata={"session_id": 0xAAAAAAAAAAAAAAAA, "server_salt": 0x1234},
            )
        )
        generated = iter((0x1111111111111111, 0x2222222222222222))
        monkeypatch.setattr(invoke_module.secrets, "randbits", lambda _bits: next(generated))
        config = ClientConfig(api_id=1, api_hash="hash", session_storage=storage)

        first = await build_sender_from_session(config, storage)
        second = await build_sender_from_session(config, storage)

        assert isinstance(first, MTProtoSender)
        assert isinstance(second, MTProtoSender)
        assert first.state.server_salt == 0x1234
        assert second.state.server_salt == 0x1234
        assert first.state.session_id == 0x1111111111111111
        assert second.state.session_id == 0x2222222222222222

    run(scenario())


def test_auth_key_duplicated_drops_sender_without_clearing_stored_key() -> None:
    async def scenario() -> None:
        storage = storage_with_auth()
        sender = FakeSender([rpc_error(406, "AUTH_KEY_DUPLICATED")])
        client = await connected_client(sender, storage=storage)
        with pytest.raises(AuthKeyRegenerationRequired):
            await client.invoke(functions.HelpGetNearestDc())
        loaded = await storage.load()
        assert loaded is not None
        assert session_record_from_mapping(loaded).auth_key is not None
        assert sender.disconnected == 1

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
        with pytest.raises(FloodWait) as exc_info:
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
        assert sender.disconnected == 0

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
        request = functions.MessagesEditMessage(peer=types.InputPeerSelf(), id=1, message="hi")
        with pytest.raises(RpcError, match="after send"):
            await client.invoke(request)
        assert len(sender.requests) == 1
        assert sender.disconnected == 0

    run(scenario())


def test_invoke_retries_random_id_message_requests_after_transport_failure() -> None:
    async def scenario() -> None:
        response = types.UpdateShortSentMessage(id=10, pts=1, pts_count=1, date=1_700_000_000)
        sender = FakeSender([TransportError("after send"), response.serialize()])
        client = Client(ClientConfig(api_id=1, api_hash="hash", max_request_retries=1))
        client._sender_factory = lambda _record: sender
        await client.connect()
        request = functions.MessagesSendMessage(
            peer=types.InputPeerSelf(), message="hi", random_id=1
        )
        assert is_retryable_request(request)
        assert await client.invoke(request) == response
        assert len(sender.requests) == 2
        assert sender.disconnected == 0

    run(scenario())


def test_invoke_classifies_transport_failure_from_dead_sender_as_client_disconnected() -> None:
    async def scenario() -> None:
        sender = FakeSender([TransportClosed("sender disconnected")])
        client = await connected_client(
            sender, config=ClientConfig(api_id=1, api_hash="hash", max_request_retries=0)
        )
        with pytest.raises(ClientDisconnected):
            await client.invoke(functions.HelpGetNearestDc())
        assert sender.disconnected == 0

    run(scenario())


def test_invoke_does_not_drop_replacement_sender_from_stale_failure() -> None:
    async def scenario() -> None:
        first = GateFailSender(TransportError("old sender failed"))
        second = FakeSender([nearest_dc().serialize()])
        client = await connected_client(
            first, config=ClientConfig(api_id=1, api_hash="hash", max_request_retries=1)
        )
        task = asyncio.create_task(client.invoke(functions.HelpGetNearestDc()))
        await first.started.wait()
        client._sender = second
        first.release.set()
        result = await task
        assert result == nearest_dc()
        # Per-request failures never tear down connections anymore; the stale sender
        # is simply left alone and the retry proceeds on the replacement.
        assert first.disconnected == 0
        assert second.disconnected == 0
        assert len(second.requests) == 1

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

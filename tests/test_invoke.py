from __future__ import annotations

import asyncio
import gzip
from collections.abc import Callable, Coroutine, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
from tools.bench.fake_mtproto import FakeMTProtoServer

import miniproto.client as client_module
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
from miniproto.auth.bootstrap import ensure_auth_key
from miniproto.auth.key_exchange import AuthKeyExchangeResult
from miniproto.auth.service import AuthService
from miniproto.client import _CachedSessionStorage, _MediaInvokeContext
from miniproto.connection.sender import MTProtoSender
from miniproto.connection.transport import TransportClosed, TransportError
from miniproto.errors import (
    AmbiguousRpcResult,
    AuthKeyNotFound,
    AuthKeyRegenerationRequired,
    ClientDisconnected,
    DatacenterMigration,
    FloodPremiumWait,
    FloodWait,
    InvalidCode,
    InvalidDatacenter,
    ProtocolValidationError,
    ResultTypeMismatch,
    RpcError,
    SessionStorageError,
    classify_rpc_error,
)
from miniproto.invoke import (
    TELEGRAM_LAYER,
    MethodFloodWaitCache,
    RawSender,
    build_sender_from_session,
    clear_invalid_auth_key,
    decode_result_payload,
    is_retryable_request,
    load_session_record,
)
from miniproto.mtproto.codec import BadServerSalt, GzipPacked, RpcErrorBody, RpcResult, encode_message_body, gzip_pack
from miniproto.observability import InMemoryMetrics, get_metrics_sink, set_metrics_sink
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, UpdateState, session_record_from_mapping
from miniproto.session.storage import EncryptedSQLiteSessionStorage, SessionPayload, SessionStorage

AUTH_KEY = b"k" * 256


def run(coro):
    return event_loop.run(coro)


@dataclass(slots=True)
class FakeSender:
    responses: list[object]
    requests: list[object] = field(default_factory=list)
    retry_safety: list[bool] = field(default_factory=list)
    disconnected: int = 0
    is_connected: bool = True
    auth_key_dc_id: int | None = None
    state: SimpleNamespace | None = None

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        self.requests.append(body)
        self.retry_safety.append(retry_safe)
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
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
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
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
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
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
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
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
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


class BlockingCountingSessionStorage(CountingSessionStorage):
    def __init__(self, initial: SessionPayload | None = None) -> None:
        super().__init__(initial)
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def load(self):
        self.loads += 1
        self.started.set()
        await self.release.wait()
        return await InMemorySessionStorage.load(self)


class FailingSessionStorage(InMemorySessionStorage):
    def __init__(self, initial: SessionPayload | None = None) -> None:
        super().__init__(initial)
        self.fail_save = False
        self.fail_mutate = False

    async def save(self, data: SessionPayload) -> None:
        if self.fail_save:
            raise SessionStorageError("save failed")
        await super().save(data)

    async def mutate(self, transform):
        if self.fail_mutate:
            raise SessionStorageError("mutate failed")
        return await super().mutate(transform)


class MutationOnlySessionStorage(InMemorySessionStorage):
    async def save(self, data: SessionPayload) -> None:
        del data
        raise AssertionError("read-modify-write persistence must use atomic mutate")


def test_cached_session_storage_serializes_concurrent_first_loads() -> None:
    async def scenario() -> None:
        backend = BlockingCountingSessionStorage({"value": 1})
        storage = _CachedSessionStorage(backend)
        first_task = asyncio.create_task(storage.load())
        second_task = asyncio.create_task(storage.load())
        await backend.started.wait()
        await asyncio.sleep(0)
        backend.release.set()
        first, second = await asyncio.gather(first_task, second_task)
        assert first == {"value": 1}
        assert second == {"value": 1}
        assert backend.loads == 1

    run(scenario())


def test_cached_session_storage_updates_cache_and_revisions_only_after_commit() -> None:
    async def scenario() -> None:
        backend = FailingSessionStorage({"value": 1})
        storage = _CachedSessionStorage(backend)
        assert await storage.load() == {"value": 1}
        revisions_before = dict(storage.domain_revisions())

        backend.fail_save = True
        with pytest.raises(SessionStorageError, match="save failed"):
            await storage.save({"value": 2})
        assert await storage.load() == {"value": 1}
        assert storage.domain_revisions() == revisions_before

        backend.fail_save = False
        backend.fail_mutate = True
        with pytest.raises(SessionStorageError, match="mutate failed"):
            await storage.mutate(lambda payload: {"value": 3})
        assert await storage.load() == {"value": 1}
        assert storage.domain_revisions() == revisions_before

        backend.fail_mutate = False

        def increment(payload):
            assert payload is not None
            return {"value": int(payload["value"]) + 1}

        committed = await storage.mutate(increment)
        assert committed == {"value": 2}
        assert await storage.load() == {"value": 2}
        assert storage.domain_revisions()["payload"] == revisions_before["payload"] + 1

    run(scenario())


def nearest_dc() -> types.NearestDc:
    return types.NearestDc(country="US", this_dc=2, nearest_dc=2)


def rpc_error(code: int, text: str) -> bytes:
    return encode_message_body(RpcErrorBody(error_code=code, error_message=text))


def storage_with_auth(*, dc_id: int = 2, user: UserIdentity | None = None) -> InMemorySessionStorage:
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
    sender: RawSender, storage: InMemorySessionStorage | None = None, *, config: ClientConfig | None = None
) -> Client:
    client = Client(
        config or ClientConfig(api_id=1, api_hash="hash", session_storage=storage or InMemorySessionStorage())
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
            functions.HelpGetNearestDc(), ensure_sender=ensure_sender, drop_sender=drop_sender, without_updates=True
        )
        await client._invoke_via_sender(
            functions.HelpGetNearestDc(), ensure_sender=ensure_sender, drop_sender=drop_sender, without_updates=True
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
                api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
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
                    bad_msg_id=message.msg_id, bad_msg_seq_no=message.seq_no, error_code=48, new_server_salt=new_salt
                )
            return RpcResult(req_msg_id=message.msg_id, result=nearest_dc().serialize())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            storage = fake_server_storage(server)
            config = ClientConfig(api_id=1, api_hash="hash", session_storage=storage, transport=transport)
            client = Client(config)
            await client.connect()
            assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
            await client._flush_server_salt()
            loaded = await storage.load()
            assert loaded is not None
            record = session_record_from_mapping(loaded)
            assert record.metadata["server_salt"] == new_salt
            await client.disconnect()
            reopened = InMemorySessionStorage(loaded)
            rebuilt = await build_sender_from_session(config, reopened)
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


@pytest.mark.parametrize("as_object", [False, True])
def test_decode_result_payload_bounds_gzip_and_preserves_concatenated_members(as_object: bool) -> None:
    expected = nearest_dc()
    serialized = expected.serialize()
    midpoint = len(serialized) // 2
    packed = GzipPacked(gzip.compress(serialized[:midpoint]) + gzip.compress(serialized[midpoint:]) + b"\x00\x00")
    data = packed if as_object else encode_message_body(packed)
    assert decode_result_payload(data, "NearestDc", max_output_size=len(serialized)) == expected
    with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
        decode_result_payload(data, "NearestDc", max_output_size=len(serialized) - 1)


def test_decode_result_payload_bounds_gzip_nesting() -> None:
    expected = nearest_dc()
    packed: object = expected
    for _ in range(16):
        packed = gzip_pack(packed)
    assert decode_result_payload(encode_message_body(packed), "NearestDc") == expected
    with pytest.raises(ProtocolValidationError, match="gzip_wrapper_depth"):
        decode_result_payload(encode_message_body(gzip_pack(packed)), "NearestDc")


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
            sender,
            config=ClientConfig(
                api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=1
            ),
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


def test_invoke_reuses_method_flood_wait_before_touching_the_sender() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5")])
        client = await connected_client(sender)
        request = functions.HelpGetNearestDc()

        with pytest.raises(FloodWait) as server_wait:
            await client.invoke(request)
        with pytest.raises(FloodWait) as cached_wait:
            await client.invoke(request)

        assert server_wait.value.seconds == 5
        assert cached_wait.value.seconds == 5
        assert cached_wait.value.request is request
        assert len(sender.requests) == 1

    run(scenario())


def test_invoke_method_flood_cache_keys_the_innermost_wrapped_request() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(420, "FLOOD_PREMIUM_WAIT_7")])
        client = await connected_client(sender)
        request = functions.HelpGetNearestDc()
        wrapped = functions.InvokeWithoutUpdates(query=request)

        with pytest.raises(FloodPremiumWait):
            await client.invoke(wrapped)
        with pytest.raises(FloodPremiumWait) as cached_wait:
            await client.invoke(request)

        assert cached_wait.value.seconds == 7
        assert cached_wait.value.request is request
        assert len(sender.requests) == 1

    run(scenario())


def test_invoke_does_not_share_slowmode_waits_between_request_arguments() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(420, "SLOWMODE_WAIT_5"), rpc_error(420, "SLOWMODE_WAIT_6")])
        client = await connected_client(sender)
        request = functions.HelpGetNearestDc()

        with pytest.raises(FloodWait) as first_wait:
            await client.invoke(request)
        with pytest.raises(FloodWait) as second_wait:
            await client.invoke(request)

        assert type(first_wait.value).__name__ == "SlowmodeWait"
        assert type(second_wait.value).__name__ == "SlowmodeWait"
        assert len(sender.requests) == 2

    run(scenario())


def test_method_flood_cache_is_bounded_lazily_expires_and_never_shortens_a_deadline() -> None:
    now = [100.0]
    cache = MethodFloodWaitCache(2, clock=lambda: now[0])
    first = type("FirstRequest", (), {"QUALNAME": "help.first"})()
    second = type("SecondRequest", (), {"QUALNAME": "help.second"})()
    third = type("ThirdRequest", (), {"QUALNAME": "help.third"})()

    assert cache.remember(first, FloodWait(10, message="FLOOD_WAIT_10"))
    now[0] += 1
    assert cache.remember(first, FloodWait(2, message="FLOOD_WAIT_2"))
    active = cache.get(first)
    assert active is not None and active.seconds == 9

    assert cache.remember(second, FloodPremiumWait(4, message="FLOOD_PREMIUM_WAIT_4"))
    assert cache.remember(third, FloodWait(3, message="FLOOD_WAIT_3"))
    assert len(cache) == 2
    assert cache.get(first) is None
    premium = cache.get(second)
    assert isinstance(premium, FloodPremiumWait)

    now[0] += 5
    assert cache.get(second) is None
    assert cache.get(third) is None
    assert len(cache) == 0


def test_invoke_concurrent_callers_share_a_populated_method_wait() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5")])
        client = await connected_client(sender)
        first, second = await asyncio.gather(
            client.invoke(functions.HelpGetNearestDc()),
            client.invoke(functions.HelpGetNearestDc()),
            return_exceptions=True,
        )

        assert isinstance(first, FloodWait)
        assert isinstance(second, FloodWait)
        assert len(sender.requests) == 1

    run(scenario())


def test_invoke_method_flood_cache_does_not_block_distinct_methods() -> None:
    class FirstRequest:
        QUALNAME = "help.first"

    class SecondRequest:
        QUALNAME = "help.second"

    async def scenario() -> None:
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5"), rpc_error(420, "FLOOD_WAIT_6")])
        client = await connected_client(sender)
        with pytest.raises(FloodWait) as first_wait:
            await client.invoke(FirstRequest())
        with pytest.raises(FloodWait) as second_wait:
            await client.invoke(SecondRequest())
        assert first_wait.value.seconds == 5
        assert second_wait.value.seconds == 6
        assert len(sender.requests) == 2

    run(scenario())


def test_client_config_rejects_non_positive_method_flood_cache_size() -> None:
    with pytest.raises(ValueError, match="method_flood_cache_size"):
        ClientConfig(api_id=1, api_hash="hash", method_flood_cache_size=0)


def test_invoke_cached_flood_wait_can_sleep_before_sending(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        now = [100.0]
        sleeps: list[float] = []

        async def advance_clock(delay: float) -> None:
            sleeps.append(delay)
            now[0] += delay

        monkeypatch.setattr(client_module.asyncio, "sleep", advance_clock)
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_2"), nearest_dc().serialize()])
        client = await connected_client(sender)
        client._method_flood_wait_cache = MethodFloodWaitCache(8, clock=lambda: now[0])

        with pytest.raises(FloodWait):
            await client.invoke(functions.HelpGetNearestDc())
        result = await client.invoke(functions.HelpGetNearestDc(), flood_sleep_threshold=2)

        assert result == nearest_dc()
        assert sleeps == [2]
        assert len(sender.requests) == 2

    run(scenario())


def test_invoke_cached_flood_sleep_is_cancellation_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        async def cancel_sleep(_delay: float) -> None:
            raise asyncio.CancelledError

        monkeypatch.setattr(client_module.asyncio, "sleep", cancel_sleep)
        sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5")])
        client = await connected_client(sender)
        with pytest.raises(FloodWait):
            await client.invoke(functions.HelpGetNearestDc())
        with pytest.raises(asyncio.CancelledError):
            await client.invoke(functions.HelpGetNearestDc(), flood_sleep_threshold=5)
        with pytest.raises(FloodWait):
            await client.invoke(functions.HelpGetNearestDc())
        assert len(sender.requests) == 1

    run(scenario())


def test_invoke_flood_metrics_distinguish_server_and_cache_without_arguments() -> None:
    async def scenario() -> None:
        metrics = InMemoryMetrics()
        previous = get_metrics_sink()
        set_metrics_sink(metrics)
        try:
            sender = FakeSender([rpc_error(420, "FLOOD_WAIT_5")])
            client = await connected_client(sender)
            request = functions.HelpGetNearestDc()
            with pytest.raises(FloodWait):
                await client.invoke(request)
            with pytest.raises(FloodWait):
                await client.invoke(request)
        finally:
            set_metrics_sink(previous)

        waits = [event for event in metrics.events if event.name == "rpc.flood_wait_seconds"]
        assert [event.attributes["source"] for event in waits] == ["server", "cache"]
        assert all(event.attributes["request"] == "help.getNearestDc" for event in waits)
        assert all(event.attributes["remaining_seconds"] == 5 for event in waits)
        assert all(event.attributes["threshold"] is None for event in waits)
        assert all(event.attributes["action"] == "raise" for event in waits)
        assert all("request_args" not in event.attributes for event in waits)

    run(scenario())


def test_invoke_retries_retryable_transport_failures_for_read_requests() -> None:
    async def scenario() -> None:
        sender = FakeSender([TransportError("temporary"), nearest_dc().serialize()])
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=1)
        )
        client._sender_factory = lambda _record: sender
        await client.connect()
        result = await client.invoke(functions.HelpGetNearestDc())
        assert result == nearest_dc()
        assert len(sender.requests) == 2
        assert sender.retry_safety == [True, True]
        assert sender.disconnected == 0

    run(scenario())


def test_invoke_retries_retryable_rpc_timeout_errors_for_read_requests() -> None:
    async def scenario() -> None:
        sender = FakeSender([rpc_error(-503, "MSG_WAIT_TIMEOUT"), nearest_dc().serialize()])
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=1)
        )
        client._sender_factory = lambda _record: sender
        await client.connect()
        result = await client.invoke(functions.HelpGetNearestDc())
        assert result == nearest_dc()
        assert len(sender.requests) == 2

    run(scenario())


def test_invoke_does_not_retry_unsafe_requests_after_transport_failure() -> None:
    async def scenario() -> None:
        sender = FakeSender([TransportError("after send")])
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=1)
        )
        client._sender_factory = lambda _record: sender
        await client.connect()
        request = functions.MessagesEditMessage(peer=types.InputPeerSelf(), id=1, message="hi")
        with pytest.raises(RpcError, match="after send"):
            await client.invoke(request)
        assert len(sender.requests) == 1
        assert sender.retry_safety == [False]
        assert sender.disconnected == 0

    run(scenario())


@pytest.mark.parametrize(
    ("callback", "retry_override", "expect_retry"),
    [(True, None, False), (False, None, True), (True, True, True), (False, False, False)],
)
def test_callback_button_replay_differs_from_reads_and_honors_override(
    callback: bool, retry_override: bool | None, expect_retry: bool
) -> None:
    async def scenario() -> None:
        request = (
            functions.MessagesGetBotCallbackAnswer(peer=types.InputPeerSelf(), msg_id=42, data=b"press")
            if callback
            else functions.MessagesGetMessages(id=())
        )
        expected = (
            types.MessagesBotCallbackAnswer(cache_time=0)
            if callback
            else types.MessagesMessages(messages=(), topics=(), chats=(), users=())
        )
        retried_calls = 0

        def handle(message):
            nonlocal retried_calls
            if message.seq_no % 2 == 0:
                return None
            retried_calls += 1
            return RpcResult(req_msg_id=message.msg_id, result=expected.serialize())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=60)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle, drop_connections_after_packet=1) as server:
            client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport))  # fmt: skip
            try:
                await client.connect()
                if expect_retry:
                    assert await client.invoke(request, retry=retry_override, request_timeout=3) == expected
                else:
                    with pytest.raises(AmbiguousRpcResult):
                        await client.invoke(request, retry=retry_override, request_timeout=3)
                assert retried_calls == int(expect_retry)
            finally:
                await client.disconnect()

    run(scenario())


def test_invoke_retries_random_id_message_requests_after_transport_failure() -> None:
    async def scenario() -> None:
        response = types.UpdateShortSentMessage(id=10, pts=1, pts_count=1, date=1_700_000_000)
        sender = FakeSender([TransportError("after send"), response.serialize()])
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=1)
        )
        client._sender_factory = lambda _record: sender
        await client.connect()
        request = functions.MessagesSendMessage(peer=types.InputPeerSelf(), message="hi", random_id=1)
        assert is_retryable_request(request)
        assert await client.invoke(request) == response
        assert len(sender.requests) == 2
        assert sender.retry_safety == [True, True]
        assert sender.disconnected == 0

    run(scenario())


def test_invoke_classifies_transport_failure_from_dead_sender_as_client_disconnected() -> None:
    async def scenario() -> None:
        sender = FakeSender([TransportClosed("sender disconnected")])
        client = await connected_client(
            sender,
            config=ClientConfig(
                api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=0
            ),
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
            first,
            config=ClientConfig(
                api_id=1, api_hash="hash", session_storage=InMemorySessionStorage(), max_request_retries=1
            ),
        )
        task = asyncio.create_task(client.invoke(functions.HelpGetNearestDc()))
        await first.started.wait()
        client._sender = second
        first.release.set()
        result = await task
        assert result == nearest_dc()
        # A stale failure must leave the replacement sender connected so the retry can use it
        assert first.disconnected == 0
        assert second.disconnected == 0
        assert len(second.requests) == 1

    run(scenario())


def test_invoke_handles_dc_migration_and_retries_safe_request_with_new_sender(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        storage = storage_with_auth(dc_id=2)
        first = FakeSender([rpc_error(303, "USER_MIGRATE_4")])
        migration_sender = FakeSender([])
        second = FakeSender([nearest_dc().serialize()])
        senders = [first, migration_sender, second]
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, max_request_retries=1))
        client._sender_factory = lambda _record: senders.pop(0)

        async def ensure_target_auth(dc_id: int) -> tuple[bytes, int]:
            assert dc_id == 4
            return b"t" * 256, 456

        monkeypatch.setattr(client, "_ensure_media_dc_auth", ensure_target_auth)
        await client.connect()
        result = await client.invoke(functions.HelpGetNearestDc())
        assert result == nearest_dc()
        loaded = await storage.load()
        assert loaded is not None
        assert session_record_from_mapping(loaded).dc_id == 4
        assert first.disconnected == 1
        assert migration_sender.disconnected == 1
        assert len(second.requests) == 1

    run(scenario())


def test_main_dc_migration_imports_authorization_and_activates_target_key(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        user_identity = UserIdentity(id=42, access_hash=9000, username="alice")
        raw_user = types.User(self_=True, id=42, access_hash=9000, username="alice")
        storage = storage_with_auth(user=user_identity)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        old_sender = FakeSender([])
        exported = types.AuthExportedAuthorization(id=55, bytes=b"exported")
        target_key = b"t" * 256
        target_salt = 456
        temporary = FakeSender([types.AuthAuthorization(user=raw_user).serialize()])

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.AuthExportAuthorization)
            assert request.dc_id == 4
            return exported

        async def ensure_target_auth(dc_id: int) -> tuple[bytes, int]:
            assert dc_id == 4
            return target_key, target_salt

        async def build_target(*args: object, **kwargs: object) -> RawSender:
            del args
            assert kwargs["dc_id_override"] == 4
            assert kwargs["auth_key_override"] == target_key
            return temporary

        monkeypatch.setattr(client, "invoke", invoke)
        monkeypatch.setattr(client, "_ensure_media_dc_auth", ensure_target_auth)
        monkeypatch.setattr(client_module, "build_sender_from_session", build_target)

        await client._migrate_main_session(old_sender, DatacenterMigration(4, kind="USER"))

        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.dc_id == 4
        assert record.auth_key is not None
        assert record.auth_key.dc_id == 4
        assert record.auth_key.key == target_key
        assert record.metadata["server_salt"] == target_salt
        assert record.metadata["dc_auth"]["2"]["key"] == AUTH_KEY
        assert temporary.disconnected == 1
        assert temporary.requests

    run(scenario())


def test_auth_request_does_not_force_ambiguous_transport_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        observed: list[bool | None] = []

        async def invoke(request: object, *, retry: bool | None = None, **kwargs: object) -> object:
            del request, kwargs
            observed.append(retry)
            return types.AuthSentCode(type=types.AuthSentCodeTypeApp(length=5), phone_code_hash="hash")

        monkeypatch.setattr(client, "invoke", invoke)

        await client._invoke_auth_request(
            functions.AuthSendCode(phone_number="+1", api_id=1, api_hash="hash", settings=types.CodeSettings())
        )

        assert observed == [False]

    run(scenario())


def test_invoke_clears_invalid_auth_key_when_telegram_rejects_it() -> None:
    async def scenario() -> None:
        storage = storage_with_auth(user=UserIdentity(id=42, access_hash=9000, username="alice", phone="+9996621234"))
        sender = FakeSender([rpc_error(401, "AUTH_KEY_UNREGISTERED")], auth_key_dc_id=2, state=SimpleNamespace(auth_key=AUTH_KEY))  # fmt: skip
        client = await connected_client(sender, storage)
        with pytest.raises(AuthKeyNotFound):
            await client.invoke(functions.HelpGetNearestDc())
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key is None
        assert record.user is None

    run(scenario())


def test_invalid_auth_clear_uses_atomic_mutation_and_preserves_unrelated_state() -> None:
    async def scenario() -> None:
        storage = MutationOnlySessionStorage(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
                user=UserIdentity(id=42, access_hash=9000),
                metadata={"server_salt": 123},
            )
        )
        await clear_invalid_auth_key(storage, ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key is None
        assert record.user is None
        assert record.metadata["server_salt"] == 123

    run(scenario())


def test_server_salt_persistence_uses_atomic_mutation() -> None:
    async def scenario() -> None:
        storage = MutationOnlySessionStorage(
            SessionRecord(dc_id=2, peers=(PeerCacheEntry(id=42, kind="user", access_hash=9000),))
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._latest_server_salt = 456
        client._salt_dirty = True
        await client._persist_server_salt()
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.metadata["server_salt"] == 456
        assert record.peers[0].id == 42

    run(scenario())


def test_auth_bootstrap_and_service_persistence_use_atomic_mutation() -> None:
    async def scenario() -> None:
        auth_key = AuthKey(dc_id=2, key=AUTH_KEY, key_id=123)
        storage = MutationOnlySessionStorage(SessionRecord(dc_id=2, auth_key=auth_key))
        config = ClientConfig(api_id=1, api_hash="hash", session_storage=storage)
        await ensure_auth_key(config, storage)
        service = AuthService(config, storage, lambda _request: None)
        options = await service.persist_dc_options(
            SimpleNamespace(
                this_dc=2,
                dc_options=(
                    types.DcOption(id=2, ip_address="149.154.167.50", port=443),
                    types.DcOption(id=4, ip_address="149.154.167.91", port=443),
                ),
            )
        )
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key == auth_key
        assert record.dc_options == options

    run(scenario())


@pytest.mark.parametrize("media_only", [False, True])
def test_media_dc_auth_persistence_uses_atomic_mutation(monkeypatch: pytest.MonkeyPatch, media_only: bool) -> None:
    async def scenario() -> None:
        exchanged_roles: list[bool] = []

        class FakeTransport:
            def __init__(self, *args, **kwargs) -> None:
                del args, kwargs

            async def close(self) -> None:
                return None

        class FakeExchange:
            def __init__(self, *args, **kwargs) -> None:
                del args
                assert kwargs["dc_id"] == 4
                exchanged_roles.append(kwargs["media_only"])

            async def create_auth_key(self):
                return SimpleNamespace(auth_key=b"m" * 256, server_salt=789)

        monkeypatch.setattr("miniproto.client.UnencryptedAuthKeyTransport", FakeTransport)
        monkeypatch.setattr("miniproto.client.AuthKeyExchange", FakeExchange)
        storage = MutationOnlySessionStorage(
            SessionRecord(
                dc_id=2,
                dc_options=(
                    DCOption(id=2, ip_address="127.0.0.1", port=443),
                    DCOption(id=4, ip_address="127.0.0.1", port=444, media_only=media_only),
                ),
                update_state=UpdateState(pts=17),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client._ensure_media_dc_auth(4) == (b"m" * 256, 789)
        assert exchanged_roles == [media_only]
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.update_state.pts == 17
        assert record.metadata["dc_auth"]["4"] == {"key": b"m" * 256, "salt": 789}

    run(scenario())


def test_cdn_sender_uses_cdn_endpoint_and_cdn_public_key(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        cdn_option = DCOption(id=4, ip_address="203.0.113.4", port=443, media_only=True, cdn=True)
        storage = InMemorySessionStorage(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443), cdn_option),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        cdn_key = object()
        sender = FakeSender([])
        observed: dict[str, object] = {}

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.HelpGetCdnConfig)
            return types.CdnConfig(public_keys=(types.CdnPublicKey(dc_id=4, public_key="cdn-pem"),))

        class FakeTransport:
            def __init__(self, endpoint: object, config: ClientConfig) -> None:
                del config
                observed["endpoint"] = endpoint

            async def close(self) -> None:
                observed["transport_closed"] = True

        class FakeExchange:
            def __init__(self, transport: object, *, dc_id: int, rsa_keys: object, test_mode: bool, media_only: bool) -> None:  # fmt: skip
                del transport, test_mode
                observed["exchange_dc_id"] = dc_id
                observed["media_only"] = media_only
                observed["rsa_keys"] = rsa_keys

            async def create_auth_key(self) -> object:
                return SimpleNamespace(auth_key=b"c" * 256, server_salt=789)

        async def build_target(*args: object, **kwargs: object) -> RawSender:
            del args
            observed["build_kwargs"] = kwargs
            return sender

        monkeypatch.setattr(client, "invoke", invoke)
        monkeypatch.setattr(client_module, "rsa_key_from_pem", lambda pem: cdn_key if pem == "cdn-pem" else None)
        monkeypatch.setattr(client_module, "UnencryptedAuthKeyTransport", FakeTransport)
        monkeypatch.setattr(client_module, "AuthKeyExchange", FakeExchange)
        monkeypatch.setattr(client_module, "build_sender_from_session", build_target)

        assert await client._get_cdn_sender(4) is sender
        endpoint = cast(Any, observed["endpoint"])
        assert (endpoint.host, endpoint.port) == ("203.0.113.4", 443)
        assert observed["exchange_dc_id"] == 4
        assert observed["media_only"] is False
        assert observed["rsa_keys"] == (cdn_key,)
        assert observed["transport_closed"] is True
        assert cast(dict[str, object], observed["build_kwargs"])["dc_id_override"] == 4
        assert cast(dict[str, object], observed["build_kwargs"])["auth_key_override"] == b"c" * 256

    run(scenario())


def test_media_invoke_context_routes_cdn_rpc_through_cdn_sender(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        sender = FakeSender([types.UploadCdnFile(bytes=b"cdn").serialize()])
        observed: list[int] = []

        async def get_cdn_sender(dc_id: int) -> RawSender:
            observed.append(dc_id)
            return sender

        monkeypatch.setattr(client, "_get_cdn_sender", get_cdn_sender)
        await client.connect()
        context = _MediaInvokeContext(client, 0, kind="download")
        result = await context.invoke_cdn(
            functions.UploadGetCdnFile(file_token=b"token", offset=0, limit=4096), dc_id=4
        )

        assert result == types.UploadCdnFile(bytes=b"cdn")
        assert observed == [4]
        assert sender.requests

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


PRIMARY_KEY = b"p" * 256


SECONDARY_KEY = b"s" * 256


REPLACEMENT_KEY = b"r" * 256


UNRELATED_KEY = b"u" * 256


STORAGE_KEY = b"synthetic-storage-key-for-tests"


def stored_record() -> SessionRecord:
    return SessionRecord(
        dc_id=2,
        auth_key=AuthKey(dc_id=2, key=PRIMARY_KEY),
        user=UserIdentity(id=42, username="synthetic"),
        dc_options=(DCOption(id=2, ip_address="127.0.0.2", port=443), DCOption(id=4, ip_address="127.0.0.4", port=443)),
        metadata={
            "server_salt": 17,
            "unrelated": "retained",
            "dc_auth": {"4": {"key": SECONDARY_KEY, "salt": 23}, "5": {"key": UNRELATED_KEY, "salt": 29}},
        },
    )


def auth_error(name: str, representation: str) -> object:
    if representation == "wire":
        return encode_message_body(RpcErrorBody(error_code=401, error_message=name))
    if representation == "generated":
        return types.Error(code=401, text=name).serialize()
    error = RpcError(name, code=401)
    return classify_rpc_error(error) if representation == "typed" else error


class KeyedSender:
    def __init__(self, dc_id: int, key: bytes, response: object, *, blocked: bool = False) -> None:
        self.auth_key_dc_id = dc_id
        self.state = SimpleNamespace(auth_key=key)
        self.response = response
        self.is_connected = True
        self.disconnected = 0
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        if not blocked:
            self.release.set()

    async def request(self, body: object, *, content_related: bool = True, retry_safe: bool, request_timeout: float | None = None) -> object:  # fmt: skip
        del body, content_related, retry_safe, request_timeout
        self.started.set()
        await self.release.wait()
        if isinstance(self.response, BaseException):
            raise self.response
        return self.response

    async def disconnect(self) -> None:
        self.disconnected += 1
        self.is_connected = False


def client_for(storage: SessionStorage) -> Client:
    client = Client(ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage, media_idle_close=None))
    client._connected = True
    return client


async def install_route(client: Client, sender: KeyedSender, route: str) -> Callable[[], Coroutine[Any, Any, object]]:
    if route == "main":
        client._sender = sender

        async def invoke_main() -> object:
            return await client.invoke(functions.HelpGetNearestDc())

        return invoke_main
    dc_id = sender.auth_key_dc_id
    if route == "cdn":
        client._cdn_senders[dc_id] = sender
        context = _MediaInvokeContext(client, 0, kind="download")

        async def invoke_cdn() -> object:
            return await context.invoke_cdn(functions.UploadGetCdnFile(file_token=b"synthetic", offset=0, limit=4096), dc_id=dc_id)  # fmt: skip

        return invoke_cdn
    assert route == "download" or route == "upload"
    pool = await client._get_media_pool(kind=route, lane_count=1, dc_id=dc_id)
    pool._lanes[0]._sender = sender

    async def invoke_media() -> object:
        async with _MediaInvokeContext(client, 1, kind=route, dc_id=dc_id) as context:
            request = (
                functions.UploadSaveFilePart(file_id=1, file_part=0, bytes=b"synthetic")
                if route == "upload"
                else functions.UploadGetFile(
                    location=types.InputDocumentFileLocation(
                        id=1, access_hash=2, file_reference=b"synthetic", thumb_size=""
                    ),
                    offset=0,
                    limit=4096,
                )
            )
            return await context(request)

    return invoke_media


@pytest.mark.parametrize("route", ["cdn", "download", "upload"])
@pytest.mark.parametrize("name", ["AUTH_KEY_INVALID", "AUTH_KEY_PERM_EMPTY", "AUTH_KEY_UNREGISTERED"])
def test_secondary_failure_preserves_primary_login_on_disk(tmp_path: Path, route: str, name: str) -> None:
    async def scenario() -> None:
        path = tmp_path / "session.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, STORAGE_KEY)
        before = stored_record()
        await storage.save(before)
        client = client_for(storage)
        primary = KeyedSender(2, PRIMARY_KEY, types.NearestDc(country="FR", this_dc=2, nearest_dc=2))
        client._sender = primary
        sender = KeyedSender(4, SECONDARY_KEY, auth_error(name, "wire"))
        client._cdn_auth_cache = {4: (SECONDARY_KEY, 23), 5: (UNRELATED_KEY, 29)}
        client._dc_auth_cache = {4: (SECONDARY_KEY, 23), 5: (UNRELATED_KEY, 29)}
        invoke = await install_route(client, sender, route)
        with pytest.raises(AuthKeyNotFound):
            await invoke()
        assert sender.disconnected == 1
        assert primary.disconnected == 0
        assert isinstance(await client.invoke(functions.HelpGetNearestDc()), types.NearestDc)
        if route == "cdn":
            expected = before
            assert client._cdn_auth_cache == {5: (UNRELATED_KEY, 29)}
            assert client._dc_auth_cache == {4: (SECONDARY_KEY, 23), 5: (UNRELATED_KEY, 29)}
            assert 4 not in client._cdn_senders
        else:
            expected = replace(
                before, metadata={**before.metadata, "dc_auth": {"5": {"key": UNRELATED_KEY, "salt": 29}}}
            )
            assert client._dc_auth_cache == {5: (UNRELATED_KEY, 29)}
            assert client._cdn_auth_cache == {4: (SECONDARY_KEY, 23), 5: (UNRELATED_KEY, 29)}
        await storage.close()
        reopened = EncryptedSQLiteSessionStorage(path, STORAGE_KEY)
        try:
            assert load_session_record(await reopened.load(), 2) == expected
        finally:
            await reopened.close()

    asyncio.run(scenario())


@pytest.mark.parametrize("representation", ["wire", "generated", "typed", "raw"])
@pytest.mark.parametrize("route", ["main", "cdn"])
def test_error_forms_share_scoped_cleanup_even_when_cdn_key_bytes_match_primary(
    route: str, representation: str
) -> None:
    async def scenario() -> None:
        before = stored_record()
        storage = InMemorySessionStorage(before)
        client = client_for(storage)
        sender = KeyedSender(2, PRIMARY_KEY, auth_error("AUTH_KEY_UNREGISTERED", representation))
        client._cdn_auth_cache[2] = (PRIMARY_KEY, 17)
        invoke = await install_route(client, sender, route)
        with pytest.raises(AuthKeyNotFound):
            await invoke()
        expected = before if route == "cdn" else replace(before, auth_key=None, user=None)
        assert load_session_record(await storage.load(), 2) == expected
        assert sender.disconnected == 1
        assert (2 in client._cdn_auth_cache) == (route == "main")

    asyncio.run(scenario())


def test_same_dc_media_failure_clears_its_shared_primary_key() -> None:
    async def scenario() -> None:
        before = stored_record()
        storage = InMemorySessionStorage(before)
        client = client_for(storage)
        sender = KeyedSender(2, PRIMARY_KEY, auth_error("AUTH_KEY_INVALID", "generated"))
        invoke = await install_route(client, sender, "download")
        with pytest.raises(AuthKeyNotFound):
            await invoke()
        assert load_session_record(await storage.load(), 2) == replace(before, auth_key=None, user=None)
        assert sender.disconnected == 1

    asyncio.run(scenario())


@pytest.mark.parametrize("route", ["main", "cdn", "download"])
def test_stale_failure_preserves_replacement_key_and_sender(route: str) -> None:
    async def scenario() -> None:
        before = stored_record()
        storage = InMemorySessionStorage(before)
        client = client_for(storage)
        dc_id, old_key = (2, PRIMARY_KEY) if route == "main" else (4, SECONDARY_KEY)
        sender = KeyedSender(dc_id, old_key, auth_error("AUTH_KEY_UNREGISTERED", "raw"), blocked=True)
        invoke = await install_route(client, sender, route)
        task = asyncio.create_task(invoke())
        await sender.started.wait()
        replacement = KeyedSender(dc_id, REPLACEMENT_KEY, True)
        await install_route(client, replacement, route)
        if route == "main":
            expected = replace(before, auth_key=AuthKey(dc_id=2, key=REPLACEMENT_KEY), user=UserIdentity(id=99))
        elif route == "download":
            expected = replace(before, metadata={**before.metadata, "dc_auth": {**before.metadata["dc_auth"], "4": {"key": REPLACEMENT_KEY, "salt": 31}}})  # fmt: skip
        else:
            expected = before
        await client._storage.save(expected)
        client._dc_auth_cache[dc_id] = (REPLACEMENT_KEY, 31)
        client._cdn_auth_cache[dc_id] = (REPLACEMENT_KEY, 31)
        sender.state.auth_key = REPLACEMENT_KEY
        sender.release.set()
        with pytest.raises(AuthKeyNotFound):
            await task
        assert load_session_record(await storage.load(), 2) == expected
        assert client._dc_auth_cache[dc_id] == (REPLACEMENT_KEY, 31)
        assert client._cdn_auth_cache[dc_id] == (REPLACEMENT_KEY, 31)
        assert replacement.disconnected == 0

    asyncio.run(scenario())


def test_old_primary_failure_after_migration_only_clears_matching_source_dc_credential() -> None:
    async def scenario() -> None:
        before = stored_record()
        storage = InMemorySessionStorage(before)
        client = client_for(storage)
        sender = KeyedSender(2, PRIMARY_KEY, auth_error("AUTH_KEY_UNREGISTERED", "typed"), blocked=True)
        invoke = await install_route(client, sender, "main")
        task = asyncio.create_task(invoke())
        await sender.started.wait()
        migrated = replace(before, dc_id=4, auth_key=AuthKey(dc_id=4, key=SECONDARY_KEY), metadata={**before.metadata, "dc_auth": {"2": {"key": PRIMARY_KEY, "salt": 17}, "4": {"key": SECONDARY_KEY, "salt": 23}}})  # fmt: skip
        await client._storage.save(migrated)
        replacement = KeyedSender(4, SECONDARY_KEY, True)
        client._sender = replacement
        client._dc_auth_cache = {2: (PRIMARY_KEY, 17), 4: (SECONDARY_KEY, 23)}
        sender.release.set()
        with pytest.raises(AuthKeyNotFound):
            await task
        expected = replace(
            migrated, metadata={**migrated.metadata, "dc_auth": {"4": {"key": SECONDARY_KEY, "salt": 23}}}
        )
        assert load_session_record(await storage.load(), 2) == expected
        assert client._dc_auth_cache == {4: (SECONDARY_KEY, 23)}
        assert replacement.disconnected == 0

    asyncio.run(scenario())


@pytest.mark.parametrize("provenance", ["unknown", "different-dc"])
def test_missing_or_different_dc_provenance_cannot_clear_primary(provenance: str) -> None:
    async def scenario() -> None:
        before = stored_record()
        storage = InMemorySessionStorage(before)
        client = client_for(storage)
        sender = KeyedSender(4, PRIMARY_KEY, auth_error("AUTH_KEY_INVALID", "typed"))
        if provenance == "unknown":
            del sender.auth_key_dc_id
        invoke = await install_route(client, sender, "main")
        with pytest.raises(AuthKeyNotFound):
            await invoke()
        assert load_session_record(await storage.load(), 2) == before
        assert sender.disconnected == 1

    asyncio.run(scenario())


def test_builtin_sender_construction_binds_selected_dc_to_actual_encryption_key() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(stored_record())
        config = ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage)
        sender = await build_sender_from_session(config, storage, dc_id_override=4, auth_key_override=SECONDARY_KEY)
        assert cast(Any, sender).auth_key_dc_id == 4
        assert cast(Any, sender).state.auth_key == SECONDARY_KEY

    asyncio.run(scenario())


@pytest.mark.parametrize("route", ["main", "download"])
def test_replacement_committed_immediately_before_atomic_cleanup_survives(route: str) -> None:
    async def scenario() -> None:
        class PausedMutationStorage(InMemorySessionStorage):
            def __init__(self) -> None:
                super().__init__(stored_record())
                self.started = asyncio.Event()
                self.release = asyncio.Event()

            async def mutate(self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None:  # fmt: skip
                self.started.set()
                await self.release.wait()
                return await super().mutate(transform)

        storage = PausedMutationStorage()
        client = client_for(storage)
        dc_id, key = (2, PRIMARY_KEY) if route == "main" else (4, SECONDARY_KEY)
        sender = KeyedSender(dc_id, key, auth_error("AUTH_KEY_UNREGISTERED", "typed"))
        invoke = await install_route(client, sender, route)
        task = asyncio.create_task(invoke())
        await storage.started.wait()
        before = stored_record()
        replacement = replace(before, auth_key=AuthKey(dc_id=2, key=REPLACEMENT_KEY), user=UserIdentity(id=99), metadata={**before.metadata, "dc_auth": {"4": {"key": REPLACEMENT_KEY, "salt": 31}}})  # fmt: skip
        await storage.save(replacement)
        storage.release.set()
        with pytest.raises(AuthKeyNotFound):
            await task
        assert load_session_record(await storage.load(), 2) == replacement
        assert load_session_record(await client._storage.load(), 2) == replacement
        assert sender.disconnected == 1

    asyncio.run(scenario())


SOURCE_KEY = b"s" * 256


TARGET_KEY = b"t" * 256


SOURCE_SALT = 123


TARGET_SALT = 789


EXPORTED = types.AuthExportedAuthorization(id=55, bytes=b"synthetic-export")


def source_record(*, authenticated: bool) -> SessionRecord:
    return SessionRecord(
        dc_id=2,
        auth_key=AuthKey(dc_id=2, key=SOURCE_KEY),
        dc_options=(DCOption(id=2, ip_address="127.0.0.2", port=443), DCOption(id=4, ip_address="127.0.0.4", port=443)),
        user=UserIdentity(id=42, username="alice") if authenticated else None,
        metadata={"server_salt": SOURCE_SALT, "unrelated": "preserved"},
    )


class MigrationScenario:
    def __init__(self, storage: SessionStorage, monkeypatch: pytest.MonkeyPatch) -> None:
        self.storage = storage
        self.client = Client(ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage))
        self.client._connected = True
        self.client._latest_server_salt = SOURCE_SALT
        self.source = MigrationSender(self, source=True)
        self.client._sender = self.source
        self.targets: list[MigrationSender] = []
        self.failure: str | None = None
        self.block: str | None = None
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.exports = 0
        self.transport_closes = 0
        self.setup_calls = 0
        scenario = self

        class Transport:
            def __init__(self, *args: object, **kwargs: object) -> None:
                pass

            async def close(self) -> None:
                scenario.transport_closes += 1

        async def exchange(_exchange: object) -> AuthKeyExchangeResult:
            scenario.setup_calls += 1
            await scenario.step("setup")
            return AuthKeyExchangeResult(auth_key=TARGET_KEY, auth_key_id=b"t" * 8, server_salt=TARGET_SALT, time_offset=0, dc_id=4)  # fmt: skip

        async def build(*args: object, **kwargs: object) -> MigrationSender:
            assert kwargs["dc_id_override"] == 4
            assert kwargs["auth_key_override"] == TARGET_KEY
            assert kwargs["server_salt_override"] == TARGET_SALT
            await scenario.step("build")
            sender = MigrationSender(scenario, source=False)
            scenario.targets.append(sender)
            return sender

        monkeypatch.setattr(client_module, "UnencryptedAuthKeyTransport", Transport)
        monkeypatch.setattr(client_module.AuthKeyExchange, "create_auth_key", exchange)
        monkeypatch.setattr(client_module, "build_sender_from_session", build)

    async def step(self, stage: str) -> None:
        await self.assert_source()
        if self.failure == stage:
            raise RuntimeError(f"{stage} failed")
        if self.block == stage:
            self.started.set()
            await self.release.wait()

    async def assert_source(self) -> SessionRecord:
        record = load_session_record(await self.storage.load(), 2)
        assert record.dc_id == 2
        assert record.auth_key is not None
        assert record.auth_key.dc_id == 2
        assert record.auth_key.key == SOURCE_KEY
        assert record.metadata["server_salt"] == SOURCE_SALT
        assert record.metadata["unrelated"] == "preserved"
        assert self.client._latest_server_salt == SOURCE_SALT
        assert self.source.disconnected == 0
        return record

    async def migrate(self) -> None:
        await self.client._migrate_main_session(self.source, DatacenterMigration(4, kind="USER"))

    async def assert_target(self) -> None:
        record = load_session_record(await self.storage.load(), 2)
        assert record.dc_id == 4
        assert record.auth_key is not None
        assert record.auth_key.dc_id == 4
        assert record.auth_key.key == TARGET_KEY
        assert record.metadata["server_salt"] == TARGET_SALT
        assert record.metadata["dc_auth"]["2"] == {"key": SOURCE_KEY, "salt": SOURCE_SALT}
        assert record.metadata["dc_auth"]["4"] == {"key": TARGET_KEY, "salt": TARGET_SALT}
        assert record.metadata["unrelated"] == "preserved"
        assert self.client._latest_server_salt == TARGET_SALT


class MigrationSender:
    def __init__(self, scenario: MigrationScenario, *, source: bool) -> None:
        self.scenario = scenario
        self.source = source
        self.disconnected = 0
        self.connection_initialized = False
        self.is_connected = True

    async def request(self, body: object, *, retry_safe: bool, **kwargs: object) -> bytes:
        request = body
        while hasattr(request, "query"):
            request = request.query
        assert retry_safe is False
        if self.source:
            assert isinstance(request, functions.AuthExportAuthorization)
            assert request.dc_id == 4
            self.scenario.exports += 1
            await self.scenario.step("export")
            return EXPORTED.serialize()
        assert isinstance(request, functions.AuthImportAuthorization)
        assert request.id == EXPORTED.id
        assert request.bytes == EXPORTED.bytes
        await self.scenario.step("import")
        return types.AuthAuthorization(user=types.User(id=42, username="alice")).serialize()

    async def disconnect(self) -> None:
        self.disconnected += 1
        if not self.source:
            await self.scenario.step("disconnect")
        self.is_connected = False


@pytest.mark.parametrize(
    ("authenticated", "stage"),
    [
        (False, "setup"),
        (True, "setup"),
        (False, "build"),
        (True, "build"),
        (True, "import"),
        (False, "disconnect"),
        (True, "disconnect"),
    ],
)
def test_migration_failure_keeps_source_active_and_allows_retry(
    monkeypatch: pytest.MonkeyPatch, authenticated: bool, stage: str
) -> None:
    async def scenario() -> None:
        initial = source_record(authenticated=authenticated)
        storage = InMemorySessionStorage(initial)
        migration = MigrationScenario(storage, monkeypatch)
        migration.failure = stage
        with pytest.raises(RuntimeError, match=f"{stage} failed"):
            await migration.migrate()
        retained = await migration.assert_source()
        assert retained.user == initial.user
        assert migration.transport_closes == 1
        if stage in {"import", "disconnect"}:
            assert migration.targets[0].disconnected == 1
        rebuilt = cast(MTProtoSender, await build_sender_from_session(migration.client.config, storage))
        assert rebuilt.endpoint.host == "127.0.0.2"
        assert rebuilt.state.auth_key == SOURCE_KEY
        assert rebuilt.state.server_salt == SOURCE_SALT
        migration.failure = None
        await migration.migrate()
        await migration.assert_target()
        assert migration.exports == (2 if authenticated else 0)
        assert migration.targets[-1].disconnected == 1
        assert not migration.targets[-1].is_connected
        assert migration.setup_calls == (2 if stage == "setup" else 1)

    asyncio.run(scenario())


@pytest.mark.parametrize("selection", ["persisted", "legacy_default", "override"])
def test_sender_rejects_key_dc_mismatch_before_construction(monkeypatch: pytest.MonkeyPatch, selection: str) -> None:
    async def scenario() -> None:
        initial: SessionPayload
        if selection == "legacy_default":
            initial = {
                "auth_key": {"dc_id": 2, "key": SOURCE_KEY},
                "dc_options": [{"id": 4, "ip_address": "127.0.0.4", "port": 443}],
            }
        else:
            initial = replace(source_record(authenticated=True), dc_id=2 if selection == "override" else 4)
        storage = InMemorySessionStorage(initial)
        config = ClientConfig(api_id=1, api_hash="synthetic", dc_id=4, session_storage=storage)
        before = await storage.load()

        def forbid_construction(*args: object, **kwargs: object) -> None:
            pytest.fail("mismatched key/DC reached built-in sender construction")

        monkeypatch.setattr(invoke_module, "MTProtoState", forbid_construction)
        monkeypatch.setattr(invoke_module, "MTProtoSender", forbid_construction)
        with pytest.raises(InvalidDatacenter, match="selected DC does not match the stored auth key DC"):
            await build_sender_from_session(config, storage, dc_id_override=4 if selection == "override" else None)
        assert await storage.load() == before

    asyncio.run(scenario())


@pytest.mark.parametrize("stored_dc", [2, 4])
def test_paired_dc_and_key_override_preserves_target_provenance(stored_dc: int) -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(replace(source_record(authenticated=True), dc_id=stored_dc))
        config = ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage)
        before = await storage.load()
        sender = await build_sender_from_session(
            config, storage, dc_id_override=4, auth_key_override=TARGET_KEY, server_salt_override=TARGET_SALT
        )
        assert isinstance(sender, MTProtoSender)
        assert sender.endpoint.host == "127.0.0.4"
        assert sender.state.auth_key == TARGET_KEY
        assert sender.state.server_salt == TARGET_SALT
        assert cast(Any, sender).auth_key_dc_id == 4
        assert await storage.load() == before

    asyncio.run(scenario())


def test_sender_without_selected_dc_uses_stored_key_owner_before_config_default() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(replace(source_record(authenticated=True), dc_id=None))
        config = ClientConfig(api_id=1, api_hash="synthetic", dc_id=4, session_storage=storage)
        sender = await build_sender_from_session(config, storage)
        assert isinstance(sender, MTProtoSender)
        assert sender.endpoint.host == "127.0.0.2"
        assert sender.state.auth_key == SOURCE_KEY
        assert cast(Any, sender).auth_key_dc_id == 2

    asyncio.run(scenario())


def test_custom_sender_factory_keeps_its_documented_construction_bypass(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        initial = replace(source_record(authenticated=True), dc_id=4)
        storage = InMemorySessionStorage(initial)
        config = ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage)
        custom_sender = cast(RawSender, object())

        def factory(record: SessionRecord) -> RawSender:
            assert record.dc_id == 4
            assert record.auth_key is not None and record.auth_key.dc_id == 2
            return custom_sender

        def forbid_construction(*args: object, **kwargs: object) -> None:
            pytest.fail("custom factory reached built-in sender construction")

        monkeypatch.setattr(invoke_module, "MTProtoSender", forbid_construction)
        assert await build_sender_from_session(config, storage, factory) is custom_sender

    asyncio.run(scenario())


@pytest.mark.parametrize("stage", ["setup", "build", "import", "disconnect"])
def test_migration_cancellation_keeps_source_active_and_drains_cleanup(
    monkeypatch: pytest.MonkeyPatch, stage: str
) -> None:
    async def scenario() -> None:
        migration = MigrationScenario(InMemorySessionStorage(source_record(authenticated=True)), monkeypatch)
        migration.block = stage
        task = asyncio.create_task(migration.migrate())
        await asyncio.wait_for(migration.started.wait(), timeout=2)
        task.cancel()
        if stage == "disconnect":
            await asyncio.sleep(0)
            assert not task.done()
            task.cancel()
            migration.release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        await migration.assert_source()
        if stage in {"import", "disconnect"}:
            assert migration.targets[0].disconnected == 1
            assert not migration.targets[0].is_connected
        assert migration.transport_closes == 1
        migration.block = None
        await migration.migrate()
        await migration.assert_target()
        assert migration.exports == 2

    asyncio.run(scenario())


def test_migration_cleanup_failure_preserves_import_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        migration = MigrationScenario(InMemorySessionStorage(source_record(authenticated=True)), monkeypatch)
        migration.failure = "import"

        async def fail_cleanup(sender: MigrationSender) -> None:
            sender.disconnected += 1
            raise ValueError("cleanup failed")

        monkeypatch.setattr(MigrationSender, "disconnect", fail_cleanup)
        with pytest.raises(RuntimeError, match="import failed"):
            await migration.migrate()
        await migration.assert_source()
        assert migration.targets[0].disconnected == 1

    asyncio.run(scenario())


def test_failed_migration_retains_source_in_reopened_storage(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    async def scenario() -> None:
        path = tmp_path / "migration.sqlite"
        storage = EncryptedSQLiteSessionStorage(path, key=b"synthetic-storage-key-for-tests")
        await storage.save(source_record(authenticated=True))
        migration = MigrationScenario(storage, monkeypatch)
        migration.failure = "import"
        with pytest.raises(RuntimeError, match="import failed"):
            await migration.migrate()
        await migration.client._storage.close()
        reopened = EncryptedSQLiteSessionStorage(path, key=b"synthetic-storage-key-for-tests")
        retry = MigrationScenario(reopened, monkeypatch)
        await retry.assert_source()
        await retry.migrate()
        await retry.assert_target()
        assert retry.setup_calls == 0
        assert retry.exports == 1
        await retry.client._storage.close()

    asyncio.run(scenario())


@pytest.mark.parametrize("replacement_present", [False, True])
def test_cancellation_after_activation_starts_reconciles_committed_target(
    monkeypatch: pytest.MonkeyPatch, replacement_present: bool
) -> None:
    class CommitGateStorage(InMemorySessionStorage):
        def __init__(self) -> None:
            super().__init__(source_record(authenticated=True))
            self.started = asyncio.Event()
            self.release = asyncio.Event()

        async def mutate(self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None:  # fmt: skip
            current = await self.load()
            transformed = transform(current)
            if isinstance(transformed, SessionRecord) and transformed.dc_id == 4:
                self.started.set()
                await self.release.wait()
            return await super().mutate(transform)

    async def scenario() -> None:
        class TargetSender:
            connection_initialized = True
            is_connected = True
            disconnected = 0

            async def request(self, body: object, **kwargs: object) -> bytes:
                assert isinstance(body, functions.HelpGetNearestDc)
                return types.NearestDc(country="CH", this_dc=4, nearest_dc=4).serialize()

            async def disconnect(self) -> None:
                self.disconnected += 1
                self.is_connected = False

        storage = CommitGateStorage()
        migration = MigrationScenario(storage, monkeypatch)
        task = asyncio.create_task(migration.migrate())
        await asyncio.wait_for(storage.started.wait(), timeout=2)
        replacement = TargetSender() if replacement_present else None
        if replacement is not None:
            migration.client._sender = replacement
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        storage.release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        await migration.assert_target()
        cached = load_session_record(await migration.client._storage.load(), 2)
        assert cached.dc_id == 4
        assert cached.auth_key is not None and cached.auth_key.key == TARGET_KEY
        assert migration.client._sender is replacement
        assert migration.source.disconnected == (0 if replacement_present else 1)
        if replacement is not None:
            assert replacement.disconnected == 0
        else:
            assert not migration.source.is_connected

        def rebuild(record: SessionRecord) -> TargetSender:
            assert record.dc_id == 4
            assert record.auth_key is not None and record.auth_key.key == TARGET_KEY
            assert record.metadata["server_salt"] == TARGET_SALT
            return TargetSender()

        monkeypatch.setattr(client_module, "build_sender_from_session", build_sender_from_session)
        migration.client._sender_factory = rebuild
        result = await migration.client.invoke(functions.HelpGetNearestDc())
        assert isinstance(result, types.NearestDc)
        assert result.this_dc == 4

    asyncio.run(scenario())

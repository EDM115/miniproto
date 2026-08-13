from __future__ import annotations

import asyncio
import hashlib
from datetime import UTC, datetime
from typing import Any, cast

import pytest
from tests.support.fake_mtproto import FakeAuthMTProtoServer, FakeMTProtoServer

import miniproto.auth.bootstrap as auth_bootstrap
from miniproto import (
    AmbiguousRpcResult,
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    FloodWait,
    InMemorySessionStorage,
    Media,
    NewMessage,
    SessionRecord,
    TransportConfig,
    event_loop,
)
from miniproto.media import BIG_FILE_THRESHOLD, decrypt_cdn_chunk, download_file, upload_file
from miniproto.mtproto.codec import (
    DecodedEncryptedMessage,
    MessageContainer,
    MessageContainerItem,
    RpcErrorBody,
    RpcResult,
)
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, UpdateState, session_record_from_mapping
from miniproto.tl.codec import decode_object

AUTH_KEY = b"a" * 256


def run(coro: Any) -> Any:
    return event_loop.run(coro)


def decode_innermost_request(message: DecodedEncryptedMessage) -> object:
    request, offset = decode_object(message.body)
    assert offset == len(message.body)
    while isinstance(request, (functions.InvokeWithLayer, functions.InitConnection, functions.InvokeWithoutUpdates)):
        request = request.query
    return request


def fake_server_storage(
    server: FakeMTProtoServer, *, metadata: dict[str, object] | None = None
) -> InMemorySessionStorage:
    endpoint = server.endpoint
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),),
            metadata=metadata or {},
        )
    )


def test_auth_key_handshake_persists_and_reconnect_reuses_it_for_initialized_rpc(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        seen_requests: list[str] = []

        def handle(message: DecodedEncryptedMessage) -> object | None:
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            seen_requests.append(getattr(type(request), "QUALNAME", type(request).__name__))
            if isinstance(request, functions.AuthImportBotAuthorization):
                assert request.bot_auth_token == "123:acceptance-token"  # noqa: S105 - fake credential
                return RpcResult(
                    req_msg_id=message.msg_id,
                    result=types.AuthAuthorization(
                        user=types.User(
                            id=42,
                            access_hash=9000,
                            self_=True,
                            bot=True,
                            bot_info_version=1,
                            first_name="Acceptance bot",
                        )
                    ),
                )
            if isinstance(request, functions.HelpGetNearestDc):
                return RpcResult(
                    req_msg_id=message.msg_id, result=types.NearestDc(country="CH", this_dc=2, nearest_dc=2)
                )
            raise AssertionError(f"unexpected auth journey request {request!r}")

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeAuthMTProtoServer(transport, handle) as server:
            monkeypatch.setattr(auth_bootstrap, "telegram_rsa_public_keys", lambda *, test_mode: (server.rsa_key,))
            endpoint = server.endpoint
            storage = InMemorySessionStorage(
                SessionRecord(dc_id=2, dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),))
            )
            config = ClientConfig(api_id=1, api_hash="hash", session_storage=storage, transport=transport)
            first = Client(config, _updates_enabled=False)
            authorization = await first.sign_in_bot("123:acceptance-token")
            assert isinstance(authorization, types.AuthAuthorization)
            assert await first.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            persisted = await storage.load()
            assert persisted is not None
            record = session_record_from_mapping(persisted)
            assert record.auth_key is not None
            assert record.auth_key.key == server.auth_key
            assert record.metadata["server_salt"] == server.server_salt
            await first.disconnect()

            reopened = InMemorySessionStorage(persisted)
            second = Client(
                ClientConfig(api_id=1, api_hash="hash", session_storage=reopened, transport=transport),
                _updates_enabled=False,
            )
            await second.connect()
            assert await second.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            await second.disconnect()

            assert server.auth_handshakes == 1
            assert server.encrypted_connections == 2
            assert seen_requests == ["auth.importBotAuthorization", "help.getNearestDc", "help.getNearestDc"]
            assert server.errors == []

    run(scenario())


def test_method_flood_cache_blocks_second_real_sender_send_and_preserves_request_correlation() -> None:
    async def scenario() -> None:
        attempts = 0

        def handle(message: DecodedEncryptedMessage) -> object | None:
            nonlocal attempts
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            assert isinstance(request, functions.HelpGetNearestDc)
            attempts += 1
            return RpcResult(
                req_msg_id=message.msg_id, result=RpcErrorBody(error_code=420, error_message="FLOOD_WAIT_5")
            )

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
                ),
                _updates_enabled=False,
            )
            await client.connect()
            first_request = functions.HelpGetNearestDc()
            second_request = functions.HelpGetNearestDc()
            with pytest.raises(FloodWait) as server_wait:
                await client.invoke(first_request)
            with pytest.raises(FloodWait) as cached_wait:
                await client.invoke(second_request)
            assert server_wait.value.request is first_request
            assert cached_wait.value.request is second_request
            assert server_wait.value.seconds == cached_wait.value.seconds == 5
            assert attempts == 1
            await client.disconnect()

    run(scenario())


def test_reset_before_acceptance_replays_safe_raw_request_but_accepted_unsafe_request_is_ambiguous() -> None:
    async def safe_scenario() -> None:
        accepted = 0

        def handle(message: DecodedEncryptedMessage) -> object | None:
            nonlocal accepted
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            assert isinstance(request, functions.HelpGetNearestDc)
            accepted += 1
            return RpcResult(req_msg_id=message.msg_id, result=types.NearestDc(country="CH", this_dc=2, nearest_dc=2))

        transport = TransportConfig(
            mode="tcp_intermediate", read_timeout=2.0, reconnect_backoff_initial=0, reconnect_backoff_max=0
        )
        async with FakeMTProtoServer(AUTH_KEY, transport, handle, drop_connections_before_packet=1) as server:
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
                ),
                _updates_enabled=False,
            )
            await client.connect()
            assert await client.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            assert server.connections_accepted == 2
            assert accepted == 1
            await client.disconnect()

    async def unsafe_scenario() -> None:
        accepted = 0

        def handle(message: DecodedEncryptedMessage) -> object | None:
            nonlocal accepted
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            assert isinstance(request, functions.AccountUpdateProfile)
            accepted += 1
            raise ValueError("accepted unsafe request before closing")

        transport = TransportConfig(
            mode="tcp_intermediate", read_timeout=2.0, reconnect_backoff_initial=0, reconnect_backoff_max=0
        )
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
                ),
                _updates_enabled=False,
            )
            await client.connect()
            request = functions.AccountUpdateProfile(first_name="unsafe")
            with pytest.raises(AmbiguousRpcResult) as ambiguous:
                await client.invoke(request)
            assert ambiguous.value.request == "account.updateProfile"
            assert ambiguous.value.context == {"attempts": 1}
            assert accepted == 1
            await client.disconnect()

    run(safe_scenario())
    run(unsafe_scenario())


def test_global_and_channel_gap_recovery_is_ordered_and_cursors_survive_real_sender_reconnect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        monkeypatch.setattr("miniproto.updates.manager.POSSIBLE_GAP_GRACE_SECONDS", 0.0)
        help_calls = 0
        global_difference_calls = 0
        channel_difference_calls = 0
        channel_id = 123

        def raw_message(message_id: int, text: str, *, date: int) -> types.Message:
            return types.Message(id=message_id, peer_id=types.PeerUser(user_id=42), date=date, message=text)

        def raw_channel_message(message_id: int, text: str, *, date: int) -> types.Message:
            return types.Message(
                id=message_id, peer_id=types.PeerChannel(channel_id=channel_id), date=date, message=text
            )

        def response_with_update(message: DecodedEncryptedMessage, update: object) -> MessageContainer:
            return MessageContainer(
                messages=(
                    MessageContainerItem(msg_id=message.msg_id + 1, seq_no=1, body=update),
                    MessageContainerItem(
                        msg_id=message.msg_id + 5,
                        seq_no=3,
                        body=RpcResult(
                            req_msg_id=message.msg_id, result=types.NearestDc(country="CH", this_dc=2, nearest_dc=2)
                        ),
                    ),
                )
            )

        def handle(message: DecodedEncryptedMessage) -> object | None:
            nonlocal help_calls, global_difference_calls, channel_difference_calls
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            if isinstance(request, functions.HelpGetNearestDc):
                help_calls += 1
                if help_calls == 1:
                    return response_with_update(
                        message,
                        types.UpdateShortMessage(
                            id=112, user_id=42, message="global-current", pts=13, pts_count=1, date=101
                        ),
                    )
                if help_calls == 2:
                    return response_with_update(
                        message,
                        types.UpdateNewChannelMessage(
                            message=raw_channel_message(212, "channel-current", date=201), pts=13, pts_count=1
                        ),
                    )
                if help_calls == 3:
                    return response_with_update(
                        message,
                        types.UpdateShortMessage(
                            id=113, user_id=42, message="global-next", pts=14, pts_count=1, date=102
                        ),
                    )
                if help_calls == 4:
                    return response_with_update(
                        message,
                        types.UpdateNewChannelMessage(
                            message=raw_channel_message(213, "channel-next", date=202), pts=14, pts_count=1
                        ),
                    )
                raise AssertionError("unexpected help.getNearestDc call")
            if isinstance(request, functions.UpdatesGetDifference):
                global_difference_calls += 1
                assert request.pts == 10
                return RpcResult(
                    req_msg_id=message.msg_id,
                    result=types.UpdatesDifference(
                        new_messages=(raw_message(111, "global-missing", date=100),),
                        new_encrypted_messages=(),
                        other_updates=(),
                        chats=(),
                        users=(types.User(id=42, access_hash=9000, first_name="Alice", username="alice"),),
                        state=types.UpdatesState(pts=12, qts=0, date=100, seq=0, unread_count=0),
                    ),
                )
            if isinstance(request, functions.UpdatesGetChannelDifference):
                channel_difference_calls += 1
                assert request.pts == 10
                assert isinstance(request.channel, types.InputChannel)
                assert request.channel.channel_id == channel_id
                assert request.channel.access_hash == 999
                return RpcResult(
                    req_msg_id=message.msg_id,
                    result=types.UpdatesChannelDifference(
                        final=True,
                        pts=12,
                        new_messages=(raw_channel_message(211, "channel-missing", date=200),),
                        other_updates=(),
                        chats=(
                            types.Channel(
                                id=channel_id,
                                access_hash=999,
                                title="Acceptance channel",
                                photo=types.ChatPhotoEmpty(),
                                date=1_700_000_000,
                            ),
                        ),
                        users=(),
                    ),
                )
            raise AssertionError(f"unexpected request {request!r}")

        async def next_text(client: Client) -> str:
            update = await asyncio.wait_for(anext(client.iter_updates()), timeout=2.0)
            assert isinstance(update, NewMessage)
            assert update.message is not None
            return update.message.text

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            endpoint = server.endpoint
            storage = InMemorySessionStorage(
                SessionRecord(
                    dc_id=2,
                    auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
                    dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),),
                    peers=(PeerCacheEntry(id=channel_id, kind="channel", access_hash=999),),
                    update_state=UpdateState(pts=10, qts=0, seq=0, date=datetime.fromtimestamp(50, UTC)),
                    metadata={
                        "updates": {
                            "channels": {
                                str(channel_id): {"pts": 10, "date": datetime.fromtimestamp(50, UTC).isoformat()}
                            }
                        }
                    },
                )
            )
            config = ClientConfig(api_id=1, api_hash="hash", session_storage=storage, transport=transport)
            first = Client(config)
            await first.connect()
            assert await first.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            assert [await next_text(first), await next_text(first)] == ["global-missing", "global-current"]
            assert await first.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            assert [await next_text(first), await next_text(first)] == ["channel-missing", "channel-current"]
            persisted = await storage.load()
            assert persisted is not None
            first_record = session_record_from_mapping(persisted)
            assert first_record.update_state.pts == 13
            assert first_record.metadata["updates"]["channels"][str(channel_id)]["pts"] == 13
            await first.disconnect()

            reopened = InMemorySessionStorage(persisted)
            second = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=reopened, transport=transport))
            await second.connect()
            assert await second.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            assert await next_text(second) == "global-next"
            assert await second.invoke(functions.HelpGetNearestDc()) == types.NearestDc(
                country="CH", this_dc=2, nearest_dc=2
            )
            assert await next_text(second) == "channel-next"
            await second.disconnect()

            assert global_difference_calls == 1
            assert channel_difference_calls == 1

    run(scenario())


def test_small_big_upload_and_cdn_download_traverse_real_sender_transport() -> None:
    async def scenario() -> None:
        requests: list[object] = []
        cdn_key = bytes(range(32))
        cdn_iv = bytes(range(16))
        cdn_plaintext = b"verified-cdn-data"
        cdn_ciphertext = decrypt_cdn_chunk(cdn_plaintext, key=cdn_key, iv=cdn_iv, offset=0)

        def handle(message: DecodedEncryptedMessage) -> object | None:
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            requests.append(request)
            if isinstance(request, functions.UploadSaveFilePart | functions.UploadSaveBigFilePart):
                result: object = types.BoolTrue()
            elif isinstance(request, functions.UploadGetFile):
                assert isinstance(request.location, types.InputDocumentFileLocation)
                assert request.location.id == 11
                result = types.UploadFileCdnRedirect(
                    dc_id=4,
                    file_token=b"cdn-token",
                    encryption_key=cdn_key,
                    encryption_iv=cdn_iv,
                    file_hashes=(
                        types.FileHash(offset=0, limit=len(cdn_plaintext), hash=hashlib.sha256(cdn_plaintext).digest()),
                    ),
                )
            elif isinstance(request, functions.UploadGetCdnFile):
                result = types.UploadCdnFile(bytes=cdn_ciphertext[request.offset : request.offset + request.limit])
            else:
                raise AssertionError(f"unexpected request {request!r}")
            return RpcResult(req_msg_id=message.msg_id, result=result)

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=3.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
                ),
                _updates_enabled=False,
            )
            await client.connect()
            small_payload = b"s" * 2049
            small = await upload_file(
                client.invoke, small_payload, file_name="small.bin", file_id=101, part_size=1024, concurrency=2
            )
            big_payload = b"b" * (BIG_FILE_THRESHOLD + 1)
            big = await upload_file(
                client.invoke, big_payload, file_name="big.bin", file_id=202, part_size=512 * 1024, concurrency=4
            )
            cdn = await download_file(
                client.invoke,
                types.InputDocumentFileLocation(id=11, access_hash=22, file_reference=b"cdn-ref", thumb_size=""),
                limit=len(cdn_plaintext),
                part_size=4096,
                concurrency=1,
                adaptive_part_size=False,
                max_part_size=4096,
            )
            await client.disconnect()

            small_requests = [
                request
                for request in requests
                if isinstance(request, functions.UploadSaveFilePart) and request.file_id == 101
            ]
            big_requests = [
                request
                for request in requests
                if isinstance(request, functions.UploadSaveBigFilePart) and request.file_id == 202
            ]
            assert small.big is False
            assert small.parts == 3
            assert (
                b"".join(request.bytes for request in sorted(small_requests, key=lambda item: item.file_part))
                == small_payload
            )
            assert big.big is True
            assert big.parts == 21
            assert len(big_requests) == big.parts
            assert all(request.file_total_parts == big.parts for request in big_requests)
            assert cdn.data == cdn_plaintext
            assert any(isinstance(request, functions.UploadGetFile) for request in requests)
            assert any(isinstance(request, functions.UploadGetCdnFile) for request in requests)

    run(scenario())


def test_plain_download_byte_window_bounds_simultaneous_real_media_lanes() -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 64
        active = 0
        max_active = 0
        two_started = asyncio.Event()
        release = asyncio.Event()

        async def handle(message: DecodedEncryptedMessage) -> object | None:
            nonlocal active, max_active
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            assert isinstance(request, functions.UploadGetFile)
            active += 1
            max_active = max(max_active, active)
            if active == 2:
                two_started.set()
            try:
                await release.wait()
                result = types.UploadFile(
                    type=types.StorageFileUnknown(),
                    mtime=1_700_000_000,
                    bytes=payload[request.offset : request.offset + request.limit],
                )
                return RpcResult(req_msg_id=message.msg_id, result=result)
            finally:
                active -= 1

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=3.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
                ),
                _updates_enabled=False,
            )
            await client.connect()
            task = asyncio.create_task(
                client.download_media(
                    Media(
                        id=10,
                        size=len(payload),
                        location=types.InputDocumentFileLocation(
                            id=10, access_hash=20, file_reference=b"plain-ref", thumb_size=""
                        ),
                    ),
                    part_size=4096,
                    max_part_size=4096,
                    concurrency=4,
                    media_lanes=4,
                    max_in_flight_bytes=8192,
                    adaptive_concurrency=False,
                    adaptive_part_size=False,
                )
            )
            await asyncio.wait_for(two_started.wait(), timeout=2.0)
            await asyncio.sleep(0.05)
            assert active == 2
            assert max_active == 2
            release.set()
            result = await asyncio.wait_for(task, timeout=3.0)
            assert result.data == payload
            assert max_active == 2
            await client.disconnect()

    run(scenario())


def test_upload_cancellation_clears_real_sender_pending_requests() -> None:
    async def scenario() -> None:
        started = asyncio.Event()
        release = asyncio.Event()

        async def handle(message: DecodedEncryptedMessage) -> object | None:
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            assert isinstance(request, functions.UploadSaveFilePart)
            started.set()
            await release.wait()
            return RpcResult(req_msg_id=message.msg_id, result=types.BoolTrue())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=3.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            client = Client(
                ClientConfig(
                    api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
                ),
                _updates_enabled=False,
            )
            await client.connect()
            task = asyncio.create_task(
                upload_file(client.invoke, b"x" * (16 * 1024), file_name="cancel.bin", part_size=1024, concurrency=2)
            )
            await asyncio.wait_for(started.wait(), timeout=2.0)
            task.cancel()
            done_before_response, _ = await asyncio.wait({task}, timeout=0.5)
            sender = client._sender
            assert sender is not None
            pending_before_response = cast(Any, sender).sender_state.pending_count
            release.set()
            done_after_response, _ = await asyncio.wait({task}, timeout=2.0)
            assert task in done_after_response
            with pytest.raises(asyncio.CancelledError):
                task.result()
            await asyncio.sleep(0.05)
            await client.disconnect()
            assert task in done_before_response
            assert pending_before_response == 0

    run(scenario())


def test_file_migrate_uses_real_target_dc_pool_and_export_import_without_changing_main_dc() -> None:
    async def scenario() -> None:
        home_requests: list[str] = []
        target_requests: list[str] = []
        payload = b"foreign-dc-payload"

        def home_handle(message: DecodedEncryptedMessage) -> object | None:
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            home_requests.append(getattr(type(request), "QUALNAME", type(request).__name__))
            if isinstance(request, functions.UploadGetFile):
                result: object = RpcErrorBody(error_code=303, error_message="FILE_MIGRATE_5")
            elif isinstance(request, functions.AuthExportAuthorization):
                assert request.dc_id == 5
                result = types.AuthExportedAuthorization(id=77, bytes=b"exported-auth")
            else:
                raise AssertionError(f"unexpected home-DC request {request!r}")
            return RpcResult(req_msg_id=message.msg_id, result=result)

        def target_handle(message: DecodedEncryptedMessage) -> object | None:
            if message.seq_no % 2 == 0:
                return None
            request = decode_innermost_request(message)
            target_requests.append(getattr(type(request), "QUALNAME", type(request).__name__))
            if isinstance(request, functions.AuthImportAuthorization):
                assert request.id == 77
                assert request.bytes == b"exported-auth"
                result: object = types.AuthAuthorization(user=types.UserEmpty(id=42))
            elif isinstance(request, functions.UploadGetFile):
                result = types.UploadFile(
                    type=types.StorageFileUnknown(),
                    mtime=1_700_000_000,
                    bytes=payload[request.offset : request.offset + request.limit],
                )
            else:
                raise AssertionError(f"unexpected target-DC request {request!r}")
            return RpcResult(req_msg_id=message.msg_id, result=result)

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=3.0)
        async with (
            FakeMTProtoServer(AUTH_KEY, transport, target_handle) as target_server,
            FakeMTProtoServer(AUTH_KEY, transport, home_handle) as home_server,
        ):
            storage = InMemorySessionStorage(
                SessionRecord(
                    dc_id=2,
                    auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
                    dc_options=(
                        DCOption(id=2, ip_address=home_server.endpoint.host, port=home_server.endpoint.port),
                        DCOption(
                            id=5,
                            ip_address=target_server.endpoint.host,
                            port=target_server.endpoint.port,
                            media_only=True,
                        ),
                    ),
                    metadata={"dc_auth": {"5": {"key": AUTH_KEY, "salt": target_server.server_salt}}},
                )
            )
            client = Client(
                ClientConfig(api_id=1, api_hash="hash", session_storage=storage, transport=transport),
                _updates_enabled=False,
            )
            await client.connect()
            result = await client.download_media(
                Media(
                    id=10,
                    size=len(payload),
                    location=types.InputDocumentFileLocation(
                        id=10, access_hash=20, file_reference=b"migrate-ref", thumb_size=""
                    ),
                ),
                limit=len(payload),
                part_size=4096,
                max_part_size=4096,
                concurrency=1,
                media_lanes=1,
                max_retries=0,
                adaptive_concurrency=False,
                adaptive_part_size=False,
            )
            assert result.data == payload
            persisted = await storage.load()
            assert persisted is not None
            assert session_record_from_mapping(persisted).dc_id == 2
            await client.disconnect()

        assert home_requests == ["upload.getFile", "auth.exportAuthorization"]
        assert target_requests == ["auth.importAuthorization", "upload.getFile"]

    run(scenario())

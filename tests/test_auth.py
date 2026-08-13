from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DatacenterMigration,
    DCOption,
    FloodWait,
    InMemorySessionStorage,
    InvalidCode,
    PasswordRequired,
    SessionRecord,
    TransportFlood,
    UserIdentity,
    event_loop,
)
from miniproto.auth import (
    AuthKeyExchange,
    AuthService,
    ClientDHInnerData,
    PQInnerDataDC,
    ResPQ,
    RSAKey,
    ServerDHInnerData,
    ServerDHParamsOk,
    compute_auth_key,
    compute_check_password,
    dc_options_from_env,
    decrypt_server_dh_answer,
    encode_client_dh_inner_data,
    encode_pq_inner_data_dc,
    factorize_pq,
    public_rsa_fingerprint,
    rsa_pad,
    server_salt,
)
from miniproto.auth.key_exchange import encode_server_dh_answer
from miniproto.errors import AuthKeyNotFound, RpcError, classify_rpc_error
from miniproto.invoke import clear_invalid_auth_key
from miniproto.raw import functions, types
from miniproto.session.models import session_record_from_mapping

_TELEGRAM_DH_PRIME_BYTES = bytes.fromhex(
    "C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C3720FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C595F642477FE96BB2A941D5BCD1D4AC8CC49880708FA9B378E3C4F3A9060BEE67CF9A4A4A695811051907E162753B56B0F6B410DBA74D8A84B2A14B3144E0EF1284754FD17ED950D5965B4B9DD46582DB1178D169C6BC465B0D6FF9CA3928FEF5B9AE4E418FC15E83EBEA0F87FA9FF5EED70050DED2849F47BF959D956850CE929851F0D8115F635B105EE2E4E15D04B2454BF6F4FADF034B10403119CD8E3B92FCC5B"
)
_TELEGRAM_DH_PRIME = int.from_bytes(_TELEGRAM_DH_PRIME_BYTES, "big")
_DH_PUBLIC_VALUE_BOUNDARY = 1 << (2048 - 64)


def run(coro):
    return event_loop.run(coro)


class FakeAuthClient(Client):
    def __init__(self, config: ClientConfig, handler: Callable[[object], object | Awaitable[object]]) -> None:
        super().__init__(config)
        self.requests: list[object] = []
        self._handler = handler

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
        quick_ack: bool = False,
        quick_ack_callback: object | None = None,
    ) -> object:
        del quick_ack, quick_ack_callback
        self.requests.append(raw_request)
        result = self._handler(raw_request)
        return await result if inspect.isawaitable(result) else result


def auth_storage() -> InMemorySessionStorage:
    return InMemorySessionStorage(SessionRecord(dc_id=2, auth_key=AuthKey(dc_id=2, key=b"k" * 256, key_id=123)))


def user_authorization(*, user_id: int = 42, bot: bool = False) -> types.AuthAuthorization:
    user = types.User(
        id=user_id,
        access_hash=9000 + user_id,
        self_=True,
        bot=bot,
        first_name="Bot" if bot else "Alice",
        username="phase6bot" if bot else "alice",
        phone=None if bot else "+9996621234",
    )
    return types.AuthAuthorization(user=user)


def _sample_bot_token() -> str:
    return "123" + ":" + "token"


def sent_code() -> types.AuthSentCode:
    return types.AuthSentCode(type=types.AuthSentCodeTypeApp(length=5), phone_code_hash="hash-1", timeout=30)


def empty_password_state() -> types.AccountPassword:
    return types.AccountPassword(
        has_password=False,
        new_algo=types.PasswordKdfAlgoUnknown(),
        new_secure_algo=types.SecurePasswordKdfAlgoUnknown(),
        secure_random=b"random",
    )


def srp_password_state(*, p: int = _TELEGRAM_DH_PRIME, g: int = 3, srp_b: int | bytes) -> types.AccountPassword:
    srp_b_bytes = srp_b if isinstance(srp_b, bytes) else srp_b.to_bytes(256, "big")
    return types.AccountPassword(
        has_password=True,
        current_algo=types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(
            salt1=b"salt-one", salt2=b"salt-two", g=g, p=p.to_bytes(256, "big")
        ),
        srp_B=srp_b_bytes,
        srp_id=42,
        new_algo=types.PasswordKdfAlgoUnknown(),
        new_secure_algo=types.SecurePasswordKdfAlgoUnknown(),
        secure_random=b"random",
    )


class FakeDHTransport:
    def __init__(self, *, rsa_key: RSAKey, server_inner: ServerDHInnerData, new_nonce: int) -> None:
        self.rsa_key = rsa_key
        self.server_inner = server_inner
        self.new_nonce = new_nonce
        self.calls = 0

    async def send_unencrypted(self, body: bytes) -> bytes:
        self.calls += 1
        if self.calls == 1:
            return ResPQ(
                nonce=self.server_inner.nonce,
                server_nonce=self.server_inner.server_nonce,
                pq=(17 * 23).to_bytes(2, "big"),
                server_public_key_fingerprints=(self.rsa_key.fingerprint,),
            ).serialize()
        if self.calls == 2:
            padding = b"\x00" * (-(20 + len(self.server_inner.serialize())) % 16)
            encrypted_answer = encode_server_dh_answer(
                self.server_inner,
                new_nonce=self.new_nonce,
                server_nonce=self.server_inner.server_nonce,
                padding=padding,
            )
            return ServerDHParamsOk(
                nonce=self.server_inner.nonce,
                server_nonce=self.server_inner.server_nonce,
                encrypted_answer=encrypted_answer,
            ).serialize()
        raise AssertionError("invalid DH parameters must not reach set_client_DH_params")


def test_auth_key_service_constructor_primitives_round_trip() -> None:
    res_pq = ResPQ(
        nonce=0x0102030405060708090A0B0C0D0E0F10,
        server_nonce=0x1112131415161718191A1B1C1D1E1F20,
        pq=(17 * 23).to_bytes(2, "big"),
        server_public_key_fingerprints=(1, 2, 3),
    )
    assert ResPQ.deserialize(res_pq.serialize()) == res_pq
    assert factorize_pq(17 * 23) == (17, 23)
    inner = PQInnerDataDC(
        pq=res_pq.pq,
        p=b"\x11",
        q=b"\x17",
        nonce=res_pq.nonce,
        server_nonce=res_pq.server_nonce,
        new_nonce=0x2122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F40,
        dc_id=10002,
    )
    assert encode_pq_inner_data_dc(inner) == inner.serialize()
    rsa_key = RSAKey(modulus=(1 << 2048) - 159, exponent=1)
    padded = rsa_pad(inner.serialize(), rsa_key, random_bytes=lambda size: b"\x01" * size)
    assert len(padded) == 256
    assert public_rsa_fingerprint(rsa_key) == rsa_key.fingerprint
    server_inner = ServerDHInnerData(
        nonce=res_pq.nonce,
        server_nonce=res_pq.server_nonce,
        g=3,
        dh_prime=_TELEGRAM_DH_PRIME_BYTES,
        g_a=(_DH_PUBLIC_VALUE_BOUNDARY + 1).to_bytes(256, "big"),
        server_time=1_771_000_000,
    )
    answer_padding = b"\x00" * (-(20 + len(server_inner.serialize())) % 16)
    encrypted = encode_server_dh_answer(
        server_inner, new_nonce=inner.new_nonce, server_nonce=res_pq.server_nonce, padding=answer_padding
    )
    assert (
        decrypt_server_dh_answer(encrypted, new_nonce=inner.new_nonce, server_nonce=res_pq.server_nonce) == server_inner
    )
    client_inner = ClientDHInnerData(
        nonce=res_pq.nonce,
        server_nonce=res_pq.server_nonce,
        retry_id=0,
        g_b=(_DH_PUBLIC_VALUE_BOUNDARY + 2).to_bytes(256, "big"),
    )
    assert encode_client_dh_inner_data(client_inner).startswith(b"T\xb6Cf")
    auth_key = compute_auth_key(g_a=_DH_PUBLIC_VALUE_BOUNDARY + 1, b=7, dh_prime=_TELEGRAM_DH_PRIME)
    assert len(auth_key) == 256
    assert server_salt(inner.new_nonce, res_pq.server_nonce) == server_salt(inner.new_nonce, res_pq.server_nonce)


def test_auth_key_exchange_rejects_weak_group_before_private_exponent() -> None:
    nonce = int.from_bytes(b"\x01" * 16, "little")
    server_nonce = 0x1112131415161718191A1B1C1D1E1F20
    new_nonce = int.from_bytes(b"\x01" * 32, "little")
    rsa_key = RSAKey(modulus=(1 << 2048) - 159, exponent=1)
    transport = FakeDHTransport(
        rsa_key=rsa_key,
        server_inner=ServerDHInnerData(
            nonce=nonce,
            server_nonce=server_nonce,
            g=3,
            dh_prime=(7919).to_bytes(2, "big"),
            g_a=pow(3, 5, 7919).to_bytes(2, "big"),
            server_time=1_771_000_000,
        ),
        new_nonce=new_nonce,
    )
    requested_sizes: list[int] = []

    def random_bytes(size: int) -> bytes:
        requested_sizes.append(size)
        return b"\x01" * size

    exchange = AuthKeyExchange(transport, dc_id=2, rsa_keys=(rsa_key,), random_bytes=random_bytes)
    with pytest.raises(ValueError, match="2048-bit"):
        run(exchange.create_auth_key())
    assert transport.calls == 2
    assert 256 not in requested_sizes


def test_auth_key_exchange_validates_generated_public_value_before_send() -> None:
    nonce = int.from_bytes(b"\x01" * 16, "little")
    server_nonce = 0x1112131415161718191A1B1C1D1E1F20
    new_nonce = int.from_bytes(b"\x01" * 32, "little")
    rsa_key = RSAKey(modulus=(1 << 2048) - 159, exponent=1)
    transport = FakeDHTransport(
        rsa_key=rsa_key,
        server_inner=ServerDHInnerData(
            nonce=nonce,
            server_nonce=server_nonce,
            g=3,
            dh_prime=_TELEGRAM_DH_PRIME_BYTES,
            g_a=(_TELEGRAM_DH_PRIME // 2).to_bytes(256, "big"),
            server_time=1_771_000_000,
        ),
        new_nonce=new_nonce,
    )

    def random_bytes(size: int) -> bytes:
        if size == 256:
            return b"\x01" + (b"\x00" * 255)
        return b"\x01" * size

    exchange = AuthKeyExchange(transport, dc_id=2, rsa_keys=(rsa_key,), random_bytes=random_bytes)
    with pytest.raises(ValueError, match="g_b"):
        run(exchange.create_auth_key())
    assert transport.calls == 2


def test_password_srp_rejects_weak_group_before_secret_derivation(monkeypatch: pytest.MonkeyPatch) -> None:
    def unexpected_secret_work(*args: object, **kwargs: object) -> bytes:
        raise AssertionError("invalid SRP parameters reached secret derivation")

    monkeypatch.setattr("miniproto.auth.password.hashlib.pbkdf2_hmac", unexpected_secret_work)
    monkeypatch.setattr("miniproto.auth.password.os.urandom", unexpected_secret_work)
    with pytest.raises(ValueError, match="2048-bit"):
        compute_check_password("secret", srp_password_state(p=7919, srp_b=3))


@pytest.mark.parametrize(
    "srp_b",
    [
        b"\x01" * 247,
        b"\x01" * 257,
        b"\x00" * 248,
        _TELEGRAM_DH_PRIME_BYTES,
        b"\x00" + (_TELEGRAM_DH_PRIME // 2).to_bytes(256, "big"),
    ],
)
def test_password_srp_rejects_invalid_b_encoding_or_range_before_secret_derivation(
    monkeypatch: pytest.MonkeyPatch, srp_b: bytes
) -> None:
    def unexpected_secret_work(*args: object, **kwargs: object) -> bytes:
        raise AssertionError("invalid SRP B reached secret derivation")

    monkeypatch.setattr("miniproto.auth.password.hashlib.pbkdf2_hmac", unexpected_secret_work)
    monkeypatch.setattr("miniproto.auth.password.os.urandom", unexpected_secret_work)
    with pytest.raises(ValueError, match="SRP B"):
        compute_check_password("secret", srp_password_state(srp_b=srp_b))


def test_password_srp_accepts_248_byte_b(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("miniproto.auth.password.os.urandom", lambda size: b"\x01" * size)
    result = compute_check_password("secret", srp_password_state(srp_b=b"\x01" * 248))
    assert isinstance(result, types.InputCheckPasswordSRP)


def test_password_srp_rejects_generated_a_at_strong_boundary(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("miniproto.auth.password.os.urandom", lambda size: (b"\x00" * (size - 1)) + b"\x01")
    with pytest.raises(ValueError, match="SRP A"):
        compute_check_password("secret", srp_password_state(srp_b=_TELEGRAM_DH_PRIME // 2))


def test_password_srp_accepts_official_group(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("miniproto.auth.password.os.urandom", lambda size: b"\x01" * size)
    result = compute_check_password("secret", srp_password_state(srp_b=_TELEGRAM_DH_PRIME // 2))
    assert isinstance(result, types.InputCheckPasswordSRP)
    assert len(result.A) == 256
    assert len(result.M1) == 32


def test_phone_sign_in_uses_generated_requests_and_persists_user_identity() -> None:
    async def scenario() -> None:
        storage = auth_storage()

        def handler(request: object) -> object:
            if isinstance(request, functions.AuthSendCode):
                assert isinstance(request.settings, types.CodeSettings)
                assert request.phone_number == "+9996621234"
                return sent_code()
            if isinstance(request, functions.AuthSignIn):
                assert request.phone_code_hash == "hash-1"
                assert request.phone_code == "22222"
                return user_authorization(user_id=42)
            if isinstance(request, functions.UpdatesGetState):
                return types.UpdatesState(pts=10, qts=0, date=1_700_000_000, seq=4, unread_count=0)
            raise AssertionError(f"unexpected request {request!r}")

        client = FakeAuthClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, dc_id=2), handler)
        result = await client.sign_in_phone("+9996621234", lambda: "22222")
        assert isinstance(result, types.AuthAuthorization)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.user is not None
        assert record.user.id == 42
        assert record.user.phone == "+9996621234"
        assert record.peers[0].kind == "self"
        assert [type(request) for request in client.requests] == [
            functions.AuthSendCode,
            functions.AuthSignIn,
            functions.UpdatesGetState,
        ]

    run(scenario())


def test_phone_sign_in_uses_password_callback_for_2fa() -> None:
    async def scenario() -> None:
        storage = auth_storage()
        password_values: list[str] = []

        def handler(request: object) -> object:
            if isinstance(request, functions.AuthSendCode):
                return sent_code()
            if isinstance(request, functions.AuthSignIn):
                raise RpcError("SESSION_PASSWORD_NEEDED", code=401)
            if isinstance(request, functions.AccountGetPassword):
                return empty_password_state()
            if isinstance(request, functions.AuthCheckPassword):
                assert isinstance(request.password, types.InputCheckPasswordEmpty)
                return user_authorization(user_id=77)
            if isinstance(request, functions.UpdatesGetState):
                return types.UpdatesState(pts=11, qts=0, date=1_700_000_002, seq=6, unread_count=0)
            raise AssertionError(f"unexpected request {request!r}")

        async def password_callback() -> str:
            password_values.append("called")
            return "secret-password"

        client = FakeAuthClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), handler)
        await client.sign_in_phone("+9996627777", lambda: "22222", password_callback)
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.user is not None
        assert record.user.id == 77
        assert password_values == ["called"]
        assert [type(request) for request in client.requests] == [
            functions.AuthSendCode,
            functions.AuthSignIn,
            functions.AccountGetPassword,
            functions.AuthCheckPassword,
            functions.UpdatesGetState,
        ]

    run(scenario())


def test_phone_sign_in_requires_password_callback_when_2fa_is_enabled() -> None:
    async def scenario() -> None:
        def handler(request: object) -> object:
            if isinstance(request, functions.AuthSendCode):
                return sent_code()
            if isinstance(request, functions.AuthSignIn):
                raise RpcError("SESSION_PASSWORD_NEEDED", code=401)
            raise AssertionError(f"unexpected request {request!r}")

        client = FakeAuthClient(
            ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()), handler
        )
        with pytest.raises(PasswordRequired):
            await client.sign_in_phone("+9996627777", lambda: "22222")

    run(scenario())


def test_wrong_phone_code_maps_to_invalid_code() -> None:
    async def scenario() -> None:
        def handler(request: object) -> object:
            if isinstance(request, functions.AuthSendCode):
                return sent_code()
            if isinstance(request, functions.AuthSignIn):
                raise RpcError("PHONE_CODE_INVALID", code=400)
            raise AssertionError(f"unexpected request {request!r}")

        client = FakeAuthClient(
            ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()), handler
        )
        with pytest.raises(InvalidCode):
            await client.sign_in_phone("+9996621234", lambda: "00000")

    run(scenario())


def test_bot_sign_in_uses_generated_import_bot_authorization_and_persists_bot_user() -> None:
    async def scenario() -> None:
        storage = auth_storage()

        def handler(request: object) -> object:
            if isinstance(request, functions.AuthImportBotAuthorization):
                assert request.flags == 0
                assert request.api_id == 1
                assert request.api_hash == "hash"
                assert request.bot_auth_token == _sample_bot_token()
                return user_authorization(user_id=123, bot=True)
            if isinstance(request, functions.UpdatesGetState):
                return types.UpdatesState(pts=22, qts=0, date=1_700_000_001, seq=5, unread_count=0)
            raise AssertionError(f"unexpected request {request!r}")

        client = FakeAuthClient(ClientConfig(api_id=1, api_hash="hash", session_storage=storage), handler)
        await client.sign_in_bot(_sample_bot_token())
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.user is not None
        assert record.user.is_bot
        assert record.user.username == "phase6bot"
        assert record.update_state.pts == 22
        assert [type(request) for request in client.requests] == [
            functions.AuthImportBotAuthorization,
            functions.UpdatesGetState,
        ]

    run(scenario())


def test_dc_options_env_and_migration_export_authorization() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"k" * 256, key_id=123),
                user=UserIdentity(id=42, access_hash=9042, username="alice", phone="+9996621234"),
            )
        )
        exported = types.AuthExportedAuthorization(id=55, bytes=b"exported")

        def handler(request: object) -> object:
            if isinstance(request, functions.AuthExportAuthorization):
                assert request.dc_id == 4
                return exported
            raise AssertionError(f"unexpected request {request!r}")

        service = AuthService(ClientConfig(api_id=1, api_hash="hash"), storage, handler)
        raw_config = type(
            "RawConfig",
            (),
            {
                "this_dc": 2,
                "dc_options": (
                    types.DcOption(id=2, ip_address="149.154.167.50", port=443),
                    types.DcOption(id=4, ip_address="149.154.167.91", port=443, ipv6=True),
                ),
            },
        )()
        options = await service.persist_dc_options(raw_config)
        assert options == (
            DCOption(id=2, ip_address="149.154.167.50", port=443),
            DCOption(id=4, ip_address="149.154.167.91", port=443, ipv6=True),
        )
        assert dc_options_from_env({"MINIPROTO_TEST_DC5": "[2001:db8::5]:443"}) == (
            DCOption(id=5, ip_address="2001:db8::5", port=443, static=True),
        )
        result = await service.handle_dc_migration(DatacenterMigration(4, kind="PHONE"))
        assert result == exported
        loaded = await storage.load()
        assert loaded is not None
        assert session_record_from_mapping(loaded).dc_id == 4

    run(scenario())


def test_auth_rpc_error_classification() -> None:
    assert isinstance(classify_rpc_error(RpcError("AUTH_KEY_UNREGISTERED", code=401)), AuthKeyNotFound)
    migration = classify_rpc_error(RpcError("USER_MIGRATE_4", code=303))
    assert isinstance(migration, DatacenterMigration)
    assert migration.dc_id == 4
    flood = classify_rpc_error(RpcError("FLOOD_WAIT_9", code=420))
    assert isinstance(flood, FloodWait)
    # Ordinary RPC flood waits are not transport-level 429s.
    assert not isinstance(flood, TransportFlood)
    assert flood.seconds == 9


def test_auth_key_not_found_recovery_clears_key_and_user_identity() -> None:
    async def scenario() -> None:
        storage = InMemorySessionStorage(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"k" * 256, key_id=123),
                user=UserIdentity(id=42, access_hash=9042, username="alice", phone="+9996621234"),
            )
        )
        await clear_invalid_auth_key(storage, ClientConfig(api_id=1, api_hash="hash", dc_id=2))
        loaded = await storage.load()
        assert loaded is not None
        record = session_record_from_mapping(loaded)
        assert record.auth_key is None
        assert record.user is None

    run(scenario())

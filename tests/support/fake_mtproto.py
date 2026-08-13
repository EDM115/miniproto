from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable, Iterator
from dataclasses import dataclass, field

from miniproto.auth.dh_validation import _TELEGRAM_DH_PRIME_BYTES
from miniproto.auth.key_exchange import (
    ResPQ,
    RSAKey,
    ServerDHInnerData,
    ServerDHParamsOk,
    compute_new_nonce_hash,
    derive_tmp_aes_key_iv,
    encode_server_dh_answer,
    serialize_dh_gen_ok,
    server_salt,
)
from miniproto.config import TransportConfig
from miniproto.connection.tcp_abridged import TcpAbridgedTransport
from miniproto.connection.tcp_intermediate import TcpIntermediateTransport, TcpPaddedIntermediateTransport
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.crypto.native import aes_256_ige_decrypt, sha1_digest, sha256_digest, xor_bytes
from miniproto.mtproto.codec import (
    DecodedEncryptedMessage,
    MessageContainer,
    MsgsAck,
    decode_encrypted_message,
    decode_message_body,
    decode_unencrypted_message,
    encode_encrypted_message,
    encode_message_body,
    encode_unencrypted_message,
)
from miniproto.mtproto.state import MTProtoState
from miniproto.tl.codec import decode_bytes, decode_constructor_id, decode_int128, decode_long

FakeHandler = Callable[[DecodedEncryptedMessage], Awaitable[bytes | object | None] | bytes | object | None]


@dataclass(slots=True)
class FakeMTProtoServer:
    auth_key: bytes
    config: TransportConfig
    handler: FakeHandler
    server_salt: int = 0x1111222233334444
    session_id: int = 0x5555666677778888
    host: str = "127.0.0.1"
    drop_connections_before_packet: int = 0
    connections_accepted: int = 0
    acks_received: list[int] = field(default_factory=list)
    containered_bodies: int = 0
    _server: asyncio.AbstractServer | None = None
    _state: MTProtoState | None = None

    @property
    def endpoint(self) -> ConnectionEndpoint:
        if self._server is None:
            raise RuntimeError("fake server is not started")
        sockets = getattr(self._server, "sockets", None)
        if not sockets:
            raise RuntimeError("fake server has no bound socket")
        socket = sockets[0]
        host, port = socket.getsockname()[:2]
        return ConnectionEndpoint(str(host), int(port))

    async def __aenter__(self) -> FakeMTProtoServer:
        await self.start()
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.close()

    async def start(self) -> None:
        self._state = MTProtoState(auth_key=self.auth_key, server_salt=self.server_salt, session_id=self.session_id)
        self._server = await asyncio.start_server(self._handle_client, self.host, 0)

    async def close(self) -> None:
        if self._server is None:
            return
        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        transport = _ServerTransport(reader, writer, self.config)
        try:
            await transport.read_handshake()
            self.connections_accepted += 1
            if self.drop_connections_before_packet > 0:
                self.drop_connections_before_packet -= 1
                return
            while True:
                packet = await transport.read_packet()
                incoming = decode_encrypted_message(self.auth_key, packet, client_to_server=True)
                for leaf in self._leaves(incoming):
                    response = self.handler(leaf)
                    if asyncio.iscoroutine(response):
                        response = await response
                    if response is None:
                        continue
                    state = self._state
                    if state is None:
                        raise RuntimeError("fake server state missing")
                    msg_id = state.next_msg_id() | 1
                    seq_no = state.next_seq_no(content_related=True)
                    await transport.send_packet(
                        encode_encrypted_message(
                            self.auth_key,
                            incoming.server_salt,
                            incoming.session_id,
                            msg_id,
                            seq_no,
                            response,
                            client_to_server=False,
                        )
                    )
        except (asyncio.IncompleteReadError, ConnectionError, ValueError):
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    def _leaves(self, incoming: DecodedEncryptedMessage) -> Iterator[DecodedEncryptedMessage]:
        """Unwrap client-sent msg_containers into individual handler dispatches.

        Ack messages riding inside containers are recorded on ``acks_received``
        instead of reaching the handler, mirroring how a real server consumes
        them; top-level MsgsAck frames still reach the handler for tests that
        assert standalone ack flushes.
        """
        body = decode_message_body(incoming.body)
        if not isinstance(body, MessageContainer):
            yield incoming
            return
        for item in body.messages:
            body_bytes = item.body if isinstance(item.body, bytes | memoryview) else encode_message_body(item.body)
            nested_body = decode_message_body(body_bytes)
            if isinstance(nested_body, MsgsAck):
                self.acks_received.extend(nested_body.msg_ids)
                continue
            self.containered_bodies += 1
            yield DecodedEncryptedMessage(
                auth_key_id=incoming.auth_key_id,
                server_salt=incoming.server_salt,
                session_id=incoming.session_id,
                msg_id=item.msg_id,
                seq_no=item.seq_no,
                body=body_bytes,
                padding=b"",
            )


@dataclass(slots=True)
class FakeAuthMTProtoServer:
    """Socket fake that performs one real MTProto auth-key exchange, then serves encrypted RPCs.

    The fixture advertises an exponent-one RSA key so tests can reverse Telegram's
    RSA_PAD envelope without embedding a private production/test key. All DH,
    temporary-AES, nonce-hash, transport, and encrypted-envelope work on the
    client side still runs through production code.
    """

    config: TransportConfig
    handler: FakeHandler
    host: str = "127.0.0.1"
    rsa_key: RSAKey = field(default_factory=lambda: RSAKey(modulus=(1 << 2048) - 159, exponent=1))
    auth_key: bytes | None = field(default=None, init=False, repr=False)
    server_salt: int | None = field(default=None, init=False)
    auth_handshakes: int = field(default=0, init=False)
    encrypted_connections: int = field(default=0, init=False)
    encrypted_requests: int = field(default=0, init=False)
    acks_received: list[int] = field(default_factory=list)
    containered_bodies: int = 0
    errors: list[BaseException] = field(default_factory=list)
    _server: asyncio.AbstractServer | None = field(default=None, init=False, repr=False)
    _state: MTProtoState | None = field(default=None, init=False, repr=False)

    @property
    def endpoint(self) -> ConnectionEndpoint:
        if self._server is None:
            raise RuntimeError("fake auth server is not started")
        sockets = getattr(self._server, "sockets", None)
        if not sockets:
            raise RuntimeError("fake auth server has no bound socket")
        host, port = sockets[0].getsockname()[:2]
        return ConnectionEndpoint(str(host), int(port))

    async def __aenter__(self) -> FakeAuthMTProtoServer:
        await self.start()
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.close()

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handle_client, self.host, 0)

    async def close(self) -> None:
        if self._server is None:
            return
        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        transport = _ServerTransport(reader, writer, self.config)
        try:
            await transport.read_handshake()
            first_packet = await transport.read_packet()
            if first_packet[:8] == b"\x00" * 8:
                await self._handle_auth_exchange(transport, first_packet)
            else:
                self.encrypted_connections += 1
                await self._handle_encrypted_connection(transport, first_packet)
        except (asyncio.IncompleteReadError, ConnectionError):
            pass
        except BaseException as exc:
            self.errors.append(exc)
        finally:
            writer.close()
            await writer.wait_closed()

    async def _handle_auth_exchange(self, transport: _ServerTransport, first_packet: bytes) -> None:
        if self.auth_key is not None:
            raise ValueError("fake auth server received a duplicate auth-key exchange")
        req_pq = decode_unencrypted_message(first_packet)
        constructor_id, offset = decode_constructor_id(req_pq.body, 0)
        if constructor_id != 0xBE7E8EF1:
            raise ValueError("fake auth server expected req_pq_multi")
        nonce, offset = decode_int128(req_pq.body, offset)
        if offset != len(req_pq.body):
            raise ValueError("req_pq_multi has trailing bytes")
        server_nonce = int.from_bytes(b"fake-server-nonc", "little")
        await self._send_unencrypted(
            transport,
            ResPQ(
                nonce=nonce,
                server_nonce=server_nonce,
                pq=(17 * 23).to_bytes(2, "big"),
                server_public_key_fingerprints=(self.rsa_key.fingerprint,),
            ).serialize(),
        )

        req_dh_message = decode_unencrypted_message(await transport.read_packet())
        new_nonce = self._decode_req_dh_params(req_dh_message.body, nonce=nonce, server_nonce=server_nonce)
        dh_prime = int.from_bytes(_TELEGRAM_DH_PRIME_BYTES, "big")
        private_a = int.from_bytes(bytes(range(256)), "little")
        g_a = pow(3, private_a, dh_prime)
        server_inner = ServerDHInnerData(
            nonce=nonce,
            server_nonce=server_nonce,
            g=3,
            dh_prime=_TELEGRAM_DH_PRIME_BYTES,
            g_a=g_a.to_bytes(256, "big"),
            server_time=int(time.time()),
        )
        padding = b"\x00" * (-(20 + len(server_inner.serialize())) % 16)
        await self._send_unencrypted(
            transport,
            ServerDHParamsOk(
                nonce=nonce,
                server_nonce=server_nonce,
                encrypted_answer=encode_server_dh_answer(
                    server_inner, new_nonce=new_nonce, server_nonce=server_nonce, padding=padding
                ),
            ).serialize(),
        )

        set_client_dh = decode_unencrypted_message(await transport.read_packet())
        g_b = self._decode_set_client_dh_params(
            set_client_dh.body, nonce=nonce, server_nonce=server_nonce, new_nonce=new_nonce
        )
        self.auth_key = pow(g_b, private_a, dh_prime).to_bytes(256, "big")
        self.server_salt = server_salt(new_nonce, server_nonce)
        self._state = MTProtoState(auth_key=self.auth_key, server_salt=self.server_salt, session_id=0x5555666677778888)
        self.auth_handshakes += 1
        await self._send_unencrypted(
            transport, serialize_dh_gen_ok(nonce, server_nonce, compute_new_nonce_hash(new_nonce, self.auth_key, 1))
        )

    def _decode_req_dh_params(self, body: bytes | memoryview, *, nonce: int, server_nonce: int) -> int:
        constructor_id, offset = decode_constructor_id(body, 0)
        if constructor_id != 0xD712E4BE:
            raise ValueError("fake auth server expected req_DH_params")
        request_nonce, offset = decode_int128(body, offset)
        request_server_nonce, offset = decode_int128(body, offset)
        p, offset = decode_bytes(body, offset)
        q, offset = decode_bytes(body, offset)
        fingerprint, offset = decode_long(body, offset)
        encrypted_data, offset = decode_bytes(body, offset)
        if offset != len(body):
            raise ValueError("req_DH_params has trailing bytes")
        if request_nonce != nonce or request_server_nonce != server_nonce:
            raise ValueError("req_DH_params nonce mismatch")
        if int.from_bytes(p, "big") * int.from_bytes(q, "big") != 17 * 23:
            raise ValueError("req_DH_params factors mismatch")
        if fingerprint != self.rsa_key.fingerprint:
            raise ValueError("req_DH_params RSA fingerprint mismatch")
        inner = _reverse_exponent_one_rsa_pad(bytes(encrypted_data))
        constructor_id, cursor = decode_constructor_id(inner, 0)
        if constructor_id != 0xA9F55F95:
            raise ValueError("fake auth server expected p_q_inner_data_dc")
        _pq, cursor = decode_bytes(inner, cursor)
        _p, cursor = decode_bytes(inner, cursor)
        _q, cursor = decode_bytes(inner, cursor)
        inner_nonce, cursor = decode_int128(inner, cursor)
        inner_server_nonce, cursor = decode_int128(inner, cursor)
        new_nonce = int.from_bytes(inner[cursor : cursor + 32], "little")
        if inner_nonce != nonce or inner_server_nonce != server_nonce:
            raise ValueError("p_q_inner_data_dc nonce mismatch")
        return new_nonce

    @staticmethod
    def _decode_set_client_dh_params(body: bytes | memoryview, *, nonce: int, server_nonce: int, new_nonce: int) -> int:
        constructor_id, offset = decode_constructor_id(body, 0)
        if constructor_id != 0xF5045F1F:
            raise ValueError("fake auth server expected set_client_DH_params")
        request_nonce, offset = decode_int128(body, offset)
        request_server_nonce, offset = decode_int128(body, offset)
        encrypted_data, offset = decode_bytes(body, offset)
        if offset != len(body) or request_nonce != nonce or request_server_nonce != server_nonce:
            raise ValueError("set_client_DH_params nonce or length mismatch")
        key, iv = derive_tmp_aes_key_iv(new_nonce, server_nonce)
        plaintext = aes_256_ige_decrypt(bytes(encrypted_data), key, iv)
        constructor_id, cursor = decode_constructor_id(plaintext, 20)
        if constructor_id != 0x6643B654:
            raise ValueError("fake auth server expected client_DH_inner_data")
        inner_nonce, cursor = decode_int128(plaintext, cursor)
        inner_server_nonce, cursor = decode_int128(plaintext, cursor)
        _retry_id, cursor = decode_long(plaintext, cursor)
        g_b, cursor = decode_bytes(plaintext, cursor)
        if inner_nonce != nonce or inner_server_nonce != server_nonce:
            raise ValueError("client_DH_inner_data nonce mismatch")
        if sha1_digest(plaintext[20:cursor]) != plaintext[:20]:
            raise ValueError("client_DH_inner_data SHA1 mismatch")
        return int.from_bytes(g_b, "big")

    async def _handle_encrypted_connection(self, transport: _ServerTransport, first_packet: bytes) -> None:
        packet = first_packet
        while True:
            auth_key = self.auth_key
            if auth_key is None:
                raise ValueError("encrypted connection arrived before auth-key exchange")
            incoming = decode_encrypted_message(auth_key, packet, client_to_server=True)
            for leaf in self._leaves(incoming):
                self.encrypted_requests += 1
                response = self.handler(leaf)
                if asyncio.iscoroutine(response):
                    response = await response
                if response is None:
                    continue
                state = self._state
                if state is None:
                    raise RuntimeError("fake auth server state missing")
                await transport.send_packet(
                    encode_encrypted_message(
                        auth_key,
                        incoming.server_salt,
                        incoming.session_id,
                        state.next_msg_id() | 1,
                        state.next_seq_no(content_related=True),
                        response,
                        client_to_server=False,
                    )
                )
            packet = await transport.read_packet()

    def _leaves(self, incoming: DecodedEncryptedMessage) -> Iterator[DecodedEncryptedMessage]:
        body = decode_message_body(incoming.body)
        if not isinstance(body, MessageContainer):
            yield incoming
            return
        for item in body.messages:
            body_bytes = item.body if isinstance(item.body, bytes | memoryview) else encode_message_body(item.body)
            nested_body = decode_message_body(body_bytes)
            if isinstance(nested_body, MsgsAck):
                self.acks_received.extend(nested_body.msg_ids)
                continue
            self.containered_bodies += 1
            yield DecodedEncryptedMessage(
                auth_key_id=incoming.auth_key_id,
                server_salt=incoming.server_salt,
                session_id=incoming.session_id,
                msg_id=item.msg_id,
                seq_no=item.seq_no,
                body=body_bytes,
                padding=b"",
            )

    @staticmethod
    async def _send_unencrypted(transport: _ServerTransport, body: bytes) -> None:
        msg_id = (int(time.time() * 2**32) & ~3) | 1
        await transport.send_packet(encode_unencrypted_message(msg_id, body))


def _reverse_exponent_one_rsa_pad(encrypted_data: bytes) -> bytes:
    if len(encrypted_data) != 256:
        raise ValueError("RSA_PAD envelope must be 256 bytes")
    temp_key_xor = encrypted_data[:32]
    aes_encrypted = encrypted_data[32:]
    temp_key = xor_bytes(temp_key_xor, sha256_digest(aes_encrypted))
    decrypted = aes_256_ige_decrypt(aes_encrypted, temp_key, b"\x00" * 32)
    data_with_padding = decrypted[:192][::-1]
    if sha256_digest(temp_key + data_with_padding) != decrypted[192:]:
        raise ValueError("RSA_PAD integrity mismatch")
    return data_with_padding


class _ServerTransport:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, config: TransportConfig) -> None:
        self.reader = reader
        self.writer = writer
        self.config = config
        match config.mode:
            case "tcp_abridged":
                self._codec = TcpAbridgedTransport(ConnectionEndpoint("127.0.0.1", 1), config)
            case "tcp_intermediate":
                self._codec = TcpIntermediateTransport(ConnectionEndpoint("127.0.0.1", 1), config)
            case "tcp_padded_intermediate":
                self._codec = TcpPaddedIntermediateTransport(ConnectionEndpoint("127.0.0.1", 1), config)
            case _:
                raise ValueError(f"unsupported transport mode {config.mode!r}")

    async def read_handshake(self) -> None:
        tag = self._codec.handshake_tag
        if tag:
            received = await self.reader.readexactly(len(tag))
            if received != tag:
                raise ValueError("unexpected transport handshake tag")

    async def read_packet(self) -> bytes:
        return await self._codec.read_packet(self.reader)

    async def send_packet(self, payload: bytes) -> None:
        self.writer.write(self._codec.encode_packet(payload))
        await self.writer.drain()

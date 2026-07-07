from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterator
from dataclasses import dataclass, field

from miniproto.config import TransportConfig
from miniproto.connection.tcp_abridged import TcpAbridgedTransport
from miniproto.connection.tcp_intermediate import (
    TcpIntermediateTransport,
    TcpPaddedIntermediateTransport,
)
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.mtproto.codec import (
    DecodedEncryptedMessage,
    MessageContainer,
    MsgsAck,
    decode_encrypted_message,
    decode_message_body,
    encode_encrypted_message,
    encode_message_body,
)
from miniproto.mtproto.state import MTProtoState

FakeHandler = Callable[
    [DecodedEncryptedMessage], Awaitable[bytes | object | None] | bytes | object | None
]


@dataclass(slots=True)
class FakeMTProtoServer:
    auth_key: bytes
    config: TransportConfig
    handler: FakeHandler
    server_salt: int = 0x1111222233334444
    session_id: int = 0x5555666677778888
    host: str = "127.0.0.1"
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
        self._state = MTProtoState(
            auth_key=self.auth_key, server_salt=self.server_salt, session_id=self.session_id
        )
        self._server = await asyncio.start_server(self._handle_client, self.host, 0)

    async def close(self) -> None:
        if self._server is None:
            return
        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        transport = _ServerTransport(reader, writer, self.config)
        try:
            await transport.read_handshake()
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
            if isinstance(item.body, MsgsAck):
                self.acks_received.extend(item.body.msg_ids)
                continue
            self.containered_bodies += 1
            yield DecodedEncryptedMessage(
                auth_key_id=incoming.auth_key_id,
                server_salt=incoming.server_salt,
                session_id=incoming.session_id,
                msg_id=item.msg_id,
                seq_no=item.seq_no,
                body=encode_message_body(item.body),
                padding=b"",
            )


class _ServerTransport:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, config: TransportConfig
    ) -> None:
        self.reader = reader
        self.writer = writer
        self.config = config
        match config.mode:
            case "tcp_abridged":
                self._codec = TcpAbridgedTransport(ConnectionEndpoint("127.0.0.1", 1), config)
            case "tcp_intermediate":
                self._codec = TcpIntermediateTransport(ConnectionEndpoint("127.0.0.1", 1), config)
            case "tcp_padded_intermediate":
                self._codec = TcpPaddedIntermediateTransport(
                    ConnectionEndpoint("127.0.0.1", 1), config
                )
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

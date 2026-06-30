from __future__ import annotations

import asyncio

from miniproto.connection.transport import StreamTransportBase, TransportError, read_exactly_bounded


class TcpIntermediateTransport(StreamTransportBase):
    handshake_tag = b"\xee\xee\xee\xee"

    def encode_packet(self, payload: bytes) -> bytes:
        if len(payload) > 0x7FFFFFFF:
            raise TransportError("tcp intermediate payload is too large")
        return len(payload).to_bytes(4, "little", signed=True) + payload

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        length = int.from_bytes(
            await read_exactly_bounded(reader, 4, self.config.max_payload_size),
            "little",
            signed=True,
        )
        return await read_exactly_bounded(reader, length, self.config.max_payload_size)


class TcpPaddedIntermediateTransport(TcpIntermediateTransport):
    handshake_tag = b"\xdd\xdd\xdd\xdd"

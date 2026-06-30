from __future__ import annotations

import asyncio

from miniproto.connection.transport import StreamTransportBase, TransportError, read_exactly_bounded


class TcpAbridgedTransport(StreamTransportBase):
    handshake_tag = b"\xef"

    def encode_packet(self, payload: bytes) -> bytes:
        if len(payload) % 4 != 0:
            raise TransportError("tcp abridged payload length must be divisible by 4")
        length_words = len(payload) // 4
        if length_words < 0x7F:
            return bytes([length_words]) + payload
        if length_words > 0xFFFFFF:
            raise TransportError("tcp abridged payload is too large")
        return b"\x7f" + length_words.to_bytes(3, "little") + payload

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        first = await read_exactly_bounded(reader, 1, self.config.max_payload_size)
        if first[0] < 0x7F:
            length_words = first[0]
        else:
            length_words = int.from_bytes(
                await read_exactly_bounded(reader, 3, self.config.max_payload_size), "little"
            )
        return await read_exactly_bounded(reader, length_words * 4, self.config.max_payload_size)

"""Telegram's abridged TCP transport specialization."""

from miniproto.connection.transport import StreamTransportBase


class TcpAbridgedTransport(StreamTransportBase):
    """Stream transport using Telegram's compact four-byte-word TCP framing.

    The base class owns connection, timeout, quick-ACK and close behavior;
    this specialization only selects its wire handshake and codec mode.
    """

    handshake_tag = b"\xef"
    transport_mode = "tcp_abridged"

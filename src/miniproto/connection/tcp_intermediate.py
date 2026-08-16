"""Telegram intermediate and padded-intermediate TCP transport specializations."""

from miniproto.connection.transport import StreamTransportBase


class TcpIntermediateTransport(StreamTransportBase):
    """Stream transport using Telegram's fixed-width intermediate framing."""

    handshake_tag = b"\xee\xee\xee\xee"
    transport_mode = "tcp_intermediate"


class TcpPaddedIntermediateTransport(TcpIntermediateTransport):
    """Intermediate transport variant that adds random wire padding per frame."""

    handshake_tag = b"\xdd\xdd\xdd\xdd"
    transport_mode = "tcp_padded_intermediate"

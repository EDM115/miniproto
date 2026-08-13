from miniproto.connection.transport import StreamTransportBase


class TcpIntermediateTransport(StreamTransportBase):
    handshake_tag = b"\xee\xee\xee\xee"
    transport_mode = "tcp_intermediate"


class TcpPaddedIntermediateTransport(TcpIntermediateTransport):
    handshake_tag = b"\xdd\xdd\xdd\xdd"
    transport_mode = "tcp_padded_intermediate"

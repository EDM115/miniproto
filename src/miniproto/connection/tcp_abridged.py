from miniproto.connection.transport import StreamTransportBase


class TcpAbridgedTransport(StreamTransportBase):
    handshake_tag = b"\xef"
    transport_mode = "tcp_abridged"

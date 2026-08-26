"""MTProto encrypted framing and core service-message body codecs."""

from __future__ import annotations

import gzip
from dataclasses import dataclass
from typing import cast

from miniproto.crypto.native import mtproto_decode_message as _mtproto_decode_message
from miniproto.crypto.native import mtproto_encode_message as _mtproto_encode_message
from miniproto.tl import (
    decode_bytes,
    decode_constructor_id,
    decode_int,
    decode_string,
    encode_bytes,
    encode_constructor_id,
    encode_int,
    encode_string,
    encode_vector,
)
from miniproto.tl.fast import decode_fast, encode_fast

_MSGS_ACK_ID = 0x62D6B459
_MSGS_STATE_REQ_ID = 0xDA69FB52
_MSGS_STATE_INFO_ID = 0x04DEB57D
_MSG_RESEND_REQ_ID = 0x7D861A08
_MSG_CONTAINER_ID = 0x73F1F8DC
_GZIP_PACKED_ID = 0x3072CFA1
_PING_ID = 0x7ABE77EC
_PING_DELAY_DISCONNECT_ID = 0xF3427B8C
_PONG_ID = 0x347773C5
_BAD_MSG_NOTIFICATION_ID = 0xA7EFF811
_BAD_SERVER_SALT_ID = 0xEDAB447B
_NEW_SESSION_CREATED_ID = 0x9EC20908
_RPC_RESULT_ID = 0xF35C6D01
_RPC_ERROR_ID = 0x2144CA19
_FAST_SERVICE_IDS = frozenset(
    {
        _MSGS_ACK_ID,
        _MSGS_STATE_REQ_ID,
        _MSGS_STATE_INFO_ID,
        _MSG_RESEND_REQ_ID,
        _MSG_CONTAINER_ID,
        _GZIP_PACKED_ID,
        _PONG_ID,
        _BAD_MSG_NOTIFICATION_ID,
        _BAD_SERVER_SALT_ID,
        _RPC_RESULT_ID,
    }
)
type ByteBuffer = bytes | memoryview


@dataclass(frozen=True, slots=True)
class DecodedEncryptedMessage:
    """Authenticated encrypted MTProto envelope with decrypted body and padding.

    Attributes:
        auth_key_id: Eight-byte authorization-key identifier from the envelope.
        server_salt: Decrypted 64-bit server salt.
        session_id: Decrypted 64-bit session ID.
        msg_id: MTProto message ID.
        seq_no: MTProto sequence number.
        body: Decrypted message body view.
        padding: Decrypted trailing padding view.
    """

    auth_key_id: bytes
    server_salt: int
    session_id: int
    msg_id: int
    seq_no: int
    body: ByteBuffer
    padding: ByteBuffer


@dataclass(frozen=True, slots=True)
class UnencryptedMessage:
    """Unencrypted MTProto envelope carrying a message ID and raw body.

    Attributes:
        msg_id: MTProto message ID.
        body: Raw unencrypted message-body view.
    """

    msg_id: int
    body: ByteBuffer


@dataclass(frozen=True, slots=True)
class MsgsAck:
    """MTProto ``msgs_ack`` body acknowledging received message IDs.

    Attributes:
        msg_ids: Acknowledged MTProto message IDs.
    """

    msg_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MsgsStateReq:
    """MTProto ``msgs_state_req`` body requesting message states.

    Attributes:
        msg_ids: Message IDs whose states are requested.
    """

    msg_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MsgsStateInfo:
    """MTProto ``msgs_state_info`` body answering a state request.

    Attributes:
        req_msg_id: Message ID of the corresponding state request.
        info: Opaque state information bytes.
    """

    req_msg_id: int
    info: bytes


@dataclass(frozen=True, slots=True)
class MsgResendReq:
    """MTProto ``msg_resend_req`` body requesting retransmission of message IDs.

    Attributes:
        msg_ids: Message IDs requested for retransmission.
    """

    msg_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MessageContainerItem:
    """One message entry inside an MTProto message container.

    Attributes:
        msg_id: Contained MTProto message ID.
        seq_no: Contained MTProto sequence number.
        body: Raw or encodable contained message body.
    """

    msg_id: int
    seq_no: int
    body: ByteBuffer | object


@dataclass(frozen=True, slots=True)
class MessageContainer:
    """MTProto ``msg_container`` body containing ordered message entries.

    Attributes:
        messages: Ordered contained message entries.
    """

    messages: tuple[MessageContainerItem, ...]


@dataclass(frozen=True, slots=True)
class GzipPacked:
    """MTProto ``gzip_packed`` service body holding compressed message bytes.

    Attributes:
        packed_data: Gzip-compressed message-body bytes.
    """

    packed_data: ByteBuffer

    def unpack(self) -> bytes:
        """Decompress the contained gzip payload.

        Returns:
            Uncompressed message-body bytes.

        Raises:
            OSError: If the stored bytes are not a valid gzip stream.
        """
        return gzip.decompress(self.packed_data)


@dataclass(frozen=True, slots=True)
class Pong:
    """MTProto ``pong`` response correlating a server message and ping ID.

    Attributes:
        msg_id: Server message ID carrying the response.
        ping_id: Caller-selected ID from the corresponding ping.
    """

    msg_id: int
    ping_id: int


@dataclass(frozen=True, slots=True)
class BadMsgNotification:
    """MTProto notice that a message ID, sequence number or other field was invalid.

    Attributes:
        bad_msg_id: Rejected message ID.
        bad_msg_seq_no: Rejected sequence number.
        error_code: MTProto validation error code.
    """

    bad_msg_id: int
    bad_msg_seq_no: int
    error_code: int


@dataclass(frozen=True, slots=True)
class BadServerSalt:
    """MTProto bad-message notice that additionally carries a replacement server salt.

    Attributes:
        bad_msg_id: Rejected message ID.
        bad_msg_seq_no: Rejected sequence number.
        error_code: MTProto validation error code.
        new_server_salt: Replacement 64-bit server salt.
    """

    bad_msg_id: int
    bad_msg_seq_no: int
    error_code: int
    new_server_salt: int


@dataclass(frozen=True, slots=True)
class NewSessionCreated:
    """MTProto notification that establishes a new server session and salt.

    Attributes:
        first_msg_id: First client message ID in the session.
        unique_id: Server-provided session uniqueness value.
        server_salt: Initial 64-bit server salt.
    """

    first_msg_id: int
    unique_id: int
    server_salt: int


@dataclass(frozen=True, slots=True)
class RpcErrorBody:
    """Decoded MTProto ``rpc_error`` result body.

    Attributes:
        error_code: Telegram RPC error code.
        error_message: Telegram RPC error name or detail string.
    """

    error_code: int
    error_message: str


@dataclass(frozen=True, slots=True)
class RpcResult:
    """MTProto ``rpc_result`` body containing raw or decoded result data.

    Attributes:
        req_msg_id: Message ID of the corresponding RPC request.
        result: Raw result bytes or a decoded result object.
    """

    req_msg_id: int
    result: ByteBuffer | object


def encode_unencrypted_message(msg_id: int, body: bytes | object) -> bytes:
    """Frame an unencrypted MTProto message with ``auth_key_id = 0``.

    Args:
        msg_id: MTProto message identifier.
        body: Raw body bytes or a supported encodable body object.

    Returns:
        Complete unencrypted MTProto envelope bytes.
    """
    body_bytes = encode_message_body(body)
    return b"\x00" * 8 + _pack_i64(msg_id) + encode_int(len(body_bytes)) + body_bytes


def decode_unencrypted_message(packet: ByteBuffer) -> UnencryptedMessage:
    """Validate and decode an unencrypted MTProto envelope.

    Args:
        packet: Complete unencrypted packet bytes.

    Returns:
        Message identifier and a body memoryview.

    Raises:
        ValueError: If the packet is too short, nonzero-authenticated or malformed.
    """
    packet_view = memoryview(packet)
    if len(packet) < 20:
        raise ValueError("unencrypted MTProto packet is too short")
    if packet_view[:8] != b"\x00" * 8:
        raise ValueError("unencrypted MTProto packet must have auth_key_id=0")
    msg_id = _unpack_i64(packet, 8)
    body_len, offset = decode_int(packet, 16)
    if body_len < 0 or offset + body_len > len(packet):
        raise ValueError("unencrypted MTProto packet body length is invalid")
    return UnencryptedMessage(msg_id=msg_id, body=packet_view[offset : offset + body_len])


def encode_encrypted_message(
    auth_key: bytes,
    server_salt: int,
    session_id: int,
    msg_id: int,
    seq_no: int,
    body: bytes | object,
    *,
    client_to_server: bool = True,
    padding: bytes | None = None,
) -> bytes:
    """Encrypt and frame one MTProto message using the configured authorization key.

    Args:
        auth_key: 256-byte MTProto authorization key.
        server_salt: Current 64-bit server salt.
        session_id: Current 64-bit session ID.
        msg_id: MTProto message identifier.
        seq_no: MTProto sequence number.
        body: Raw or supported encoded body.
        client_to_server: Use client-to-server derivation, defaulting to ``True``.
        padding: Optional explicit padding; native codec chooses valid padding when omitted.

    Returns:
        Complete encrypted MTProto packet bytes.
    """
    body_bytes = encode_message_body(body)
    return _mtproto_encode_message(
        auth_key,
        server_salt,
        session_id,
        msg_id,
        seq_no,
        body_bytes,
        client_to_server=client_to_server,
        padding=padding,
    )


def decode_encrypted_message(
    auth_key: bytes, packet: ByteBuffer, *, client_to_server: bool = False
) -> DecodedEncryptedMessage:
    """Authenticate, decrypt and parse one MTProto encrypted envelope.

    Args:
        auth_key: 256-byte MTProto authorization key.
        packet: Complete encrypted packet bytes.
        client_to_server: Direction used for message-key derivation; defaults to server-to-client.

    Returns:
        Decrypted envelope fields with body and padding views.

    Raises:
        ValueError: If the native codec rejects framing, key or integrity data.
    """
    auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding = _mtproto_decode_message(
        auth_key, packet, client_to_server=client_to_server
    )
    return DecodedEncryptedMessage(
        auth_key_id=auth_key_id,
        server_salt=server_salt,
        session_id=session_id,
        msg_id=msg_id,
        seq_no=seq_no,
        body=memoryview(body),
        padding=memoryview(padding),
    )


def encode_message_body(body: ByteBuffer | object) -> bytes:
    """Encode raw, generated or built-in MTProto service message bodies.

    Args:
        body: Bytes, generated TL object or supported service-body object.

    Returns:
        Constructor-prefixed MTProto body bytes where applicable.

    Raises:
        TypeError: If the body is not supported by this codec.
    """
    if isinstance(body, bytes):
        return body
    if isinstance(body, bytearray | memoryview):
        return bytes(body)
    serialize = getattr(body, "serialize", None)
    if callable(serialize):
        return serialize()
    match body:
        case MsgsAck(msg_ids=msg_ids):
            return encode_fast(_MSGS_ACK_ID, (msg_ids,)) or encode_constructor_id(_MSGS_ACK_ID) + encode_vector(
                msg_ids, "long"
            )
        case MsgsStateReq(msg_ids=msg_ids):
            return encode_fast(_MSGS_STATE_REQ_ID, (msg_ids,)) or encode_constructor_id(
                _MSGS_STATE_REQ_ID
            ) + encode_vector(msg_ids, "long")
        case MsgsStateInfo(req_msg_id=req_msg_id, info=info):
            return encode_fast(_MSGS_STATE_INFO_ID, (req_msg_id, info)) or encode_constructor_id(
                _MSGS_STATE_INFO_ID
            ) + _pack_i64(req_msg_id) + encode_bytes(info)
        case MsgResendReq(msg_ids=msg_ids):
            return encode_fast(_MSG_RESEND_REQ_ID, (msg_ids,)) or encode_constructor_id(
                _MSG_RESEND_REQ_ID
            ) + encode_vector(msg_ids, "long")
        case MessageContainer(messages=messages):
            encoded_messages = tuple(
                (message.msg_id, message.seq_no, encode_message_body(message.body)) for message in messages
            )
            native = encode_fast(_MSG_CONTAINER_ID, (encoded_messages,))
            if native is not None:
                return native
            output = bytearray(encode_constructor_id(_MSG_CONTAINER_ID))
            output.extend(encode_int(len(messages)))
            for msg_id, seq_no, body_bytes in encoded_messages:
                output.extend(_pack_i64(msg_id))
                output.extend(encode_int(seq_no))
                output.extend(encode_int(len(body_bytes)))
                output.extend(body_bytes)
            return bytes(output)
        case GzipPacked(packed_data=packed_data):
            packed_bytes = bytes(packed_data)
            return encode_fast(_GZIP_PACKED_ID, (packed_bytes,)) or encode_constructor_id(
                _GZIP_PACKED_ID
            ) + encode_bytes(packed_bytes)
        case Pong(msg_id=msg_id, ping_id=ping_id):
            return encode_fast(_PONG_ID, (msg_id, ping_id)) or encode_constructor_id(_PONG_ID) + _pack_i64(
                msg_id
            ) + _pack_i64(ping_id)
        case BadServerSalt(
            bad_msg_id=bad_msg_id, bad_msg_seq_no=bad_msg_seq_no, error_code=error_code, new_server_salt=new_server_salt
        ):
            return encode_fast(_BAD_SERVER_SALT_ID, (bad_msg_id, bad_msg_seq_no, error_code, new_server_salt)) or (
                encode_constructor_id(_BAD_SERVER_SALT_ID)
                + _pack_i64(bad_msg_id)
                + encode_int(bad_msg_seq_no)
                + encode_int(error_code)
                + _pack_u64(new_server_salt)
            )
        case BadMsgNotification(bad_msg_id=bad_msg_id, bad_msg_seq_no=bad_msg_seq_no, error_code=error_code):
            return encode_fast(_BAD_MSG_NOTIFICATION_ID, (bad_msg_id, bad_msg_seq_no, error_code)) or (
                encode_constructor_id(_BAD_MSG_NOTIFICATION_ID)
                + _pack_i64(bad_msg_id)
                + encode_int(bad_msg_seq_no)
                + encode_int(error_code)
            )
        case NewSessionCreated(first_msg_id=first_msg_id, unique_id=unique_id, server_salt=server_salt):
            return (
                encode_constructor_id(_NEW_SESSION_CREATED_ID)
                + _pack_i64(first_msg_id)
                + _pack_i64(unique_id)
                + _pack_u64(server_salt)
            )
        case RpcErrorBody(error_code=error_code, error_message=error_message):
            return encode_constructor_id(_RPC_ERROR_ID) + encode_int(error_code) + encode_string(error_message)
        case RpcResult(req_msg_id=req_msg_id, result=result):
            result_bytes = encode_message_body(result)
            return (
                encode_fast(_RPC_RESULT_ID, (req_msg_id, result_bytes))
                or encode_constructor_id(_RPC_RESULT_ID) + _pack_i64(req_msg_id) + result_bytes
            )
        case _:
            raise TypeError(f"cannot encode MTProto body {type(body).__name__}")


def decode_message_body(data: ByteBuffer) -> ByteBuffer | object:
    """Decode recognized MTProto service bodies, preserving unknown data as a view.

    Args:
        data: Exactly one MTProto body.

    Returns:
        Service-body dataclass, ping tuple, RPC error/result or the original ``ByteBuffer`` input for an unknown constructor.

    Raises:
        ValueError: If a recognized body is truncated, malformed or has trailing bytes.
    """
    data_view = memoryview(data)
    constructor_id, offset = decode_constructor_id(data, 0)
    if constructor_id in _FAST_SERVICE_IDS and len(data) <= 4096:
        native = decode_fast(constructor_id, bytes(data), 0)
        if native is not None:
            values, native_offset = native
            _require_consumed(data, native_offset)
            return _materialize_fast_service(constructor_id, values)
    if constructor_id == _MSGS_ACK_ID:
        msg_ids, offset = _decode_long_vector(data, offset)
        _require_consumed(data, offset)
        return MsgsAck(msg_ids=msg_ids)
    if constructor_id == _MSGS_STATE_REQ_ID:
        msg_ids, offset = _decode_long_vector(data, offset)
        _require_consumed(data, offset)
        return MsgsStateReq(msg_ids=msg_ids)
    if constructor_id == _MSGS_STATE_INFO_ID:
        req_msg_id = _unpack_i64(data, offset)
        info, offset = decode_bytes(data, offset + 8)
        _require_consumed(data, offset)
        return MsgsStateInfo(req_msg_id=req_msg_id, info=bytes(info))
    if constructor_id == _MSG_RESEND_REQ_ID:
        msg_ids, offset = _decode_long_vector(data, offset)
        _require_consumed(data, offset)
        return MsgResendReq(msg_ids=msg_ids)
    if constructor_id == _MSG_CONTAINER_ID:
        count, offset = decode_int(data, offset)
        if count < 0:
            raise ValueError("MTProto container count cannot be negative")
        messages: list[MessageContainerItem] = []
        for _ in range(count):
            msg_id = _unpack_i64(data, offset)
            offset += 8
            seq_no, offset = decode_int(data, offset)
            body_len, offset = decode_int(data, offset)
            if body_len < 0 or offset + body_len > len(data):
                raise ValueError("MTProto container item length is invalid")
            body_bytes = data_view[offset : offset + body_len]
            offset += body_len
            messages.append(MessageContainerItem(msg_id=msg_id, seq_no=seq_no, body=body_bytes))
        _require_consumed(data, offset)
        return MessageContainer(messages=tuple(messages))
    if constructor_id == _GZIP_PACKED_ID:
        packed, offset = decode_bytes(data, offset)
        _require_consumed(data, offset)
        return GzipPacked(packed_data=packed)
    if constructor_id == _PING_ID:
        ping_id = _unpack_i64(data, offset)
        _require_consumed(data, offset + 8)
        return ("ping", ping_id)
    if constructor_id == _PING_DELAY_DISCONNECT_ID:
        ping_id = _unpack_i64(data, offset)
        disconnect_delay, offset = decode_int(data, offset + 8)
        _require_consumed(data, offset)
        return ("ping_delay_disconnect", ping_id, disconnect_delay)
    if constructor_id == _PONG_ID:
        msg_id = _unpack_i64(data, offset)
        ping_id = _unpack_i64(data, offset + 8)
        _require_consumed(data, offset + 16)
        return Pong(msg_id=msg_id, ping_id=ping_id)
    if constructor_id == _BAD_SERVER_SALT_ID:
        bad_msg_id = _unpack_i64(data, offset)
        bad_msg_seq_no, offset = decode_int(data, offset + 8)
        error_code, offset = decode_int(data, offset)
        new_server_salt = _unpack_u64(data, offset)
        _require_consumed(data, offset + 8)
        return BadServerSalt(
            bad_msg_id=bad_msg_id, bad_msg_seq_no=bad_msg_seq_no, error_code=error_code, new_server_salt=new_server_salt
        )
    if constructor_id == _BAD_MSG_NOTIFICATION_ID:
        bad_msg_id = _unpack_i64(data, offset)
        bad_msg_seq_no, offset = decode_int(data, offset + 8)
        error_code, offset = decode_int(data, offset)
        _require_consumed(data, offset)
        return BadMsgNotification(bad_msg_id=bad_msg_id, bad_msg_seq_no=bad_msg_seq_no, error_code=error_code)
    if constructor_id == _NEW_SESSION_CREATED_ID:
        first_msg_id = _unpack_i64(data, offset)
        unique_id = _unpack_i64(data, offset + 8)
        server_salt = _unpack_u64(data, offset + 16)
        _require_consumed(data, offset + 24)
        return NewSessionCreated(first_msg_id=first_msg_id, unique_id=unique_id, server_salt=server_salt)
    if constructor_id == _RPC_ERROR_ID:
        error_code, offset = decode_int(data, offset)
        error_message, offset = decode_string(data, offset)
        _require_consumed(data, offset)
        return RpcErrorBody(error_code=error_code, error_message=error_message)
    if constructor_id == _RPC_RESULT_ID:
        req_msg_id = _unpack_i64(data, offset)
        return RpcResult(req_msg_id=req_msg_id, result=data_view[offset + 8 :])
    return data


def _materialize_fast_service(constructor_id: int, values: tuple[object, ...]) -> object:
    """Materialize a recognized native fast-path result as its service dataclass.

    Args:
        constructor_id: Recognized MTProto service constructor ID.
        values: Native decoder field values in manifest order.
    """
    if constructor_id == _MSGS_ACK_ID:
        return MsgsAck(msg_ids=tuple(cast(tuple[int, ...], values[0])))
    if constructor_id == _MSGS_STATE_REQ_ID:
        return MsgsStateReq(msg_ids=tuple(cast(tuple[int, ...], values[0])))
    if constructor_id == _MSGS_STATE_INFO_ID:
        return MsgsStateInfo(req_msg_id=cast(int, values[0]), info=cast(bytes, values[1]))
    if constructor_id == _MSG_RESEND_REQ_ID:
        return MsgResendReq(msg_ids=tuple(cast(tuple[int, ...], values[0])))
    if constructor_id == _MSG_CONTAINER_ID:
        messages = tuple(
            MessageContainerItem(msg_id=item[0], seq_no=item[1], body=memoryview(item[2]))
            for item in cast(tuple[tuple[int, int, bytes], ...], values[0])
        )
        return MessageContainer(messages=messages)
    if constructor_id == _GZIP_PACKED_ID:
        return GzipPacked(packed_data=memoryview(cast(bytes, values[0])))
    if constructor_id == _PONG_ID:
        return Pong(msg_id=cast(int, values[0]), ping_id=cast(int, values[1]))
    if constructor_id == _BAD_MSG_NOTIFICATION_ID:
        return BadMsgNotification(
            bad_msg_id=cast(int, values[0]), bad_msg_seq_no=cast(int, values[1]), error_code=cast(int, values[2])
        )
    if constructor_id == _BAD_SERVER_SALT_ID:
        return BadServerSalt(
            bad_msg_id=cast(int, values[0]),
            bad_msg_seq_no=cast(int, values[1]),
            error_code=cast(int, values[2]),
            new_server_salt=cast(int, values[3]),
        )
    if constructor_id == _RPC_RESULT_ID:
        return RpcResult(req_msg_id=cast(int, values[0]), result=memoryview(cast(bytes, values[1])))
    raise ValueError(f"unsupported generated MTProto service constructor 0x{constructor_id:08x}")


def encode_ping(ping_id: int) -> bytes:
    """Encode an MTProto ``ping`` service body.

    Args:
        ping_id: Caller-chosen 64-bit ping correlation ID.

    Returns:
        Constructor-prefixed ``ping`` body bytes.
    """
    return encode_constructor_id(_PING_ID) + _pack_i64(ping_id)


def encode_ping_delay_disconnect(ping_id: int, disconnect_delay: int) -> bytes:
    """Encode an MTProto ``ping_delay_disconnect`` service body.

    Args:
        ping_id: Caller-chosen 64-bit ping correlation ID.
        disconnect_delay: Requested disconnect-delay seconds.

    Returns:
        Constructor-prefixed service-body bytes.
    """
    return encode_constructor_id(_PING_DELAY_DISCONNECT_ID) + _pack_i64(ping_id) + encode_int(disconnect_delay)


def gzip_pack(body: ByteBuffer | object) -> GzipPacked:
    """Compress an encodable MTProto body into a ``gzip_packed`` service object.

    Args:
        body: Raw or supported encodable body.

    Returns:
        Service object containing gzip-compressed body bytes.
    """
    return GzipPacked(packed_data=gzip.compress(encode_message_body(body)))


def _decode_long_vector(data: ByteBuffer, offset: int) -> tuple[tuple[int, ...], int]:
    """Decode the MTProto ``Vector<long>`` form used by service bodies.

    Args:
        data: Service-body wire bytes.
        offset: Offset at the vector constructor.
    """
    constructor_id, offset = decode_constructor_id(data, offset)
    if constructor_id != 0x1CB5C415:
        raise ValueError("expected TL vector constructor")
    count, offset = decode_int(data, offset)
    if count < 0:
        raise ValueError("TL vector count cannot be negative")
    values: list[int] = []
    for _ in range(count):
        values.append(_unpack_i64(data, offset))
        offset += 8
    return tuple(values), offset


def _pack_i64(value: int) -> bytes:
    """Pack one signed 64-bit MTProto integer.

    Args:
        value: Integer to encode.
    """
    return int(value).to_bytes(8, "little", signed=True)


def _pack_u64(value: int) -> bytes:
    """Pack one masked unsigned 64-bit MTProto integer.

    Args:
        value: Integer whose low 64 bits are encoded.
    """
    return int(value & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little", signed=False)


def _unpack_i64(data: ByteBuffer, offset: int) -> int:
    """Read one signed 64-bit little-endian field after checking its length.

    Args:
        data: Wire bytes containing the field.
        offset: Starting byte offset.
    """
    _require_length(data, offset, 8)
    return int.from_bytes(data[offset : offset + 8], "little", signed=True)


def _unpack_u64(data: ByteBuffer, offset: int) -> int:
    """Read one unsigned 64-bit little-endian field after checking its length.

    Args:
        data: Wire bytes containing the field.
        offset: Starting byte offset.
    """
    _require_length(data, offset, 8)
    return int.from_bytes(data[offset : offset + 8], "little", signed=False)


def _require_length(data: ByteBuffer, offset: int, length: int) -> None:
    """Reject a field range that is outside an MTProto payload.

    Args:
        data: Wire bytes being bounds-checked.
        offset: Requested field start offset.
        length: Requested field length in bytes.
    """
    if offset < 0 or offset + length > len(data):
        raise ValueError("MTProto payload ended before the requested field")


def _require_consumed(data: ByteBuffer, offset: int) -> None:
    """Reject recognized MTProto bodies that contain trailing bytes.

    Args:
        data: Complete recognized body bytes.
        offset: First unread byte offset.
    """
    if offset != len(data):
        raise ValueError("MTProto body has trailing bytes")


__all__ = [
    "BadMsgNotification",
    "BadServerSalt",
    "DecodedEncryptedMessage",
    "GzipPacked",
    "MessageContainer",
    "MessageContainerItem",
    "MsgResendReq",
    "MsgsAck",
    "MsgsStateInfo",
    "MsgsStateReq",
    "NewSessionCreated",
    "Pong",
    "RpcResult",
    "UnencryptedMessage",
    "decode_encrypted_message",
    "decode_message_body",
    "decode_unencrypted_message",
    "encode_encrypted_message",
    "encode_message_body",
    "encode_ping",
    "encode_ping_delay_disconnect",
    "encode_unencrypted_message",
    "gzip_pack",
]

from __future__ import annotations

import gzip
from dataclasses import dataclass

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
type ByteBuffer = bytes | memoryview


@dataclass(frozen=True, slots=True)
class DecodedEncryptedMessage:
    auth_key_id: bytes
    server_salt: int
    session_id: int
    msg_id: int
    seq_no: int
    body: ByteBuffer
    padding: ByteBuffer


@dataclass(frozen=True, slots=True)
class UnencryptedMessage:
    msg_id: int
    body: ByteBuffer


@dataclass(frozen=True, slots=True)
class MsgsAck:
    msg_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MsgsStateReq:
    msg_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MsgsStateInfo:
    req_msg_id: int
    info: bytes


@dataclass(frozen=True, slots=True)
class MsgResendReq:
    msg_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MessageContainerItem:
    msg_id: int
    seq_no: int
    body: ByteBuffer | object


@dataclass(frozen=True, slots=True)
class MessageContainer:
    messages: tuple[MessageContainerItem, ...]


@dataclass(frozen=True, slots=True)
class GzipPacked:
    packed_data: ByteBuffer

    def unpack(self) -> bytes:
        return gzip.decompress(self.packed_data)


@dataclass(frozen=True, slots=True)
class Pong:
    msg_id: int
    ping_id: int


@dataclass(frozen=True, slots=True)
class BadMsgNotification:
    bad_msg_id: int
    bad_msg_seq_no: int
    error_code: int


@dataclass(frozen=True, slots=True)
class BadServerSalt:
    bad_msg_id: int
    bad_msg_seq_no: int
    error_code: int
    new_server_salt: int


@dataclass(frozen=True, slots=True)
class NewSessionCreated:
    first_msg_id: int
    unique_id: int
    server_salt: int


@dataclass(frozen=True, slots=True)
class RpcErrorBody:
    error_code: int
    error_message: str


@dataclass(frozen=True, slots=True)
class RpcResult:
    req_msg_id: int
    result: ByteBuffer | object


def encode_unencrypted_message(msg_id: int, body: bytes | object) -> bytes:
    body_bytes = encode_message_body(body)
    return b"\x00" * 8 + _pack_i64(msg_id) + encode_int(len(body_bytes)) + body_bytes


def decode_unencrypted_message(packet: ByteBuffer) -> UnencryptedMessage:
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
    if isinstance(body, bytes):
        return body
    if isinstance(body, bytearray | memoryview):
        return bytes(body)
    serialize = getattr(body, "serialize", None)
    if callable(serialize):
        return serialize()
    match body:
        case MsgsAck(msg_ids=msg_ids):
            return encode_constructor_id(_MSGS_ACK_ID) + encode_vector(msg_ids, "long")
        case MsgsStateReq(msg_ids=msg_ids):
            return encode_constructor_id(_MSGS_STATE_REQ_ID) + encode_vector(msg_ids, "long")
        case MsgsStateInfo(req_msg_id=req_msg_id, info=info):
            return (
                encode_constructor_id(_MSGS_STATE_INFO_ID)
                + _pack_i64(req_msg_id)
                + encode_bytes(info)
            )
        case MsgResendReq(msg_ids=msg_ids):
            return encode_constructor_id(_MSG_RESEND_REQ_ID) + encode_vector(msg_ids, "long")
        case MessageContainer(messages=messages):
            output = bytearray(encode_constructor_id(_MSG_CONTAINER_ID))
            output.extend(encode_int(len(messages)))
            for message in messages:
                body_bytes = encode_message_body(message.body)
                output.extend(_pack_i64(message.msg_id))
                output.extend(encode_int(message.seq_no))
                output.extend(encode_int(len(body_bytes)))
                output.extend(body_bytes)
            return bytes(output)
        case GzipPacked(packed_data=packed_data):
            return encode_constructor_id(_GZIP_PACKED_ID) + encode_bytes(bytes(packed_data))
        case Pong(msg_id=msg_id, ping_id=ping_id):
            return encode_constructor_id(_PONG_ID) + _pack_i64(msg_id) + _pack_i64(ping_id)
        case BadServerSalt(
            bad_msg_id=bad_msg_id,
            bad_msg_seq_no=bad_msg_seq_no,
            error_code=error_code,
            new_server_salt=new_server_salt,
        ):
            return (
                encode_constructor_id(_BAD_SERVER_SALT_ID)
                + _pack_i64(bad_msg_id)
                + encode_int(bad_msg_seq_no)
                + encode_int(error_code)
                + _pack_u64(new_server_salt)
            )
        case BadMsgNotification(
            bad_msg_id=bad_msg_id, bad_msg_seq_no=bad_msg_seq_no, error_code=error_code
        ):
            return (
                encode_constructor_id(_BAD_MSG_NOTIFICATION_ID)
                + _pack_i64(bad_msg_id)
                + encode_int(bad_msg_seq_no)
                + encode_int(error_code)
            )
        case NewSessionCreated(
            first_msg_id=first_msg_id, unique_id=unique_id, server_salt=server_salt
        ):
            return (
                encode_constructor_id(_NEW_SESSION_CREATED_ID)
                + _pack_i64(first_msg_id)
                + _pack_i64(unique_id)
                + _pack_u64(server_salt)
            )
        case RpcErrorBody(error_code=error_code, error_message=error_message):
            return (
                encode_constructor_id(_RPC_ERROR_ID)
                + encode_int(error_code)
                + encode_string(error_message)
            )
        case RpcResult(req_msg_id=req_msg_id, result=result):
            return (
                encode_constructor_id(_RPC_RESULT_ID)
                + _pack_i64(req_msg_id)
                + encode_message_body(result)
            )
        case _:
            raise TypeError(f"cannot encode MTProto body {type(body).__name__}")


def decode_message_body(data: ByteBuffer) -> ByteBuffer | object:
    data_view = memoryview(data)
    constructor_id, offset = decode_constructor_id(data, 0)
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
            bad_msg_id=bad_msg_id,
            bad_msg_seq_no=bad_msg_seq_no,
            error_code=error_code,
            new_server_salt=new_server_salt,
        )
    if constructor_id == _BAD_MSG_NOTIFICATION_ID:
        bad_msg_id = _unpack_i64(data, offset)
        bad_msg_seq_no, offset = decode_int(data, offset + 8)
        error_code, offset = decode_int(data, offset)
        _require_consumed(data, offset)
        return BadMsgNotification(
            bad_msg_id=bad_msg_id, bad_msg_seq_no=bad_msg_seq_no, error_code=error_code
        )
    if constructor_id == _NEW_SESSION_CREATED_ID:
        first_msg_id = _unpack_i64(data, offset)
        unique_id = _unpack_i64(data, offset + 8)
        server_salt = _unpack_u64(data, offset + 16)
        _require_consumed(data, offset + 24)
        return NewSessionCreated(
            first_msg_id=first_msg_id, unique_id=unique_id, server_salt=server_salt
        )
    if constructor_id == _RPC_ERROR_ID:
        error_code, offset = decode_int(data, offset)
        error_message, offset = decode_string(data, offset)
        _require_consumed(data, offset)
        return RpcErrorBody(error_code=error_code, error_message=error_message)
    if constructor_id == _RPC_RESULT_ID:
        req_msg_id = _unpack_i64(data, offset)
        return RpcResult(req_msg_id=req_msg_id, result=data_view[offset + 8 :])
    return data


def encode_ping(ping_id: int) -> bytes:
    return encode_constructor_id(_PING_ID) + _pack_i64(ping_id)


def encode_ping_delay_disconnect(ping_id: int, disconnect_delay: int) -> bytes:
    return (
        encode_constructor_id(_PING_DELAY_DISCONNECT_ID)
        + _pack_i64(ping_id)
        + encode_int(disconnect_delay)
    )


def gzip_pack(body: ByteBuffer | object) -> GzipPacked:
    return GzipPacked(packed_data=gzip.compress(encode_message_body(body)))


def _decode_long_vector(data: ByteBuffer, offset: int) -> tuple[tuple[int, ...], int]:
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
    return int(value).to_bytes(8, "little", signed=True)


def _pack_u64(value: int) -> bytes:
    return int(value & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little", signed=False)


def _unpack_i64(data: ByteBuffer, offset: int) -> int:
    _require_length(data, offset, 8)
    return int.from_bytes(data[offset : offset + 8], "little", signed=True)


def _unpack_u64(data: ByteBuffer, offset: int) -> int:
    _require_length(data, offset, 8)
    return int.from_bytes(data[offset : offset + 8], "little", signed=False)


def _require_length(data: ByteBuffer, offset: int, length: int) -> None:
    if offset < 0 or offset + length > len(data):
        raise ValueError("MTProto payload ended before the requested field")


def _require_consumed(data: ByteBuffer, offset: int) -> None:
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

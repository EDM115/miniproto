from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

import pytest

from miniproto.mtproto.codec import (
    BadMsgNotification,
    BadServerSalt,
    GzipPacked,
    MessageContainer,
    MessageContainerItem,
    MsgResendReq,
    MsgsAck,
    MsgsStateInfo,
    MsgsStateReq,
    Pong,
    RpcResult,
    decode_message_body,
    encode_message_body,
)
from miniproto.raw import functions, types
from miniproto.raw.base import TLObject
from miniproto.tl import fast
from miniproto.tl.codec import TLCodecError
from miniproto.tl.fast_metadata import FAST_PATHS, FAST_PATHS_BY_ID, SCHEMA_JSON_SHA256, SCHEMA_LAYER

_API_PATHS = tuple(entry for entry in FAST_PATHS if entry["source"] == "api")
_SERVICE_PATHS = tuple(entry for entry in FAST_PATHS if entry["source"] == "mtproto")
_INT_VALUES = (0, -1, 2**31 - 1, -(2**31), 123456)
_LONG_VALUES = (0, -1, 2**63 - 1, -(2**63), 1 << 40)
_BYTE_LENGTHS = (0, 1, 253, 254, 300)


def _has_direction(entry: dict[str, Any], direction: str) -> bool:
    return direction in cast(list[str], entry["directions"])


def test_fast_path_metadata_is_layer_and_schema_pinned_with_thirty_unique_entries() -> None:
    assert SCHEMA_LAYER == 229
    assert SCHEMA_JSON_SHA256 == "0631ec65da66e15bcfc45d34ac32bfbbca244985f8c1ffdd928a28ef64c49d8c"
    assert len(FAST_PATHS) == 30
    assert len(FAST_PATHS_BY_ID) == 30
    assert len(_API_PATHS) == 20
    assert len(_SERVICE_PATHS) == 10


@pytest.mark.parametrize("entry", _API_PATHS, ids=lambda entry: cast(str, entry["name"]))
@pytest.mark.parametrize("variant", range(5))
def test_every_selected_api_constructor_matches_generated_python_oracle(
    entry: dict[str, Any], variant: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not fast.native_fast_paths_available():
        pytest.skip("native TL fast paths are unavailable")
    obj = cast(Any, _api_object(entry, variant))
    native_boxed = obj._serialize(boxed=True)
    native_bare = obj._serialize(boxed=False)
    with monkeypatch.context() as fallback:
        fallback.setattr(fast, "_native_encode", None)
        python_boxed = obj._serialize(boxed=True)
        python_bare = obj._serialize(boxed=False)
    assert native_boxed == python_boxed
    assert native_bare == python_bare

    if not _has_direction(entry, "decode"):
        return
    prefix = b"prep"
    suffix = b"tail"
    cls = cast(Any, type(obj))
    native_obj, native_offset = cls._deserialize(prefix + native_boxed + suffix, len(prefix), boxed=True)
    with monkeypatch.context() as fallback:
        fallback.setattr(fast, "_native_decode", None)
        python_obj, python_offset = cls._deserialize(prefix + python_boxed + suffix, len(prefix), boxed=True)
    assert native_obj == python_obj == obj
    assert native_offset == python_offset == len(prefix) + len(native_boxed)


@pytest.mark.parametrize("entry", _SERVICE_PATHS, ids=lambda entry: cast(str, entry["name"]))
@pytest.mark.parametrize("variant", range(5))
def test_every_selected_service_constructor_matches_python_oracle(
    entry: dict[str, Any], variant: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not fast.native_fast_paths_available():
        pytest.skip("native TL fast paths are unavailable")
    body = _service_object(cast(str, entry["name"]), variant)
    native_encoded = encode_message_body(body)
    with monkeypatch.context() as fallback:
        fallback.setattr(fast, "_native_encode", None)
        python_encoded = encode_message_body(body)
    assert native_encoded == python_encoded

    native_decoded = decode_message_body(native_encoded)
    with monkeypatch.context() as fallback:
        fallback.setattr(fast, "_native_decode", None)
        python_decoded = decode_message_body(python_encoded)
    assert native_decoded == python_decoded


@pytest.mark.parametrize(
    "entry",
    tuple(entry for entry in _API_PATHS if _has_direction(entry, "decode")),
    ids=lambda entry: cast(str, entry["name"]),
)
def test_selected_api_decoders_preserve_mismatch_and_malformed_failures(entry: dict[str, Any]) -> None:
    if not fast.native_fast_paths_available():
        pytest.skip("native TL fast paths are unavailable")
    obj = cast(Any, _api_object(entry, 4))
    cls = cast(Any, type(obj))
    encoded = obj.serialize()
    with pytest.raises(TLCodecError, match="expected constructor"):
        cls._deserialize(b"\x00\x00\x00\x00")
    for truncated in (b"", encoded[:1], encoded[:-1]):
        with pytest.raises(ValueError):
            cls._deserialize(truncated)


@pytest.mark.parametrize("entry", _SERVICE_PATHS, ids=lambda entry: cast(str, entry["name"]))
def test_selected_service_decoders_reject_malformed_input(entry: dict[str, Any]) -> None:
    if not fast.native_fast_paths_available():
        pytest.skip("native TL fast paths are unavailable")
    body = _service_object(cast(str, entry["name"]), 4)
    encoded = encode_message_body(body)
    with pytest.raises(ValueError):
        fast.decode_fast(cast(int, entry["constructor_id"]), b"\x00\x00\x00\x00")
    with pytest.raises(ValueError):
        fast.decode_fast(cast(int, entry["constructor_id"]), encoded[:3])


def test_unknown_constructor_and_incomplete_native_capability_use_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    if fast.native_fast_paths_available():
        assert fast.encode_fast(0xDEADBEEF, (), boxed=True) is None
        assert fast.decode_fast(0xDEADBEEF, b"", 0, boxed=False) is None
    obj = functions.UploadSaveFilePart(file_id=1, file_part=2, bytes=b"part")
    expected = obj.serialize()
    monkeypatch.setattr(fast, "_native_encode", None)
    monkeypatch.setattr(fast, "_native_decode", None)
    assert obj.serialize() == expected
    assert type(obj).deserialize(expected) == obj


def test_mtproto_service_decoder_leaves_selected_api_results_for_generic_dispatch() -> None:
    value = types.UploadFile(type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=b"payload")
    encoded = value.serialize()

    assert bytes(cast(bytes | memoryview, decode_message_body(encoded))) == encoded


def _api_object(entry: dict[str, Any], variant: int) -> TLObject:
    namespace = functions if entry["kind"] == "function" else types
    cls = cast(type[TLObject], getattr(namespace, cast(str, entry["python_type"])))
    kwargs = {field.python_name: _api_value(field.type, field.name, variant) for field in cls.TL_FIELDS}
    return cls(**kwargs)


def _api_value(type_name: str, field_name: str, variant: int) -> object:
    if type_name == "true":
        return variant % 2 == 1
    if type_name == "int":
        return _INT_VALUES[variant]
    if type_name == "long":
        return _LONG_VALUES[variant]
    if type_name == "bytes":
        return bytes((index + variant) & 0xFF for index in range(_BYTE_LENGTHS[variant]))
    if type_name == "string":
        return ("Télégram-" + field_name) * variant
    if type_name == "InputFileLocation":
        factories: tuple[Callable[[], object], ...] = (
            lambda: types.InputTakeoutFileLocation(),
            lambda: types.InputEncryptedFileLocation(id=1, access_hash=-2),
            lambda: types.InputDocumentFileLocation(id=3, access_hash=4, file_reference=b"ref", thumb_size="x"),
            lambda: types.InputPhotoFileLocation(id=5, access_hash=6, file_reference=b"photo", thumb_size="y"),
            lambda: types.InputSecureFileLocation(id=7, access_hash=8),
        )
        return factories[variant]()
    if type_name == "InputWebFileLocation":
        return types.InputWebFileLocation(url=f"https://example.invalid/{variant}", access_hash=_LONG_VALUES[variant])
    if type_name == "storage.FileType":
        classes = (
            types.StorageFileUnknown,
            types.StorageFileJpeg,
            types.StorageFilePng,
            types.StorageFileMp4,
            types.StorageFileWebp,
        )
        return classes[variant]()
    raise AssertionError(f"missing fast-path test value for {type_name!r}")


def _service_object(name: str, variant: int) -> object:
    msg_ids = tuple(_LONG_VALUES[: variant + 1])
    payload = bytes((index + variant) & 0xFF for index in range(_BYTE_LENGTHS[variant]))
    services: dict[str, object] = {
        "msgs_ack": MsgsAck(msg_ids=msg_ids),
        "msgs_state_req": MsgsStateReq(msg_ids=msg_ids),
        "msgs_state_info": MsgsStateInfo(req_msg_id=_LONG_VALUES[variant], info=payload),
        "msg_resend_req": MsgResendReq(msg_ids=msg_ids),
        "msg_container": MessageContainer(
            messages=(
                MessageContainerItem(
                    msg_id=_LONG_VALUES[variant],
                    seq_no=_INT_VALUES[variant],
                    body=Pong(msg_id=variant, ping_id=-variant),
                ),
            )
        ),
        "gzip_packed": GzipPacked(packed_data=payload),
        "pong": Pong(msg_id=_LONG_VALUES[variant], ping_id=_LONG_VALUES[(variant + 1) % len(_LONG_VALUES)]),
        "bad_msg_notification": BadMsgNotification(
            bad_msg_id=_LONG_VALUES[variant], bad_msg_seq_no=_INT_VALUES[variant], error_code=variant
        ),
        "bad_server_salt": BadServerSalt(
            bad_msg_id=_LONG_VALUES[variant],
            bad_msg_seq_no=_INT_VALUES[variant],
            error_code=variant,
            new_server_salt=(1 << 64) - 1 - variant,
        ),
        "rpc_result": RpcResult(req_msg_id=_LONG_VALUES[variant], result=payload),
    }
    return services[name]

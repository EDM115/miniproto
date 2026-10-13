from __future__ import annotations

import sys
from subprocess import run

import pytest

from miniproto.raw import functions, types
from miniproto.raw.base import TLObject
from miniproto.tl import codec as tl_codec
from miniproto.tl import decode_object, decode_vector, deserialize_object, encode_vector, serialize_object


def test_raw_facades_load_and_cache_only_requested_shards() -> None:
    probe = run(
        [
            sys.executable,
            "-c",
            (
                "import sys;"
                "from concurrent.futures import ThreadPoolExecutor;"
                "prefixes=('miniproto.raw._types_shards.','miniproto.raw._function_shards.');"
                "assert not [name for name in sys.modules if name.startswith(prefixes)];"
                "from miniproto.raw import functions,types;"
                "executor=ThreadPoolExecutor(max_workers=2);"
                "resolved=tuple(executor.map(lambda _index:types.BoolTrue,range(2)));"
                "executor.shutdown();"
                "assert resolved[0] is resolved[1] is types.BoolTrue;"
                "assert types.BoolTrue.__module__ == 'miniproto.raw.types';"
                "assert functions.help.GetConfig is functions.HelpGetConfig;"
                "assert 'BoolTrue' in dir(types);"
                "assert 'help' in dir(functions);"
                "assert 'miniproto.raw._types_shards.bucket_53' in sys.modules;"
                "assert 'miniproto.raw._function_shards.bucket_11' in sys.modules;"
                "assert not hasattr(types,'NoSuchRawType')"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert probe.returncode == 0


def test_constructor_decode_lazily_imports_only_owner_shard() -> None:
    before = {
        name
        for name in sys.modules
        if name.startswith(("miniproto.raw._types_shards.", "miniproto.raw._function_shards."))
    }

    decoded, offset = decode_object(bytes.fromhex("c97ea07d"))

    after = {
        name
        for name in sys.modules
        if name.startswith(("miniproto.raw._types_shards.", "miniproto.raw._function_shards."))
    }
    assert offset == 4
    assert decoded == types.InputPeerSelf()
    owner_shard = "miniproto.raw._types_shards.bucket_09"
    assert owner_shard in after
    assert after - before <= {owner_shard}


def test_constructor_decode_caches_resolved_class_for_direct_lookup() -> None:
    constructor_id = types.InputPeerSelf.CONSTRUCTOR_ID
    tl_codec._constructor_class_cache.clear()

    decoded, offset = decode_object(bytes.fromhex("c97ea07d"))

    assert offset == 4
    assert type(decoded) is types.InputPeerSelf
    assert tl_codec._constructor_class_cache == {constructor_id: types.InputPeerSelf}


def test_public_raw_classes_pickle_through_facades_in_fresh_process() -> None:
    producer = run(
        [
            sys.executable,
            "-c",
            (
                "import base64,json,pickle;"
                "from miniproto.raw import functions,types;"
                "values=(types.InputPeerSelf(),functions.help.GetConfig());"
                "print(json.dumps([base64.b64encode(pickle.dumps(value)).decode() for value in values]))"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    consumer = run(  # noqa: S603 - executes the running interpreter with fixed code and test data.
        [
            sys.executable,
            "-c",
            (
                "import base64,json,pickle,sys;"
                "payloads=json.loads(sys.argv[1]);"
                "values=[pickle.loads(base64.b64decode(payload)) for payload in payloads];"
                "from miniproto.raw import functions,types;"
                "assert type(values[0]) is types.InputPeerSelf;"
                "assert type(values[1]) is functions.help.GetConfig is functions.HelpGetConfig;"
                "assert type(values[0]).__module__ == 'miniproto.raw.types';"
                "assert type(values[1]).__module__ == 'miniproto.raw.functions';"
                "assert '_shards' not in repr(type(values[0]));"
                "assert '_shards' not in repr(type(values[1]))"
            ),
            producer.stdout.strip(),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert consumer.returncode == 0


def test_generated_empty_constructor_serializes_constructor_id() -> None:
    assert types.BoolTrue().serialize() == bytes.fromhex("b5757299")
    assert types.BoolTrue.deserialize(bytes.fromhex("b5757299")) == types.BoolTrue()


def test_generated_flags_and_vectors_roundtrip_from_real_schema_type() -> None:
    user = types.User(
        self_=True,
        contact=True,
        mutual_contact=False,
        deleted=False,
        bot=False,
        bot_chat_history=False,
        bot_nochats=False,
        verified=True,
        restricted=False,
        min=False,
        bot_inline_geo=False,
        support=False,
        scam=False,
        apply_min_photo=False,
        fake=False,
        bot_attach_menu=False,
        premium=True,
        attach_menu_enabled=False,
        bot_can_edit=False,
        close_friend=False,
        stories_hidden=False,
        stories_unavailable=False,
        contact_require_premium=False,
        bot_business=False,
        bot_has_main_app=False,
        id=12345,
        access_hash=99,
        first_name="Ada",
        last_name=None,
        username="ada",
        phone=None,
        photo=None,
        status=None,
        bot_info_version=None,
        restriction_reason=None,
        bot_inline_placeholder=None,
        lang_code=None,
        emoji_status=None,
        usernames=None,
        stories_max_id=None,
        color=None,
        profile_color=None,
        bot_active_users=None,
        bot_verification_icon=None,
        send_paid_messages_stars=None,
    )
    encoded = user.serialize()
    decoded = types.User.deserialize(encoded)
    assert decoded == user


def test_generated_nested_object_and_vector_request_roundtrip() -> None:
    request = functions.users.GetUsers(id=(types.InputUserSelf(), types.InputUserEmpty()))
    encoded = request.serialize()
    decoded = functions.users.GetUsers.deserialize(encoded)
    assert decoded == request
    dynamic, offset = decode_object(encoded)
    assert dynamic == request
    assert offset == len(encoded)


def test_decode_object_reuses_constructor_map() -> None:
    cache_clear = getattr(tl_codec._constructor_maps, "cache_clear", None)
    if callable(cache_clear):
        cache_clear()
    assert tl_codec._constructor_maps() is tl_codec._constructor_maps()


def test_generated_hot_raw_classes_have_specialized_codec_methods() -> None:
    assert functions.UploadGetFile.serialize is not TLObject.serialize
    assert hasattr(functions.UploadGetFile, "_deserialize")


def test_deserialize_object_can_decode_unboxed_payload_for_known_class() -> None:
    peer = types.InputPeerUser(user_id=42, access_hash=99)
    decoded, offset = deserialize_object(types.InputPeerUser, serialize_object(peer, boxed=False), boxed=False)
    assert decoded == peer
    assert offset == 16


def test_public_vector_codec_fast_paths_int_and_long_vectors() -> None:
    int_values = tuple(range(-50, 50))
    encoded_ints = encode_vector(int_values, "int")
    decoded_ints, int_offset = decode_vector(encoded_ints, 0, "int")
    assert decoded_ints == int_values
    assert int_offset == len(encoded_ints)

    long_values = (-1, 0, 1, 2**40, -(2**40))
    encoded_longs = encode_vector(long_values, "long")
    decoded_longs, long_offset = decode_vector(encoded_longs, 0, "long")
    assert decoded_longs == long_values
    assert long_offset == len(encoded_longs)


@pytest.mark.parametrize(("item_type", "width"), [("int", 4), ("long", 8)])
@pytest.mark.parametrize("as_memoryview", [False, True])
def test_public_primitive_vector_decode_rejects_count_exceeding_remaining_payload(
    item_type: str, width: int, as_memoryview: bool
) -> None:
    prefix = b"prefix"
    data = (
        prefix
        + tl_codec.VECTOR_CONSTRUCTOR_ID.to_bytes(4, "little")
        + (2).to_bytes(4, "little", signed=True)
        + bytes(width * 2 - 1)
    )
    encoded = memoryview(data) if as_memoryview else data

    with pytest.raises(ValueError, match="vector count exceeds remaining payload"):
        decode_vector(encoded, len(prefix), item_type)


@pytest.mark.parametrize("item_type", ["int", "long"])
@pytest.mark.parametrize("as_memoryview", [False, True])
def test_public_primitive_vector_decode_rejects_maximum_count_without_payload(
    item_type: str, as_memoryview: bool
) -> None:
    data = tl_codec.VECTOR_CONSTRUCTOR_ID.to_bytes(4, "little") + (2**31 - 1).to_bytes(4, "little", signed=True)
    encoded = memoryview(data) if as_memoryview else data

    with pytest.raises(ValueError, match="vector count exceeds remaining payload"):
        decode_vector(encoded, 0, item_type)


@pytest.mark.parametrize(("item_type", "values"), [("int", (-2, 0, 3)), ("long", (-(2**40), 0, 2**40))])
@pytest.mark.parametrize("as_memoryview", [False, True])
def test_public_primitive_vector_decode_preserves_trailing_byte_offset(
    item_type: str, values: tuple[int, ...], as_memoryview: bool
) -> None:
    prefix = b"pre"
    encoded_vector = encode_vector(values, item_type)
    data = prefix + encoded_vector + b"trailing"
    encoded = memoryview(data) if as_memoryview else data

    decoded, offset = decode_vector(encoded, len(prefix), item_type)

    assert decoded == values
    assert offset == len(prefix) + len(encoded_vector)


@pytest.mark.parametrize("item_type", ["int", "long"])
@pytest.mark.parametrize("offset", [-1, 1, 7, 2**63])
@pytest.mark.parametrize("as_memoryview", [False, True])
def test_public_primitive_vector_decode_normalizes_invalid_offsets(
    item_type: str, offset: int, as_memoryview: bool
) -> None:
    data = tl_codec.VECTOR_CONSTRUCTOR_ID.to_bytes(4, "little") + (0).to_bytes(4, "little", signed=True)
    encoded = memoryview(data) if as_memoryview else data

    with pytest.raises(ValueError, match="TL data ended before the requested value could be decoded"):
        decode_vector(encoded, offset, item_type)


# Layer 230 declarations: https://raw.githubusercontent.com/tdlib/td/105481a3da3668e68ee12973dc60541ec013036a/td/generate/scheme/telegram_api.tl
# Golden bytes are hand-derived using https://core.telegram.org/mtproto/serialize
# fmt: off
@pytest.mark.parametrize(
    ("additional", "expected_hex"),
    [(False, "614cace3 00000000 03616263"), (True, "614cace3 01000000 03616263")],
)
def test_layer230_bot_username_request_encodes_additional_flag(additional: bool, expected_hex: str) -> None:
    _assert_layer230_wire(functions.BotsCheckUsername(username="abc", additional=additional), expected_hex)


@pytest.mark.parametrize(
    ("deletable", "expired", "expected_hex"),
    [(True, False, "473607b4 04000000 03616263"), (False, True, "473607b4 08000000 03616263")],
)
def test_layer230_username_flags_have_distinct_wire_bits(deletable: bool, expired: bool, expected_hex: str) -> None:
    _assert_layer230_wire(types.Username(username="abc", deletable=deletable, expired=expired), expected_hex)


@pytest.mark.parametrize(
    ("except_ids", "expected_hex"),
    [
        (None, "c0154f64 00000000 04030201 03616263"),
        ((), "c0154f64 01000000 15c4b51c 00000000 04030201 03616263"),
        ((0x0102030405060708, -2), "c0154f64 01000000 15c4b51c 02000000 0807060504030201 feffffffffffffff 04030201 03616263"),
    ],
)
def test_layer230_firebase_login_places_optional_long_vector_before_api_fields(except_ids: tuple[int, ...] | None, expected_hex: str) -> None:
    request = functions.AuthInitFirebasePnvLogin(except_ids=except_ids, api_id=0x01020304, api_hash="abc")
    _assert_layer230_wire(request, expected_hex)


@pytest.mark.parametrize("kind", ["verification", "settings", "request"])
def test_layer230_bot_verification_descriptions_are_boxed_text_with_entities(kind: str) -> None:
    description = types.TextWithEntities(text="abc", entities=(types.MessageEntityBold(offset=1, length=2),))
    description_hex = "46311f75 03616263 15c4b51c 01000000 c90b61bd 01000000 02000000"
    if kind == "verification":
        value = types.BotVerification(bot_id=0x0102030405060708, icon=0x1112131415161718, description=description)
        expected_hex = "d90e2ef7 0807060504030201 1817161514131211 " + description_hex
    elif kind == "settings":
        value = types.BotVerifierSettings(can_modify_custom_description=True, icon=0x1112131415161718, company="XYZ", custom_description=description)
        expected_hex = "ffef2aa1 03000000 1817161514131211 0358595a " + description_hex
    else:
        value = functions.BotsSetCustomVerification(enabled=True, peer=types.InputPeerSelf(), custom_description=description)
        expected_hex = "576794f4 06000000 c97ea07d " + description_hex
    _assert_layer230_wire(value, expected_hex)


def test_layer230_wallet_update_dispatch_preserves_nested_state_and_wire_offset() -> None:
    value = types.UpdateWalletState(state=types.WalletState(backup_enabled=True, can_enable_backup=True, address="abc", public_key=b"\x10\x20", balance=0x0102030405060708))
    _assert_layer230_wire(value, "aaf2c36a 6b34c595 05000000 03616263 02102000 0807060504030201")


def test_layer230_removed_firebase_passkey_constructor_is_not_decodable() -> None:
    with pytest.raises(tl_codec.TLCodecError, match="unknown TL constructor 0x5b1ccb28"):
        decode_object(bytes.fromhex("28cb1c5b 03616263"))


def _assert_layer230_wire(value: TLObject, expected_hex: str) -> None:
    expected = bytes.fromhex(expected_hex)
    assert value.serialize() == expected
    assert type(value).deserialize(expected) == value
    decoded, offset = decode_object(b"head" + expected + b"tail", 4)
    assert decoded == value
    assert offset == 4 + len(expected)
# fmt: on

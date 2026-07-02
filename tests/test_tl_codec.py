from __future__ import annotations

from miniproto.raw import functions, types
from miniproto.tl import (
    decode_object,
    decode_vector,
    deserialize_object,
    encode_vector,
    serialize_object,
)


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


def test_deserialize_object_can_decode_unboxed_payload_for_known_class() -> None:
    peer = types.InputPeerUser(user_id=42, access_hash=99)
    decoded, offset = deserialize_object(
        types.InputPeerUser, serialize_object(peer, boxed=False), boxed=False
    )
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

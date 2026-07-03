from __future__ import annotations

from miniproto import decode_file_id, encode_file_id, input_media_from_file_id, media_from_file_id
from miniproto.raw import types


def test_file_id_round_trips_document_like_media() -> None:
    document = types.Document(
        id=100,
        access_hash=200,
        file_reference=b"ref",
        date=1_700_000_000,
        mime_type="video/mp4",
        size=1234,
        dc_id=4,
        attributes=(
            types.DocumentAttributeVideo(duration=1.5, w=320, h=240),
            types.DocumentAttributeFilename(file_name="clip.mp4"),
        ),
    )
    file_id = encode_file_id(document)
    decoded = decode_file_id(file_id)
    assert decoded.kind == "document"
    assert decoded.id == 100
    assert decoded.access_hash == 200
    assert decoded.file_reference == b"ref"
    assert decoded.dc_id == 4
    assert decoded.size == 1234
    assert decoded.file_name == "clip.mp4"
    assert decoded.mime_type == "video/mp4"
    media = media_from_file_id(file_id)
    assert media.file_id == file_id
    assert isinstance(media.location, types.InputDocumentFileLocation)
    input_media = input_media_from_file_id(file_id, spoiler=True)
    assert isinstance(input_media, types.InputMediaDocument)
    assert input_media.spoiler is True
    assert isinstance(input_media.id, types.InputDocument)
    assert input_media.id.id == 100


def test_file_id_round_trips_photo_media() -> None:
    photo = types.Photo(
        has_stickers=False,
        id=101,
        access_hash=201,
        file_reference=b"photo-ref",
        date=1_700_000_000,
        sizes=(types.PhotoSize(type="x", w=1280, h=720, size=4567),),
        video_sizes=(),
        dc_id=2,
    )
    file_id = encode_file_id(photo)
    decoded = decode_file_id(file_id)
    assert decoded.kind == "photo"
    assert decoded.thumb_size == "x"
    assert decoded.size == 4567
    media = media_from_file_id(file_id)
    assert media.mime_type == "image/jpeg"
    assert isinstance(media.location, types.InputPhotoFileLocation)
    input_media = input_media_from_file_id(file_id)
    assert isinstance(input_media, types.InputMediaPhoto)
    assert isinstance(input_media.id, types.InputPhoto)

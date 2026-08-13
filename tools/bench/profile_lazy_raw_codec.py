from __future__ import annotations

import gc
import json
import statistics
import time
from collections.abc import Callable
from typing import Any

from miniproto.media import DEFAULT_CHUNK_SIZE
from miniproto.raw import functions, types
from miniproto.raw._registry import CONSTRUCTORS
from miniproto.tl import codec as tl_codec
from miniproto.tl import decode_object


def _interleaved(cases: dict[str, Callable[[], Any]], *, rounds: int = 10) -> dict[str, dict[str, Any]]:
    durations = {name: [] for name in cases}
    names = tuple(cases)
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        for round_index in range(rounds):
            offset = round_index % len(names)
            for name in (*names[offset:], *names[:offset]):
                start = time.perf_counter()
                cases[name]()
                durations[name].append((time.perf_counter() - start) * 1000)
    finally:
        if was_enabled:
            gc.enable()
    return {
        name: {"best_ms": min(samples), "median_ms": statistics.median(samples), "samples_ms": samples}
        for name, samples in durations.items()
    }


def main() -> int:
    request_type = functions.UploadGetFile
    location_type = types.InputDocumentFileLocation
    upload_file_type = types.UploadFile
    request = request_type(
        precise=True,
        cdn_supported=True,
        location=location_type(id=1, access_hash=2, file_reference=b"ref", thumb_size=""),
        offset=0,
        limit=DEFAULT_CHUNK_SIZE,
    )
    encoded = upload_file_type(
        type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=b"x" * DEFAULT_CHUNK_SIZE
    ).serialize()
    decode_object(encoded)
    constructor_id = upload_file_type.CONSTRUCTOR_ID
    cached_constructor = {constructor_id: upload_file_type}
    tl_codec._constructor_class_cache[constructor_id] = upload_file_type

    def encode_local() -> int:
        total = 0
        for _index in range(10_000):
            total += len(request.serialize())
        return total

    def encode_class_method() -> int:
        total = 0
        serialize = request_type.serialize
        for _index in range(10_000):
            total += len(serialize(request))
        return total

    def decode_current_mapping() -> int:
        found = 0
        for _index in range(100_000):
            found += CONSTRUCTORS.get(constructor_id) is upload_file_type
        return found

    def decode_direct_dict() -> int:
        found = 0
        for _index in range(100_000):
            found += cached_constructor.get(constructor_id) is upload_file_type
        return found

    def decode_codec_hot_cache() -> int:
        found = 0
        for _index in range(100_000):
            found += tl_codec._constructor_class_cache.get(constructor_id) is upload_file_type
        return found

    def facade_attribute() -> int:
        found = 0
        for _index in range(100_000):
            found += types.UploadFile is upload_file_type
        return found

    def direct_local_attribute() -> int:
        found = 0
        for _index in range(100_000):
            found += upload_file_type is upload_file_type
        return found

    def decode_full() -> int:
        total = 0
        for _index in range(100):
            decoded, offset = decode_object(encoded)
            if offset != len(encoded) or not isinstance(decoded, upload_file_type):
                raise AssertionError("unexpected decode result")
            total += len(decoded.bytes)
        return total

    measurements = _interleaved(
        {
            "encode_local_10k": encode_local,
            "encode_bound_class_method_10k": encode_class_method,
            "constructor_lazy_mapping_100k": decode_current_mapping,
            "constructor_direct_dict_100k": decode_direct_dict,
            "constructor_codec_hot_cache_100k": decode_codec_hot_cache,
            "facade_attribute_100k": facade_attribute,
            "direct_local_attribute_100k": direct_local_attribute,
            "decode_full_100": decode_full,
        }
    )
    results = {
        "class_identity": {
            "facade_is_shard": request_type
            is __import__(request_type.__dict__["_serialize"].__module__, fromlist=[request_type.__name__]).__dict__[
                request_type.__name__
            ],
            "serialize_code_identity": request_type.serialize.__code__ is request.serialize.__func__.__code__,
        },
        **measurements,
    }
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

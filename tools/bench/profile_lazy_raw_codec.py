"""Microprofile lazy raw-codec paths in milliseconds within one controlled process.

Results compare interleaved fixed-iteration operations, not end-to-end Telegram
workloads. Garbage collection is temporarily disabled during timed loops and is
restored afterwards, so measurements are advisory implementation evidence only.
"""

from __future__ import annotations

import argparse
import gc
import json
import statistics
import time
from collections.abc import Callable, Sequence
from typing import Any

from miniproto.media import DEFAULT_CHUNK_SIZE
from miniproto.raw import functions, types
from miniproto.raw._registry import CONSTRUCTORS
from miniproto.tl import codec as tl_codec
from miniproto.tl import decode_object


def _interleaved(cases: dict[str, Callable[[], Any]], *, rounds: int = 10) -> dict[str, dict[str, Any]]:
    """Run fixed cases round-robin and report per-invocation elapsed milliseconds.

    Args:
        cases: Named zero-argument operations to run in rotated order.
        rounds: Number of round-robin passes per operation. Defaults to ``10``.
    """
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


def main(argv: Sequence[str] | None = None) -> int:
    """Profile selected lazy generated-codec paths and print JSON microbenchmark evidence.

    Args:
        argv: Optional CLI arguments; none are currently accepted.

    Returns:
        Zero after emitting best, median, and raw milliseconds samples.
    """
    parser = argparse.ArgumentParser(description="Profile the lazy generated raw API codec paths")
    parser.parse_args(argv)
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
        """Serialize the request ten thousand times through its bound instance method."""
        total = 0
        for _index in range(10_000):
            total += len(request.serialize())
        return total

    def encode_class_method() -> int:
        """Serialize the same request ten thousand times through the class function."""
        total = 0
        serialize = request_type.serialize
        for _index in range(10_000):
            total += len(serialize(request))
        return total

    def decode_current_mapping() -> int:
        """Probe the lazy generated constructor mapping one hundred thousand times."""
        found = 0
        for _index in range(100_000):
            found += CONSTRUCTORS.get(constructor_id) is upload_file_type
        return found

    def decode_direct_dict() -> int:
        """Probe an equivalent eager local constructor dictionary one hundred thousand times."""
        found = 0
        for _index in range(100_000):
            found += cached_constructor.get(constructor_id) is upload_file_type
        return found

    def decode_codec_hot_cache() -> int:
        """Probe the codec's warmed constructor cache one hundred thousand times."""
        found = 0
        for _index in range(100_000):
            found += tl_codec._constructor_class_cache.get(constructor_id) is upload_file_type
        return found

    def facade_attribute() -> int:
        """Read the generated facade attribute one hundred thousand times."""
        found = 0
        for _index in range(100_000):
            found += types.UploadFile is upload_file_type
        return found

    def direct_local_attribute() -> int:
        """Read the already-bound local type one hundred thousand times as a baseline."""
        found = 0
        for _index in range(100_000):
            found += upload_file_type is upload_file_type
        return found

    def decode_full() -> int:
        """Decode and validate one hundred serialized upload-file payloads."""
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

from __future__ import annotations

import io
from itertools import pairwise
from typing import BinaryIO, cast

import pytest

from miniproto.media.multi_session import MIB, assemble_download_parts, download_session_count, plan_download_ranges


@pytest.mark.parametrize(
    ("size", "expected"),
    [(1, 1), (50 * MIB, 1), (50 * MIB + 1, 2), (250 * MIB, 2), (250 * MIB + 1, 4), (2_000 * MIB, 4)],
)
def test_download_session_count_uses_benchmarked_thresholds(size: int, expected: int) -> None:
    assert download_session_count(size) == expected


def test_plan_download_ranges_is_contiguous_aligned_and_complete() -> None:
    total = 503 * MIB + 123
    ranges = plan_download_ranges(total, session_count=4)
    assert len(ranges) == 4
    assert ranges[0].offset == 0
    assert all(item.offset % MIB == 0 for item in ranges)
    assert all(item.limit % MIB == 0 for item in ranges[:-1])
    assert all(left.offset + left.limit == right.offset for left, right in pairwise(ranges))
    assert ranges[-1].offset + ranges[-1].limit == total


@pytest.mark.parametrize(("total", "sessions"), [(0, 1), (1, 0)])
def test_plan_download_ranges_rejects_invalid_values(total: int, sessions: int) -> None:
    with pytest.raises(ValueError):
        plan_download_ranges(total, session_count=sessions)


def test_assemble_download_parts_returns_bytes_in_range_order(tmp_path) -> None:
    parts = (tmp_path / "part-0", tmp_path / "part-1")
    parts[0].write_bytes(b"abc")
    parts[1].write_bytes(b"def")
    destination, data = assemble_download_parts(parts, None, expected_size=6)
    assert destination is None
    assert data == b"abcdef"


def test_assemble_download_parts_writes_destination_path(tmp_path) -> None:
    parts = (tmp_path / "part-0", tmp_path / "part-1")
    parts[0].write_bytes(b"abc")
    parts[1].write_bytes(b"def")
    target = tmp_path / "result.bin"
    destination, data = assemble_download_parts(parts, target, expected_size=6)
    assert destination == target
    assert data is None
    assert target.read_bytes() == b"abcdef"


def test_assemble_download_parts_preserves_existing_path_on_size_mismatch(tmp_path) -> None:
    first = tmp_path / "part-0.bin"
    second = tmp_path / "part-1.bin"
    first.write_bytes(b"abc")
    second.write_bytes(b"def")
    target = tmp_path / "result.bin"
    target.write_bytes(b"previous-good-result")

    with pytest.raises(RuntimeError, match="size mismatch"):
        assemble_download_parts((first, second), target, expected_size=7)

    assert target.read_bytes() == b"previous-good-result"


@pytest.mark.parametrize("accepted_bytes", [0, 2, None])
def test_assemble_download_parts_rejects_incomplete_destination_writes(tmp_path, accepted_bytes: int | None) -> None:
    class IncompleteWriter:
        def __init__(self) -> None:
            self.buffer = io.BytesIO()

        def write(self, payload: bytes) -> int | None:
            if accepted_bytes is None:
                return None
            return self.buffer.write(payload[:accepted_bytes])

    part = tmp_path / "part.bin"
    part.write_bytes(b"abcdefgh")
    destination = IncompleteWriter()
    with pytest.raises(RuntimeError, match="destination write"):
        assemble_download_parts((part,), cast(BinaryIO, destination), expected_size=8)
    assert not destination.buffer.closed
    expected = b"ab" if accepted_bytes == 2 else b""
    assert destination.buffer.getvalue() == expected

from __future__ import annotations

import io
import os
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, cast

MIB = 1024 * 1024
_TWO_SESSION_MAX_SIZE = 250 * MIB
_SINGLE_SESSION_MAX_SIZE = 50 * MIB


@dataclass(frozen=True, slots=True)
class DownloadRange:
    index: int
    offset: int
    limit: int


def download_session_count(total_size: int) -> int:
    if total_size <= 0:
        raise ValueError("total_size must be positive")
    if total_size <= _SINGLE_SESSION_MAX_SIZE:
        return 1
    if total_size <= _TWO_SESSION_MAX_SIZE:
        return 2
    return 4


def plan_download_ranges(total_size: int, *, session_count: int, alignment: int = MIB) -> tuple[DownloadRange, ...]:
    if total_size <= 0:
        raise ValueError("total_size must be positive")
    if session_count <= 0:
        raise ValueError("session_count must be positive")
    if alignment <= 0:
        raise ValueError("alignment must be positive")
    full_units, tail = divmod(total_size, alignment)
    if full_units == 0:
        return (DownloadRange(index=0, offset=0, limit=total_size),)
    active_sessions = min(session_count, full_units)
    base_units, extra_units = divmod(full_units, active_sessions)
    ranges: list[DownloadRange] = []
    offset = 0
    for index in range(active_sessions):
        units = base_units + (1 if index < extra_units else 0)
        limit = units * alignment
        if index == active_sessions - 1:
            limit += tail
        ranges.append(DownloadRange(index=index, offset=offset, limit=limit))
        offset += limit
    return tuple(ranges)


def assemble_download_parts(
    part_paths: Sequence[Path], destination: str | os.PathLike[str] | BinaryIO | None, *, expected_size: int
) -> tuple[Path | BinaryIO | None, bytes | None]:
    data_buffer: io.BytesIO | None = None
    should_close = False
    if destination is None:
        data_buffer = io.BytesIO()
        output: BinaryIO = data_buffer
        resolved_destination: Path | BinaryIO | None = None
    elif isinstance(destination, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], destination))
        path.parent.mkdir(parents=True, exist_ok=True)
        output = path.open("wb")
        resolved_destination = path
        should_close = True
    else:
        output = destination
        resolved_destination = destination
    written = 0
    try:
        for part_path in part_paths:
            with part_path.open("rb") as part:
                while chunk := part.read(4 * MIB):
                    output.write(chunk)
                    written += len(chunk)
    finally:
        if should_close:
            output.close()
    if written != expected_size:
        raise RuntimeError(f"assembled download size mismatch: expected {expected_size}, wrote {written}")
    return resolved_destination, data_buffer.getvalue() if data_buffer is not None else None

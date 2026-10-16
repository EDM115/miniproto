"""Deterministic multi-session range planning and ordered download-part assembly.

Assembly reads completed part files in caller-supplied order and leaves them caller-owned. Caller streams remain open at their post-write position, in-memory bytes are not zeroized, and path outputs are replaced atomically after size validation. Session scheduling belongs to the client.
"""

from __future__ import annotations

import io
import os
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, cast

MIB = 1024 * 1024
_TWO_SESSION_MAX_SIZE = 250 * MIB
_SINGLE_SESSION_MAX_SIZE = 50 * MIB


@dataclass(frozen=True, slots=True)
class DownloadRange:
    """A contiguous byte interval assigned to one parallel download session.

    Attributes:
        index: Zero-based session/range number.
        offset: Inclusive starting byte offset.
        limit: Number of bytes in the range.
    """

    index: int
    offset: int
    limit: int


def download_session_count(total_size: int) -> int:
    """Choose the supported session count for a positive whole-file size.

    Args:
        total_size: Total media size in bytes.

    Returns:
        One session for files up to 50 MiB, two for files above 50 MiB through 250 MiB, four for larger files.

    Raises:
        ValueError: ``total_size`` is not positive.
    """
    if total_size <= 0:
        raise ValueError("total_size must be positive")
    if total_size <= _SINGLE_SESSION_MAX_SIZE:
        return 1
    if total_size <= _TWO_SESSION_MAX_SIZE:
        return 2
    return 4


def plan_download_ranges(total_size: int, *, session_count: int, alignment: int = MIB) -> tuple[DownloadRange, ...]:
    """Partition a file into contiguous, aligned ranges for multiple sessions.

    Args:
        total_size: Positive total file size in bytes.
        session_count: Requested number of parallel sessions, capped by the number of full alignment units, with one range for smaller files.
        alignment: Positive byte alignment for every offset and non-tail range length, defaults to one MiB.

    Returns:
        Ordered, gap-free ranges whose limits sum exactly to ``total_size``.

    Raises:
        ValueError: Any size, session count or alignment is non-positive.
    """
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
    """Concatenate completed range files into a destination in their supplied order.

    Args:
        part_paths: Ordered filesystem paths of completed session outputs.
        destination: Output path, binary stream or ``None`` to return in-memory bytes.
        expected_size: Exact aggregate byte count required for successful assembly.

    Returns:
        The resolved output destination and bytes only when ``destination`` is ``None``.

    Destination Effects:
        A path destination creates parent directories, writes to a temporary sibling, flushes and calls ``fsync`` before replacing the target after exact-size validation. An existing target survives failures before replacement. A caller stream stays open at its post-write position, without rollback after a write failure. ``None`` returns immutable bytes without zeroization. Completed part files remain caller-owned.

    Raises:
        OSError: A part or path destination cannot be read, created or written.
        RuntimeError: Part metadata or copied data does not contain exactly ``expected_size`` bytes, or the destination reports an incomplete write. Path destinations are not replaced on this error.
    """
    source_size = sum(part_path.stat().st_size for part_path in part_paths)
    if source_size != expected_size:
        raise RuntimeError(f"assembled download size mismatch: expected {expected_size}, found {source_size}")
    data_buffer: io.BytesIO | None = None
    should_close = False
    temporary_path: Path | None = None
    final_path: Path | None = None
    if destination is None:
        data_buffer = io.BytesIO()
        output: BinaryIO = data_buffer
        resolved_destination: Path | BinaryIO | None = None
    elif isinstance(destination, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], destination))
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        output = os.fdopen(descriptor, "wb")
        temporary_path = Path(temporary_name)
        final_path = path
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
                    accepted = output.write(chunk)
                    if accepted != len(chunk):
                        raise RuntimeError(
                            f"destination write at offset {written} expected {len(chunk)} bytes but wrote {accepted}"
                        )
                    written += len(chunk)
        if written != expected_size:
            raise RuntimeError(f"assembled download size mismatch: expected {expected_size}, wrote {written}")
        if should_close:
            output.flush()
            os.fsync(output.fileno())
            output.close()
        if final_path is not None and temporary_path is not None:
            os.replace(temporary_path, final_path)
            temporary_path = None
    except BaseException:
        if should_close and not output.closed:
            output.close()
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    return resolved_destination, data_buffer.getvalue() if data_buffer is not None else None

from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from tools.bench.reporting import BENCHMARK_SCHEMA, collect_environment, write_benchmark_report

MATRIX_SCHEMA = "miniproto.benchmark-matrix.v1"
MatrixExecutor = Callable[["MatrixCell", Path, Path], int]


@dataclass(frozen=True, slots=True)
class MatrixCell:
    lanes: int
    byte_window: int
    chunk_size: int
    launch_stagger: bool
    destination: Literal["file", "memory"]
    warm: bool
    repeat: int

    @property
    def id(self) -> str:
        """Return a stable filesystem-safe identity for this matrix cell."""
        stagger = "stagger" if self.launch_stagger else "burst"
        warmth = "warm" if self.warm else "cold"
        chunk_kib = self.chunk_size // 1024
        return f"l{self.lanes}-w{self.byte_window}m-c{chunk_kib}k-{stagger}-{self.destination}-{warmth}-r{self.repeat}"


def build_matrix(mode: str) -> tuple[MatrixCell, ...]:
    """Build the bounded smoke subset or complete requested live matrix."""
    if mode == "smoke":
        return (
            MatrixCell(1, 4, 512 * 1024, True, "file", False, 1),
            MatrixCell(1, 32, 512 * 1024, False, "memory", True, 1),
            MatrixCell(4, 4, 1024 * 1024, False, "file", True, 1),
            MatrixCell(4, 32, 1024 * 1024, True, "memory", False, 1),
        )
    if mode != "full":
        raise ValueError("matrix mode must be smoke or full")
    return tuple(
        MatrixCell(lanes, window, chunk, stagger, destination, warm, repeat)
        for lanes, window, chunk, stagger, destination, warm, repeat in itertools.product(
            (1, 2, 4),
            (4, 8, 16, 32),
            (512 * 1024, 1024 * 1024),
            (False, True),
            ("file", "memory"),
            (False, True),
            (1, 2, 3),
        )
    )


def prepare_run_directory(path: Path, *, mode: str, resume: bool) -> None:
    """Create or validate a task-owned matrix directory without overwriting unrelated history."""
    manifest_path = path / "configuration.json"
    if path.exists() and any(path.iterdir()):
        if not resume or not manifest_path.exists():
            raise FileExistsError(f"refusing to reuse non-empty matrix directory: {path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema") != MATRIX_SCHEMA or manifest.get("mode") != mode:
            raise ValueError("resume directory does not match the requested matrix mode")
    else:
        path.mkdir(parents=True, exist_ok=True)
        manifest = {
            "schema": MATRIX_SCHEMA,
            "mode": mode,
            "cells": [asdict(cell) | {"id": cell.id} for cell in build_matrix(mode)],
        }
        write_benchmark_report(manifest_path, manifest)
        write_benchmark_report(path / "environment.json", collect_environment())
    (path / "raw").mkdir(exist_ok=True)
    (path / "logs").mkdir(exist_ok=True)


def run_matrix(cells: Sequence[MatrixCell], output: Path, *, execute: MatrixExecutor, resume: bool) -> dict[str, Any]:
    """Run/resume cells, preserving completed artifacts and retrying failed or missing cells."""
    completed: list[str] = []
    failures: list[dict[str, Any]] = []
    previously_failed = _previous_failed_cells(output) if resume else set()
    for cell in cells:
        raw_path = output / "raw" / f"{cell.id}.json"
        log_path = output / "logs" / f"{cell.id}.log"
        if resume and cell.id not in previously_failed and _complete_raw_report(raw_path):
            completed.append(cell.id)
            continue
        exit_code = execute(cell, raw_path, log_path)
        if exit_code == 0 and _complete_raw_report(raw_path):
            completed.append(cell.id)
        else:
            failures.append({"cell": cell.id, "exit_code": exit_code})
    status = {"schema": MATRIX_SCHEMA, "completed": completed, "failed": failures}
    write_benchmark_report(output / "status.json", status)
    aggregate_run(cells, output, failures=failures)
    return status


def aggregate_run(
    cells: Sequence[MatrixCell], output: Path, *, failures: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Aggregate completed raw cells deterministically and render the comparison table."""
    rows: list[dict[str, Any]] = []
    failed_cells = {str(failure["cell"]) for failure in failures if isinstance(failure.get("cell"), str)}
    for cell in sorted(cells, key=lambda item: item.id):
        if cell.id in failed_cells:
            continue
        raw_path = output / "raw" / f"{cell.id}.json"
        if not _complete_raw_report(raw_path):
            continue
        report = json.loads(raw_path.read_text(encoding="utf-8"))
        throughput = report.get("throughput", {})
        statistics = report.get("statistics") or {}
        rows.append(
            asdict(cell)
            | {
                "id": cell.id,
                "throughput_mib_per_second": _throughput_mib(report, throughput),
                "median": statistics.get("median"),
                "p95": statistics.get("p95"),
                "p99": statistics.get("p99"),
                "rss_delta_bytes": (report.get("rss") or {}).get("delta_bytes"),
                "loop_lag_p95_ms": (report.get("loop_lag") or {}).get("p95_ms"),
                "loop_lag_max_ms": (report.get("loop_lag") or {}).get("max_ms"),
            }
        )
    aggregate = {
        "schema": MATRIX_SCHEMA,
        "cells": rows,
        "failures": [dict(failure) for failure in failures],
        "summary": {"completed": len(rows), "failed": len(failures), "total": len(cells)},
    }
    write_benchmark_report(output / "aggregate.json", aggregate)
    (output / "comparison.md").write_text(_markdown_table(rows), encoding="utf-8", newline="\n")
    return aggregate


def build_live_command(cell: MatrixCell, raw_path: Path) -> list[str]:
    """Build the secret-free live benchmark command for one matrix cell."""
    command = [
        sys.executable,
        "-u",
        "tools/bench/benchmark_live_media_limit.py",
        "--actor",
        "bot",
        "--operation",
        "download",
        "--repeat",
        "1",
        "--warmup-repeat",
        "1" if cell.warm else "0",
        "--download-media-lanes",
        str(cell.lanes),
        "--download-concurrency",
        str(max(cell.lanes * 3, 1)),
        "--download-max-in-flight-bytes",
        str(cell.byte_window * 1024 * 1024),
        "--download-chunk-size",
        str(cell.chunk_size),
        "--download-max-chunk-size",
        str(cell.chunk_size),
        "--download-destination",
        cell.destination,
        "--json",
        str(raw_path),
        "--loop-lag",
    ]
    command.append("--download-launch-stagger" if cell.launch_stagger else "--no-download-launch-stagger")
    return command


def subprocess_executor(cell: MatrixCell, raw_path: Path, log_path: Path) -> int:
    """Execute one live cell and preserve combined output even on failure."""
    command = build_live_command(cell, raw_path)
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        completed = subprocess.run(  # noqa: S603 - command is built only from validated MatrixCell fields
            command, check=False, stdout=log, stderr=subprocess.STDOUT, env=os.environ.copy()
        )
    return completed.returncode


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or resume the miniproto live media benchmark matrix")
    parser.add_argument("--mode", choices=("smoke", "full"), default="smoke")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if os.environ.get("MINIPROTO_LIVE_BENCH") != "1":
        print("Refusing to run a live matrix without MINIPROTO_LIVE_BENCH=1", file=sys.stderr)
        return 2
    output = args.output or Path(".tmp/benchmark-matrix") / datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    prepare_run_directory(output, mode=args.mode, resume=args.resume)
    status = run_matrix(build_matrix(args.mode), output, execute=subprocess_executor, resume=args.resume)
    print(json.dumps(status, indent=2, sort_keys=True))
    return 1 if status["failed"] else 0


def _complete_raw_report(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(value, dict) and (value.get("schema") == BENCHMARK_SCHEMA or "results" in value)


def _previous_failed_cells(output: Path) -> set[str]:
    status_path = output / "status.json"
    if not status_path.is_file():
        return set()
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    failed = status.get("failed", []) if isinstance(status, Mapping) else []
    return {str(item["cell"]) for item in failed if isinstance(item, Mapping) and isinstance(item.get("cell"), str)}


def _throughput_mib(report: Mapping[str, Any], throughput: Mapping[str, Any]) -> float | None:
    direct = throughput.get("download_mib_per_second")
    if isinstance(direct, int | float):
        return float(direct)
    values = [
        float(result["transfer_mib_s"])
        for result in report.get("results", [])
        if isinstance(result, Mapping)
        and result.get("operation") == "download"
        and isinstance(result.get("transfer_mib_s"), int | float)
    ]
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def _markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Benchmark matrix comparison",
        "",
        "| lanes | byte window MiB | chunk KiB | stagger | destination | warmth | repeat | MiB/s | RSS delta | loop p95 ms | loop max ms |",
        "| ---: | ---: | ---: | :---: | :--- | :---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['lanes']} | {row['byte_window']} | {row['chunk_size'] // 1024} | {'on' if row['launch_stagger'] else 'off'} | {row['destination']} | {'warm' if row['warm'] else 'cold'} | {row['repeat']} | {_display(row['throughput_mib_per_second'])} | {_display(row['rss_delta_bytes'])} | {_display(row['loop_lag_p95_ms'])} | {_display(row['loop_lag_max_ms'])} |"
        )
    return "\n".join(lines) + "\n"


def _display(value: Any) -> str:
    if value is None:
        return "—"
    return f"{value:.3f}" if isinstance(value, float) else str(value)


__all__ = [
    "MATRIX_SCHEMA",
    "MatrixCell",
    "aggregate_run",
    "build_live_command",
    "build_matrix",
    "prepare_run_directory",
    "run_matrix",
]


if __name__ == "__main__":
    raise SystemExit(main())

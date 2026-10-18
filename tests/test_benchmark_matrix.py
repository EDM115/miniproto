from __future__ import annotations

import json
from pathlib import Path

from tools.bench.benchmark_matrix import MatrixCell, aggregate_run, build_matrix, prepare_run_directory, run_matrix
from tools.bench.reporting import BENCHMARK_SCHEMA


def test_full_matrix_covers_requested_dimensions_and_three_repeats() -> None:
    cells = build_matrix("full")

    assert len(cells) == 3 * 4 * 2 * 2 * 2 * 2 * 3
    assert {cell.lanes for cell in cells} == {1, 2, 4}
    assert {cell.byte_window for cell in cells} == {4, 8, 16, 32}
    assert {cell.chunk_size for cell in cells} == {512 * 1024, 1024 * 1024}
    assert {cell.launch_stagger for cell in cells} == {False, True}
    assert {cell.destination for cell in cells} == {"file", "memory"}
    assert {cell.warm for cell in cells} == {False, True}
    assert {cell.repeat for cell in cells} == {1, 2, 3}
    assert len({cell.id for cell in cells}) == len(cells)


def test_smoke_matrix_is_bounded_but_covers_lane_window_and_destination_edges() -> None:
    cells = build_matrix("smoke")

    assert 1 < len(cells) < 20
    assert {cell.lanes for cell in cells} == {1, 4}
    assert {cell.byte_window for cell in cells} == {4, 32}
    assert {cell.destination for cell in cells} == {"file", "memory"}
    assert {cell.warm for cell in cells} == {False, True}
    assert {cell.repeat for cell in cells} == {1}


def test_prepare_run_directory_refuses_unrelated_nonempty_history(tmp_path: Path) -> None:
    output = tmp_path / "existing"
    output.mkdir()
    (output / "unrelated.txt").write_text("keep", encoding="utf-8")

    try:
        prepare_run_directory(output, mode="smoke", resume=False)
    except FileExistsError:
        pass
    else:
        raise AssertionError("non-empty unrelated history should not be reused")

    assert (output / "unrelated.txt").read_text(encoding="utf-8") == "keep"


def test_matrix_resume_skips_completed_cells_and_preserves_failed_cells(tmp_path: Path) -> None:
    cells = (
        MatrixCell(
            lanes=1, byte_window=4, chunk_size=512 * 1024, launch_stagger=True, destination="file", warm=False, repeat=1
        ),
        MatrixCell(
            lanes=4,
            byte_window=32,
            chunk_size=1024 * 1024,
            launch_stagger=False,
            destination="memory",
            warm=True,
            repeat=1,
        ),
    )
    calls: list[str] = []

    def execute(cell: MatrixCell, raw_path: Path, log_path: Path) -> int:
        calls.append(cell.id)
        log_path.write_text(f"ran {cell.id}\n", encoding="utf-8")
        if cell.lanes == 4:
            raw_path.write_text(
                json.dumps(
                    {
                        "schema": BENCHMARK_SCHEMA,
                        "statistics": {"median": 99.0, "p95": 99.0, "p99": 99.0},
                        "throughput": {"download_mib_per_second": 1.0},
                    }
                ),
                encoding="utf-8",
            )
            return 7
        raw_path.write_text(
            json.dumps(
                {
                    "schema": BENCHMARK_SCHEMA,
                    "statistics": {"median": 10.0, "p95": 12.0, "p99": 13.0},
                    "throughput": {"download_mib_per_second": 42.0},
                    "loop_lag": {"max_ms": 1.0, "p95_ms": 0.5},
                    "rss": {"delta_bytes": 1024},
                }
            ),
            encoding="utf-8",
        )
        return 0

    prepare_run_directory(tmp_path, mode="smoke", resume=False)
    first = run_matrix(cells, tmp_path, execute=execute, resume=False)
    first_aggregate = json.loads((tmp_path / "aggregate.json").read_text(encoding="utf-8"))
    second = run_matrix(cells, tmp_path, execute=execute, resume=True)

    assert calls == [cells[0].id, cells[1].id, cells[1].id]
    assert first["completed"] == [cells[0].id]
    assert first["failed"] == [{"cell": cells[1].id, "exit_code": 7}]
    assert first_aggregate["summary"] == {"completed": 1, "failed": 1, "total": 2}
    assert [row["id"] for row in first_aggregate["cells"]] == [cells[0].id]
    assert second["completed"] == [cells[0].id]
    assert second["failed"] == [{"cell": cells[1].id, "exit_code": 7}]
    assert (tmp_path / "raw" / f"{cells[0].id}.json").exists()
    assert (tmp_path / "logs" / f"{cells[1].id}.log").exists()


def test_aggregate_run_is_deterministic_and_writes_markdown_table(tmp_path: Path) -> None:
    cell = MatrixCell(
        lanes=2, byte_window=8, chunk_size=512 * 1024, launch_stagger=True, destination="file", warm=True, repeat=1
    )
    prepare_run_directory(tmp_path, mode="smoke", resume=False)
    raw = tmp_path / "raw" / f"{cell.id}.json"
    raw.write_text(
        json.dumps(
            {
                "schema": BENCHMARK_SCHEMA,
                "statistics": {"median": 10.0, "p95": 12.0, "p99": 13.0},
                "throughput": {"download_mib_per_second": 42.0},
                "loop_lag": {"max_ms": 1.0, "p95_ms": 0.5},
                "rss": {"delta_bytes": 1024},
            }
        ),
        encoding="utf-8",
    )

    first = aggregate_run((cell,), tmp_path, failures=[])
    aggregate_bytes = (tmp_path / "aggregate.json").read_bytes()
    table_bytes = (tmp_path / "comparison.md").read_bytes()
    second = aggregate_run((cell,), tmp_path, failures=[])

    assert first == second
    assert (tmp_path / "aggregate.json").read_bytes() == aggregate_bytes
    assert (tmp_path / "comparison.md").read_bytes() == table_bytes
    assert first["schema"] == "miniproto.benchmark-matrix.v1"
    assert first["cells"][0]["throughput_mib_per_second"] == 42.0
    assert "| lanes | byte window MiB |" in table_bytes.decode()

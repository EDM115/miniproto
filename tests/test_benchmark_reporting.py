from __future__ import annotations

import asyncio
import json
import subprocess
from collections.abc import Mapping
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from typing import Any, TextIO

import pytest
import tools.bench.reporting as reporting
from tools.bench import benchmark_live_media_limit as benchmark
from tools.bench import benchmark_matrix as matrix
from tools.bench.reporting import (
    BENCHMARK_SCHEMA,
    LoopLagProbe,
    _advance_probe_target,
    build_benchmark_report,
    sample_statistics,
    write_benchmark_report,
)

from miniproto.file_id import encode_file_id
from miniproto.media.download import MediaDownloadResult
from miniproto.types import Media


def test_loop_lag_probe_skips_missed_cadences_instead_of_emitting_a_catch_up_storm() -> None:
    assert _advance_probe_target(target=1.0, observed=1.026, interval=0.01) == pytest.approx(1.03)
    assert _advance_probe_target(target=1.0, observed=1.001, interval=0.01) == pytest.approx(1.01)


def test_sample_statistics_reports_hand_checked_percentiles() -> None:
    statistics = sample_statistics([1.0, 2.0, 3.0, 4.0, 100.0])

    assert statistics == {
        "count": 5,
        "min": 1.0,
        "max": 100.0,
        "mean": 22.0,
        "median": 3.0,
        "p50": 3.0,
        "p95": pytest.approx(80.8),
        "p99": pytest.approx(96.16),
    }


def test_benchmark_report_has_normalized_schema_and_redacts_feature_secrets() -> None:
    report = build_benchmark_report(
        benchmark="fixture",
        mode="smoke",
        warmup=2,
        samples=[1.0, 2.0, 3.0],
        unit="ms",
        configuration={"lanes": 2, "bot_token": "secret", "nested": {"api_hash": "secret"}},
        throughput={"bytes_per_second": 123.0},
        rss={"start_bytes": 10, "peak_bytes": 20, "end_bytes": 15},
        loop_lag={"enabled": False, "samples": 0},
        environment={"package_version": "0.1.0", "commit": "abc"},
    )

    assert report["schema"] == BENCHMARK_SCHEMA
    assert report["benchmark"] == "fixture"
    assert report["mode"] == "smoke"
    assert report["warmup"] == 2
    assert report["sample_unit"] == "ms"
    assert report["samples"] == [1.0, 2.0, 3.0]
    assert report["statistics"]["p95"] == pytest.approx(2.9)
    assert report["configuration"] == {"bot_token": "<redacted>", "lanes": 2, "nested": {"api_hash": "<redacted>"}}
    assert report["throughput"] == {"bytes_per_second": 123.0}
    assert report["rss"]["peak_bytes"] == 20
    assert report["environment"]["commit"] == "abc"


def test_write_benchmark_report_is_deterministic_and_creates_parent(tmp_path: Path) -> None:
    report = build_benchmark_report(
        benchmark="fixture",
        mode="full",
        warmup=0,
        samples=[3.0],
        unit="seconds",
        configuration={},
        environment={"package_version": "0.1.0"},
    )
    destination = tmp_path / "nested" / "report.json"

    write_benchmark_report(destination, report)

    assert destination.read_text(encoding="utf-8") == json.dumps(report, indent=2, sort_keys=True) + "\n"


def test_loop_lag_probe_lifecycle_reports_samples_and_callback_overhead() -> None:
    async def scenario() -> dict[str, Any]:
        probe = LoopLagProbe(interval_s=0.001, stall_threshold_s=0.005)
        await probe.start()
        await asyncio.sleep(0.004)
        await asyncio.sleep(0.012)
        return await probe.stop()

    report = asyncio.run(scenario())

    assert report["enabled"] is True
    assert report["interval_ms"] == 1.0
    assert report["stall_threshold_ms"] == 5.0
    assert isinstance(report["samples"], int)
    assert report["samples"] > 0
    assert report["max_ms"] >= 0
    assert report["p50_ms"] >= 0
    assert report["p95_ms"] >= report["p50_ms"]
    assert report["p99_ms"] >= report["p95_ms"]
    assert report["callback_overhead_ns"]["count"] == report["samples"]


def test_loop_lag_probe_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="interval_s"):
        LoopLagProbe(interval_s=0)
    with pytest.raises(ValueError, match="stall_threshold_s"):
        LoopLagProbe(interval_s=0.001, stall_threshold_s=-1)


def test_environment_distinguishes_running_loop_from_platform_preference(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(reporting, "_command_output", lambda command: None)
    monkeypatch.setattr(reporting.event_loop, "backend_name", lambda: "preferred-loop")
    monkeypatch.setattr(reporting.event_loop, "backend_version", lambda: "1.2.3")

    async def collect():
        loop = asyncio.get_running_loop()
        return reporting.collect_environment(), f"{type(loop).__module__}.{type(loop).__name__}"

    environment, actual = asyncio.run(collect())
    assert environment["event_loop"]["preferred_backend"] == "preferred-loop"
    assert environment["event_loop"]["running_backend"] == actual
    assert reporting.collect_environment()["event_loop"]["running_backend"] is None


class OfflineClient:
    def __init__(self, *, fail_upload: bool = False) -> None:
        self.media = Media(id=17, access_hash=23, file_reference=b"synthetic", dc_id=2, size=4, file_name="sample.bin")
        self.fail_upload = fail_upload
        self.upload_peers: list[str] = []
        self.history_peers: list[str] = []
        self.downloads = 0
        self.disconnected = False
        self.caption = ""

    async def send_file(self, peer: str, source: Path, **kwargs: Any) -> SimpleNamespace:
        self.upload_peers.append(peer)
        if self.fail_upload:
            raise RuntimeError("phone peer is not cached")
        assert await asyncio.to_thread(source.read_bytes) == b"data"
        self.caption = kwargs["caption"]
        await kwargs["progress"](4, 4)
        return SimpleNamespace(id=31, media=None)

    async def get_history(self, peer: str, *, limit: int) -> list[SimpleNamespace]:
        self.history_peers.append(peer)
        assert limit == 20
        return [SimpleNamespace(id=31, text=self.caption, media=self.media)]

    async def download_media(self, media: Media, target: Path | None, **kwargs: Any) -> MediaDownloadResult:
        assert media.id == 17
        assert target is None
        assert kwargs["limit"] == kwargs["total_size"] == 4
        self.downloads += 1
        await kwargs["progress"](4, 4)
        return MediaDownloadResult(bytes_downloaded=4, offset=0, destination=None, data=b"data")

    async def disconnect(self) -> None:
        self.disconnected = True


def install_offline_client(monkeypatch: pytest.MonkeyPatch, client: OfflineClient) -> None:
    def forbid_live_work(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline privacy tests must not use credentials, sessions or Telegram")

    def require_offline_env(env: Mapping[str, str], *, actor: str) -> None:
        assert actor in {"user", "bot"}
        assert set(env) <= {
            "MINIPROTO_LIVE_BENCH_USER_PEER",
            "MINIPROTO_LIVE_BENCH_BOT_PEER",
            "MINIPROTO_LIVE_BENCH_BOT_FILE_ID",
        }

    async def authorize(actor: str, _args: object, env: Mapping[str, str]) -> OfflineClient:
        require_offline_env(env, actor=actor)
        return client

    for name in ("Client", "EncryptedSQLiteSessionStorage", "load_dotenv"):
        monkeypatch.setattr(benchmark, name, forbid_live_work)
    monkeypatch.setattr(benchmark, "require_live_env", require_offline_env)
    monkeypatch.setattr(benchmark, "authorized_client", authorize)


def report_args(tmp_path: Path, actor: str) -> Any:
    source = tmp_path / "source.bin"
    source.write_bytes(b"data")
    return benchmark.parse_args(
        [
            "--actor",
            actor,
            "--operation",
            "both",
            "--size",
            "4",
            "--file",
            str(source),
            "--download-destination",
            "memory",
            "--progress-interval",
            "0",
            "--json",
            str(tmp_path / "summary.json"),
        ],
        {},
    )


@pytest.mark.parametrize(
    ("actor", "peer", "expected_label"),
    [
        ("user", "+15550198276", "user:configured-peer"),
        ("bot", "+15550923481", "bot:configured-peer"),
        ("user", "@private_user_target", "user:configured-peer"),
        ("bot", "@private_bot_target", "bot:configured-peer"),
        ("user", "-1007654321987", "user:configured-peer"),
        ("bot", "-1008123456790", "bot:configured-peer"),
        ("user", "self", "self"),
        ("user", "Saved_Messages", "self"),
    ],
)
def test_transfer_reports_omit_configured_peers_but_preserve_rpc_targets(
    actor: str,
    peer: str,
    expected_label: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = OfflineClient()
    install_offline_client(monkeypatch, client)
    summaries: list[benchmark.BenchmarkSummary] = []
    print_summary = benchmark.print_summary

    def capture_summary(summary: benchmark.BenchmarkSummary) -> None:
        summaries.append(summary)
        print_summary(summary)

    monkeypatch.setattr(benchmark, "print_summary", capture_summary)
    args = report_args(tmp_path, actor)
    env = {f"MINIPROTO_LIVE_BENCH_{actor.upper()}_PEER": peer}

    assert asyncio.run(benchmark._run_benchmark(args, env, None)) == 0

    captured = capsys.readouterr()
    raw_json = (tmp_path / "summary.json").read_bytes()
    report = json.loads(raw_json)
    if expected_label != "self":
        assert peer not in captured.out + captured.err
        assert peer.encode() not in raw_json
    assert f"peer={expected_label}" in captured.out
    assert client.upload_peers == [peer]
    assert client.history_peers == [peer]
    assert client.downloads == 1
    assert client.disconnected
    assert [result.peer for result in summaries[0].results] == [expected_label, expected_label]
    assert [result["operation"] for result in report["results"]] == ["upload", "download"]
    for result in report["results"]:
        assert result["peer"] == expected_label
        assert result["bytes"] == 4
        assert result["media_dc_id"] == 2
        assert result["message_id"] == 31
        assert result["file_id"] == encode_file_id(client.media)
        assert result["transfer_mib_s"] == pytest.approx(4 / (1024 * 1024 * result["transfer_duration_s"]))


def test_failed_upload_does_not_print_confidential_peer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    peer = "+15550741926"
    client = OfflineClient(fail_upload=True)
    install_offline_client(monkeypatch, client)
    args = report_args(tmp_path, "user")

    with pytest.raises(RuntimeError, match="phone peer is not cached"):
        asyncio.run(benchmark._run_benchmark(args, {"MINIPROTO_LIVE_BENCH_USER_PEER": peer}, None))

    captured = capsys.readouterr()
    assert "peer=user:configured-peer" in captured.out
    assert peer not in captured.out + captured.err
    assert client.upload_peers == [peer]
    assert client.disconnected
    assert not (tmp_path / "summary.json").exists()


def test_matrix_artifacts_capture_redacted_download_reports(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    peer = "+15550379824"
    client = OfflineClient()
    install_offline_client(monkeypatch, client)
    env = {"MINIPROTO_LIVE_BENCH_BOT_PEER": peer, "MINIPROTO_LIVE_BENCH_BOT_FILE_ID": encode_file_id(client.media)}
    monkeypatch.setattr(matrix.os, "environ", env)
    monkeypatch.setattr(matrix, "collect_environment", lambda: {"python": "offline"})
    matrix.prepare_run_directory(tmp_path, mode="smoke", resume=False)
    cell = matrix.MatrixCell(
        lanes=1, byte_window=4, chunk_size=512 * 1024, launch_stagger=True, destination="memory", warm=False, repeat=1
    )

    def execute_offline_child(
        command: list[str], *, check: bool, stdout: TextIO, stderr: int, env: dict[str, str]
    ) -> subprocess.CompletedProcess[str]:
        assert command[2] == "tools/bench/benchmark_live_media_limit.py"
        assert check is False
        assert stderr == subprocess.STDOUT
        args = benchmark.parse_args(command[3:], env)
        with redirect_stdout(stdout), redirect_stderr(stdout):
            result = asyncio.run(benchmark.run_benchmark(args, env))
        return subprocess.CompletedProcess(command, result)

    monkeypatch.setattr(matrix.subprocess, "run", execute_offline_child)

    status = matrix.run_matrix((cell,), tmp_path, execute=matrix.subprocess_executor, resume=False)

    assert status["completed"] == [cell.id]
    assert status["failed"] == []
    assert client.downloads == 1
    report = json.loads((tmp_path / "raw" / f"{cell.id}.json").read_text(encoding="utf-8"))
    assert report["results"][0]["peer"] == "bot:configured-peer"
    assert report["results"][0]["bytes"] == 4
    log = (tmp_path / "logs" / f"{cell.id}.log").read_text(encoding="utf-8")
    assert "bot.download:" in log
    for artifact in tmp_path.rglob("*"):
        if artifact.is_file():
            assert peer.encode() not in artifact.read_bytes()

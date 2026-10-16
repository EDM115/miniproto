from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
from tools.bench import benchmark_live_media_limit as benchmark
from tools.bench import benchmark_matrix as matrix
from tools.bench import benchmark_multi_session_download as multi_session
from tools.bench import benchmark_runtime_paths as runtime
from tools.bench import benchmark_tl_fast_paths as tl
from tools.bench import benchmark_transport_framing as framing

from miniproto import Client
from miniproto.file_id import encode_file_id
from miniproto.media.download import MediaDownloadResult, _open_destination
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry
from miniproto.tl import fast
from miniproto.types import Media, Peer


@pytest.mark.parametrize("mode,expected", [("smoke", (8, 65536, 3)), ("full", (100, 1048576, 30))])
def test_tl_mode_passes_effective_dimensions_to_workload(
    mode: str, expected: tuple[int, int, int], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    measured: list[tuple[int, int, int]] = []

    def measure(*, iterations: int, payload_bytes: int, rounds: int) -> tl.Result:
        measured.append((iterations, payload_bytes, rounds))
        return tl.Result(native_ms=(1.0,), fallback_ms=(2.0,))

    monkeypatch.setattr(tl, "_benchmark", measure)
    monkeypatch.setattr(tl.fast, "native_fast_paths_available", lambda: True)
    monkeypatch.setattr(tl, "collect_environment", lambda: {})
    monkeypatch.setattr(
        sys,
        "argv",
        ["benchmark", "--mode", mode, "--iterations", "100", "--payload-bytes", "1048576", "--rounds", "30"],
    )

    assert tl.main() == 0
    report = json.loads(capsys.readouterr().out)
    assert measured == [expected]
    assert tuple(report["configuration"][name] for name in ("iterations", "payload_bytes", "rounds")) == expected
    assert report["throughput"]["native_mix_iterations_per_second"] == expected[0] * 1000


@pytest.mark.parametrize("mode,expected", [("smoke", (1024, 3)), ("full", (4096, 30))])
def test_transport_mode_passes_effective_dimensions_to_workload(
    mode: str, expected: tuple[int, int], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    measured: list[tuple[int, int]] = []

    async def measure(payload: bytes, *, frames: int, rounds: int, raw_native: bool):
        assert len(payload) == 72
        assert raw_native is False
        measured.append((frames, rounds))
        return (framing.Result("tcp_abridged", native_ms=(1.0,), legacy_ms=(3.0,)),), "test.ActualLoop"

    monkeypatch.setattr(framing, "_benchmark_all", measure)
    monkeypatch.setattr(framing, "native_transport_available", lambda: True)
    monkeypatch.setattr(framing, "collect_environment", lambda: {"event_loop": {"running_backend": None}})
    monkeypatch.setattr(sys, "argv", ["benchmark", "--mode", mode, "--frames", "4096", "--rounds", "30"])

    assert framing.main() == 0
    report = json.loads(capsys.readouterr().out)
    assert measured == [expected]
    assert (report["configuration"]["frames"], report["configuration"]["rounds"]) == expected
    assert report["environment"]["event_loop"]["running_backend"] == "test.ActualLoop"


@pytest.mark.parametrize("kind", ["tl", "transport"])
@pytest.mark.parametrize("eligible", [True, False])
def test_numeric_check_failure_is_saved_before_nonzero_outcome(
    kind: str, eligible: bool, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = tmp_path / "report.json"
    if kind == "tl":
        benchmark = tl
        payload_bytes = 65536 if eligible else 64
        monkeypatch.setattr(tl.fast, "native_fast_paths_available", lambda: True)
        monkeypatch.setattr(
            tl, "_benchmark", lambda **kwargs: tl.Result(native_ms=(2.0,), fallback_ms=(1.0 if eligible else 8.0,))
        )
    else:
        benchmark = framing
        payload_bytes = 72 if eligible else 88
        monkeypatch.setattr(framing, "native_transport_available", lambda: True)

        async def measure(*args: Any, **kwargs: Any):
            return (
                framing.Result("tcp_abridged", native_ms=(2.0,), legacy_ms=(1.0 if eligible else 8.0,)),
            ), "test.ActualLoop"

        monkeypatch.setattr(framing, "_benchmark_all", measure)
    monkeypatch.setattr(benchmark, "collect_environment", lambda: {"event_loop": {"running_backend": None}})
    monkeypatch.setattr(
        sys, "argv", ["benchmark", "--check", "--payload-bytes", str(payload_bytes), "--json", str(destination)]
    )

    with pytest.raises(RuntimeError):
        benchmark.main()
    report = json.loads(destination.read_text(encoding="utf-8"))
    assert json.loads(capsys.readouterr().out) == report
    assert report["configuration"]["check"]["enabled"] is True
    assert report["configuration"]["check"]["eligible"] is eligible
    assert report["configuration"]["check"]["target_speedup"] == (1.5 if kind == "tl" else 2.0)
    assert report["failures"][0]["type"] == ("PerformanceThresholdError" if eligible else "BenchmarkConfigurationError")


@pytest.mark.parametrize("corruption", ["encoded_bytes", "decoded_hash", "decoded_payload"])
def test_tl_preflight_rejects_same_length_or_unchecked_field_corruption(
    corruption: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not fast.native_fast_paths_available():
        pytest.skip("native TL fast paths are unavailable")
    encode = fast._native_encode
    decode = fast._native_decode
    assert encode is not None and decode is not None

    def wrong_encode(constructor_id, values, boxed):
        result = encode(constructor_id, values, boxed)
        if result is not None and constructor_id == functions.UploadSaveBigFilePart.CONSTRUCTOR_ID:
            result = bytes(result)
            return result[:4] + bytes([result[4] ^ 1]) + result[5:]
        return result

    def wrong_decode(constructor_id, data, offset, boxed):
        result = decode(constructor_id, data, offset, boxed)
        if result is None:
            return None
        values, cursor = result
        values = list(values)
        if corruption == "decoded_hash" and constructor_id == types.FileHash.CONSTRUCTOR_ID:
            values[-1] = b"x" * len(values[-1])
        if corruption == "decoded_payload" and constructor_id == types.UploadCdnFile.CONSTRUCTOR_ID:
            values[0] = b"x" * len(values[0])
        return values, cursor

    monkeypatch.setattr(fast, "_native_encode", wrong_encode if corruption == "encoded_bytes" else encode)
    monkeypatch.setattr(fast, "_native_decode", wrong_decode)
    with pytest.raises(AssertionError, match="parity"):
        tl._benchmark(iterations=1, payload_bytes=64, rounds=1)


def test_peer_preflight_rejects_wrong_warm_results_before_timing(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime.now(UTC)
    entries = tuple(
        PeerCacheEntry(
            id=index + 1,
            kind="user",
            access_hash=index + 10000,
            username=f"bench_user_{index}",
            phone=f"+1202{index:07d}",
            updated_at=now,
        )
        for index in range(1000)
    )
    original = runtime.PeerCache.resolve_peer

    async def wrong_after_cold(self, query):
        if self.index_stats["rebuilds"] == 0:
            return await original(self, query)
        return Peer(id=987654321, kind="user", access_hash=1)

    durations = iter([1.0] * 4 + [25.0] * 4)

    async def deterministic_timing(*args: Any, **kwargs: Any) -> float:
        return next(durations)

    monkeypatch.setattr(runtime, "_peer_entries_10k", lambda: entries)
    monkeypatch.setattr(runtime.PeerCache, "resolve_peer", wrong_after_cold)
    monkeypatch.setattr(runtime, "_median_lookup_ns", deterministic_timing)
    with pytest.raises(AssertionError, match="peer lookup parity"):
        asyncio.run(runtime._bench_peer_cache_10k())


class OfflineClient:
    def __init__(self, media: Media, *, fail: bool = False, history_fallback: bool = False) -> None:
        self.media = media
        self.fail = fail
        self.history_fallback = history_fallback
        self.targets: list[Path | None] = []
        self.caption = ""
        self.history_calls = 0

    async def send_file(self, peer: str, source: Path, **kwargs: Any) -> SimpleNamespace:
        self.caption = kwargs["caption"]
        return SimpleNamespace(id=19, media=None if self.history_fallback else self.media)

    async def get_history(self, peer: str, *, limit: int) -> list[SimpleNamespace]:
        assert limit == 20
        self.history_calls += 1
        return [SimpleNamespace(id=19, text=self.caption, media=self.media)]

    async def download_media(self, media: Media, target: Path | None, **kwargs: Any) -> MediaDownloadResult:
        self.targets.append(target)
        assert media.file_name == self.media.file_name
        destination = _open_destination(target, resume=False)
        try:
            if self.fail:
                raise RuntimeError("synthetic retrieval failure")
            destination.handle.write(b"data")
        finally:
            destination.handle.close()
        return MediaDownloadResult(
            bytes_downloaded=4, offset=0, destination=target, data=b"data" if target is None else None
        )


def media_with_name(name: str | None) -> Media:
    return Media(id=1, access_hash=2, file_reference=b"synthetic", dc_id=2, size=4, file_name=name)


def run_benchmark(
    client: OfflineClient,
    root: Path,
    *,
    actor: benchmark.Actor = "user",
    operation: benchmark.Operation = "download",
    destination: str = "file",
    file_id: str | None = None,
) -> tuple[benchmark.TransferSummary, ...]:
    return asyncio.run(
        benchmark.benchmark_actor(
            cast(Client, client),
            actor=actor,
            operation=operation,
            repeat_index=1,
            peer="self",
            source=root.parent / "source.bin",
            benchmark_size=4,
            download_dir=root,
            dc_id=2,
            file_id=file_id or encode_file_id(client.media),
            upload_concurrency=1,
            upload_media_lanes=1,
            download_concurrency=1,
            download_media_lanes=1,
            download_adaptive_concurrency=False,
            download_max_in_flight_bytes=None,
            download_adaptive_part_size=False,
            download_max_chunk_size=benchmark.MAX_DOWNLOAD_CHUNK_SIZE,
            download_read_ahead_bytes=0,
            download_range_cache_bytes=0,
            upload_request_timeout=1,
            upload_part_retries=0,
            download_request_timeout=1,
            download_part_retries=0,
            download_flood_sleep_threshold=0,
            download_chunk_size=benchmark.DEFAULT_CHUNK_SIZE,
            verify_digest=False,
            progress_interval_s=0,
            download_destination=destination,
        )
    )


@pytest.mark.parametrize("actor", ["user", "bot"])
@pytest.mark.parametrize("separator", ["/", "\\"])
@pytest.mark.parametrize("prefix_exists", [False, True])
@pytest.mark.parametrize("fail", [False, True])
def test_file_id_name_cannot_delete_or_truncate_outside_file(
    actor: benchmark.Actor, separator: str, prefix_exists: bool, fail: bool, tmp_path: Path
) -> None:
    root = tmp_path / "downloads"
    sentinel = tmp_path / "outside.bin"
    sentinel.write_bytes(b"preserve this existing file")
    prefix = root / f"{actor}-dc2-nested"
    if prefix_exists:
        prefix.mkdir(parents=True)
    name = separator.join(("nested", "..", "..", "outside.bin"))
    client = OfflineClient(media_with_name(name), fail=fail)
    file_id = benchmark.file_id_for_actor(
        argparse.Namespace(file_id="unused shared identifier"),
        {f"MINIPROTO_LIVE_BENCH_{actor.upper()}_FILE_ID": encode_file_id(client.media)},
        actor,
    )

    if fail:
        with pytest.raises(RuntimeError, match="synthetic retrieval failure"):
            run_benchmark(client, root, actor=actor, file_id=file_id)
    else:
        run_benchmark(client, root, actor=actor, file_id=file_id)

    assert sentinel.read_bytes() == b"preserve this existing file"
    target = root / f"{actor}-dc2-nested_.._.._outside.bin"
    assert client.targets == [target]
    assert prefix.exists() is prefix_exists
    if not fail:
        assert target.read_bytes() == b"data"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("/absolute/file.bin", "_absolute_file.bin"),
        (r"C:\temp\file.bin", "C__temp_file.bin"),
        (r"C:file.bin", "C_file.bin"),
        (r"\\server\share\file.bin", "__server_share_file.bin"),
        ("file.bin:stream", "file.bin_stream"),
        ('a<>:"|?*\x00.bin', "a________.bin"),
        ("...", "telegram-file.bin"),
        ("", "telegram-file.bin"),
        ("file.bin...", "file.bin"),
        ("échantillon_42-漢字.bin", "échantillon_42-漢字.bin"),
    ],
)
def test_shared_filename_policy_handles_portable_path_syntax(name: str, expected: str) -> None:
    assert multi_session.safe_file_name(name) == expected
    assert benchmark.safe_file_name(name) == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [("échantillon_42.bin", "échantillon_42.bin"), (None, "source.bin"), ("...", "telegram-file.bin"), ("CON", "CON")],
)
def test_ordinary_and_fallback_names_preserve_file_output(name: str | None, expected: str, tmp_path: Path) -> None:
    root = tmp_path / "downloads"
    root.mkdir()
    target = root / f"user-dc2-{expected}"
    target.write_bytes(b"previous benchmark output")
    client = OfflineClient(media_with_name(name))

    summaries = run_benchmark(client, root)

    assert client.targets == [target]
    assert target.read_bytes() == b"data"
    assert summaries[0].path == str(target)
    assert summaries[0].bytes == 4


def test_memory_destination_never_creates_download_directory(tmp_path: Path) -> None:
    root = tmp_path / "downloads"
    client = OfflineClient(media_with_name("nested/../../outside.bin"))

    summaries = run_benchmark(client, root, destination="memory")

    assert client.targets == [None]
    assert not root.exists()
    assert summaries[0].path is None


@pytest.mark.parametrize("history_fallback", [False, True])
def test_uploaded_and_history_media_use_the_same_confined_destination(history_fallback: bool, tmp_path: Path) -> None:
    root = tmp_path / "downloads"
    (tmp_path / "source.bin").write_bytes(b"data")
    sentinel = tmp_path / "outside.bin"
    sentinel.write_bytes(b"unchanged")
    client = OfflineClient(media_with_name("nested/../../outside.bin"), history_fallback=history_fallback)

    summaries = run_benchmark(client, root, operation="both")

    assert sentinel.read_bytes() == b"unchanged"
    assert client.targets == [root / "user-dc2-nested_.._.._outside.bin"]
    assert client.history_calls == int(history_fallback)
    assert [summary.operation for summary in summaries] == ["upload", "download"]


def test_existing_symlink_escape_is_rejected_before_unlink_or_download(tmp_path: Path) -> None:
    root = tmp_path / "downloads"
    root.mkdir()
    sentinel = tmp_path / "outside.bin"
    sentinel.write_bytes(b"unchanged")
    target = root / "user-dc2-file.bin"
    try:
        target.symlink_to(sentinel)
    except OSError as exc:
        pytest.skip(f"symlinks unavailable: {exc}")
    client = OfflineClient(media_with_name("file.bin"))

    with pytest.raises(ValueError, match="download directory"):
        run_benchmark(client, root)

    assert client.targets == []
    assert target.is_symlink()
    assert sentinel.read_bytes() == b"unchanged"


def test_matrix_file_cell_uses_the_confined_download_boundary(tmp_path: Path) -> None:
    cell = matrix.MatrixCell(1, 4, benchmark.DEFAULT_CHUNK_SIZE, True, "file", False, 1)
    command = matrix.build_live_command(cell, tmp_path / "report.json")
    client = OfflineClient(media_with_name("nested/../../outside.bin"))
    env = {"MINIPROTO_LIVE_BENCH_BOT_FILE_ID": encode_file_id(client.media)}
    args = benchmark.parse_args(command[3:], env)
    root = tmp_path / "downloads"

    run_benchmark(
        client,
        root,
        actor=args.actor,
        operation=args.operation,
        destination=args.download_destination,
        file_id=benchmark.file_id_for_actor(args, env, args.actor),
    )

    target = root / "bot-dc2-nested_.._.._outside.bin"
    assert client.targets == [target]
    assert target.read_bytes() == b"data"

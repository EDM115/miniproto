from __future__ import annotations

import asyncio
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from tools.bench import benchmark_runtime_paths as runtime
from tools.bench import benchmark_tl_fast_paths as tl
from tools.bench import benchmark_transport_framing as framing

from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry
from miniproto.tl import fast
from miniproto.types import Peer


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

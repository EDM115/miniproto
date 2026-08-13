from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from collections.abc import Mapping, Sequence
from typing import Any

CASES: Mapping[str, str] = {
    "import_miniproto": "import miniproto",
    "import_client": "from miniproto import Client, ClientConfig",
    "first_raw_attribute": "from miniproto.raw import types; types.InputPeerSelf",
    "first_decode": "from miniproto.tl import decode_object; decode_object(bytes.fromhex('c97ea07d'))",
}


def summarize(samples: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    raw_modules = sorted({module for sample in samples for module in sample.get("raw_modules", ())})
    return {
        "median_seconds": statistics.median(float(sample["seconds"]) for sample in samples),
        "median_retained_bytes": statistics.median(int(sample.get("retained_bytes", 0)) for sample in samples),
        "median_peak_bytes": statistics.median(int(sample.get("peak_bytes", 0)) for sample in samples),
        "raw_modules": raw_modules,
        "samples": list(samples),
    }


def measure_case(name: str, *, runs: int, tracemalloc_enabled: bool = False) -> list[dict[str, Any]]:
    statement = CASES[name]
    child_code = _child_code(statement, tracemalloc_enabled=tracemalloc_enabled)
    samples: list[dict[str, Any]] = []
    for _run in range(runs):
        result = subprocess.run(  # noqa: S603 - executes the running interpreter with fixed arguments.
            [sys.executable, "-c", child_code], check=True, capture_output=True, text=True
        )
        samples.append(json.loads(result.stdout))
    return samples


def _child_code(statement: str, *, tracemalloc_enabled: bool) -> str:
    trace_start = "import tracemalloc; tracemalloc.start();" if tracemalloc_enabled else ""
    memory_read = (
        "retained_bytes,peak_bytes=tracemalloc.get_traced_memory();"
        if tracemalloc_enabled
        else "retained_bytes=0;peak_bytes=0;"
    )
    return (
        "import json,sys,time;"
        f"{trace_start}"
        "start=time.perf_counter();"
        f"{statement};"
        "seconds=time.perf_counter()-start;"
        f"{memory_read}"
        "print(json.dumps({"
        "'seconds':seconds,"
        "'retained_bytes':retained_bytes,"
        "'peak_bytes':peak_bytes,"
        "'raw_modules':sorted(name for name in sys.modules if name.startswith('miniproto.raw'))"
        "}))"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark fresh-process miniproto import paths.")
    parser.add_argument("--runs", type=int, default=10)
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error("--runs must be at least one")
    results = {
        "runs": args.runs,
        "cases": {name: summarize(measure_case(name, runs=args.runs)) for name in CASES},
        "import_miniproto_tracemalloc": summarize(
            measure_case("import_miniproto", runs=args.runs, tracemalloc_enabled=True)
        ),
    }
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

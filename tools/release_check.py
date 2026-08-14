from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.bench.reporting import collect_environment, write_benchmark_report

StageRunner = Callable[["Stage", dict[str, str]], int]


@dataclass(frozen=True, slots=True)
class ReleaseConfig:
    mode: str
    keep_going: bool
    artifacts_dir: Path


@dataclass(frozen=True, slots=True)
class Stage:
    name: str
    command: tuple[str, ...] | None
    pending_reason: str | None = None


def parse_args(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> argparse.Namespace:
    """Parse release-check modes without accepting credentials on the command line."""
    values = os.environ if env is None else env
    parser = argparse.ArgumentParser(description="Run the canonical non-mutating miniproto release checks")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--quick", dest="mode", action="store_const", const="quick")
    modes.add_argument("--offline", dest="mode", action="store_const", const="offline")
    modes.add_argument("--live", dest="mode", action="store_const", const="live")
    parser.set_defaults(mode="offline")
    parser.add_argument("--keep-going", action="store_true")
    parser.add_argument(
        "--artifacts-dir", type=Path, default=Path(values.get("MINIPROTO_RELEASE_ARTIFACTS", ".tmp/release-check"))
    )
    return parser.parse_args(argv)


def build_stages(config: ReleaseConfig, *, repo: Path) -> tuple[Stage, ...]:
    """Construct the ordered check-only stage list for the requested mode."""
    python = sys.executable
    artifacts = config.artifacts_dir
    docs_present = (repo / "tools" / "docs" / "__main__.py").is_file() and (repo / "docs-site").is_dir()
    stages: list[Stage] = [
        Stage("environment", ("__internal__", "environment")),
        Stage("schema", (python, "-m", "tools.schema.generate", "--check")),
        Stage("ruff-format", (python, "-m", "ruff", "format", "--check", ".")),
        Stage("ruff-lint", (python, "-m", "ruff", "check", ".")),
        Stage("typecheck", (python, "-m", "ty", "check")),
        Stage(
            "docs",
            (python, "-m", "tools.docs", "--check", "--build") if docs_present else None,
            pending_reason=None if docs_present else "Wave 5 documentation tooling is not present",
        ),
    ]
    if config.mode == "quick":
        stages.extend(
            [
                Stage(
                    "pytest",
                    (
                        python,
                        "-m",
                        "pytest",
                        "tests/test_schema_generation.py",
                        "tests/test_native.py",
                        "tests/test_transport_runtime.py",
                        f"--basetemp={artifacts / 'pytest-tmp'}",
                    ),
                ),
                Stage("cargo-fmt", ("cargo", "fmt", "--check")),
                Stage("cargo-test", ("cargo", "test", "--workspace", "--all-features")),
            ]
        )
        return tuple(stages)
    stages.extend(
        [
            Stage("pytest", (python, "-m", "pytest", f"--basetemp={artifacts / 'pytest-tmp'}")),
            Stage("cargo-fmt", ("cargo", "fmt", "--check")),
            Stage(
                "cargo-clippy",
                ("cargo", "clippy", "--workspace", "--all-targets", "--all-features", "--", "-D", "warnings"),
            ),
            Stage("cargo-test", ("cargo", "test", "--workspace", "--all-features")),
            Stage("benchmark-imports", (python, "-m", "tools.bench.benchmark_imports", "--runs", "3")),
            Stage(
                "benchmark-smoke",
                (
                    python,
                    "-m",
                    "tools.bench.benchmark_acceptance",
                    "--mode",
                    "smoke",
                    "--json",
                    str(artifacts / "benchmarks" / "runtime-acceptance.json"),
                ),
            ),
            Stage("benchmark-media-scheduler", (python, "-m", "tools.bench.benchmark_media_scheduler")),
            Stage(
                "benchmark-native-fallback",
                (
                    python,
                    "-m",
                    "tools.bench.benchmark_native_fallback_crypto",
                    "--mode",
                    "smoke",
                    "--json",
                    str(artifacts / "benchmarks" / "native-fallback.json"),
                ),
            ),
            Stage("benchmark-runtime-paths", (python, "-m", "tools.bench.benchmark_runtime_paths")),
            Stage(
                "benchmark-frame-pump",
                (
                    python,
                    "-m",
                    "tools.bench.benchmark_transport_framing",
                    "--frames",
                    "1024",
                    "--rounds",
                    "3",
                    "--mode",
                    "smoke",
                    "--check",
                    "--json",
                    str(artifacts / "benchmarks" / "transport-framing.json"),
                ),
            ),
            Stage(
                "benchmark-hot-tl",
                (
                    python,
                    "-m",
                    "tools.bench.benchmark_tl_fast_paths",
                    "--iterations",
                    "8",
                    "--payload-bytes",
                    "65536",
                    "--rounds",
                    "3",
                    "--mode",
                    "smoke",
                    "--check",
                    "--json",
                    str(artifacts / "benchmarks" / "tl-fast-paths.json"),
                ),
            ),
            Stage("profile-lazy-raw-codec", (python, "-m", "tools.bench.profile_lazy_raw_codec")),
            Stage(
                "wheel-sdist",
                (python, "-m", "maturin", "build", "--release", "--sdist", "--out", str(artifacts / "distributions")),
            ),
            Stage("artifact-inspection", ("__internal__", "artifact-inspection")),
            Stage("clean-import", ("__internal__", "clean-import")),
        ]
    )
    if config.mode == "live":
        stages.extend(
            [
                Stage("live-integration", (python, "-m", "pytest", "tests/integration", "-m", "integration")),
                Stage(
                    "live-benchmark-matrix",
                    (
                        python,
                        "-m",
                        "tools.bench.benchmark_matrix",
                        "--mode",
                        "smoke",
                        "--output",
                        str(artifacts / "live-matrix"),
                    ),
                ),
            ]
        )
    return tuple(stages)


def build_release_environment(
    mode: str,
    base_environment: Mapping[str, str],
    *,
    platform_name: str = os.name,
    python_base_prefix: Path = Path(sys.base_prefix),
) -> dict[str, str]:
    """Build the hermetic stage environment, including the Windows Python DLL search path."""
    environment = dict(base_environment)
    environment["MINIPROTO_INTEGRATION"] = "1" if mode == "live" else "0"
    environment["MINIPROTO_REAL_INTEGRATION"] = "1" if mode == "live" else "0"
    if platform_name == "nt":
        separator = ";"
        existing_path = environment.get("PATH", "")
        python_path = str(python_base_prefix)
        environment["PATH"] = separator.join(part for part in (python_path, existing_path) if part)
    return environment


def run_stages(stages: Sequence[Stage], config: ReleaseConfig, *, runner: StageRunner) -> dict[str, Any]:
    """Execute ordered stages, fail fast by default, and preserve the first failing exit code."""
    environment = build_release_environment(config.mode, os.environ)
    results: list[dict[str, Any]] = []
    first_failure = 0
    for stage in stages:
        if stage.command is None:
            results.append(
                {"name": stage.name, "status": "pending", "duration_seconds": 0.0, "reason": stage.pending_reason}
            )
            continue
        started = time.perf_counter()
        exit_code = runner(stage, environment)
        duration = time.perf_counter() - started
        status = "passed" if exit_code == 0 else "failed"
        result: dict[str, Any] = {
            "name": stage.name,
            "status": status,
            "duration_seconds": duration,
            "exit_code": exit_code,
        }
        results.append(result)
        if exit_code and first_failure == 0:
            first_failure = exit_code
            if not config.keep_going:
                break
    return {"schema": "miniproto.release-check.v1", "mode": config.mode, "exit_code": first_failure, "stages": results}


def inspect_wheel(path: Path) -> dict[str, Any]:
    """Reject editable/path-only wheel artifacts and require bundled Python plus native code."""
    with zipfile.ZipFile(path) as archive:
        names = sorted(archive.namelist())
        entry_point_files = [name for name in names if name.endswith(".dist-info/entry_points.txt")]
        console_scripts: dict[str, str] = {}
        for entry_point_file in entry_point_files:
            parser = configparser.ConfigParser(interpolation=None)
            parser.read_string(archive.read(entry_point_file).decode("utf-8"))
            if parser.has_section("console_scripts"):
                console_scripts.update(parser.items("console_scripts"))
    python_sources = any(name.startswith("miniproto/") and name.endswith(".py") for name in names)
    native_extension = any(
        name.startswith("miniproto/_native") and name.casefold().endswith((".pyd", ".so", ".dylib")) for name in names
    )
    pth_files = [name for name in names if name.casefold().endswith(".pth")]
    cache_files = [
        name for name in names if "__pycache__/" in name.casefold() or name.casefold().endswith((".pyc", ".pyo"))
    ]
    failures: list[str] = []
    if not python_sources:
        failures.append("Python sources are missing")
    if not native_extension:
        failures.append("native extension is missing")
    if pth_files:
        failures.append("pth files are forbidden")
    if cache_files:
        failures.append("cache files are forbidden")
    if not console_scripts:
        failures.append("console scripts are missing")
    for script, target in sorted(console_scripts.items()):
        module = target.split(":", 1)[0].strip()
        module_path = module.replace(".", "/")
        if f"{module_path}.py" not in names and f"{module_path}/__init__.py" not in names:
            failures.append(f"console script target {script} -> {module} is missing")
    if failures:
        raise ValueError(f"invalid wheel {path.name}: {'; '.join(failures)}")
    return {
        "path": str(path),
        "sha256": _sha256(path),
        "size": path.stat().st_size,
        "python_sources": python_sources,
        "native_extension": native_extension,
        "pth_files": pth_files,
        "cache_files": cache_files,
        "console_scripts": sorted(console_scripts),
    }


def inspect_artifacts(directory: Path) -> dict[str, Any]:
    """Inspect every built wheel and sdist and record stable hashes."""
    wheels = sorted(directory.glob("*.whl"))
    sdists = sorted(directory.glob("*.tar.gz"))
    if not wheels:
        raise ValueError("release build produced no wheel")
    if not sdists:
        raise ValueError("release build produced no sdist")
    return {
        "wheels": [inspect_wheel(wheel) for wheel in wheels],
        "sdists": [{"path": str(path), "sha256": _sha256(path), "size": path.stat().st_size} for path in sdists],
    }


def default_runner(config: ReleaseConfig, *, repo: Path) -> StageRunner:
    """Create the streaming subprocess/internal-stage runner for one release-check invocation."""

    def run(stage: Stage, env: dict[str, str]) -> int:
        assert stage.command is not None
        if stage.command[0] != "__internal__":
            return subprocess.run(  # noqa: S603 - stages come from the fixed release-check registry
                stage.command, cwd=repo, env=env, check=False
            ).returncode
        try:
            if stage.command[1] == "environment":
                _write_environment(config.artifacts_dir)
            elif stage.command[1] == "artifact-inspection":
                manifest = inspect_artifacts(config.artifacts_dir / "distributions")
                write_benchmark_report(config.artifacts_dir / "artifact-manifest.json", manifest)
            elif stage.command[1] == "clean-import":
                _clean_import(config.artifacts_dir, repo=repo, env=env)
            else:
                raise ValueError(f"unknown internal release stage: {stage.command[1]}")
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            print(f"{stage.name}: {exc}", file=sys.stderr)
            return 1
        return 0

    return run


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    config = ReleaseConfig(args.mode, args.keep_going, args.artifacts_dir.resolve())
    if config.mode == "live" and os.environ.get("MINIPROTO_RELEASE_LIVE") != "1":
        print("Refusing live release checks without MINIPROTO_RELEASE_LIVE=1", file=sys.stderr)
        return 2
    repo = Path.cwd().resolve()
    config.artifacts_dir.mkdir(parents=True, exist_ok=True)
    stages = build_stages(config, repo=repo)
    report = run_stages(stages, config, runner=default_runner(config, repo=repo))
    report["environment"] = collect_environment()
    report["artifacts_dir"] = str(config.artifacts_dir)
    write_benchmark_report(config.artifacts_dir / "release-check.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return int(report["exit_code"])


def _write_environment(artifacts_dir: Path) -> None:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    tools = collect_environment()
    tools["uv"] = _version(("uv", "--version"))
    tools["ruff"] = _version((sys.executable, "-m", "ruff", "--version"))
    tools["ty"] = _version((sys.executable, "-m", "ty", "--version"))
    tools["maturin"] = _version((sys.executable, "-m", "maturin", "--version"))
    tools["cargo"] = _version(("cargo", "--version"))
    write_benchmark_report(artifacts_dir / "environment.json", tools)


def _clean_import(artifacts_dir: Path, *, repo: Path, env: Mapping[str, str]) -> None:
    distributions = artifacts_dir / "distributions"
    wheels = sorted(distributions.glob("*.whl"))
    if not wheels:
        raise ValueError("clean import has no wheel to install")
    environment_dir = artifacts_dir / "clean-env"
    uv = shutil.which("uv")
    if uv is None:
        raise ValueError("uv is unavailable for clean-environment verification")
    subprocess.run(  # noqa: S603 - executable and paths are locally resolved release artifacts
        (uv, "venv", "--clear", "--python", sys.executable, str(environment_dir)), cwd=repo, env=env, check=True
    )
    python = environment_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(  # noqa: S603 - executable and wheel are locally resolved release artifacts
        (uv, "pip", "install", "--python", str(python), str(wheels[0])), cwd=repo, env=env, check=True
    )
    smoke = (
        "import miniproto, miniproto._native; assert miniproto.__file__; assert miniproto._native.native_available()"
    )
    subprocess.run(  # noqa: S603 - interpreter is from the task-owned clean environment
        (str(python), "-I", "-c", smoke), cwd=artifacts_dir, env=env, check=True
    )


def _version(command: tuple[str, ...]) -> str | None:
    try:
        completed = subprocess.run(  # noqa: S603 - callers pass fixed tool-version commands only
            command, check=False, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (completed.stdout or completed.stderr).strip()
    return output if completed.returncode == 0 and output else None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

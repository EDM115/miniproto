from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from tools.release_check import (
    ReleaseConfig,
    Stage,
    build_release_environment,
    build_stages,
    inspect_wheel,
    parse_args,
    run_stages,
)


def test_release_check_defaults_to_offline_and_cli_overrides_artifact_environment() -> None:
    args = parse_args([], {"MINIPROTO_RELEASE_ARTIFACTS": ".tmp/from-env"})
    explicit = parse_args(["--quick", "--artifacts-dir", ".tmp/explicit"], {})

    assert args.mode == "offline"
    assert args.artifacts_dir.as_posix() == ".tmp/from-env"
    assert explicit.mode == "quick"
    assert explicit.artifacts_dir.as_posix() == ".tmp/explicit"


def test_offline_stage_order_uses_check_only_commands_and_marks_future_docs_pending(tmp_path: Path) -> None:
    config = ReleaseConfig(mode="offline", keep_going=False, artifacts_dir=tmp_path / "artifacts")
    stages = build_stages(config, repo=tmp_path)

    assert [stage.name for stage in stages] == [
        "environment",
        "schema",
        "ruff-format",
        "ruff-lint",
        "typecheck",
        "docs",
        "pytest",
        "cargo-fmt",
        "cargo-clippy",
        "cargo-test",
        "benchmark-imports",
        "benchmark-smoke",
        "benchmark-media-scheduler",
        "benchmark-native-fallback",
        "benchmark-runtime-paths",
        "benchmark-frame-pump",
        "benchmark-hot-tl",
        "profile-lazy-raw-codec",
        "wheel-sdist",
        "artifact-inspection",
        "clean-import",
    ]
    commands = {stage.name: stage.command for stage in stages}
    schema = commands["schema"]
    ruff_format = commands["ruff-format"]
    ruff_lint = commands["ruff-lint"]
    cargo_fmt = commands["cargo-fmt"]
    cargo_clippy = commands["cargo-clippy"]
    assert schema is not None and schema[-1] == "--check"
    assert ruff_format is not None and ruff_format[-2:] == ("--check", ".")
    assert ruff_lint is not None and "--fix" not in ruff_lint
    assert cargo_fmt is not None and cargo_fmt[-1] == "--check"
    assert cargo_clippy is not None and cargo_clippy[-2:] == ("-D", "warnings")
    assert (
        next(stage for stage in stages if stage.name == "docs").pending_reason
        == "Wave 5 documentation tooling is not present"
    )


def test_quick_mode_is_bounded_and_excludes_artifact_builds(tmp_path: Path) -> None:
    stages = build_stages(ReleaseConfig(mode="quick", keep_going=False, artifacts_dir=tmp_path), repo=tmp_path)

    names = {stage.name for stage in stages}
    assert "pytest" in names
    assert "cargo-test" in names
    assert "benchmark-smoke" not in names
    assert "wheel-sdist" not in names
    assert "clean-import" not in names


def test_windows_release_environment_prepends_uv_base_python_for_pyo3_dll_resolution() -> None:
    environment = build_release_environment(
        "offline",
        {"PATH": "C:/Windows/System32", "MINIPROTO_INTEGRATION": "1"},
        platform_name="nt",
        python_base_prefix=Path("C:/uv/python/cpython-3.14"),
    )

    assert Path(environment["PATH"].split(";")[0]) == Path("C:/uv/python/cpython-3.14")
    assert environment["MINIPROTO_INTEGRATION"] == "0"
    assert environment["MINIPROTO_REAL_INTEGRATION"] == "0"


def test_fail_fast_preserves_exit_code_and_keep_going_collects_later_failures(tmp_path: Path) -> None:
    stages = (Stage("first", ("first",)), Stage("second", ("second",)), Stage("third", ("third",)))
    calls: list[str] = []

    def runner(stage: Stage, env: dict[str, str]) -> int:
        del env
        calls.append(stage.name)
        return {"first": 0, "second": 7, "third": 9}[stage.name]

    fail_fast = run_stages(stages, ReleaseConfig("offline", False, tmp_path), runner=runner)
    assert calls == ["first", "second"]
    assert fail_fast["exit_code"] == 7
    assert [result["status"] for result in fail_fast["stages"]] == ["passed", "failed"]

    calls.clear()
    complete = run_stages(stages, ReleaseConfig("offline", True, tmp_path), runner=runner)
    assert calls == ["first", "second", "third"]
    assert complete["exit_code"] == 7
    assert [result["status"] for result in complete["stages"]] == ["passed", "failed", "failed"]


def test_pending_stage_is_reported_without_invoking_runner(tmp_path: Path) -> None:
    stage = Stage("docs", None, pending_reason="Wave 5 documentation tooling is not present")

    report = run_stages((stage,), ReleaseConfig("offline", False, tmp_path), runner=lambda *_: 99)

    assert report["exit_code"] == 0
    assert report["stages"] == [
        {
            "name": "docs",
            "status": "pending",
            "duration_seconds": 0.0,
            "reason": "Wave 5 documentation tooling is not present",
        }
    ]


def test_wheel_inspection_requires_python_sources_and_native_extension_without_pth(tmp_path: Path) -> None:
    good = tmp_path / "good.whl"
    with zipfile.ZipFile(good, "w") as archive:
        archive.writestr("miniproto/__init__.py", "")
        archive.writestr("miniproto/_native.cp314-win_amd64.pyd", b"native")
        archive.writestr("miniproto-0.1.0.dist-info/METADATA", "Name: miniproto\n")
        archive.writestr(
            "miniproto-0.1.0.dist-info/entry_points.txt",
            "[console_scripts]\nminiproto-release-check = tools.release_check:main\n",
        )
        archive.writestr("tools/release_check.py", "def main(): return 0\n")

    result = inspect_wheel(good)

    assert result["python_sources"] is True
    assert result["native_extension"] is True
    assert result["pth_files"] == []
    assert result["console_scripts"] == ["miniproto-release-check"]

    bad = tmp_path / "bad.whl"
    with zipfile.ZipFile(bad, "w") as archive:
        archive.writestr("miniproto.pth", "C:/checkout/src")
        archive.writestr("miniproto-0.1.0.dist-info/METADATA", "Name: miniproto\n")
    with pytest.raises(ValueError, match=r"Python sources|native extension|pth"):
        inspect_wheel(bad)

    missing_cli = tmp_path / "missing-cli.whl"
    with zipfile.ZipFile(missing_cli, "w") as archive:
        archive.writestr("miniproto/__init__.py", "")
        archive.writestr("miniproto/_native.cp314-win_amd64.pyd", b"native")
        archive.writestr(
            "miniproto-0.1.0.dist-info/entry_points.txt",
            "[console_scripts]\nminiproto-release-check = tools.release_check:main\n",
        )
    with pytest.raises(ValueError, match="console script target"):
        inspect_wheel(missing_cli)

    cached = tmp_path / "cached.whl"
    with zipfile.ZipFile(cached, "w") as archive:
        archive.writestr("miniproto/__init__.py", "")
        archive.writestr("miniproto/_native.cp314-win_amd64.pyd", b"native")
        archive.writestr("miniproto-0.1.0.dist-info/METADATA", "Name: miniproto\n")
        archive.writestr(
            "miniproto-0.1.0.dist-info/entry_points.txt",
            "[console_scripts]\nminiproto-release-check = tools.release_check:main\n",
        )
        archive.writestr("tools/release_check.py", "def main(): return 0\n")
        archive.writestr("tools/__pycache__/release_check.cpython-314.pyc", b"cached")
    with pytest.raises(ValueError, match="cache files"):
        inspect_wheel(cached)


def test_release_summary_is_machine_readable(tmp_path: Path) -> None:
    report = run_stages((Stage("ok", ("ok",)),), ReleaseConfig("quick", False, tmp_path), runner=lambda *_: 0)

    assert json.loads(json.dumps(report))["mode"] == "quick"

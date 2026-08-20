from __future__ import annotations

import io
import json
import tarfile
import zipfile
from pathlib import Path

import pytest
import tools.release_check as release_check
from tools.release_check import (
    ReleaseConfig,
    Stage,
    build_release_environment,
    build_stages,
    inspect_artifacts,
    inspect_wheel,
    parse_args,
    run_stages,
)


def _release_metadata() -> str:
    return """Metadata-Version: 2.4
Name: miniproto
Version: 0.1.0
Summary: Async-first MTProto client core for Python with bundled Rust acceleration
Keywords: telegram,mtproto,asyncio,pyo3,rust
Author-email: EDM115 <miniproto@edm115.dev>
License-Expression: MIT
License-File: LICENSE
Requires-Python: >=3.13
Description-Content-Type: text/markdown
Classifier: Development Status :: 3 - Alpha
Classifier: Framework :: AsyncIO
Classifier: Intended Audience :: Developers
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Programming Language :: Python :: 3.13
Classifier: Programming Language :: Python :: 3.14
Classifier: Programming Language :: Rust
Classifier: Typing :: Typed
Project-URL: Homepage, https://miniproto.edm115.dev/
Project-URL: Documentation, https://miniproto.edm115.dev/
Project-URL: Source, https://github.com/EDM115/miniproto
Project-URL: Changelog, https://github.com/EDM115/miniproto/blob/master/CHANGELOG.md
Project-URL: Issues, https://github.com/EDM115/miniproto/issues
Project-URL: Funding, https://github.com/EDM115#support-me-
Project-URL: Security, https://github.com/EDM115/miniproto/security/policy
Requires-Dist: cryptography==50.0.0
Requires-Dist: uvloop==0.22.1; sys_platform == 'linux' or sys_platform == 'darwin'
Requires-Dist: winloop==0.6.3; sys_platform == 'win32'
Requires-Dist: maturin==1.14.1; extra == 'dev'
Requires-Dist: griffe==2.2.0; extra == 'docs'
Provides-Extra: dev
Provides-Extra: docs

miniproto
"""


def _write_release_wheel(
    path: Path, *, include_script_target: bool = True, extra_files: dict[str, str | bytes] | None = None
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("miniproto/__init__.py", "")
        archive.writestr("miniproto/py.typed", "")
        archive.writestr("miniproto/_native.cp314-win_amd64.pyd", b"native")
        archive.writestr("miniproto/raw/functions.py", "")
        archive.writestr("miniproto/raw/functions.pyi", "")
        archive.writestr("miniproto/raw/types.py", "")
        archive.writestr("miniproto/raw/types.pyi", "")
        archive.writestr("miniproto/raw/_function_shards/bucket_00.py", "")
        archive.writestr("miniproto/raw/_types_shards/bucket_00.py", "")
        archive.writestr("miniproto-0.1.0.dist-info/METADATA", _release_metadata())
        archive.writestr("miniproto-0.1.0.dist-info/licenses/LICENSE", "MIT License\n")
        archive.writestr(
            "miniproto-0.1.0.dist-info/entry_points.txt",
            "[console_scripts]\nminiproto-release-check = tools.release_check:main\n",
        )
        if include_script_target:
            archive.writestr("tools/release_check.py", "def main(): return 0\n")
        for name, payload in (extra_files or {}).items():
            archive.writestr(name, payload)


def _write_release_sdist(path: Path, *, extra_files: dict[str, str | bytes] | None = None) -> None:
    files: dict[str, str | bytes] = dict.fromkeys(release_check._REQUIRED_SDIST_PAYLOAD, "")
    files["PKG-INFO"] = _release_metadata()
    files["src/miniproto/raw/_function_shards/bucket_00.py"] = ""
    files["src/miniproto/raw/_types_shards/bucket_00.py"] = ""
    files.update(extra_files or {})
    with tarfile.open(path, "w:gz") as archive:
        for name, value in files.items():
            payload = value.encode() if isinstance(value, str) else value
            member = tarfile.TarInfo(f"miniproto-0.1.0/{name}")
            member.size = len(payload)
            archive.addfile(member, io.BytesIO(payload))


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
        "benchmark-session-crypto",
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


def test_release_stage_runner_prints_live_progress_for_running_pending_and_failed_stages(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The multi-minute release CLI must expose stage progress before its final JSON report."""
    stages = (
        Stage("first", ("first",)),
        Stage("docs", None, pending_reason="not configured"),
        Stage("last", ("last",)),
    )

    run_stages(
        stages,
        ReleaseConfig("offline", True, tmp_path),
        runner=lambda stage, _environment: 0 if stage.name == "first" else 7,
    )

    output = capsys.readouterr().out
    assert "[release-check 1/3] first: running" in output
    assert "[release-check 1/3] first: passed in" in output
    assert "[release-check 2/3] docs: pending - not configured" in output
    assert "[release-check 3/3] last: running" in output
    assert "[release-check 3/3] last: failed with exit code 7 in" in output


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
    _write_release_wheel(good)

    result = inspect_wheel(good)

    assert result["python_sources"] is True
    assert result["native_extension"] is True
    assert result["pth_files"] == []
    assert result["console_scripts"] == ["miniproto-release-check"]
    assert result["metadata"]["runtime_dependencies"] == ["cryptography", "uvloop", "winloop"]

    bad = tmp_path / "bad.whl"
    _write_release_wheel(bad, extra_files={"miniproto.pth": "C:/checkout/src"})
    with pytest.raises(ValueError, match="pth"):
        inspect_wheel(bad)

    missing_cli = tmp_path / "missing-cli.whl"
    _write_release_wheel(missing_cli, include_script_target=False)
    with pytest.raises(ValueError, match="console script target"):
        inspect_wheel(missing_cli)

    cached = tmp_path / "cached.whl"
    _write_release_wheel(cached, extra_files={"tools/__pycache__/release_check.cpython-314.pyc": b"cached"})
    with pytest.raises(ValueError, match="cache files"):
        inspect_wheel(cached)


def test_wheel_inspection_rejects_incomplete_release_metadata_and_public_payload(tmp_path: Path) -> None:
    incomplete = tmp_path / "miniproto-0.1.0-cp314-cp314-win_amd64.whl"
    with zipfile.ZipFile(incomplete, "w") as archive:
        archive.writestr("miniproto/__init__.py", "")
        archive.writestr("miniproto/_native.cp314-win_amd64.pyd", b"native")
        archive.writestr(
            "miniproto-0.1.0.dist-info/METADATA", "Metadata-Version: 2.4\nName: miniproto\nVersion: 0.1.0\n"
        )
        archive.writestr(
            "miniproto-0.1.0.dist-info/entry_points.txt",
            "[console_scripts]\nminiproto-release-check = tools.release_check:main\n",
        )
        archive.writestr("tools/release_check.py", "def main(): return 0\n")

    with pytest.raises(ValueError, match=r"release metadata|public package payload"):
        inspect_wheel(incomplete)


def test_artifact_inspection_rejects_sdist_without_required_source_build_inputs(tmp_path: Path) -> None:
    wheel = tmp_path / "miniproto-0.1.0-cp314-cp314-win_amd64.whl"
    _write_release_wheel(wheel)
    sdist = tmp_path / "miniproto-0.1.0.tar.gz"
    with tarfile.open(sdist, "w:gz") as archive:
        payload = _release_metadata().encode()
        member = tarfile.TarInfo("miniproto-0.1.0/PKG-INFO")
        member.size = len(payload)
        archive.addfile(member, io.BytesIO(payload))

    with pytest.raises(ValueError, match=r"source distribution.*required source/build inputs"):
        inspect_artifacts(tmp_path)


def test_artifact_inspection_rejects_forbidden_sdist_residue(tmp_path: Path) -> None:
    wheel = tmp_path / "miniproto-0.1.0-cp314-cp314-win_amd64.whl"
    _write_release_wheel(wheel)
    _write_release_sdist(tmp_path / "miniproto-0.1.0.tar.gz", extra_files={".env": "EXAMPLE=value"})

    with pytest.raises(ValueError, match="forbidden temporary/cache paths"):
        inspect_artifacts(tmp_path)


def test_clean_import_verifies_wheel_and_sdist_in_separate_environments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artifacts = tmp_path / "artifacts"
    distributions = artifacts / "distributions"
    distributions.mkdir(parents=True)
    wheel = distributions / "miniproto-0.1.0-cp314-cp314-win_amd64.whl"
    sdist = distributions / "miniproto-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()
    calls: list[tuple[str, ...]] = []

    monkeypatch.setattr(release_check.shutil, "which", lambda _name: "uv")

    def record(command: tuple[str, ...], **_kwargs: object) -> None:
        calls.append(tuple(str(part) for part in command))

    monkeypatch.setattr(release_check.subprocess, "run", record)

    release_check._clean_import(artifacts, env={})

    venv_commands = [command for command in calls if command[:2] == ("uv", "venv")]
    install_commands = [command for command in calls if command[:3] == ("uv", "pip", "install")]
    smoke_commands = [command for command in calls if "-I" in command]
    assert len(venv_commands) == 2
    assert len({command[-1] for command in venv_commands}) == 2
    assert {Path(command[-1]).name for command in install_commands} == {wheel.name, sdist.name}
    assert len(smoke_commands) == 2


def test_release_summary_is_machine_readable(tmp_path: Path) -> None:
    report = run_stages((Stage("ok", ("ok",)),), ReleaseConfig("quick", False, tmp_path), runner=lambda *_: 0)

    assert json.loads(json.dumps(report))["mode"] == "quick"

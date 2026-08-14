from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import yaml
from packaging.requirements import Requirement

ROOT = Path(__file__).parents[1]


class GitHubWorkflowLoader(yaml.SafeLoader):
    pass


for resolvers in GitHubWorkflowLoader.yaml_implicit_resolvers.values():
    resolvers[:] = [resolver for resolver in resolvers if resolver[0] != "tag:yaml.org,2002:bool"]


def load_workflow(name: str) -> dict[str, Any]:
    path = ROOT / ".github" / "workflows" / name
    assert path.is_file(), f"missing workflow: {path}"
    value = yaml.load(
        path.read_text(encoding="utf-8"),
        Loader=GitHubWorkflowLoader,  # noqa: S506 - SafeLoader subclass; only YAML boolean resolution changes.
    )
    assert isinstance(value, dict)
    return value


def test_ci_workflow_covers_python_rust_benchmarks_and_free_threaded_runtime_without_building_wheels() -> None:
    workflow = load_workflow("ci.yml")
    jobs = workflow["jobs"]

    assert set(jobs["python"]["strategy"]["matrix"]["python-version"]) == {"3.13", "3.14", "3.14t"}
    assert set(jobs["free-threaded"]["strategy"]["matrix"]["python-version"]) == {"3.14t"}
    assert jobs["rust"]["steps"][1]["with"]["toolchain"] == "1.97"
    benchmark_steps = jobs["benchmark-smoke"]["steps"]
    assert any(
        step.get("uses", "").startswith("actions/upload-artifact@") and step.get("if") == "always()"
        for step in benchmark_steps
    )
    assert "wheels" not in jobs
    assert "sdist" in jobs

    free_threaded_steps = "\n".join(str(step.get("run", "")) for step in jobs["free-threaded"]["steps"])
    assert 'find_spec("cryptography") is not None' in free_threaded_steps
    assert 'find_spec("uvloop") is not None' in free_threaded_steps


def test_benchmark_smoke_runs_on_every_native_platform_with_regular_and_free_threaded_python() -> None:
    workflow = load_workflow("ci.yml")
    job = workflow["jobs"]["benchmark-smoke"]
    matrix = job["strategy"]["matrix"]

    assert job["runs-on"] == "${{ matrix.platform.runner }}"
    assert {item["python-version"] for item in matrix["python"]} == {"3.14", "3.14t"}
    assert {
        (item["platform"], item["arch"], item["runner"], item["python-architecture"]) for item in matrix["platform"]
    } == {
        ("linux", "x86_64", "ubuntu-24.04", "x64"),
        ("linux", "aarch64", "ubuntu-24.04-arm", "arm64"),
        ("windows", "x86_64", "windows-latest", "x64"),
        ("windows", "aarch64", "windows-11-arm", "arm64"),
        ("macos", "x86_64", "macos-15-intel", "x64"),
        ("macos", "aarch64", "macos-15", "arm64"),
    }
    assert len(matrix["python"]) * len(matrix["platform"]) == 12

    setup_python = next(step for step in job["steps"] if step.get("uses", "").startswith("actions/setup-python@"))
    assert setup_python["with"] == {
        "python-version": "${{ matrix.python.python-version }}",
        "architecture": "${{ matrix.platform.python-architecture }}",
    }
    setup_uv = next(step for step in job["steps"] if step.get("uses", "").startswith("astral-sh/setup-uv@"))
    assert "python-version" not in setup_uv["with"]
    build_step = next(step for step in job["steps"] if step.get("name") == "Sync and build native extension")
    build_commands = [line.strip() for line in build_step["run"].splitlines() if line.strip()]
    assert "uv sync --python python --extra dev --frozen --no-install-project" in build_commands
    assert "uv run --no-sync maturin develop --release --locked" in build_commands

    serialized_steps = "\n".join(str(step) for step in job["steps"])
    assert "Py_GIL_DISABLED" in serialized_steps
    assert "_is_gil_enabled" in serialized_steps
    assert "native_available" in serialized_steps
    assert "environment.json" in serialized_steps
    assert "PYTHON_GIL" not in serialized_steps
    assert "uv run --no-sync maturin develop --release --locked" in serialized_steps
    assert (
        "benchmark-smoke-${{ matrix.platform.platform }}-${{ matrix.platform.arch }}-${{ matrix.python.artifact }}"
        in serialized_steps
    )


def test_manual_wheel_workflow_is_dispatch_only_and_covers_all_required_abis() -> None:
    workflow = load_workflow("build-wheels.yml")

    assert set(workflow["on"]) == {"workflow_dispatch"}
    jobs = workflow["jobs"]
    assert set(jobs) == {"linux-wheels", "native-wheels"}

    linux_matrix = jobs["linux-wheels"]["strategy"]["matrix"]
    assert {item["python-version"] for item in linux_matrix["python"]} == {"3.13", "3.14", "3.14t"}
    assert {(item["libc"], item["arch"], item["target"]) for item in linux_matrix["platform"]} == {
        ("glibc", "x86_64", "x86_64-unknown-linux-gnu"),
        ("glibc", "aarch64", "aarch64-unknown-linux-gnu"),
        ("musl", "x86_64", "x86_64-unknown-linux-musl"),
        ("musl", "aarch64", "aarch64-unknown-linux-musl"),
    }
    assert len(linux_matrix["python"]) * len(linux_matrix["platform"]) == 12

    native_matrix = jobs["native-wheels"]["strategy"]["matrix"]
    assert {item["python-version"] for item in native_matrix["python"]} == {"3.13", "3.14", "3.14t"}
    assert {(item["platform"], item["arch"], item["target"]) for item in native_matrix["platform"]} == {
        ("windows", "x86_64", "x86_64-pc-windows-msvc"),
        ("windows", "aarch64", "aarch64-pc-windows-msvc"),
        ("macos", "x86_64", "x86_64-apple-darwin"),
        ("macos", "aarch64", "aarch64-apple-darwin"),
    }
    assert len(native_matrix["python"]) * len(native_matrix["platform"]) == 12
    assert (
        sum(
            len(job["strategy"]["matrix"]["python"]) * len(job["strategy"]["matrix"]["platform"])
            for job in jobs.values()
        )
        == 24
    )


def test_windows_arm64_omits_unsupported_cryptography_dependency_and_requires_the_bundled_native_backend() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    cryptography = Requirement(
        next(item for item in project["project"]["dependencies"] if item.startswith("cryptography"))
    )
    assert cryptography.specifier == Requirement("cryptography==50.0.0").specifier
    assert cryptography.marker is not None

    windows_arm64 = {"sys_platform": "win32", "platform_machine": "ARM64"}
    windows_x86_64 = {"sys_platform": "win32", "platform_machine": "AMD64"}
    linux_arm64 = {"sys_platform": "linux", "platform_machine": "aarch64"}
    assert not cryptography.marker.evaluate(windows_arm64)
    assert cryptography.marker.evaluate(windows_x86_64)
    assert cryptography.marker.evaluate(linux_arm64)

    workflow = load_workflow("build-wheels.yml")
    native_job = workflow["jobs"]["native-wheels"]
    platforms = {(item["platform"], item["arch"]): item for item in native_job["strategy"]["matrix"]["platform"]}
    assert platforms[("windows", "aarch64")]["expect-cryptography"] == "false"
    assert all(
        platform["expect-cryptography"] == "true"
        for key, platform in platforms.items()
        if key != ("windows", "aarch64")
    )
    acceptance = next(
        step for step in native_job["steps"] if step.get("name") == "Install and exercise wheel in clean runner Python"
    )
    assert acceptance["env"]["EXPECT_CRYPTOGRAPHY"] == "${{ matrix.platform.expect-cryptography }}"
    assert 'assert (importlib.util.find_spec("cryptography") is not None) == expected_cryptography' in acceptance["run"]
    assert "assert _native.native_available()" in acceptance["run"]


def test_ci_creates_the_pytest_basetemp_parent_before_running_tests() -> None:
    workflow = load_workflow("ci.yml")
    test_step = next(step for step in workflow["jobs"]["python"]["steps"] if step.get("name") == "Tests")
    commands = [line.strip() for line in test_step["run"].splitlines() if line.strip()]

    assert commands.index("mkdir -p .tmp") < next(
        index for index, command in enumerate(commands) if command.startswith("uv run pytest ")
    )


def test_ci_runs_every_offline_benchmark_cli() -> None:
    workflow = load_workflow("ci.yml")
    benchmark_step = next(
        step
        for step in workflow["jobs"]["benchmark-smoke"]["steps"]
        if step.get("name") == "Run deterministic benchmark gates"
    )
    command = benchmark_step["run"]
    expected_scripts = {
        "miniproto-bench-acceptance",
        "miniproto-bench-imports",
        "miniproto-bench-media-scheduler",
        "miniproto-bench-native-fallback-crypto",
        "miniproto-bench-runtime-paths",
        "miniproto-bench-session-crypto",
        "miniproto-bench-tl-fast-paths",
        "miniproto-bench-transport-framing",
        "miniproto-profile-lazy-raw-codec",
    }

    assert {script for script in expected_scripts if f"uv run --no-sync {script}" in command} == expected_scripts
    uv_commands = [line.strip() for line in command.splitlines() if line.strip().startswith("uv run")]
    assert uv_commands
    assert all(line.startswith("uv run --no-sync ") for line in uv_commands)


def test_cross_platform_benchmark_matrix_records_speed_without_enforcing_host_specific_targets() -> None:
    workflow = load_workflow("ci.yml")
    benchmark_step = next(
        step
        for step in workflow["jobs"]["benchmark-smoke"]["steps"]
        if step.get("name") == "Run deterministic benchmark gates"
    )
    command = benchmark_step["run"]

    assert "miniproto-bench-tl-fast-paths --mode smoke" in command
    assert "miniproto-bench-transport-framing --mode smoke" in command
    assert "--check" not in command


def test_benchmark_rust_cache_isolated_between_regular_and_free_threaded_abis() -> None:
    workflow = load_workflow("ci.yml")
    job = workflow["jobs"]["benchmark-smoke"]
    rust_setup = next(
        step for step in job["steps"] if step.get("uses", "").startswith("actions-rust-lang/setup-rust-toolchain@")
    )

    assert {item["artifact"] for item in job["strategy"]["matrix"]["python"]} == {"py314", "py314t"}
    assert rust_setup["with"]["cache-key"] == "${{ matrix.python.artifact }}"


def test_manual_wheel_jobs_test_native_free_threading_and_every_console_script() -> None:
    workflow = load_workflow("build-wheels.yml")

    for job_name in ("linux-wheels", "native-wheels"):
        serialized_steps = "\n".join(str(step.get("run", "")) for step in workflow["jobs"][job_name]["steps"])
        assert "Py_GIL_DISABLED" in serialized_steps
        assert "_is_gil_enabled" in serialized_steps
        assert "ThreadPoolExecutor" in serialized_steps
        assert 'metadata.distribution("miniproto").entry_points' in serialized_steps
        assert 'subprocess.check_call([executable, "--help"])' in serialized_steps
        assert 'path=sysconfig.get_path("scripts")' in serialized_steps
        assert "--no-deps" not in serialized_steps
        assert "PYTHON_GIL" not in serialized_steps

    linux_steps = "\n".join(str(step.get("run", "")) for step in workflow["jobs"]["linux-wheels"]["steps"])
    native_steps = "\n".join(str(step.get("run", "")) for step in workflow["jobs"]["native-wheels"]["steps"])
    assert 'find_spec("cryptography") is not None' in linux_steps
    assert 'find_spec("cryptography") is not None) == expected_cryptography' in native_steps
    assert 'find_spec("uvloop") is not None' in linux_steps
    assert 'find_spec("uvloop" if sys.platform == "darwin" else "winloop") is not None' in native_steps


def test_pull_request_ci_has_no_telegram_secret_or_live_benchmark_contract() -> None:
    workflow = load_workflow("ci.yml")
    assert "pull_request" in workflow["on"]

    serialized = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "secrets.MINIPROTO" not in serialized
    assert "MINIPROTO_REAL_INTEGRATION: 1" not in serialized
    assert "benchmark_live_media_limit.py" not in serialized


def test_live_workflow_is_manual_secret_gated_cross_platform_and_uploads_failures() -> None:
    workflow = load_workflow("live-media-bench.yml")
    triggers = workflow["on"]
    inputs = triggers["workflow_dispatch"]["inputs"]

    assert set(inputs["mode"]["options"]) == {"smoke", "matrix", "tglib"}
    assert set(inputs["runner"]["options"]) == {"linux", "windows", "both"}
    assert set(inputs["matrix_profile"]["options"]) == {"smoke", "full"}
    assert inputs["matrix_profile"]["default"] == "smoke"
    job = workflow["jobs"]["live-benchmark"]
    matrix_runner = job["strategy"]["matrix"]["runner"]
    assert "fromJSON" in matrix_runner
    assert "inputs.runner" in matrix_runner
    assert "if" not in job
    assert "matrix.runner" in job["runs-on"]
    assert job["env"]["MINIPROTO_LIVE_BENCH"] == "1"
    assert job["env"]["MINIPROTO_INTEGRATION"] == "1"
    assert job["env"]["MINIPROTO_REAL_INTEGRATION"] == "1"
    assert job["env"]["MINIPROTO_TGLIB_BENCH"] == "1"
    assert any(
        step.get("uses", "").startswith("actions/upload-artifact@") and step.get("if") == "always()"
        for step in job["steps"]
    )
    run_step = next(step for step in job["steps"] if step.get("name") == "Run selected live benchmark")
    assert '--mode "${{ inputs.matrix_profile }}"' in run_step["run"]


def test_schema_upstream_workflow_remains_scheduled_and_manual() -> None:
    workflow = load_workflow("schema-upstream.yml")

    assert "schedule" in workflow["on"]
    assert "workflow_dispatch" in workflow["on"]

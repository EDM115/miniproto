from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

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
        ("glibc", "armv7l", "armv7-unknown-linux-gnueabihf"),
        ("musl", "x86_64", "x86_64-unknown-linux-musl"),
        ("musl", "aarch64", "aarch64-unknown-linux-musl"),
        ("musl", "armv7l", "armv7-unknown-linux-musleabihf"),
    }
    assert len(linux_matrix["python"]) * len(linux_matrix["platform"]) == 18

    native_matrix = jobs["native-wheels"]["strategy"]["matrix"]
    assert {item["python-version"] for item in native_matrix["python"]} == {"3.13", "3.14", "3.14t"}
    assert {(item["platform"], item["arch"], item["target"]) for item in native_matrix["platform"]} == {
        ("windows", "x86_64", "x86_64-pc-windows-msvc"),
        ("windows", "aarch64", "aarch64-pc-windows-msvc"),
        ("macos", "x86_64", "x86_64-apple-darwin"),
        ("macos", "aarch64", "aarch64-apple-darwin"),
    }
    assert len(native_matrix["python"]) * len(native_matrix["platform"]) == 12


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

    assert {script for script in expected_scripts if f"uv run {script}" in command} == expected_scripts


def test_manual_wheel_jobs_test_native_free_threading_and_every_console_script() -> None:
    workflow = load_workflow("build-wheels.yml")

    for job_name in ("linux-wheels", "native-wheels"):
        serialized_steps = "\n".join(str(step.get("run", "")) for step in workflow["jobs"][job_name]["steps"])
        assert "Py_GIL_DISABLED" in serialized_steps
        assert "_is_gil_enabled" in serialized_steps
        assert "ThreadPoolExecutor" in serialized_steps
        assert 'metadata.distribution("miniproto").entry_points' in serialized_steps
        assert 'subprocess.check_call([executable, "--help"])' in serialized_steps
        assert "--no-deps" not in serialized_steps
        assert 'find_spec("cryptography") is not None' in serialized_steps

    linux_steps = "\n".join(str(step.get("run", "")) for step in workflow["jobs"]["linux-wheels"]["steps"])
    native_steps = "\n".join(str(step.get("run", "")) for step in workflow["jobs"]["native-wheels"]["steps"])
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

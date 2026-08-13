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
    value = yaml.load(
        (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8"),
        Loader=GitHubWorkflowLoader,  # noqa: S506 - SafeLoader subclass; only YAML boolean resolution changes.
    )
    assert isinstance(value, dict)
    return value


def test_ci_workflow_covers_minimum_python_rust_benchmarks_and_wheel_platforms() -> None:
    workflow = load_workflow("ci.yml")
    jobs = workflow["jobs"]

    assert set(jobs["python"]["strategy"]["matrix"]["python-version"]) == {"3.13", "3.14"}
    assert jobs["rust"]["steps"][1]["with"]["toolchain"] == "1.97.0"
    benchmark_steps = jobs["benchmark-smoke"]["steps"]
    assert any(
        step.get("uses", "").startswith("actions/upload-artifact@") and step.get("if") == "always()"
        for step in benchmark_steps
    )
    wheel_matrix = jobs["wheels"]["strategy"]["matrix"]["include"]
    assert {(item["os"], item["arch"]) for item in wheel_matrix} == {
        ("ubuntu-latest", "x86_64"),
        ("windows-latest", "x86_64"),
        ("macos-15-intel", "x86_64"),
        ("macos-15", "aarch64"),
    }
    assert {item["python-version"] for item in wheel_matrix} == {"3.13", "3.14"}
    assert "sdist" in jobs


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

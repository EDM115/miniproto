from __future__ import annotations

import json
import re
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


def test_github_actions_use_free_flowing_release_tags() -> None:
    """External actions must follow the repository's release-tag update policy."""
    workflows = ROOT / ".github" / "workflows"
    action_references: list[tuple[Path, str]] = []
    for path in sorted(workflows.glob("*.yml")):
        for action, reference in re.findall(
            r"^\s*-?\s*uses:\s+([^\s@]+)@([^\s#]+)", path.read_text(encoding="utf-8"), re.MULTILINE
        ):
            if not action.startswith("./"):
                action_references.append((path, reference))

    assert action_references
    for path, reference in action_references:
        assert reference.startswith(("v", "release/v")), f"{path} uses a non-release-tag action reference: {reference}"


def test_release_reconciliation_declares_0_1_0_alpha_and_current_wave_state() -> None:
    """Release metadata and the tracker must agree after Waves 6 and 7."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    crate = tomllib.loads((ROOT / "rust/miniproto/Cargo.toml").read_text(encoding="utf-8"))
    frontend = json.loads((ROOT / "docs-site/package.json").read_text(encoding="utf-8"))
    progress = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")

    assert project["project"]["version"] == "0.1.0"
    assert "Development Status :: 3 - Alpha" in project["project"]["classifiers"]
    assert "Development Status :: 2 - Pre-Alpha" not in project["project"]["classifiers"]
    assert crate["package"]["version"] == "0.1.0"
    assert frontend["version"] == "0.1.0"
    assert "intermediary release-readiness bridge between Waves 5 and 6" in progress
    assert "At that intermediary checkpoint Wave 6 had not started" in progress
    assert "Waves 0 through 7" in progress
    task_082 = next(line for line in progress.splitlines() if "| TASK-082 |" in line)
    task_094 = next(line for line in progress.splitlines() if "| TASK-094 |" in line)
    assert "| yes | 2026-08-19 |" in task_082
    assert "| ready / user action required | 2026-08-19 |" in task_094


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
    assert "uv sync --python python --extra dev,docs --frozen --no-install-project" in build_commands
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


def test_manual_release_artifact_workflow_is_dispatch_only_and_covers_all_required_abis() -> None:
    workflow = load_workflow("build-wheels.yml")

    assert workflow["name"] == "Build release artifacts"
    assert set(workflow["on"]) == {"workflow_dispatch"}
    jobs = workflow["jobs"]
    assert set(jobs) == {"linux-wheels", "native-wheels", "python-sdist", "rust-crate", "release-manifest"}

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
            for job_name, job in jobs.items()
            if job_name in {"linux-wheels", "native-wheels"}
        )
        == 24
    )


def test_release_artifact_workflow_attests_every_distribution_and_builds_the_crate_once() -> None:
    workflow = load_workflow("build-wheels.yml")
    jobs = workflow["jobs"]

    for job_name in ("linux-wheels", "native-wheels", "python-sdist", "rust-crate", "release-manifest"):
        permissions = jobs[job_name]["permissions"]
        assert permissions["contents"] == "read"
        assert permissions["id-token"] == "write"
        assert permissions["attestations"] == "write"

    for job_name, subject in (
        ("linux-wheels", "dist/*.whl"),
        ("native-wheels", "dist/*.whl"),
        ("python-sdist", "dist/*.tar.gz"),
        ("rust-crate", "${{ env.CARGO_TARGET_DIR }}/package/*.crate"),
    ):
        attestation = next(
            step for step in jobs[job_name]["steps"] if step.get("uses", "").startswith("actions/attest@")
        )
        assert attestation["uses"] == "actions/attest@v4"
        assert attestation["with"]["subject-path"] == subject
        upload = next(
            step for step in jobs[job_name]["steps"] if step.get("uses", "").startswith("actions/upload-artifact@")
        )
        assert upload["with"]["archive"] == "false"

    crate_job = jobs["rust-crate"]
    assert "strategy" not in crate_job
    assert crate_job["env"]["CARGO_TARGET_DIR"] == "${{ github.workspace }}/.tmp/release-crate-target"
    crate_commands = "\n".join(str(step.get("run", "")) for step in crate_job["steps"])
    assert "cargo clean" not in crate_commands
    assert "cargo build --locked --release --all-features -p miniproto" in crate_commands
    assert "cargo package --locked -p miniproto --list" in crate_commands
    assert "cargo package --locked -p miniproto" in crate_commands

    manifest_job = jobs["release-manifest"]
    assert set(manifest_job["needs"]) == {"linux-wheels", "native-wheels", "python-sdist", "rust-crate"}
    manifest_steps = "\n".join(str(step) for step in manifest_job["steps"])
    assert "actions/download-artifact@v8" in manifest_steps
    assert "python -m tools.release_artifacts manifest" in manifest_steps
    assert "release-manifest.json" in manifest_steps
    assert "SHA256SUMS" in manifest_steps


def test_publish_workflow_verifies_one_build_run_then_uses_isolated_oidc_jobs() -> None:
    workflow = load_workflow("publish-release.yml")

    assert workflow["on"] == {
        "workflow_dispatch": {
            "inputs": {
                "build_run_id": {
                    "description": "Successful Build release artifacts workflow run ID",
                    "required": "true",
                    "type": "string",
                },
                "version": {
                    "description": "Exact release version without the v prefix",
                    "required": "true",
                    "type": "string",
                },
            }
        }
    }
    assert workflow["permissions"] == {}
    jobs = workflow["jobs"]
    assert set(jobs) == {"verify", "draft-release", "pypi", "crates", "publish-release"}

    verify = jobs["verify"]
    assert verify["permissions"] == {"actions": "read", "attestations": "read", "contents": "read"}
    verify_steps = "\n".join(str(step) for step in verify["steps"])
    assert "actions/download-artifact@v8" in verify_steps
    assert "run-id" in verify_steps
    assert "run-attempt" in verify_steps
    assert "digest-mismatch" in verify_steps
    assert "gh attestation verify" in verify_steps
    assert "--signer-workflow" in verify_steps
    assert "python -m tools.release_artifacts verify" in verify_steps
    assert ".github/workflows/build-wheels.yml" in verify_steps
    assert "workflow_dispatch" in verify_steps
    assert "conclusion" in verify_steps
    assert "merge-base --is-ancestor" in verify_steps

    draft_release = jobs["draft-release"]
    assert draft_release["needs"] == ["verify"]
    assert draft_release["environment"] == "release"
    assert draft_release["permissions"] == {"contents": "write"}
    draft_steps = "\n".join(str(step) for step in draft_release["steps"])
    assert "gh release create" in draft_steps
    assert "--draft" in draft_steps
    assert "gh release upload" in draft_steps

    pypi = jobs["pypi"]
    assert set(pypi["needs"]) == {"verify", "draft-release"}
    assert pypi["environment"]["name"] == "release"
    assert pypi["permissions"] == {"id-token": "write"}
    pypi_steps = "\n".join(str(step) for step in pypi["steps"])
    assert "pypa/gh-action-pypi-publish@" in pypi_steps
    assert "packages-dir" in pypi_steps
    assert "attestations" in pypi_steps

    crates = jobs["crates"]
    assert set(crates["needs"]) == {"verify", "pypi"}
    assert crates["environment"] == "release"
    assert crates["permissions"] == {"contents": "read", "id-token": "write"}
    crate_steps = "\n".join(str(step) for step in crates["steps"])
    assert "rust-lang/crates-io-auth-action@" in crate_steps
    assert "cargo publish --locked -p miniproto" in crate_steps
    assert "CARGO_REGISTRY_TOKEN" in crate_steps
    assert "crates.io already contains the attested Cargo package" in crate_steps
    assert "existing crates.io archive differs from the attested build artifact" in crate_steps

    publish_release = jobs["publish-release"]
    assert set(publish_release["needs"]) == {"verify", "crates"}
    assert publish_release["environment"] == "release"
    assert publish_release["permissions"] == {"contents": "write"}
    final_steps = "\n".join(str(step) for step in publish_release["steps"])
    assert "gh release edit" in final_steps
    assert "--draft=false" in final_steps

    serialized = (ROOT / ".github" / "workflows" / "publish-release.yml").read_text(encoding="utf-8")
    assert "secrets." not in serialized


def test_crates_io_metadata_describes_the_provenance_only_accelerator_boundary() -> None:
    manifest = tomllib.loads((ROOT / "rust" / "miniproto" / "Cargo.toml").read_text(encoding="utf-8"))
    package = manifest["package"]

    assert package["version"] == "0.1.0"
    assert package["homepage"] == "https://edm115.github.io/miniproto/"
    assert package["documentation"] == "https://docs.rs/miniproto"
    assert "authors" not in package
    assert package["readme"] == "README.md"
    assert package["publish"] == ["crates-io"]
    assert {"telegram", "mtproto", "pyo3", "python"} <= set(package["keywords"])
    assert {"api-bindings", "cryptography", "network-programming"} <= set(package["categories"])
    assert manifest["lib"] == {"name": "miniproto_native", "crate-type": ["cdylib"]}

    crate_readme = (ROOT / "rust" / "miniproto" / "README.md").read_text(encoding="utf-8")
    assert "Python accelerator" in crate_readme
    assert "not yet a supported standalone Rust library API" in crate_readme
    assert "miniproto_native" in crate_readme


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

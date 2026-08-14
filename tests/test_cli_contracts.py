from __future__ import annotations

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement

from miniproto._cli import CLI_ENTRY_POINTS

ROOT = Path(__file__).parents[1]


def test_default_wheel_installs_supported_crypto_and_platform_event_loop_backends() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    dependencies = project["dependencies"]
    cryptography = Requirement(next(item for item in dependencies if item.startswith("cryptography")))

    assert cryptography.specifier == Requirement("cryptography==50.0.0").specifier
    assert cryptography.marker is not None
    assert cryptography.marker.evaluate({"sys_platform": "linux", "platform_machine": "aarch64"})
    assert cryptography.marker.evaluate({"sys_platform": "win32", "platform_machine": "AMD64"})
    assert not cryptography.marker.evaluate({"sys_platform": "win32", "platform_machine": "ARM64"})
    assert {item for item in dependencies if not item.startswith("cryptography")} == {
        "uvloop==0.22.1; sys_platform == 'linux' or sys_platform == 'darwin'",
        "winloop==0.6.3; sys_platform == 'win32' or sys_platform == 'cygwin' or sys_platform == 'cli'",
    }
    assert "crypto-fallback" not in project["optional-dependencies"]
    assert "event-loop" not in project["optional-dependencies"]
    assert not any(dependency.startswith("cryptography") for dependency in project["optional-dependencies"]["dev"])
    assert not any(
        dependency.startswith(("uvloop==", "winloop==")) for dependency in project["optional-dependencies"]["dev"]
    )


def cli_modules() -> tuple[str, ...]:
    modules = []
    for path in sorted((ROOT / "tools").rglob("*.py")):
        if 'if __name__ == "__main__":' not in path.read_text(encoding="utf-8"):
            continue
        modules.append(".".join(path.relative_to(ROOT).with_suffix("").parts))
    return tuple(modules)


def test_every_cli_module_has_exactly_one_project_script() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]
    expected_targets = {
        script: f"miniproto._cli:{entry_function}" for script, (entry_function, _module) in CLI_ENTRY_POINTS.items()
    }

    assert scripts == expected_targets
    assert {module for _entry_function, module in CLI_ENTRY_POINTS.values()} == set(cli_modules())


def test_session_crypto_backend_benchmark_is_a_packaged_cli() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["scripts"]["miniproto-bench-session-crypto"] == "miniproto._cli:bench_session_crypto"
    assert CLI_ENTRY_POINTS["miniproto-bench-session-crypto"] == (
        "bench_session_crypto",
        "tools.bench.benchmark_session_crypto_backends",
    )


def test_maturin_tool_includes_are_source_only() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    include_paths = {item["path"] for item in pyproject["tool"]["maturin"]["include"]}

    assert include_paths == {"tools/*.py", "tools/**/*.py", "tools/**/*.json", "tools/**/*.tl", "tools/**/*.md"}


def test_project_script_help_works_outside_the_source_checkout(tmp_path: Path) -> None:
    executable = shutil.which("miniproto-bench-acceptance")
    assert executable is not None

    completed = subprocess.run(  # noqa: S603 - executable is resolved from the installed project script.
        [executable, "--help"], cwd=tmp_path, capture_output=True, text=True, timeout=30
    )

    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout.casefold()


@pytest.mark.parametrize("module", cli_modules())
def test_every_cli_supports_help_without_running_its_operation(module: str) -> None:
    completed = subprocess.run(  # noqa: S603 - sys.executable and discovered repository modules are trusted.
        [sys.executable, "-m", module, "--help"], cwd=ROOT, capture_output=True, text=True, timeout=30
    )

    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout.casefold()

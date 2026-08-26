from __future__ import annotations

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from miniproto._cli import CLI_ENTRY_POINTS

ROOT = Path(__file__).parents[1]


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

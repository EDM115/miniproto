"""Non-mutating release-check orchestration and distribution evidence collection.

Stages execute local validation, packaging and controlled subprocess checks in
order. A passing stage is evidence only for that stage's stated boundary: it
does not establish live Telegram acceptance, credential correctness or release
approval. ``live`` mode additionally requires explicit environment opt-in.
"""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
import zipfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from email import policy
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any

from tools.bench.reporting import collect_environment, write_benchmark_report

StageRunner = Callable[["Stage", dict[str, str]], int]

_REQUIRED_CLASSIFIERS = frozenset(
    {
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Rust",
        "Typing :: Typed",
    }
)
_REQUIRED_PROJECT_URLS = frozenset(
    {"Homepage", "Documentation", "Source", "Changelog", "Issues", "Funding", "Security"}
)
_REQUIRED_DEPENDENCIES = frozenset({"cryptography", "uvloop", "winloop"})
_REQUIRED_EXTRAS = frozenset({"dev", "docs"})
_REQUIRED_WHEEL_PAYLOAD = frozenset(
    {
        "miniproto/__init__.py",
        "miniproto/py.typed",
        "miniproto/raw/functions.py",
        "miniproto/raw/functions.pyi",
        "miniproto/raw/types.py",
        "miniproto/raw/types.pyi",
    }
)
_REQUIRED_SDIST_PAYLOAD = frozenset(
    {
        "Cargo.lock",
        "Cargo.toml",
        "LICENSE",
        "PKG-INFO",
        "README.md",
        "pyproject.toml",
        "rust/miniproto/Cargo.toml",
        "rust/miniproto/README.md",
        "rust/miniproto/src/lib.rs",
        "src/miniproto/__init__.py",
        "src/miniproto/py.typed",
        "src/miniproto/raw/functions.py",
        "src/miniproto/raw/functions.pyi",
        "src/miniproto/raw/types.py",
        "src/miniproto/raw/types.pyi",
        "tools/release_artifacts.py",
        "tools/release_check.py",
        "tools/schema/generate.py",
        "tools/schema/parser.py",
        "tools/schema/rpc-errors.json",
        "tools/schema/rust-fast-paths.json",
        "tools/schema/schema-core.tl",
        "tools/schema/schema-metadata.json",
        "tools/schema/schema-tdesktop.tl",
        "tools/schema/schema.tl",
        "tools/schema/telegram-bindings.json",
    }
)


@dataclass(frozen=True, slots=True)
class ReleaseConfig:
    """Requested release-check mode, failure policy and task-owned artifact location.

    Attributes:
        mode: ``quick``, ``offline`` or explicitly guarded ``live`` stage selection.
        keep_going: Continue after failures while retaining the first non-zero exit code.
        artifacts_dir: Directory used for reports, distributions and temporary clean environments.
    """

    mode: str
    keep_going: bool
    artifacts_dir: Path


@dataclass(frozen=True, slots=True)
class Stage:
    """One ordered release-check stage and its fixed subprocess or internal action.

    Attributes:
        name: Stable report label for the stage.
        command: Fixed command tuple or ``None`` when the stage is pending/unavailable.
        pending_reason: Human-readable explanation retained for an unavailable stage.
    """

    name: str
    command: tuple[str, ...] | None
    pending_reason: str | None = None


def parse_args(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> argparse.Namespace:
    """Parse release-check modes without accepting credentials on the command line.

    Args:
        argv: Optional mode, continuation and artifact-directory arguments.
        env: Environment mapping used only for the default artifact directory.

    Returns:
        CLI namespace selecting ``quick``, ``offline`` (default) or ``live`` mode.

    Raises:
        SystemExit: Mutually exclusive mode arguments or their values are invalid.
    """
    values = os.environ if env is None else env
    parser = argparse.ArgumentParser(description="Run the canonical non-mutating miniproto release checks")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--quick",
        dest="mode",
        action="store_const",
        const="quick",
        help="run the short deterministic formatting, lint, type, schema and focused-test gate",
    )
    modes.add_argument(
        "--offline",
        dest="mode",
        action="store_const",
        const="offline",
        help="run the complete non-credentialed release gate; this is the default",
    )
    modes.add_argument(
        "--live",
        dest="mode",
        action="store_const",
        const="live",
        help="include explicitly guarded credentialed Telegram acceptance stages after offline checks",
    )
    parser.set_defaults(mode="offline")
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="continue independent stages after a failure and report every observed result",
    )
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=Path(values.get("MINIPROTO_RELEASE_ARTIFACTS", ".tmp/release-check")),
        help="directory to create or update with release reports; defaults to MINIPROTO_RELEASE_ARTIFACTS or .tmp/release-check",
    )
    return parser.parse_args(argv)


def build_stages(config: ReleaseConfig, *, repo: Path) -> tuple[Stage, ...]:
    """Construct the ordered check-only stage list for the requested mode.

    Args:
        config: Mode, continuation policy and artifact destination.
        repo: Repository root used to discover optional documentation tooling.

    Returns:
        Fixed subprocess/internal stages in execution order. Missing documentation
        tooling becomes a ``pending`` stage rather than a silent success.

    Evidence Limits:
        The list describes intended checks, not their execution result and live
        stages still require the main function's opt-in guard and real credentials.
    """
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
            pending_reason=None if docs_present else "Documentation tooling is not present",
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
            Stage(
                "benchmark-session-crypto",
                (
                    python,
                    "-m",
                    "tools.bench.benchmark_session_crypto_backends",
                    "--mode",
                    "smoke",
                    "--json",
                    str(artifacts / "benchmarks" / "session-crypto.json"),
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
    """Build the stage environment, including Windows Python DLL search-path support.

    Args:
        mode: Selected release-check mode.
        base_environment: Parent environment copied before integration flags are set.
        platform_name: Injectable platform indicator for deterministic tests.
        python_base_prefix: Python base directory prepended to Windows ``PATH``.

    Returns:
        A copied environment with integration flags bound to ``mode``.

    Secret Handling:
        Existing credential values are preserved for live subprocesses but are not
        accepted by CLI parsing or emitted by this helper.
    """
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
    """Execute stages in order, report durations in seconds and preserve first failure.

    Args:
        stages: Ordered fixed checks to execute or mark pending.
        config: Mode and whether later stages continue after a failure.
        runner: Injectable subprocess/internal runner returning each stage's exit code.

    Returns:
        Schema-v1 status report with each stage's result and the first non-zero exit code.

    Evidence Limits:
        A passed stage confirms only its runner exit status. Pending stages execute
        nothing; continued stages do not repair or negate earlier failures.
    """
    environment = build_release_environment(config.mode, os.environ)
    results: list[dict[str, Any]] = []
    first_failure = 0
    stage_count = len(stages)
    for index, stage in enumerate(stages, start=1):
        progress_label = f"[release-check {index}/{stage_count}] {stage.name}"
        if stage.command is None:
            print(f"{progress_label}: pending - {stage.pending_reason}", flush=True)
            results.append(
                {"name": stage.name, "status": "pending", "duration_seconds": 0.0, "reason": stage.pending_reason}
            )
            continue
        print(f"{progress_label}: running", flush=True)
        started = time.perf_counter()
        exit_code = runner(stage, environment)
        duration = time.perf_counter() - started
        status = "passed" if exit_code == 0 else "failed"
        if exit_code == 0:
            print(f"{progress_label}: passed in {duration:.2f}s", flush=True)
        else:
            print(f"{progress_label}: failed with exit code {exit_code} in {duration:.2f}s", flush=True)
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


def _inspect_release_metadata(payload: bytes, *, source: str, expected_version: str) -> dict[str, Any]:
    """Validate the modern release metadata contract embedded in a distribution.

    Args:
        payload: RFC 822 package metadata bytes from ``METADATA`` or ``PKG-INFO``.
        source: Human-readable artifact and metadata member label used in failures.
        expected_version: Version derived independently from the artifact path.

    Returns:
        Stable selected metadata fields suitable for the artifact manifest.

    Raises:
        ValueError: Required release identity, compatibility, licensing, dependency or project-link metadata is absent or inconsistent.
    """
    message = BytesParser(policy=policy.default).parsebytes(payload)
    classifiers = {str(value) for value in message.get_all("Classifier", [])}
    project_urls: dict[str, str] = {}
    malformed_urls: list[str] = []
    for value in message.get_all("Project-URL", []):
        label, separator, url = str(value).partition(",")
        label = label.strip()
        url = url.strip()
        if not separator or not label or not url.startswith("https://"):
            malformed_urls.append(str(value))
            continue
        project_urls[label] = url
    dependencies: set[str] = set()
    for value in message.get_all("Requires-Dist", []):
        requirement, _separator, marker = str(value).partition(";")
        if "extra ==" in marker.casefold():
            continue
        match = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", requirement)
        if match is not None:
            dependencies.add(match.group(0).casefold().replace("_", "-"))
    extras = {str(value) for value in message.get_all("Provides-Extra", [])}
    keywords = {part.strip().casefold() for part in str(message.get("Keywords", "")).split(",") if part.strip()}
    license_files = [str(value) for value in message.get_all("License-File", [])]
    failures: list[str] = []
    if message.get("Metadata-Version") != "2.4":
        failures.append("Metadata-Version must be 2.4")
    if message.get("Name") != "miniproto":
        failures.append("Name must be miniproto")
    if message.get("Version") != expected_version:
        failures.append(f"Version must match {expected_version}")
    if message.get("Requires-Python") != ">=3.13":
        failures.append("Requires-Python must be >=3.13")
    if not str(message.get("Description-Content-Type", "")).startswith("text/markdown"):
        failures.append("README content type must be Markdown")
    if "miniproto@edm115.dev" not in str(message.get("Author-email", "")):
        failures.append("author contact is missing")
    if message.get("License-Expression") != "MIT" or message.get("License"):
        failures.append("modern MIT License-Expression is missing or conflicts with legacy License")
    if not any(PurePosixPath(value).name == "LICENSE" for value in license_files):
        failures.append("LICENSE is not declared by License-File")
    legacy_license_classifiers = sorted(value for value in classifiers if value.startswith("License ::"))
    if legacy_license_classifiers:
        failures.append("deprecated License classifiers are present")
    missing_classifiers = sorted(_REQUIRED_CLASSIFIERS - classifiers)
    if missing_classifiers:
        failures.append(f"classifiers are missing: {', '.join(missing_classifiers)}")
    missing_urls = sorted(_REQUIRED_PROJECT_URLS - project_urls.keys())
    if missing_urls:
        failures.append(f"project URLs are missing: {', '.join(missing_urls)}")
    if malformed_urls:
        failures.append(f"project URLs are malformed: {', '.join(malformed_urls)}")
    missing_dependencies = sorted(_REQUIRED_DEPENDENCIES - dependencies)
    if missing_dependencies:
        failures.append(f"runtime dependencies are missing: {', '.join(missing_dependencies)}")
    missing_extras = sorted(_REQUIRED_EXTRAS - extras)
    if missing_extras:
        failures.append(f"optional dependency groups are missing: {', '.join(missing_extras)}")
    missing_keywords = sorted({"telegram", "mtproto", "asyncio", "pyo3", "rust"} - keywords)
    if missing_keywords:
        failures.append(f"keywords are missing: {', '.join(missing_keywords)}")
    if failures:
        raise ValueError(f"{source} has incomplete release metadata: {'; '.join(failures)}")
    return {
        "metadata_version": str(message["Metadata-Version"]),
        "name": str(message["Name"]),
        "version": str(message["Version"]),
        "requires_python": str(message["Requires-Python"]),
        "license_expression": str(message["License-Expression"]),
        "classifiers": sorted(classifiers),
        "project_urls": dict(sorted(project_urls.items())),
        "runtime_dependencies": sorted(dependencies),
        "extras": sorted(extras),
    }


def inspect_wheel(path: Path) -> dict[str, Any]:
    """Inspect one wheel for expected bundled Python, native extension and console scripts.

    Args:
        path: Built wheel archive to inspect without installing it.

    Returns:
        Stable artifact metadata including SHA-256, byte size and discovered contents.

    Raises:
        zipfile.BadZipFile: ``path`` is not a readable wheel archive.
        ValueError: Required contents are missing or forbidden path/cache files are present.

    Evidence Limits:
        Archive inspection does not prove installation, importability, ABI support,
        console-script execution or runtime behavior; the separate clean-import
        stage covers a narrow installation/import smoke boundary.
    """
    with zipfile.ZipFile(path) as archive:
        names = sorted(archive.namelist())
        metadata_files = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_files) != 1:
            raise ValueError(f"invalid wheel {path.name}: expected exactly one METADATA file")
        metadata_file = metadata_files[0]
        metadata_directory = PurePosixPath(metadata_file).parent.name
        if not metadata_directory.startswith("miniproto-") or not metadata_directory.endswith(".dist-info"):
            raise ValueError(f"invalid wheel {path.name}: METADATA directory does not identify miniproto")
        expected_version = metadata_directory.removeprefix("miniproto-").removesuffix(".dist-info")
        metadata = _inspect_release_metadata(
            archive.read(metadata_file), source=f"wheel {path.name}:{metadata_file}", expected_version=expected_version
        )
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
    missing_payload = sorted(_REQUIRED_WHEEL_PAYLOAD - set(names))
    if missing_payload:
        failures.append(f"public package payload is missing: {', '.join(missing_payload)}")
    if not any(name.startswith("miniproto/raw/_function_shards/") and name.endswith(".py") for name in names):
        failures.append("public package payload has no generated function shard")
    if not any(name.startswith("miniproto/raw/_types_shards/") and name.endswith(".py") for name in names):
        failures.append("public package payload has no generated type shard")
    if not any(
        name.startswith(f"{metadata_directory}/licenses/") and PurePosixPath(name).name == "LICENSE" for name in names
    ):
        failures.append("declared LICENSE file is missing from the wheel")
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
        "metadata": metadata,
    }


def inspect_sdist(path: Path) -> dict[str, Any]:
    """Inspect one source distribution for release metadata, source inputs and forbidden residue.

    Args:
        path: Built ``.tar.gz`` source distribution inspected without extraction.

    Returns:
        Stable artifact metadata including SHA-256, byte size, entry count and selected package metadata.

    Raises:
        tarfile.TarError: ``path`` is not a readable tar archive.
        ValueError: The archive layout, metadata, required source/build inputs or hygiene boundary is invalid.
    """
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        names = [member.name.replace("\\", "/") for member in members]
        unsafe_names = [
            name for name in names if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
        ]
        if unsafe_names:
            raise ValueError(f"invalid source distribution {path.name}: unsafe archive paths are present")
        roots = {PurePosixPath(name).parts[0] for name in names if PurePosixPath(name).parts}
        if len(roots) != 1:
            raise ValueError(f"invalid source distribution {path.name}: expected one top-level directory")
        root = roots.pop()
        relative_names = {name.removeprefix(f"{root}/") for name in names if name != root}
        pkg_info_name = f"{root}/PKG-INFO"
        try:
            pkg_info_member = archive.getmember(pkg_info_name)
        except KeyError as exc:
            raise ValueError(f"invalid source distribution {path.name}: PKG-INFO is missing") from exc
        pkg_info = archive.extractfile(pkg_info_member)
        if pkg_info is None:
            raise ValueError(f"invalid source distribution {path.name}: PKG-INFO is not a regular file")
        expected_version = root.removeprefix("miniproto-") if root.startswith("miniproto-") else ""
        metadata = _inspect_release_metadata(
            pkg_info.read(),
            source=f"source distribution {path.name}:{pkg_info_name}",
            expected_version=expected_version,
        )
    missing_payload = sorted(_REQUIRED_SDIST_PAYLOAD - relative_names)
    if not any(
        name.startswith("src/miniproto/raw/_function_shards/") and name.endswith(".py") for name in relative_names
    ):
        missing_payload.append("src/miniproto/raw/_function_shards/*.py")
    if not any(name.startswith("src/miniproto/raw/_types_shards/") and name.endswith(".py") for name in relative_names):
        missing_payload.append("src/miniproto/raw/_types_shards/*.py")
    if missing_payload:
        raise ValueError(
            f"invalid source distribution {path.name}: required source/build inputs are missing: {', '.join(missing_payload)}"
        )
    forbidden: list[str] = []
    for name in sorted(relative_names):
        parts = PurePosixPath(name).parts
        if any(
            part in {".git", ".tmp", ".venv", "__pycache__", "target", "dist"} or part.startswith(".env")
            for part in parts
        ) or name.casefold().endswith((".pyc", ".pyo")):
            forbidden.append(name)
    if forbidden:
        raise ValueError(
            f"invalid source distribution {path.name}: forbidden temporary/cache paths are present: {', '.join(forbidden)}"
        )
    return {
        "path": str(path),
        "sha256": _sha256(path),
        "size": path.stat().st_size,
        "entries": len(names),
        "metadata": metadata,
    }


def inspect_artifacts(directory: Path) -> dict[str, Any]:
    """Inspect every wheel and sdist in a build directory and record stable hashes.

    Args:
        directory: Maturin output directory expected to contain wheels and source distributions.

    Returns:
        Per-wheel inspection records and path/hash/size records for sdists.

    Raises:
        ValueError: No wheel or no source distribution is present.
        OSError: An artifact cannot be opened or statted.
    """
    wheels = sorted(directory.glob("*.whl"))
    sdists = sorted(directory.glob("*.tar.gz"))
    if not wheels:
        raise ValueError("release build produced no wheel")
    if not sdists:
        raise ValueError("release build produced no sdist")
    return {"wheels": [inspect_wheel(wheel) for wheel in wheels], "sdists": [inspect_sdist(path) for path in sdists]}


def default_runner(config: ReleaseConfig, *, repo: Path) -> StageRunner:
    """Create the fixed-command subprocess/internal runner for one release-check invocation.

    Args:
        config: Artifact location available to internal environment, inspection and clean-import stages.
        repo: Working directory for fixed external stage commands.

    Returns:
        A runner that returns process exit codes and converts expected internal
        filesystem/package failures to ``1``.

    Subprocess Boundary:
        External commands receive the release environment and run from ``repo``.
        Only commands preconstructed by :func:`build_stages` are executed.
    """

    def run(stage: Stage, env: dict[str, str]) -> int:
        """Execute one fixed stage command or its named internal release-check action.

        Args:
            stage: Fixed release-check stage whose external or internal action is invoked.
            env: Prepared release environment passed to the stage action.
        """
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
                _clean_import(config.artifacts_dir, env=env)
            else:
                raise ValueError(f"unknown internal release stage: {stage.command[1]}")
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            print(f"{stage.name}: {exc}", file=sys.stderr)
            return 1
        return 0

    return run


def main(argv: Sequence[str] | None = None) -> int:
    """Run selected release checks, persist their report and return the first failure code.

    Args:
        argv: Optional non-secret release-check arguments.

    Returns:
        The first failing stage's exit code, ``0`` for no failures or ``2`` when
        live mode lacks explicit ``MINIPROTO_RELEASE_LIVE=1`` authorization.

    Evidence Limits:
        The report records local stage outputs and environment context; it is not
        a release approval and does not certify skipped, pending or unrun checks.
    """
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
    """Persist non-secret tool and runtime version evidence for the release report.

    Args:
        artifacts_dir: Release artifact directory that receives ``environment.json``.
    """
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    tools = collect_environment()
    tools["uv"] = _version(("uv", "--version"))
    tools["ruff"] = _version((sys.executable, "-m", "ruff", "--version"))
    tools["ty"] = _version((sys.executable, "-m", "ty", "--version"))
    tools["maturin"] = _version((sys.executable, "-m", "maturin", "--version"))
    tools["cargo"] = _version(("cargo", "--version"))
    write_benchmark_report(artifacts_dir / "environment.json", tools)


def _clean_import(artifacts_dir: Path, *, env: Mapping[str, str]) -> None:
    """Install the built wheel and sdist separately and run isolated public/native smoke tests.

    Args:
        artifacts_dir: Task-owned artifact root containing built distributions and the clean environment.
        env: Prepared release environment passed to every provisioning subprocess.

    Raises:
        ValueError: The artifact set is ambiguous/incomplete or the ``uv`` executable needed for isolated environments is unavailable.
        subprocess.CalledProcessError: Environment creation, dependency-resolving installation or an isolated public/native smoke test fails.
    """
    distributions = artifacts_dir / "distributions"
    wheels = sorted(distributions.glob("*.whl"))
    sdists = sorted(distributions.glob("*.tar.gz"))
    if len(wheels) != 1:
        raise ValueError(f"clean import expected exactly one wheel, found {len(wheels)}")
    if len(sdists) != 1:
        raise ValueError(f"clean import expected exactly one sdist, found {len(sdists)}")
    uv = shutil.which("uv")
    if uv is None:
        raise ValueError("uv is unavailable for clean-environment verification")
    smoke = (
        "import hashlib, importlib.metadata as metadata, sys; "
        "from pathlib import Path; "
        "import miniproto; "
        "from miniproto import _native; "
        "from miniproto.raw.functions import HelpGetConfig; "
        "from miniproto.raw.types import BoolTrue; "
        "assert Path(miniproto.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()); "
        "assert _native.native_available(); "
        "payload = b'miniproto-wave6'; "
        "assert _native.sha256_digest(payload) == hashlib.sha256(payload).digest(); "
        "assert HelpGetConfig().serialize().hex() == '6b18f9c4'; "
        "assert BoolTrue().serialize().hex() == 'b5757299'"
    )
    for label, distribution in (("wheel", wheels[0]), ("sdist", sdists[0])):
        environment_dir = artifacts_dir / f"clean-{label}-env"
        subprocess.run(  # noqa: S603 - executable and paths are locally resolved release artifacts
            (uv, "venv", "--clear", "--python", sys.executable, str(environment_dir)),
            cwd=artifacts_dir,
            env=env,
            check=True,
        )
        python = environment_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run(  # noqa: S603 - executable and distribution are locally resolved release artifacts
            (uv, "pip", "install", "--python", str(python), str(distribution.resolve())),
            cwd=artifacts_dir,
            env=env,
            check=True,
        )
        subprocess.run(  # noqa: S603 - interpreter is from the task-owned clean environment
            (str(python), "-I", "-c", smoke), cwd=artifacts_dir, env=env, check=True
        )


def _version(command: tuple[str, ...]) -> str | None:
    """Run one fixed version subprocess for at most ten seconds and return its text output.

    Args:
        command: Fixed version command run with a ten-second timeout.
    """
    try:
        completed = subprocess.run(  # noqa: S603 - callers pass fixed tool-version commands only
            command, check=False, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (completed.stdout or completed.stderr).strip()
    return output if completed.returncode == 0 and output else None


def _sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of a file read incrementally in one MiB blocks.

    Args:
        path: Artifact file read incrementally in one-MiB blocks.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

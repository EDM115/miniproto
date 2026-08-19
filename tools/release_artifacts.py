"""Validate, describe, and re-verify immutable miniproto release artifacts.

The build workflow uses this module to create a checksum file and a provenance manifest from the complete release candidate. The separate publication workflow uses the same validation logic before any registry or GitHub release mutation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
import tomllib
import zipfile
from collections import Counter
from email.parser import Parser
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

_DISTRIBUTION_NAME = "miniproto"
_EXPECTED_WHEEL_COUNT = 24
_EXPECTED_ABIS = {("cp313", "cp313"), ("cp314", "cp314"), ("cp314", "cp314t")}
_SIDECAR_NAMES = {"release-manifest.json", "SHA256SUMS"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SOURCE_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_VERSION_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)+(?:[A-Za-z0-9.!+_-]*)$")


class ReleaseArtifactError(ValueError):
    """Report a malformed, incomplete, mismatched, or modified release candidate."""


def _normalize_distribution_name(value: str) -> str:
    """Normalize a Python distribution name for equality checks.

    Args:
        value: Distribution name from package metadata.

    Returns:
        Lowercase PEP 503-style normalized distribution name.
    """
    return re.sub(r"[-_.]+", "-", value).lower()


def _validate_version(value: str) -> str:
    """Validate a release version before using it in filenames or tags.

    Args:
        value: Exact version supplied by the workflow or caller.

    Returns:
        The validated version unchanged.

    Raises:
        ReleaseArtifactError: The version is empty or contains unsafe syntax.
    """
    if not _VERSION_RE.fullmatch(value):
        raise ReleaseArtifactError(f"invalid release version: {value!r}")
    return value


def _validate_source_sha(value: str) -> str:
    """Validate a full lowercase Git commit SHA.

    Args:
        value: Commit identity recorded by GitHub Actions.

    Returns:
        The validated SHA unchanged.

    Raises:
        ReleaseArtifactError: The value is not a 40-character lowercase hexadecimal SHA.
    """
    if not _SOURCE_SHA_RE.fullmatch(value):
        raise ReleaseArtifactError(f"invalid source SHA: {value!r}")
    return value


def _positive_int(value: str) -> int:
    """Parse a positive integer for argparse.

    Args:
        value: Command-line integer text.

    Returns:
        Parsed positive integer.

    Raises:
        argparse.ArgumentTypeError: The value is not a positive integer.
    """
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def _sha256(path: Path) -> str:
    """Hash one artifact without loading the complete file into memory.

    Args:
        path: Artifact file to hash.

    Returns:
        Lowercase hexadecimal SHA-256 digest.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _metadata_identity(payload: bytes, source: str) -> tuple[str, str]:
    """Read a Python package name and version from core metadata.

    Args:
        payload: UTF-8-compatible METADATA or PKG-INFO bytes.
        source: Human-readable archive member used in failures.

    Returns:
        Normalized distribution name and exact version.

    Raises:
        ReleaseArtifactError: Required package metadata is absent or malformed.
    """
    message = Parser().parsestr(payload.decode("utf-8"))
    name = message.get("Name")
    version = message.get("Version")
    if not name or not version:
        raise ReleaseArtifactError(f"missing Name or Version metadata in {source}")
    return _normalize_distribution_name(name), version


def _single_member(names: Sequence[str], suffix: str, source: Path) -> str:
    """Select exactly one archive member ending with a required suffix.

    Args:
        names: Archive member names.
        suffix: Required path suffix.
        source: Archive path used in failures.

    Returns:
        The unique matching member name.

    Raises:
        ReleaseArtifactError: The archive has zero or multiple matching members.
    """
    matches = [name for name in names if name.endswith(suffix)]
    if len(matches) != 1:
        raise ReleaseArtifactError(f"expected one {suffix} member in {source.name}, found {matches}")
    return matches[0]


def _validate_python_identity(name: str, embedded_version: str, expected_version: str, source: Path) -> None:
    """Require one Python distribution to identify as the expected release.

    Args:
        name: Normalized embedded distribution name.
        embedded_version: Version read from archive metadata.
        expected_version: Version selected for the release.
        source: Artifact path used in failures.

    Raises:
        ReleaseArtifactError: The embedded package identity differs from the release identity.
    """
    if name != _DISTRIBUTION_NAME:
        raise ReleaseArtifactError(f"unexpected embedded distribution name in {source.name}: {name}")
    if embedded_version != expected_version:
        raise ReleaseArtifactError(
            f"embedded version mismatch in {source.name}: expected {expected_version}, found {embedded_version}"
        )


def _validate_wheel(path: Path, version: str) -> tuple[str, str, str]:
    """Validate one wheel filename and its embedded METADATA identity.

    Args:
        path: Wheel archive to inspect.
        version: Exact release version.

    Returns:
        Python tag, ABI tag, and platform tag from the wheel filename.

    Raises:
        ReleaseArtifactError: The filename, archive, or metadata does not match the release.
    """
    parts = path.name.removesuffix(".whl").split("-", 4)
    if len(parts) != 5:
        raise ReleaseArtifactError(f"malformed wheel filename: {path.name}")
    distribution, filename_version, python_tag, abi_tag, platform_tag = parts
    if _normalize_distribution_name(distribution) != _DISTRIBUTION_NAME or filename_version != version:
        raise ReleaseArtifactError(f"wheel filename does not match miniproto {version}: {path.name}")
    try:
        with zipfile.ZipFile(path) as archive:
            metadata_name = _single_member(archive.namelist(), ".dist-info/METADATA", path)
            name, embedded_version = _metadata_identity(archive.read(metadata_name), f"{path.name}:{metadata_name}")
    except (OSError, UnicodeDecodeError, zipfile.BadZipFile) as exc:
        raise ReleaseArtifactError(f"invalid wheel archive {path.name}: {exc}") from exc
    _validate_python_identity(name, embedded_version, version, path)
    return python_tag, abi_tag, platform_tag


def _validate_sdist(path: Path, version: str) -> None:
    """Validate the Python sdist filename and embedded PKG-INFO identity.

    Args:
        path: Source distribution to inspect.
        version: Exact release version.

    Raises:
        ReleaseArtifactError: The filename, archive, or metadata does not match the release.
    """
    expected_name = f"{_DISTRIBUTION_NAME}-{version}.tar.gz"
    if path.name != expected_name:
        raise ReleaseArtifactError(f"unexpected Python sdist filename: {path.name}; expected {expected_name}")
    try:
        with tarfile.open(path, "r:gz") as archive:
            member_name = _single_member(archive.getnames(), "/PKG-INFO", path)
            member = archive.extractfile(member_name)
            if member is None:
                raise ReleaseArtifactError(f"cannot read {member_name} from {path.name}")
            name, embedded_version = _metadata_identity(member.read(), f"{path.name}:{member_name}")
    except (OSError, tarfile.TarError, UnicodeDecodeError) as exc:
        raise ReleaseArtifactError(f"invalid Python sdist {path.name}: {exc}") from exc
    _validate_python_identity(name, embedded_version, version, path)


def _validate_crate(path: Path, version: str) -> None:
    """Validate the Cargo source package filename and normalized manifest.

    Args:
        path: Cargo `.crate` source archive to inspect.
        version: Exact release version.

    Raises:
        ReleaseArtifactError: The filename, archive, package name, or version does not match the release.
    """
    expected_name = f"{_DISTRIBUTION_NAME}-{version}.crate"
    if path.name != expected_name:
        raise ReleaseArtifactError(f"unexpected Cargo package filename: {path.name}; expected {expected_name}")
    try:
        with tarfile.open(path, "r:gz") as archive:
            member_name = _single_member(archive.getnames(), f"{_DISTRIBUTION_NAME}-{version}/Cargo.toml", path)
            member = archive.extractfile(member_name)
            if member is None:
                raise ReleaseArtifactError(f"cannot read {member_name} from {path.name}")
            manifest = tomllib.loads(member.read().decode("utf-8"))
    except (OSError, tarfile.TarError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ReleaseArtifactError(f"invalid Cargo package {path.name}: {exc}") from exc
    package = manifest.get("package")
    if not isinstance(package, dict):
        raise ReleaseArtifactError(f"missing [package] metadata in {path.name}")
    if package.get("name") != _DISTRIBUTION_NAME:
        raise ReleaseArtifactError(f"unexpected Cargo package name in {path.name}: {package.get('name')!r}")
    if package.get("version") != version:
        raise ReleaseArtifactError(
            f"embedded version mismatch in {path.name}: expected {version}, found {package.get('version')!r}"
        )


def _distribution_paths(artifacts_dir: Path) -> list[Path]:
    """Select direct release files while permitting the two generated sidecars.

    Args:
        artifacts_dir: Directory populated by raw workflow artifact downloads.

    Returns:
        Sorted paths for wheels, the Python sdist, and the Cargo package.

    Raises:
        ReleaseArtifactError: The directory is absent, nested, or contains an unexpected file.
    """
    if not artifacts_dir.is_dir():
        raise ReleaseArtifactError(f"artifact directory does not exist: {artifacts_dir}")
    selected: list[Path] = []
    unexpected: list[str] = []
    for path in sorted(artifacts_dir.iterdir(), key=lambda item: item.name):
        if path.name in _SIDECAR_NAMES and path.is_file():
            continue
        if path.is_file() and (path.suffix == ".whl" or path.suffix == ".crate" or path.name.endswith(".tar.gz")):
            selected.append(path)
        else:
            unexpected.append(path.name)
    if unexpected:
        raise ReleaseArtifactError(f"unexpected files or directories in release candidate: {unexpected}")
    return selected


def _collect_artifacts(artifacts_dir: Path, version: str) -> list[dict[str, object]]:
    """Validate the complete release matrix and describe every distribution.

    Args:
        artifacts_dir: Directory containing raw release distributions.
        version: Exact release version.

    Returns:
        Sorted JSON-compatible artifact records.

    Raises:
        ReleaseArtifactError: Counts, ABI coverage, filenames, metadata, or archive bytes are invalid.
    """
    paths = _distribution_paths(artifacts_dir)
    wheels = [path for path in paths if path.suffix == ".whl"]
    sdists = [path for path in paths if path.name.endswith(".tar.gz")]
    crates = [path for path in paths if path.suffix == ".crate"]
    if len(wheels) != _EXPECTED_WHEEL_COUNT or len(sdists) != 1 or len(crates) != 1:
        raise ReleaseArtifactError(
            f"expected 24 wheels, one Python sdist, and one Cargo package; found {len(wheels)}, {len(sdists)}, {len(crates)}"
        )

    wheel_tags = [_validate_wheel(path, version) for path in wheels]
    abi_counts = Counter((python_tag, abi_tag) for python_tag, abi_tag, _platform_tag in wheel_tags)
    if set(abi_counts) != _EXPECTED_ABIS or set(abi_counts.values()) != {8}:
        raise ReleaseArtifactError(f"unexpected wheel ABI coverage: {dict(sorted(abi_counts.items()))}")
    platform_sets = {
        abi: {platform_tag for python_tag, abi_tag, platform_tag in wheel_tags if (python_tag, abi_tag) == abi}
        for abi in _EXPECTED_ABIS
    }
    if (
        any(len(platforms) != 8 for platforms in platform_sets.values())
        or len({frozenset(v) for v in platform_sets.values()}) != 1
    ):
        raise ReleaseArtifactError(f"wheel platform coverage differs between ABIs: {platform_sets}")

    _validate_sdist(sdists[0], version)
    _validate_crate(crates[0], version)
    records: list[dict[str, object]] = []
    for path in paths:
        kind = "wheel" if path.suffix == ".whl" else "crate" if path.suffix == ".crate" else "sdist"
        records.append({"kind": kind, "name": path.name, "sha256": _sha256(path), "size": path.stat().st_size})
    return records


def build_release_manifest(
    *,
    artifacts_dir: Path,
    output_dir: Path,
    version: str,
    repository: str,
    workflow: str,
    run_id: int,
    run_attempt: int,
    source_sha: str,
    source_ref: str,
    event: str,
) -> tuple[Path, Path]:
    """Create checksums and provenance for one complete build workflow run.

    Args:
        artifacts_dir: Directory containing exactly 24 wheels, one Python sdist, and one Cargo package.
        output_dir: Directory receiving `release-manifest.json` and `SHA256SUMS`.
        version: Exact shared Python and Cargo version.
        repository: GitHub `owner/repository` identity that built the artifacts.
        workflow: Repository-relative signer workflow path.
        run_id: Positive GitHub Actions build run ID.
        run_attempt: Positive GitHub Actions attempt number for the run.
        source_sha: Full source commit SHA built by the workflow.
        source_ref: Git ref used to dispatch the build.
        event: GitHub Actions event; release builds require `workflow_dispatch`.

    Returns:
        Manifest path followed by checksum-file path.

    Raises:
        ReleaseArtifactError: Provenance fields or any distribution fail validation.
    """
    version = _validate_version(version)
    source_sha = _validate_source_sha(source_sha)
    if run_id <= 0 or run_attempt <= 0:
        raise ReleaseArtifactError("run ID and run attempt must be positive")
    if event != "workflow_dispatch":
        raise ReleaseArtifactError(f"release artifacts must come from workflow_dispatch, not {event!r}")
    if not repository or "/" not in repository:
        raise ReleaseArtifactError(f"invalid repository identity: {repository!r}")
    if not workflow.startswith(".github/workflows/") or not workflow.endswith((".yml", ".yaml")):
        raise ReleaseArtifactError(f"invalid signer workflow path: {workflow!r}")
    if not source_ref:
        raise ReleaseArtifactError("source ref must not be empty")

    artifacts = _collect_artifacts(artifacts_dir, version)
    counts = dict(sorted(Counter(str(item["kind"]) for item in artifacts).items()))
    manifest: dict[str, Any] = {
        "artifacts": artifacts,
        "counts": counts,
        "event": event,
        "repository": repository,
        "run_attempt": run_attempt,
        "run_id": run_id,
        "schema_version": 1,
        "source_ref": source_ref,
        "source_sha": source_sha,
        "tag": f"v{version}",
        "version": version,
        "workflow": workflow,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "release-manifest.json"
    checksums_path = output_dir / "SHA256SUMS"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    checksums_path.write_text(
        "".join(f"{item['sha256']}  {item['name']}\n" for item in artifacts), encoding="utf-8", newline="\n"
    )
    return manifest_path, checksums_path


def _load_manifest(path: Path) -> dict[str, Any]:
    """Load a JSON object from a release manifest.

    Args:
        path: Manifest path to read.

    Returns:
        Parsed manifest object.

    Raises:
        ReleaseArtifactError: The file is unreadable, invalid JSON, or not an object.
    """
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseArtifactError(f"cannot read release manifest {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseArtifactError("release manifest root must be a JSON object")
    return value


def _load_checksums(path: Path) -> dict[str, str]:
    """Parse the strict two-space SHA256SUMS format emitted by this module.

    Args:
        path: Checksum file to read.

    Returns:
        Mapping from artifact filename to lowercase SHA-256 digest.

    Raises:
        ReleaseArtifactError: A line is malformed, duplicated, or uses an invalid digest.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ReleaseArtifactError(f"cannot read checksum file {path}: {exc}") from exc
    checksums: dict[str, str] = {}
    for line_number, line in enumerate(lines, start=1):
        digest, separator, name = line.partition("  ")
        if separator != "  " or not _SHA256_RE.fullmatch(digest) or not name or Path(name).name != name:
            raise ReleaseArtifactError(f"malformed checksum line {line_number}: {line!r}")
        if name in checksums:
            raise ReleaseArtifactError(f"duplicate checksum entry: {name}")
        checksums[name] = digest
    return checksums


def verify_release_manifest(
    *,
    artifacts_dir: Path,
    manifest_path: Path,
    checksums_path: Path,
    expected_version: str,
    expected_repository: str,
    expected_workflow: str,
    expected_run_id: int,
    expected_run_attempt: int,
    expected_source_sha: str,
    expected_event: str,
) -> dict[str, Any]:
    """Re-validate artifacts and bind them to expected GitHub run metadata.

    Args:
        artifacts_dir: Directory containing downloaded raw distributions and optional sidecars.
        manifest_path: Build-generated release manifest.
        checksums_path: Build-generated SHA256SUMS file.
        expected_version: Version requested by the publication workflow.
        expected_repository: Repository authenticated by the publication workflow.
        expected_workflow: Exact build workflow path trusted as the signer.
        expected_run_id: Build run selected by the publication input.
        expected_run_attempt: Exact attempt number returned by the GitHub Actions run API.
        expected_source_sha: Commit SHA returned by the GitHub Actions run API.
        expected_event: Required source event, normally `workflow_dispatch`.

    Returns:
        The verified release manifest.

    Raises:
        ReleaseArtifactError: Context, counts, filenames, metadata, checksums, or artifact bytes differ.
    """
    expected_version = _validate_version(expected_version)
    expected_source_sha = _validate_source_sha(expected_source_sha)
    manifest = _load_manifest(manifest_path)
    expected_context: dict[str, object] = {
        "event": expected_event,
        "repository": expected_repository,
        "run_attempt": expected_run_attempt,
        "run_id": expected_run_id,
        "schema_version": 1,
        "source_sha": expected_source_sha,
        "tag": f"v{expected_version}",
        "version": expected_version,
        "workflow": expected_workflow,
    }
    for key, expected in expected_context.items():
        if manifest.get(key) != expected:
            raise ReleaseArtifactError(f"manifest {key} mismatch: expected {expected!r}, found {manifest.get(key)!r}")
    if expected_run_attempt <= 0:
        raise ReleaseArtifactError(f"invalid expected run attempt: {expected_run_attempt!r}")
    if not isinstance(manifest.get("source_ref"), str) or not manifest["source_ref"]:
        raise ReleaseArtifactError("manifest source ref is missing")

    actual_artifacts = _collect_artifacts(artifacts_dir, expected_version)
    if manifest.get("artifacts") != actual_artifacts:
        raise ReleaseArtifactError("manifest artifact records or digests differ from downloaded files")
    actual_counts = dict(sorted(Counter(str(item["kind"]) for item in actual_artifacts).items()))
    if manifest.get("counts") != actual_counts:
        raise ReleaseArtifactError(
            f"manifest counts differ: expected {actual_counts}, found {manifest.get('counts')!r}"
        )
    expected_checksums = {str(item["name"]): str(item["sha256"]) for item in actual_artifacts}
    actual_checksums = _load_checksums(checksums_path)
    if actual_checksums != expected_checksums:
        raise ReleaseArtifactError("checksum file entries or digests differ from downloaded files")
    return manifest


def _parser() -> argparse.ArgumentParser:
    """Build the side-effect-free command-line parser.

    Returns:
        Configured parser with `manifest` and `verify` subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="miniproto-release-artifacts",
        description="Create or verify checksums and provenance for a complete miniproto release candidate.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest = subparsers.add_parser("manifest", help="Validate a build run and create its manifest sidecars.")
    manifest.add_argument("--artifacts-dir", type=Path, required=True, help="Directory with raw release distributions.")
    manifest.add_argument("--output-dir", type=Path, required=True, help="Directory receiving manifest sidecars.")
    manifest.add_argument("--version", required=True, help="Exact shared Python and Cargo version.")
    manifest.add_argument("--repository", required=True, help="GitHub owner/repository identity.")
    manifest.add_argument("--workflow", required=True, help="Repository-relative signer workflow path.")
    manifest.add_argument("--run-id", type=_positive_int, required=True, help="Positive GitHub Actions run ID.")
    manifest.add_argument("--run-attempt", type=_positive_int, required=True, help="Positive workflow attempt number.")
    manifest.add_argument("--source-sha", required=True, help="Full source commit SHA.")
    manifest.add_argument("--source-ref", required=True, help="Git ref used to dispatch the build.")
    manifest.add_argument("--event", required=True, help="GitHub Actions event that created the build.")

    verify = subparsers.add_parser("verify", help="Re-validate downloaded distributions and build provenance.")
    verify.add_argument(
        "--artifacts-dir", type=Path, required=True, help="Directory with raw distributions and sidecars."
    )
    verify.add_argument("--manifest", type=Path, required=True, help="Path to release-manifest.json.")
    verify.add_argument("--checksums", type=Path, required=True, help="Path to SHA256SUMS.")
    verify.add_argument("--version", required=True, help="Exact release version requested for publication.")
    verify.add_argument("--repository", required=True, help="Expected GitHub owner/repository identity.")
    verify.add_argument("--workflow", required=True, help="Expected repository-relative signer workflow path.")
    verify.add_argument("--run-id", type=_positive_int, required=True, help="Expected positive build run ID.")
    verify.add_argument(
        "--run-attempt", type=_positive_int, required=True, help="Expected positive workflow attempt number."
    )
    verify.add_argument("--source-sha", required=True, help="Expected full source commit SHA.")
    verify.add_argument("--event", required=True, help="Expected source workflow event.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run release manifest generation or verification.

    Args:
        argv: Optional argument sequence; defaults to process arguments.

    Returns:
        Zero when validation succeeds. Invalid candidates terminate with status one, while argparse usage errors use status two.
    """
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "manifest":
            manifest_path, checksums_path = build_release_manifest(
                artifacts_dir=args.artifacts_dir,
                output_dir=args.output_dir,
                version=args.version,
                repository=args.repository,
                workflow=args.workflow,
                run_id=args.run_id,
                run_attempt=args.run_attempt,
                source_sha=args.source_sha,
                source_ref=args.source_ref,
                event=args.event,
            )
            print(f"Validated 24 wheels, one Python sdist, and one Cargo package for miniproto {args.version}.")
            print(f"Wrote {manifest_path} and {checksums_path}.")
            return 0
        manifest = verify_release_manifest(
            artifacts_dir=args.artifacts_dir,
            manifest_path=args.manifest,
            checksums_path=args.checksums,
            expected_version=args.version,
            expected_repository=args.repository,
            expected_workflow=args.workflow,
            expected_run_id=args.run_id,
            expected_run_attempt=args.run_attempt,
            expected_source_sha=args.source_sha,
            expected_event=args.event,
        )
        print(
            f"Verified {len(manifest['artifacts'])} release distributions from build run {manifest['run_id']} "
            f"at {manifest['source_sha']}."
        )
        return 0
    except ReleaseArtifactError as exc:
        parser.exit(1, f"release artifact validation failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())

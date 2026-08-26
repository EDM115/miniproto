from __future__ import annotations

import hashlib
import importlib
import io
import json
import tarfile
import zipfile
from pathlib import Path
from types import ModuleType

import pytest


def _release_artifacts_module() -> ModuleType:
    """Import the release-artifact module after the test has started.

    Returns:
        The imported release-artifact module.
    """
    return importlib.import_module("tools.release_artifacts")


def _write_wheel(path: Path, version: str) -> None:
    """Create a minimal wheel-shaped ZIP with embedded package metadata.

    Args:
        path: Destination wheel path.
        version: Package version written into the wheel metadata.
    """
    metadata = f"Metadata-Version: 2.4\nName: miniproto\nVersion: {version}\n\n"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(f"miniproto-{version}.dist-info/METADATA", metadata)


def _write_tar_member(archive: tarfile.TarFile, name: str, payload: bytes) -> None:
    """Write one deterministic in-memory member to a tar archive.

    Args:
        archive: Open tar archive receiving the member.
        name: Archive-relative member name.
        payload: Member bytes.
    """
    info = tarfile.TarInfo(name)
    info.size = len(payload)
    info.mtime = 0
    archive.addfile(info, io.BytesIO(payload))


def _write_sdist(path: Path, version: str) -> None:
    """Create a minimal Python source distribution with PKG-INFO metadata.

    Args:
        path: Destination source-distribution path.
        version: Package version written into PKG-INFO.
    """
    metadata = f"Metadata-Version: 2.4\nName: miniproto\nVersion: {version}\n\n".encode()
    with tarfile.open(path, "w:gz") as archive:
        _write_tar_member(archive, f"miniproto-{version}/PKG-INFO", metadata)


def _write_crate(path: Path, version: str) -> None:
    """Create a minimal Cargo source package with normalized manifest metadata.

    Args:
        path: Destination Cargo package path.
        version: Package version written into Cargo.toml.
    """
    manifest = f'[package]\nname = "miniproto"\nversion = "{version}"\n'.encode()
    with tarfile.open(path, "w:gz") as archive:
        _write_tar_member(archive, f"miniproto-{version}/Cargo.toml", manifest)


def _release_fixture(root: Path, version: str = "0.1.0") -> Path:
    """Create the complete supported release-artifact matrix.

    Args:
        root: Directory receiving synthetic artifacts.
        version: Version shared by filenames and embedded metadata.

    Returns:
        The populated artifact directory.
    """
    root.mkdir(parents=True)
    platforms = (
        "manylinux_2_17_x86_64",
        "manylinux_2_17_aarch64",
        "musllinux_1_2_x86_64",
        "musllinux_1_2_aarch64",
        "win_amd64",
        "win_arm64",
        "macosx_10_12_x86_64",
        "macosx_11_0_arm64",
    )
    for abi in ("cp313-cp313", "cp314-cp314", "cp314-cp314t"):
        for platform in platforms:
            _write_wheel(root / f"miniproto-{version}-{abi}-{platform}.whl", version)
    _write_sdist(root / f"miniproto-{version}.tar.gz", version)
    _write_crate(root / f"miniproto-{version}.crate", version)
    return root


def _manifest_kwargs(artifacts: Path, output: Path) -> dict[str, object]:
    """Return stable provenance fields for manifest tests.

    Args:
        artifacts: Directory containing release distributions.
        output: Directory receiving manifest files.

    Returns:
        Keyword arguments accepted by the manifest builder.
    """
    return {
        "artifacts_dir": artifacts,
        "output_dir": output,
        "version": "0.1.0",
        "repository": "EDM115/miniproto",
        "workflow": ".github/workflows/build-wheels.yml",
        "run_id": 123456,
        "run_attempt": 2,
        "source_sha": "a" * 40,
        "source_ref": "refs/heads/master",
        "event": "workflow_dispatch",
    }


def test_manifest_records_and_verifies_the_complete_release_candidate(tmp_path: Path) -> None:
    """The build manifest must bind all 24 wheels and both source packages."""
    module = _release_artifacts_module()
    artifacts = _release_fixture(tmp_path / "artifacts")
    output = tmp_path / "manifest"

    manifest_path, checksums_path = module.build_release_manifest(**_manifest_kwargs(artifacts, output))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == 1
    assert manifest["version"] == "0.1.0"
    assert manifest["tag"] == "v0.1.0"
    assert manifest["counts"] == {"crate": 1, "sdist": 1, "wheel": 24}
    assert len(manifest["artifacts"]) == 26
    assert [item["name"] for item in manifest["artifacts"]] == sorted(item["name"] for item in manifest["artifacts"])
    expected_checksum_lines = [f"{item['sha256']}  {item['name']}" for item in manifest["artifacts"]]
    assert checksums_path.read_text(encoding="utf-8").splitlines() == expected_checksum_lines

    verified = module.verify_release_manifest(
        artifacts_dir=artifacts,
        manifest_path=manifest_path,
        checksums_path=checksums_path,
        expected_version="0.1.0",
        expected_repository="EDM115/miniproto",
        expected_workflow=".github/workflows/build-wheels.yml",
        expected_run_id=123456,
        expected_run_attempt=2,
        expected_source_sha="a" * 40,
        expected_event="workflow_dispatch",
    )
    assert verified == manifest


def test_manifest_verification_rejects_modified_artifact_bytes(tmp_path: Path) -> None:
    """Checksum verification must reject an artifact changed after the build run."""
    module = _release_artifacts_module()
    artifacts = _release_fixture(tmp_path / "artifacts")
    manifest_path, checksums_path = module.build_release_manifest(**_manifest_kwargs(artifacts, tmp_path / "manifest"))
    wheel = next(artifacts.glob("*.whl"))
    wheel.write_bytes(wheel.read_bytes() + b"tampered")

    with pytest.raises(module.ReleaseArtifactError, match="digest"):
        module.verify_release_manifest(
            artifacts_dir=artifacts,
            manifest_path=manifest_path,
            checksums_path=checksums_path,
            expected_version="0.1.0",
            expected_repository="EDM115/miniproto",
            expected_workflow=".github/workflows/build-wheels.yml",
            expected_run_id=123456,
            expected_run_attempt=2,
            expected_source_sha="a" * 40,
            expected_event="workflow_dispatch",
        )


def test_manifest_builder_rejects_embedded_distribution_version_mismatch(tmp_path: Path) -> None:
    """Filename-only version agreement must not conceal mismatched archive metadata."""
    module = _release_artifacts_module()
    artifacts = _release_fixture(tmp_path / "artifacts")
    wheel = next(artifacts.glob("*.whl"))
    _write_wheel(wheel, "0.1.1")

    with pytest.raises(module.ReleaseArtifactError, match="embedded version"):
        module.build_release_manifest(**_manifest_kwargs(artifacts, tmp_path / "manifest"))


def test_manifest_builder_rejects_unexpected_release_files(tmp_path: Path) -> None:
    """The release candidate must contain exactly the approved distribution set."""
    module = _release_artifacts_module()
    artifacts = _release_fixture(tmp_path / "artifacts")
    (artifacts / "unexpected.txt").write_text("not a release artifact", encoding="utf-8")

    with pytest.raises(module.ReleaseArtifactError, match="unexpected"):
        module.build_release_manifest(**_manifest_kwargs(artifacts, tmp_path / "manifest"))


def test_checksum_values_are_sha256_of_the_recorded_files(tmp_path: Path) -> None:
    """Manifest digests must use the actual artifact bytes and SHA-256."""
    module = _release_artifacts_module()
    artifacts = _release_fixture(tmp_path / "artifacts")
    manifest_path, _checksums_path = module.build_release_manifest(**_manifest_kwargs(artifacts, tmp_path / "manifest"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for item in manifest["artifacts"]:
        assert item["sha256"] == hashlib.sha256((artifacts / item["name"]).read_bytes()).hexdigest()


def test_manifest_verification_rejects_a_different_workflow_attempt(tmp_path: Path) -> None:
    """A rerun must not accept provenance sidecars from another run attempt."""
    module = _release_artifacts_module()
    artifacts = _release_fixture(tmp_path / "artifacts")
    manifest_path, checksums_path = module.build_release_manifest(**_manifest_kwargs(artifacts, tmp_path / "manifest"))

    with pytest.raises(module.ReleaseArtifactError, match="run_attempt"):
        module.verify_release_manifest(
            artifacts_dir=artifacts,
            manifest_path=manifest_path,
            checksums_path=checksums_path,
            expected_version="0.1.0",
            expected_repository="EDM115/miniproto",
            expected_workflow=".github/workflows/build-wheels.yml",
            expected_run_id=123456,
            expected_run_attempt=3,
            expected_source_sha="a" * 40,
            expected_event="workflow_dispatch",
        )

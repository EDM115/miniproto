from __future__ import annotations

import hashlib
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from email.message import Message
from pathlib import Path
from types import ModuleType

import pytest
import yaml


def _release_artifacts_module() -> ModuleType:
    """Import the release-artifact module after the test has started.

    Returns:
        The imported release-artifact module.
    """
    return importlib.import_module("tools.release_artifacts")


def _release_workflow_bash() -> str:
    """Locate Bash for executing publication steps with mocked external commands.

    Returns:
        Bash executable path, preferring Git Bash on Windows.
    """
    bash = shutil.which("bash")
    git = shutil.which("git")
    if os.name == "nt" and git is not None:
        bash = next(
            (
                str(parent / "bin/bash.exe")
                for parent in Path(git).resolve().parents
                if (parent / "bin/bash.exe").is_file()
            ),
            bash,
        )
    if bash is None:
        pytest.skip("Bash is required to execute the release workflow step")
    return bash


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


@pytest.mark.parametrize("next_release", ["", "## `v0.0.98` - Previous release\nOlder notes\n"])
def test_release_notes_extract_only_the_first_level_two_section(tmp_path: Path, next_release: str) -> None:
    module = _release_artifacts_module()
    changelog = tmp_path / "CHANGELOG.md"
    notes = "\n### Features\n\nNew behavior  \nSecond line\n\n```markdown\n## Example inside a code fence\n```\n\n"
    changelog.write_text(
        "# Project changelog\n\nIntroductory text\n\n## `v0.1.0` - First Alpha release\n" + notes + next_release,
        encoding="utf-8",
    )
    output = tmp_path / "release-metadata"

    result = module.main(["notes", "--changelog", str(changelog), "--output-dir", str(output)])

    assert result == 0
    assert (output / "release-title.txt").read_text(encoding="utf-8") == "v0.1.0 - First Alpha release\n"
    assert (output / "release-notes.md").read_text(encoding="utf-8") == notes


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        ("## `v0.1.0` - **First _Alpha_ release**", "v0.1.0 - First Alpha release"),
        ("  ## [v0.1.0](https://example.com/release) - *Alpha* ###", "v0.1.0 - Alpha"),
        ("## `v0.1.0_alpha` - release_candidate", "v0.1.0_alpha - release_candidate"),
        ("## ``v0.1.0_**literal**`` - ~~Preview~~", "v0.1.0_**literal** - Preview"),
    ],
)
def test_release_notes_render_the_heading_as_plain_text(heading: str, expected: str) -> None:
    module = _release_artifacts_module()

    title, notes = module.extract_changelog_release(f"{heading}\nRelease notes\n")

    assert title == expected
    assert notes == "Release notes\n"


def test_release_notes_ignore_fenced_headings_before_the_release() -> None:
    module = _release_artifacts_module()
    changelog = "~~~markdown\n## Not a release\n~~~~\n## `v0.1.0` - Alpha\nNotes\n"

    assert module.extract_changelog_release(changelog) == ("v0.1.0 - Alpha", "Notes\n")


@pytest.mark.parametrize("changelog", ["# Changelog\n### Features\n", "## \nNotes\n", "## ``\nNotes\n"])
def test_release_notes_reject_a_missing_or_empty_release_heading(changelog: str) -> None:
    module = _release_artifacts_module()

    with pytest.raises(module.ReleaseArtifactError, match="heading"):
        module.extract_changelog_release(changelog)


@pytest.mark.parametrize(
    ("registry_case", "expected_status", "should_publish"),
    [
        ("missing", 0, True),
        ("identical", 0, False),
        ("different", 1, False),
        ("forbidden", 1, False),
        ("unavailable", 1, False),
    ],
)
def test_crates_publication_checks_metadata_before_downloading(
    tmp_path: Path, registry_case: str, expected_status: int, should_publish: bool
) -> None:
    bash = _release_workflow_bash()
    workflow = yaml.safe_load(
        (Path(__file__).resolve().parents[1] / ".github/workflows/publish-release.yml").read_text(encoding="utf-8")
    )
    commands = workflow["jobs"]["crates"]["steps"][-1]["run"]
    (tmp_path / "verified-crate").mkdir()
    (tmp_path / "verified-crate/miniproto-0.0.99.crate").write_bytes(b"attested crate bytes")
    mocks = r"""
curl() {
  local output='' url='' status=200 body='attested crate bytes' write_status=false fail=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --output) output="$2"; shift 2 ;;
      --write-out) write_status=true; shift 2 ;;
      --user-agent) printf '%s\n' "$2" >> user-agents.txt; shift 2 ;;
      --fail) fail=true; shift ;;
      https://*) url="$1"; shift ;;
      *) shift ;;
    esac
  done
  printf '%s\n' "$url" >> requests.txt
  if [[ "$REGISTRY_CASE" == forbidden ]]; then
    status=403
  elif [[ "$REGISTRY_CASE" == unavailable ]]; then
    status=503
  elif [[ "$url" != */download ]]; then
    if [[ "$REGISTRY_CASE" == missing ]]; then status=404; fi
    body='{"version":{}}'
  elif [[ "$REGISTRY_CASE" == missing && ! -f published ]]; then
    status=403
  elif [[ "$REGISTRY_CASE" == different ]]; then
    body='different crate bytes'
  fi
  printf '%s' "$body" > "$output"
  if [[ "$write_status" == true ]]; then printf '%s' "$status"; fi
  if [[ "$fail" == true && "$status" -ge 400 ]]; then return 22; fi
}
cargo() { printf '%s\n' "$*" >> cargo-calls.txt; touch published; }
sleep() { :; }
"""
    script = tmp_path / "publish.sh"
    script.write_text(mocks + commands, encoding="utf-8", newline="")

    result = subprocess.run(  # noqa: S603 - Execute repository workflow code with mocked publication commands
        [bash, "--noprofile", "--norc", script.as_posix()],
        cwd=tmp_path,
        env={**os.environ, "RELEASE_VERSION": "0.0.99", "REGISTRY_CASE": registry_case},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == expected_status, result.stdout + result.stderr
    assert (tmp_path / "published").exists() is should_publish
    requests = (tmp_path / "requests.txt").read_text().splitlines()
    assert requests[0] == "https://crates.io/api/v1/crates/miniproto/0.0.99"
    assert all(agent for agent in (tmp_path / "user-agents.txt").read_text().splitlines())
    if should_publish:
        assert (tmp_path / "cargo-calls.txt").read_text().splitlines() == ["publish --locked -p miniproto"]
    if expected_status == 0:
        assert (tmp_path / "registry-miniproto-0.0.99.crate").read_bytes() == b"attested crate bytes"


@pytest.mark.parametrize(
    ("release_case", "expected_status", "expected_mutation"),
    [
        ("absent", 0, "create"),
        ("complete", 0, "edit"),
        ("partial", 0, "edit"),
        ("other-sha", 1, None),
        ("published", 1, None),
        ("extra-asset", 1, None),
        ("different-bytes", 1, None),
        ("lookup-forbidden", 22, None),
        ("metadata-unavailable", 22, None),
        ("duplicates", 1, None),
    ],
)
def test_github_publication_resumes_only_a_matching_draft(
    tmp_path: Path, release_case: str, expected_status: int, expected_mutation: str | None
) -> None:
    repo = Path(__file__).resolve().parents[1]
    workflow = yaml.safe_load((repo / ".github/workflows/publish-release.yml").read_text(encoding="utf-8"))
    commands = workflow["jobs"]["draft-release"]["steps"][-1]["run"]
    (tmp_path / "CHANGELOG.md").write_text("## `v0.1.0` - Alpha\nNotes\n", encoding="utf-8")
    (tmp_path / "release-assets").mkdir()
    artifacts = {"example.whl": b"attested wheel", "release-manifest.json": b"attested manifest"}
    for name, data in artifacts.items():
        (tmp_path / "release-assets" / name).write_bytes(data)
    remote = {
        "draft": release_case != "published",
        "target_commitish": ("b" if release_case == "other-sha" else "a") * 40,
        "assets": [
            {"name": name, "digest": "sha256:" + hashlib.sha256(data).hexdigest()}
            for name, data in artifacts.items()
            if release_case != "partial" or name == "release-manifest.json"
        ],
    }
    if release_case == "extra-asset":
        remote["assets"].append({"name": "unexpected.whl"})
    if release_case == "different-bytes":
        remote["assets"][0]["digest"] = "sha256:" + "0" * 64
    (tmp_path / "remote-release.json").write_text(json.dumps(remote), encoding="utf-8")
    mocks = r"""
python() { "$RELEASE_TEST_PYTHON" "$@"; }
gh() {
  if [[ "$1" == api ]]; then
    if [[ "$2" == */releases/123 ]]; then
      if [[ "$RELEASE_CASE" == metadata-unavailable ]]; then return 22; fi
      cat remote-release.json
      return 0
    fi
    if [[ "$RELEASE_CASE" == lookup-forbidden ]]; then return 22; fi
    if [[ "$RELEASE_CASE" == absent ]]; then return 0; fi
    if [[ "$RELEASE_CASE" == duplicates ]]; then printf '123\n456\n'; else printf '123\n'; fi
  elif [[ "$1" == release && "$2" == view ]]; then
    cat remote-release.json
  else
    printf '%s\n' "$2" >> gh-mutations.txt
    printf '%s\n' "$*" >> gh-arguments.txt
  fi
}
"""
    script = tmp_path / "draft.sh"
    script.write_text(mocks + commands, encoding="utf-8", newline="")
    result = subprocess.run(  # noqa: S603 - Execute repository workflow code with mocked publication commands
        [_release_workflow_bash(), "--noprofile", "--norc", script.as_posix()],
        cwd=tmp_path,
        env={
            **os.environ,
            "PYTHONPATH": str(repo),
            "RELEASE_TEST_PYTHON": Path(sys.executable).as_posix(),
            "RELEASE_CASE": release_case,
            "RELEASE_TAG": "v0.0.99",
            "PRERELEASE": "true",
            "SOURCE_SHA": "a" * 40,
            "GITHUB_REPOSITORY": "EDM115/miniproto",
        },
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == expected_status, result.stdout + result.stderr
    mutation_log = tmp_path / "gh-mutations.txt"
    expected_mutations = [expected_mutation] if expected_mutation else []
    if release_case in {"absent", "partial"}:
        expected_mutations.append("upload")
    assert (mutation_log.read_text().splitlines() if mutation_log.exists() else []) == expected_mutations
    if expected_mutation:
        arguments = (tmp_path / "gh-arguments.txt").read_text().splitlines()
        assert all("--clobber" not in command for command in arguments)
        assert "--prerelease=true" in arguments[0]
        assert "--draft" in arguments[0]
        if release_case in {"absent", "partial"}:
            assert "release-assets/example.whl" in arguments[-1]
            assert ("release-assets/release-manifest.json" in arguments[-1]) is (release_case == "absent")


@pytest.mark.parametrize(
    "registry_case",
    [
        "missing",
        "identical",
        "partial",
        "forbidden",
        "unavailable",
        "digest-mismatch",
        "download-mismatch",
        "download-forbidden",
        "unexpected-file",
    ],
)
def test_pypi_publication_uses_json_existence_and_verifies_existing_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, registry_case: str
) -> None:
    repo = Path(__file__).resolve().parents[1]
    workflow = yaml.safe_load((repo / ".github/workflows/publish-release.yml").read_text(encoding="utf-8"))
    commands = next(step["run"] for step in workflow["jobs"]["pypi"]["steps"] if step.get("id") == "prepare-pypi")
    code = commands.split("\n", 1)[1].rsplit("\nPY", 1)[0]
    distributions = {
        "miniproto-0.0.99-cp314-cp314-win_amd64.whl": b"attested wheel",
        "miniproto-0.0.99.tar.gz": b"attested sdist",
    }
    (tmp_path / "dist").mkdir()
    for name, data in distributions.items():
        (tmp_path / "dist" / name).write_bytes(data)
    published = []
    for name, data in distributions.items():
        if registry_case == "partial" and name.endswith(".tar.gz"):
            continue
        published.append(
            {
                "filename": name,
                "digests": {
                    "sha256": "0" * 64 if registry_case == "digest-mismatch" else hashlib.sha256(data).hexdigest()
                },
                "url": f"https://files.pythonhosted.org/{name}",
            }
        )
    if registry_case == "unexpected-file":
        published.append({"filename": "unexpected.whl"})
    requests = []

    def fake_urlopen(url: str, *, timeout: int) -> io.BytesIO:
        requests.append(url)
        if url == "https://pypi.org/pypi/miniproto/0.0.99/json":
            status = {"missing": 404, "forbidden": 403, "unavailable": 503}.get(registry_case)
            if status is not None:
                raise urllib.error.HTTPError(url, status, "fixture response", Message(), io.BytesIO())
            return io.BytesIO(json.dumps({"urls": published}).encode())
        if registry_case == "download-forbidden":
            raise urllib.error.HTTPError(url, 403, "fixture response", Message(), io.BytesIO())
        name = url.rsplit("/", 1)[-1]
        return io.BytesIO(b"different bytes" if registry_case == "download-mismatch" else distributions[name])

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("RELEASE_VERSION", "0.0.99")
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "github-output"))
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    if registry_case in {"missing", "identical", "partial"}:
        exec(compile(code, "publish-release/prepare-pypi", "exec"), {})  # noqa: S102 - Execute the workflow step with mocked HTTP
        selected = {path.name: path.read_bytes() for path in (tmp_path / "publish-dist").iterdir()}
        expected = (
            distributions
            if registry_case == "missing"
            else {
                name: data
                for name, data in distributions.items()
                if registry_case == "partial" and name.endswith(".tar.gz")
            }
        )
        assert selected == expected
        outputs = dict(line.split("=", 1) for line in (tmp_path / "github-output").read_text().splitlines())
        assert outputs["has_missing"] == ("true" if expected else "false")
    else:
        with pytest.raises((urllib.error.HTTPError, SystemExit)):
            exec(compile(code, "publish-release/prepare-pypi", "exec"), {})  # noqa: S102 - Execute the workflow step with mocked HTTP
        assert not (tmp_path / "github-output").exists()
    assert requests[0] == "https://pypi.org/pypi/miniproto/0.0.99/json"

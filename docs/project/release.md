---
title: Release
description: Build, attest, verify and publish one synchronized miniproto release to PyPI, crates.io and GitHub.
slug: /project/release/
generated: false
---

miniproto separates unprivileged artifact construction from privileged publication. One manual build run creates the complete release candidate and one separately dispatched publish run verifies that exact run ID before any registry or GitHub release is changed.

The `0.1.x` Cargo package records source provenance for the bundled PyO3 accelerator and stays version-aligned with Python. It does not yet provide a supported standalone Rust library API. Direct Rust use is deferred until the crate exposes an `rlib`, documents a Rust-facing stability policy and passes external-consumer tests.

## Version metadata and historical evidence

`pyproject.toml` and `rust/miniproto/Cargo.toml` declare version `0.1.0`. The [changelog](https://github.com/EDM115/miniproto/blob/master/CHANGELOG.md) describes that Alpha's API and compatibility boundary.

Historical hosted [CI](https://github.com/EDM115/miniproto/actions/runs/32228452630), [documentation](https://github.com/EDM115/miniproto/actions/runs/32228472756) and [24 wheel lanes](https://github.com/EDM115/miniproto/actions/runs/32228463727) passed on 2026-08-19 at commit `c81533922ba63c89337f3959b881109c3b7e5dec`. Those results apply to that commit; later source or dependency changes need fresh validation.

Historical [2026-08-19 run notes](https://github.com/EDM115/miniproto/blob/8ed6b99eb0909f87a90f604026d956c0ad16adaa/PROGRESS.md) cite local reports under `.tmp/wave6-20260819-final2/` and `.tmp/wave7-20260819-final/`. The reports are absent from this checkout, and the notes cover an earlier source and dependency set. For each release candidate, use a successful build run tied to that candidate's exact source commit.

The steps below describe a reusable release procedure. They do not report the current status of any GitHub release or registry entry; verify those remote surfaces directly before announcing publication.

## Release topology

`.github/workflows/build-wheels.yml`, named **Build release artifacts**, runs only through `workflow_dispatch`. One successful run produces:

- 24 native wheels: CPython 3.13, 3.14 and free-threaded 3.14t across Linux glibc/musl, Windows and macOS on x86-64 and ARM64.
- One Python source distribution, `miniproto-<version>.tar.gz`.
- One platform-independent Cargo source package, `miniproto-<version>.crate`.
- `SHA256SUMS` and `release-manifest.json`, generated only after all 26 distributions pass filename, embedded metadata, count, ABI and platform-coverage validation.

Every distribution and both sidecars receive a GitHub artifact attestation in the build workflow. The Cargo package is built once in an isolated `CARGO_TARGET_DIR`; the wheel matrix already compiles and exercises the native extension on all eight platform targets, so the release workflow does not perform a redundant standalone Cargo target matrix.

`.github/workflows/publish-release.yml`, named **Publish release**, accepts an exact build run ID and version. Its verification job requires a successful `workflow_dispatch` run of the expected build workflow in `EDM115/miniproto`, checks that the source commit is reachable from `master`, checks Python/Cargo/archive versions, validates all checksums and expected files and verifies every GitHub attestation against the expected signer workflow and source commit. Only then do isolated jobs create a populated draft GitHub release, publish the Cargo package through crates.io Trusted Publishing, compare the downloaded registry crate byte-for-byte with the attested candidate, publish the 25 Python distributions through PyPI Trusted Publishing and optionally make the already-populated GitHub release public.  
The GitHub release title comes from the first `##` heading in the verified source commit's `CHANGELOG.md`, with inline Markdown formatting removed. For example, ``## `v0.1.0` - First Alpha release`` becomes `v0.1.0 - First Alpha release`. The notes contain everything below that heading until the next `##` heading or EOF, preserving Markdown and ignoring heading-like text inside fenced code blocks. The release tag still comes from the exact `version` input, independently of the changelog title.

There is no transaction spanning all three services. The chosen order keeps the GitHub release as a draft until both registries succeed:

1. Verify the complete candidate.
2. Create the draft release and attach all 28 immutable assets.
3. Publish the Cargo source package to crates.io and verify its bytes.
4. Publish all wheels and the Python sdist to PyPI.
5. Publish the GitHub draft as the immutable latest release or prerelease, unless `keep_draft` is enabled.

## One-time repository and registry setup

Configure these settings once before the first publication:

1. Create a protected GitHub Actions environment named `release`. Require manual approval and restrict deployment as appropriate for the maintainers. If the only release approver is also the person dispatching the workflow, do not enable self-review prevention unless another trusted maintainer can approve it.
2. In the PyPI `miniproto` project, add a GitHub Actions Trusted Publisher with owner `EDM115`, repository `miniproto`, workflow `publish-release.yml` and environment `release`.
3. In the crates.io `miniproto` package settings, add a Trusted Publisher with repository owner `EDM115`, repository `miniproto`, workflow `publish-release.yml` and environment `release`.
4. Enable immutable releases in the GitHub repository settings before publishing the first release. Immutability applies only to releases published after the setting is enabled.

The publish workflow contains no long-lived registry secret. Each registry job receives only `id-token: write` plus the minimum read permission it requires; PyPI and crates.io exchange the GitHub OIDC identity for short-lived publication credentials. Build jobs never receive registry publication authority.

## Build the release candidate remotely

Review every intended release change, run the following read-only checks, then let the maintainer commit and push the exact tree. Agents do not stage, commit, tag or push:

```pwsh
git status --short --branch
git diff --stat
git diff --name-only
```

Verify that `pyproject.toml` and `rust/miniproto/Cargo.toml` contain the same exact version and run the release gate locally before requesting artifacts:

```pwsh
uv run miniproto-release-check --offline --artifacts-dir .tmp/release-offline
```

Dispatch the build from the exact `master` commit intended for release:

```pwsh
$repository = "EDM115/miniproto"
$sha = git rev-parse HEAD

gh workflow run build-wheels.yml `
  --repo $repository `
  --ref master

$runId = $null
for ($attempt = 1; $attempt -le 12; $attempt++) {
    $runId = gh run list `
      --repo $repository `
      --workflow build-wheels.yml `
      --event workflow_dispatch `
      --commit $sha `
      --limit 1 `
      --json databaseId `
      --jq ".[0].databaseId"
    if ($runId) {
        break
    }
    Start-Sleep -Seconds 5
}

if (-not $runId) {
    throw "No Build release artifacts run was found for $sha"
}

gh run watch $runId `
  --repo $repository `
  --exit-status
```

Do not publish a run selected only by recency. Record the run ID from the exact commit; the publish workflow independently rechecks the run identity, attempt, event, result, source SHA, versions and ancestry.

## Download and verify a candidate locally

`gh run download` keeps multiple workflow artifacts in separate directories. Flatten only files into a fresh candidate directory and reject duplicate names:

```pwsh
$downloadRoot = ".tmp/release-download-$runId"
$candidate = ".tmp/release-candidate-$runId"

if ((Test-Path $downloadRoot) -or (Test-Path $candidate)) {
    throw "Release download paths already exist; choose a fresh run-specific path"
}
New-Item -ItemType Directory $downloadRoot, $candidate | Out-Null
gh run download $runId --repo $repository --dir $downloadRoot

foreach ($file in Get-ChildItem $downloadRoot -Recurse -File) {
    $destination = Join-Path $candidate $file.Name
    if (Test-Path $destination) {
        throw "Duplicate release artifact name: $($file.Name)"
    }
    Copy-Item -LiteralPath $file.FullName -Destination $destination
}
```

Validate the exact set, embedded package metadata, manifest provenance and hashes with the same stdlib-only tool used in Actions:

```pwsh
$version = "0.1.0"
$runAttempt = gh api "repos/$repository/actions/runs/$runId" --jq .run_attempt

uv run miniproto-release-artifacts verify `
  --artifacts-dir $candidate `
  --manifest "$candidate/release-manifest.json" `
  --checksums "$candidate/SHA256SUMS" `
  --version $version `
  --repository $repository `
  --workflow .github/workflows/build-wheels.yml `
  --run-id $runId `
  --run-attempt $runAttempt `
  --source-sha $sha `
  --event workflow_dispatch
```

Verify each file's GitHub build attestation as well:

```pwsh
$signer = "$repository/.github/workflows/build-wheels.yml"

foreach ($file in Get-ChildItem $candidate -File) {
    gh attestation verify $file.FullName `
      --repo $repository `
      --signer-workflow $signer `
      --source-digest $sha `
      --deny-self-hosted-runners
}
```

A candidate is complete only when it contains exactly 24 wheels, one Python sdist, one Cargo package, `SHA256SUMS` and `release-manifest.json`. Do not combine wheels from one run with a source package or sidecar from another run.

## Publish the verified run remotely

After the build succeeds, local review is complete, the protected `release` environment is configured and immutable releases are enabled, dispatch the publisher from `master`:

```pwsh
gh workflow run publish-release.yml `
  --repo $repository `
  --ref master `
  -f build_run_id=$runId `
  -f version=$version
```

The optional Boolean inputs `keep_draft` and `prerelease` both default to `false`. Add `-f keep_draft=true` to publish packages while leaving the populated GitHub release as a draft. Add `-f prerelease=true` to mark it as a prerelease and prevent it from becoming Latest, including when combined with `keep_draft=true` for later manual publication. These controls apply to the GitHub release, both registry publication jobs still run.  
Approve the `release` environment only after checking the displayed version, source commit and build run ID. Watch the publish run through completion:

```pwsh
$publishRunId = gh run list `
  --repo $repository `
  --workflow publish-release.yml `
  --event workflow_dispatch `
  --limit 1 `
  --json databaseId `
  --jq ".[0].databaseId"

gh run watch $publishRunId `
  --repo $repository `
  --exit-status
```

Do not manually publish the draft GitHub release if either registry job failed. Once an immutable release is public, its tag and attached assets cannot be replaced or supplemented.

## Local PyPI publication is an emergency path

The supported release path is GitHub OIDC Trusted Publishing. A local token publication is reserved for bootstrap or recovery because it loses the workflow identity and normal automatic PyPI publication attestations.

Select only the 24 wheels and Python sdist, then run a non-mutating upload check:

```pwsh
$pypiArtifacts = @(
    Get-ChildItem $candidate -File |
        Where-Object { $_.Extension -eq ".whl" -or $_.Name -eq "miniproto-$version.tar.gz" }
)

if ($pypiArtifacts.Count -ne 25) {
    throw "Expected 24 wheels and one Python sdist, found $($pypiArtifacts.Count)"
}

uv publish --dry-run $pypiArtifacts.FullName
```

For a real emergency upload, use a project-scoped PyPI token through the environment and remove it immediately afterward:

```pwsh
$env:UV_PUBLISH_TOKEN = "pypi-REDACTED"

try {
    uv publish `
      --publish-url https://upload.pypi.org/legacy/ `
      --check-url https://pypi.org/simple/ `
      $pypiArtifacts.FullName
}
finally {
    Remove-Item Env:UV_PUBLISH_TOKEN
}
```

`--check-url` may skip only a file that already exists with identical bytes, which makes a carefully verified retry possible after an interrupted multi-file upload. Never put the token in the command line, repository, shell history or release artifact.

## Local crates.io publication is an emergency path

Cargo does not provide a supported command that uploads an arbitrary downloaded `.crate`. `cargo publish` packages the checked-out source itself and uploads that newly created archive. Therefore, a local recovery must use a clean checkout of the exact build SHA, reproduce the package with the pinned Rust/Cargo version and compare it with the attested candidate before publishing:

```pwsh
$env:CARGO_TARGET_DIR = ".tmp/local-crate-$runId"

try {
    cargo package --locked -p miniproto

    $generated = Get-Item "$env:CARGO_TARGET_DIR/package/miniproto-$version.crate"
    $downloaded = Get-Item "$candidate/miniproto-$version.crate"
    $generatedHash = (Get-FileHash $generated.FullName -Algorithm SHA256).Hash
    $downloadedHash = (Get-FileHash $downloaded.FullName -Algorithm SHA256).Hash
    if ($generatedHash -ne $downloadedHash) {
        throw "Local Cargo package differs from the attested release-build artifact"
    }

    cargo publish --dry-run --locked -p miniproto
}
finally {
    Remove-Item Env:CARGO_TARGET_DIR -ErrorAction SilentlyContinue
}
```

For an authorized emergency publication, expose a scoped crates.io token only for the command:

```pwsh
$env:CARGO_REGISTRY_TOKEN = "cio-REDACTED"

try {
    cargo publish --locked -p miniproto
}
finally {
    Remove-Item Env:CARGO_REGISTRY_TOKEN
}
```

Never use `--allow-dirty` or `--no-verify` for a release. A crates.io version cannot be overwritten or deleted after publication; a broken package can only be yanked.

## Failure recovery

- If the build workflow fails, fix the source or workflow and dispatch a new build. Never assemble a candidate across run IDs.
- If verification fails before the draft release, no registry or release was changed. Inspect the reported run, metadata, checksum or attestation mismatch and build a new candidate when necessary.
- If draft creation or asset upload fails, keep the draft and retry with the same still-valid candidate. The publisher resumes only a draft targeting the verified source commit, checks each existing asset's SHA-256 against the attested candidate and uploads only missing assets. Published releases, duplicate drafts, unexpected assets or mismatched bytes fail closed. Do not make a partial draft public.
- If crates.io fails, PyPI has not run and the GitHub release remains a draft. GitHub's **Re-run failed jobs** can retry the failed crates job from the same publish run and verified artifacts after an external transient problem is corrected. The job queries the version metadata API first, only a 404 means the version is absent. An archive download URL can redirect to a missing file that returns 403, so it is not an existence check. An existing version is downloaded and accepted only when its bytes match the attested candidate. If a crate was accepted but its downloaded bytes differ, keep the release draft and inspect or yank that crate.
- If PyPI fails, crates.io has already succeeded and the GitHub release remains a draft. A retry queries the version-specific PyPI JSON API, treats only 404 as an absent version, rejects unexpected filenames, compares each existing file's advertised SHA-256 digest with the attested candidate, downloads it to verify the bytes independently and passes only missing files to the Trusted Publishing action. Other HTTP errors and byte mismatches fail closed. Never rebuild the same version with different bytes.
- If a failure requires a workflow code fix, commit and push the fix, then dispatch a new **Publish release** run with the same build run ID and version. GitHub reruns retain the original workflow revision and do not pick up the fix. The new dispatch preserves matching draft assets and verifies already-published registry files before skipping their upload. Keep the draft and use the original candidate rather than rebuilding the same version.
- If both registries succeed but the final GitHub publication fails, rerun only the failed final job. Do not recreate the tag or upload replacement assets.

## Post-publication verification

After the protected workflow reports success, verify all three public surfaces without rebuilding or mutating the release. Set `$version` to the candidate; the example uses `0.1.0`.

```pwsh
$repository = "EDM115/miniproto"
$version = "0.1.0"
$tag = "v$version"

gh release view $tag `
  --repo $repository `
  --json tagName,targetCommitish,isDraft,isPrerelease,isLatest,isImmutable,url,assets

$postRelease = ".tmp/post-release-$version"
uv venv --python 3.14 $postRelease
$python = Join-Path $postRelease "Scripts/python.exe"
uv pip install --python $python "miniproto==$version"
& $python -I -c 'import importlib.metadata as m; import miniproto; from miniproto import _native; assert m.version("miniproto") == "0.1.0"; assert _native.native_available(); print(m.version("miniproto"))'

cargo info "miniproto@$version"
```

On Linux or macOS, use `$postRelease/bin/python` for the clean PyPI import. Download the GitHub assets into a new directory, using authenticated access for a retained draft, verify `SHA256SUMS` and `release-manifest.json` with `miniproto-release-artifacts verify`, then run `gh attestation verify` with `.github/workflows/build-wheels.yml` as the signer.

Confirm that PyPI lists exactly 24 wheels and one sdist. Confirm that crates.io serves the `.crate` bytes already checked by the publisher. Confirm that the GitHub release state matches the dispatch inputs: `keep_draft=true` leaves a draft, `prerelease=true` marks a prerelease without Latest, and both defaults produce a public Latest release. Its tag must target the verified build SHA and it must contain all 28 assets. If any surface disagrees, stop announcing the release, package versions and immutable release assets cannot be overwritten.

## Continuous versus authoritative artifacts

Ordinary `.github/workflows/ci.yml` keeps its Python sdist job because source-distribution construction belongs in continuous package validation. That CI artifact is evidence, not a release input. The authoritative sdist, Cargo package, wheels, checksums and manifest all come from the same manual **Build release artifacts** run.

`miniproto-release-check` remains the canonical non-mutating aggregate diagnostic. It streams checks, preserves failures and writes evidence such as environment details, benchmark reports, distribution hashes and clean-import results under a caller-owned directory. It never formats, fixes, publishes, creates tags or consumes release credentials.

Credentialed Telegram acceptance remains separately guarded and is not part of routine pull-request CI. When the required account, runner or Telegram conditions are unavailable, record that live acceptance was not run; do not reinterpret missing live evidence as a passing gate.

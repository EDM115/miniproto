---
title: Pre-merge checklist
description: Review and acceptance checks for the miniproto 0.1.0 Alpha before merging to master.
slug: /project/pre-merge/
generated: false
---

Use this checklist for the `0.1.0` Alpha preparation. The maintainer owns staging, commits, pushes, merges, tags and publication. Agents use read-only Git commands. Mark a gate complete only after recording its result and evidence.  
Preparation baseline: `012b8111d391de34a26677b64ba6e79f10a28364`, checked on 2026-10-14 before adding this page. The implementation, test and prose changes are committed. The combined adversarial review, subsequent security review and final acceptance remain pending. Later changes require fresh evidence for the affected gates.

## Recorded preparation evidence

These results describe earlier preparation runs on local Windows CPython 3.14. Preserve their reports as phase evidence, then validate the corrected candidate after the formal reviews.

| Area | Recorded result | Evidence boundary |
| --- | --- | --- |
| Python | 1,299 passed, 9 skipped, Ruff lint/format and ty passed | Four live tests, four stress tests and one POSIX permission test skipped. Ruff checked formatting across 318 files. |
| Rust | 29 tests, format and Clippy passed | Rust source stayed unchanged during the later media fixes, other platform/ABI acceptance remains pending. |
| Schema and reference | Layer 230 checks and reference freshness passed, 246 Rust units and 290 explicit parameters documented, 53 documentation tests passed | Regenerate after accepted source/docstring changes and check the final tree. |
| Site | 4,735 pages, 622,909 local references and five Pagefind filters validated, seven Chrome cases passed | Counts describe the preparation build. This new page and later changes need another build. |
| Examples | 31 offline Python examples, 62 PowerShell fences and 76 CLI argument sets checked | Credentialed examples were not executed. |
| Packages | Fresh wheel and sdist installed with dependencies in separate environments, Layer 230/native capability available, 19 CLI help checks per install | Local Windows CPython 3.14 acceptance, remaining release lanes require their own execution. |
| Scoped fixes | B1-B4/G1 regressions and five independent cleanup interaction probes passed, eight source/test hashes match the committed baseline | Upload spool/EOF, download unwind, multi-session settlement and live selection are resolved. The combined formal reviews remain pending. |

Local reports live under `.tmp/doc-review/` and `.tmp/fixes-5.1/`, which are ignored and may be absent from another checkout. The scoped file identities are in `.tmp/fixes-5.1/review/final-evidence.json`. The recorded hosted runs from 2026-08-19 belong to `c81533922ba63c89337f3959b881109c3b7e5dec`, see [release history](./release.md). Obtain hosted evidence for the corrected candidate.

## Review order

- [ ] **Identify the complete candidate.** Record its full commit SHA, staged/unstaged overlay and base. Preparation started at `9cdb0d6e41e6812dc1be39b0be1d1e3af8204f81`. Review the combined changes and generated provenance. Documentation commit `bd24156d4b015295a970fedf7bb58ed24a15bba1` allowed prose-literal changes in `tools/bench/benchmark_live_media_limit.py`, `tools/bench/provision_session.py` and `tools/docs/generate_telegram.py`. Inspect those strings in that commit. Exclude ignored probes and build output from the intended commit.

```pwsh
git -c core.fsmonitor=false status --short --branch
git -c core.fsmonitor=false diff --stat
git -c core.fsmonitor=false diff --name-only
git -c core.fsmonitor=false diff --cached --stat
git -c core.fsmonitor=false rev-parse HEAD
$preparationBase = "9cdb0d6e41e6812dc1be39b0be1d1e3af8204f81"
git -c core.fsmonitor=false log --oneline "$preparationBase..HEAD"
git -c core.fsmonitor=false diff --stat $preparationBase HEAD
```

- [ ] **Complete the adversarial review first.** Trace active implementations, callers and behavioral assertions for sender failures/replay/message IDs/ACK ownership, authorization/DC migration, gzip/TL bounds, native/fallback parity, update persistence/delivery/duplicates, peer/session concurrency, media/CDN/cache/scheduler ownership, packaging/CLI dispatch and documentation routing/search. Use official Telegram documentation as protocol authority. Each finding needs a source, trigger, impact and a test that distinguishes the bug from intended behavior.
- [ ] **Resolve accepted adversarial findings.** Require behavioral regressions that fail before and pass after each fix. Review the fixes and refresh affected tests, references and artifacts. Record any accepted Alpha deferral and its reason.
- [ ] **Complete the security review afterward.** Use the [security policy](./security.md) and [security model](../concepts/security-model.md). Cover nonce/DH/SRP, envelope/session/message validation, replay/fatal handling, bounded decompression/allocation, CDN integrity, SQLite domains/keys, native FFI/free-threaded inputs, bearer sessions/file IDs, redaction, dependencies and release OIDC/attestations. Record the reviewed tree, findings and residual risks. Resolve accepted findings and revisit earlier review evidence when behavior changes.
- [ ] **Freeze the corrected tree.** Record the source SHA, environment, commands, exit codes, report paths, artifact hashes and hosted run IDs. A later fix invalidates the checks it affects.

## Questions the formal reviews must disposition

These seven leads came from source inspection. The unchecked items remain open questions, with no vulnerability verdict or approved deferral. A resolved item records the accepted behavior and its local evidence.

- [ ] **File-ID symmetry:** decide whether `encode_file_id()` and `try_encode_file_id()` must produce values accepted by the decoder's integer, required-field, reference and size bounds. Preserve valid canonical round trips and distinguish local parsing from Telegram access. Source: `src/miniproto/file_id.py`.
- [ ] **Malformed session errors:** decide whether the shared deserializer should normalize non-object JSON and nested datetime failures to `SessionEnvelopeError`. Native session-string import already validates the outer object, assess its nested decoding separately. Source: `deserialize_session_data()` in `session/storage.py` and `import_session_string()` in `session/strings.py`.
- [x] **HTTPS proxy expectation:** `https` now verifies TLS to the proxy before CONNECT or credentials and defaults to port 443. On 2026-10-16, offline TLS proxy regressions verified successful tunnels, hostname/certificate rejection, no plaintext retry and failure cleanup under both supported event-loop modes. Source: `src/miniproto/connection/transport.py`, evidence: `tests/test_transport_runtime.py`. Live proxy acceptance and other release gates remain separate.
- [ ] **Unsupported MTProto inputs:** decide whether public native/fallback paths need the same rejection of out-of-range salt/session values and unaligned bodies. Separate valid-vector parity from acceptance of inputs outside the documented contract. Source: `crypto/native.py`, `_native_fallback.py` and Rust `mtproto.rs`.
- [ ] **Primitive TL length bounds:** locate enforcement of the `2**24-1` byte limit for supported bytes/string entry points, including public `tl/codec.py` wrappers. Decide whether primitive encoders need rejection, distinguish UTF-8 bytes from characters and checked fast paths from primitive helpers.
- [ ] **AES-GCM widths:** decide how the public API handles key/nonce widths outside its documented 32-byte/12-byte contract across backends. Protected session strings use fixed widths, assess direct fallback acceptance separately. Source: `crypto/native.py`, `_native_fallback.py`, Rust `crypto.rs` and `session/strings.py`.
- [ ] **Pushed message models:** disposition raw pushed media despite the `Message.media` annotation and omitted pushed formatting entities. Compare pushed conversion with high-level normalization and choose an explicit limitation, type/doc correction or behavior change. Source: `types.py`, `updates/manager.py` and `messages.py`.

## Alpha scope

- [ ] Confirm `0.1.0`, the Alpha classifier, compatibility warning and specified breaking changes. Python and Cargo versions must match. The Cargo package currently contains the PyO3 `cdylib`, a supported external Rust library API remains deferred.
- [ ] Confirm Python 3.13, 3.14 and 3.14t on the declared x86-64/ARM64 targets, with 3.13t and ARMv7 excluded. Windows ARM64 omits base `cryptography` and requires native capabilities for applicable AES/Scrypt operations.
- [ ] Preserve or specify changes to the documented lifecycle and data contracts: local authorization flags, storage closure on disconnect, competing update iterators, application-owned shutdown, persistence before application side effects, borrowed cache ownership and separate transfer/cache/output memory budgets. Keep the media rollback and running-thread assembly limits in [the media guide](../media.md).
- [ ] Preserve the requested published Alpha installation wording and `master`-tracking documentation. Verify public registry and deployed-site state at the publication boundary.

## Local acceptance

Run from the repository root with project Python through plain `uv run`, PowerShell 7 and frozen development/docs dependencies. Record interpreter/ABI/architecture, native capabilities, dependency presence, build/runtime GIL state and tool versions. Include Rust/Cargo, uv, Ruff, ty, Maturin, Node, pnpm, Chrome, nightly and cargo-docs-md. The Rust documentation renderer uses floating nightly. See [development commands](../development.md).

- [ ] **Validate locks and metadata.** Run `uv lock --check`, inspect Python/Cargo `0.1.0`, schema/native metadata and classifiers. Correct drift through a reviewed change.
- [ ] **Complete all 22 offline aggregate stages.** Require every expected stage in `release-check.json` to pass, inspect pending stages and explain expected skips. The 9-stage quick mode omits acceptance work. `--keep-going` preserves the first failure for diagnosis. Offline mode forces both integration guards off but inherits `MINIPROTO_STRESS`. Record whether stress ran there or separately.

```pwsh
$candidateSha = git -c core.fsmonitor=false rev-parse HEAD
$runStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$artifacts = ".tmp/premerge-offline-$candidateSha-$runStamp"
New-Item -ItemType Directory -Path $artifacts | Out-Null
uv lock --check
if ($LASTEXITCODE -ne 0) { throw "Locked dependency validation failed" }
uv run miniproto-release-check --offline --artifacts-dir $artifacts 2>&1 | Tee-Object -FilePath "$artifacts/release-check.log"
if ($LASTEXITCODE -ne 0) { throw "Offline aggregate failed" }
```

The 22 stages cover environment, schema, Ruff format/lint, typecheck, docs, pytest, Cargo format/Clippy/tests, imports, runtime smoke, scheduler, native/fallback crypto, protected sessions, runtime paths, framing, hot TL, lazy raw profiling, wheel/sdist, artifact inspection and clean import. Preserve the transcript, stage/environment JSON, benchmark JSON, distribution manifest and hashes. Some measurements and clean-install assertions exist only on stdout, the runner does not save per-stage logs.
- [ ] **Run the four stress tests without skips.** Cover the 16 MiB fake transfer, 50,000 ordered updates, 1,000 cached-peer sends and 500 client lifecycle cycles. Use fresh temporary output and restore the previous guard value.

```pwsh
$previousStress = $env:MINIPROTO_STRESS
try {
    $env:MINIPROTO_STRESS = "1"
    uv run pytest tests/stress/test_runtime_stress.py --basetemp ".tmp/premerge-stress-$runStamp"
}
finally {
    $env:MINIPROTO_STRESS = $previousStress
}
```

- [ ] **Close POSIX, ABI and platform gaps.** Run the permission test on Linux/macOS and quality/tests on the supported interpreters. Prove the free-threaded build and runtime GIL state after native import, declared dependencies, protected-session round trips and concurrent native outputs.
- [ ] **Review performance evidence.** Preserve failed samples and pair reports with their actual native artifact. The existing checked framing workload requires 2x in each supported TCP mode on 72-byte production-adapter frames, hot TL requires 1.5x for its eligible four-operation mix. Compare broader measurements with agreed same-host/ABI/workload baselines and investigate regressions, retain these thresholds' workload limits.
- [ ] **Verify isolated packages.** Install wheel and sdist separately with dependencies, use `-I` outside the checkout and verify environment-local imports/native capabilities. Inspect version, metadata, license, typing, raw shards, schema and tool payload. Compare installed console-script names with `pyproject.toml` and exercise all 19 helps. The aggregate's clean-import smoke covers fewer operations, retain the extra checks separately.
- [ ] **Validate references and the site.** Regenerate approved source/docstring changes, review the diff, then check freshness, Rust parameter coverage, current Layer 230 labels, configured frontend checks, brand prebuild, routes/assets/links, five Pagefind filters and all seven Chrome cases. Inspect handwritten schema labels as well as generated outputs. Recheck affected examples/CLI syntax. Oxfmt is a separate check. `--skip-install` requires a frozen frontend dependency install already in place.

```pwsh
pnpm --dir docs-site format --check
uv run miniproto-docs --check --build --skip-install
```

- [ ] **Validate the Pages prefix.** Repeat with `MINIPROTO_DOCS_BASE=/miniproto`, restore its previous value and inspect canonical/internal routes, trailing slashes, 404, assets, sidebar and Pagefind. Preserve root and prefixed artifacts separately. Both builds overwrite `docs-site/dist`.
- [ ] **Validate Docker delivery.** Prepare a validated root-base static artifact, build both targets and check runtime UID 101, port 6743, health, installation/Pagefind routes and absence of source/toolchains. Record resolved floating-image digests. The default target consumes existing `dist`, `source-runtime` runs only the site build and needs separate reference/browser/static acceptance.

```pwsh
docker build --file docs-site/Dockerfile --tag miniproto-docs-premerge .
docker build --file docs-site/Dockerfile --target source-runtime --build-arg MINIPROTO_DOCS_SITE=https://miniproto.edm115.dev --tag miniproto-docs-premerge-source .
```

## Authorized Telegram acceptance

A maintainer selects accounts, destinations, sessions, payload sizes and test scope. Keep credentials in approved environment/secret storage and public evidence redacted. Require executed tests and intended cells to pass, account prerequisites can otherwise produce skips.  
Direct smoke prerequisites: `MINIPROTO_INTEGRATION=1`, `MINIPROTO_REAL_INTEGRATION=1`, API ID/hash, session key, bot token, an authorized user session and an existing `MINIPROTO_TEST_UPLOAD_FILE`. Fresh phone login also requires `MINIPROTO_REAL_PHONE`, interactive `MINIPROTO_LIVE_PROMPT_CODE=1` and terminal stdin. Use `pytest -s`. Supply or enter 2FA when required. `MINIPROTO_TEST_DOWNLOAD_PATH` is optional. Do not retain an interactive login-code transcript.

- [ ] **Execute all four smokes:** bot authentication/refreshed identity, phone authentication/identity and persisted-session reconnect, Saved Messages send/history, and media byte equality. The command below supports interactive fresh login.

```pwsh
uv run pytest -s tests/integration/test_auth_live.py tests/integration/test_messages_live.py tests/integration/test_media_live.py
```

- [ ] **Close additional authorization/API scope.** Record controlled raw/high-level sends, cross-DC authorization/media migration, retry/ambiguity and disconnect, with account kind/DC and request/result sequence.
- [ ] **Close media/CDN/multi-session scope.** Exercise authorized ranges, resume, cancellation, caches, plain hashes and actual CDN redirects/control/data/hash/reupload paths. Record unencountered CDN paths as gaps. Bot multi-session needs eligible size/storage and authorized two/four-session execution, verify ordered assembly and settled failure cleanup.
- [ ] **Close update/recovery scope.** Observe pushes, global/channel gap recovery, duplicates across persisted reconnect, queue/handler delivery and shutdown. Record cursors and application effects. Establish a bounded live procedure, the current smoke tests and benchmark do not cover these recovery cases.
- [ ] **Record bounded live performance.** Enable `MINIPROTO_LIVE_BENCH=1` as well as both integration guards. Supply actor credentials, session key and an authorized `MINIPROTO_LIVE_BENCH_BOT_PEER` for bot operations, including download-only/matrix runs. User/both benchmark actors also require the phone variable. Specify size, the default is 2,097,152,000 bytes. Retain byte/digest, account/DC, timing, retries/floods, loop-lag and RSS evidence.

```pwsh
uv run miniproto-bench-live-media --actor both --operation both --size 1MiB --verify-digest --loop-lag --json .tmp/premerge-live-media.json
```

- [ ] **Complete the selected matrix and 24-stage live aggregate.** The smoke matrix has four bot/download cells, full has 576. Supply an authorized prior bot file ID through `MINIPROTO_LIVE_BENCH_BOT_FILE_ID` or shared `MINIPROTO_LIVE_BENCH_FILE_ID`, with matching `MINIPROTO_LIVE_BENCH_SIZE`, bot peer and guards. Use fresh candidate/run-specific output and require every intended cell to pass. Partial/resumed status needs complete cell evidence. Record claimed digest checks separately, matrix commands do not enable them by default. The aggregate additionally requires `MINIPROTO_RELEASE_LIVE=1`. It does not set `MINIPROTO_LIVE_BENCH`.

```pwsh
$liveRunStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$liveCandidateSha = git -c core.fsmonitor=false rev-parse HEAD
uv run miniproto-bench-matrix --mode smoke --output ".tmp/premerge-live-matrix-$liveCandidateSha-$liveRunStamp"
uv run miniproto-release-check --live --artifacts-dir ".tmp/premerge-live-aggregate-$liveCandidateSha-$liveRunStamp"
```

Authorize the aggregate's complete scope before running it: `--live` enables both integration guards for all stages, so the broad pytest stage and later explicit integration stage can each execute the four smokes, repeating sends/media transfers. A preceding direct smoke command adds another execution. Preserve redacted output-only measurements and inspect all 24 stage results.  
- [ ] **Record live platform scope.** The manual live workflow covers Linux/Windows Python 3.14. Record actual hosts/ABIs and any remaining macOS, ARM64, free-threaded or deployment gaps, with a maintainer's scope decision.

## Hosted checks and release candidate

Remote PR state, run conclusions, protections, registry settings and deployed surfaces were not inspected while preparing this checklist. After the maintainer pushes, select runs attached to the intended candidate and record IDs, attempts, events, source identity, conclusions and URLs.

- [ ] **Inspect PR and workflow identity.** Record target, draft/readiness, required check conclusions and review decisions, plus PR head/base and the tested checkout SHA. Current PR CI/docs use the synthetic merge snapshot, and the docs artifact name follows `github.sha`. Use check links and checkout evidence to identify runs. Record the Actions run's `head_sha` separately from the tested checkout SHA and PR head/base. GitHub documents the [pull-request merge SHA](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request). The workflows trigger on master push, manual dispatch and non-draft PR `ready_for_review`/`synchronize`. Opening a ready PR alone does not trigger them. Missing, skipped, cancelled or stale required checks remain pending.

```pwsh
$repository = "EDM115/miniproto"
gh pr view 4 --repo $repository --json number,state,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,mergeStateStatus,reviewDecision,statusCheckRollup
gh pr checks 4 --repo $repository
# Set $runId from the selected check's workflow run
gh api "repos/$repository/actions/runs/$runId" --jq '{id: .id, attempt: .run_attempt, headSha: .head_sha, event: .event, status: .status, conclusion: .conclusion, url: .html_url}'
```

- [ ] **Require candidate CI.** Inspect Ubuntu Python 3.13/3.14/3.14t quality/stress with live disabled, separate GIL-disabled native/dependency/threaded acceptance, Rust 1.99 checks and all 12 benchmark platform/ABI cells. Ordinary CI's sdist validates continuous source packaging, release input comes from the manual build workflow.
- [ ] **Require candidate documentation evidence.** Inspect frozen reference/site/browser/static validation under `/miniproto` and the SHA-labelled portable artifact. PR jobs build only. Master push and every manual docs dispatch deploy to `gh-pages`, including a selected non-master ref. Obtain publication authorization before using manual dispatch.
- [ ] **Obtain all 24 wheel lanes from one manual build.** Record source SHA/ref, run ID/attempt/event, result and artifact expiry. Each wheel must install and execute on its intended runner/container. Inspect GIL/native/dependency/protected-session/threaded-output/entry-point evidence. Record emulated Linux ARM64 container execution separately from native hardware. Rebuild when the intended release SHA changes.

| Targets per ABI | Coverage |
| --- | --- |
| Linux glibc and Linux musl | x86-64 and ARM64 each |
| Windows and macOS | x86-64 and ARM64 each |
| `cp313-cp313`, `cp314-cp314`, `cp314-cp314t` | Eight targets each, 24 wheels |

- [ ] **Verify candidate files and provenance.** Require 24 wheels, one sdist and one crate, plus `SHA256SUMS` and `release-manifest.json`: 26 distributions, 28 files and 25 Python distributions. Checksums cover the 26 distributions. Verify attestations for all 28 files, including sidecars. Require eight distinct platform tags per ABI, with the same tag set across all three ABIs. Compare them with the intended lane table and inspect metadata, license, typing, schema and tool resources. The validator enforces counts/tag-set equality rather than every semantic target or payload field. Inspect manifest `source_ref` against the selected build ref separately. The verifier requires only a nonempty value. Compare all expected console-script names and exercise their entry points. Use the exact-run download and verification steps in [Release](./release.md).
- [ ] **Record merge acceptance.** Include completed adversarial then security reviews, resolved accepted findings, final local/hosted evidence and explicit live/platform/container scope. Name an owner, reason and maintainer decision for unavailable gates. Recheck any different merge or release source SHA.

## Separate publication checks

Follow [the release procedure](./release.md) after the maintainer approves publication.

- [ ] Verify actual protected `release` reviewers/self-review policy, PyPI/crates.io Trusted Publishers, immutable releases and Pages configuration. Workflow declarations alone do not establish these settings.
- [ ] Verify tag/version availability, release source reachability from `master`, one expected build run/attempt, versions, hashes, attestations and unchanged bytes.
- [ ] Use the supported order: verify, populated draft with 28 assets, 25 Python distributions to PyPI, crate publication and byte verification, then immutable public GitHub release. Keep the draft on registry failure and follow same-run recovery in the release guide. A new full dispatch can fail on an existing tag.
- [ ] Verify fresh installed packages, registry files/crate bytes, immutable release/tag/source SHA/assets and deployed master routes/search/canonicals before announcing publication.

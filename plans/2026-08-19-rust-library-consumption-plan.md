---
goal: Make miniproto_native consumable as a stable Rust library without compromising the Python accelerator
version: 1
date_created: 2026-08-19
last_updated: 2026-08-19
owner: EDM115
status: 'On Hold'
tags: [architecture, rust, packaging, provenance]
---

# Introduction

![Status: On Hold](https://img.shields.io/badge/status-On%20Hold-orange)

This plan defines the deferred work required for Rust projects to depend on the `miniproto` Cargo package and import its library as `use miniproto_native::...`. It is intentionally not active, is not part of Wave 6, and must not change the current `0.1.0` boundary: the Rust crate remains the private PyO3 accelerator for the Python SDK and is published to crates.io for provenance and version parity. Implementation starts only after a separate explicit user instruction.

## 1. Requirements & Constraints

- **REQ-001**: Keep the Cargo package name `miniproto` and the Rust library crate name `miniproto_native`; direct consumers must write `use miniproto_native::...`.
- **REQ-002**: Provide a documented Rust API that can compile and run without a Python interpreter, Python headers, or an initialized PyO3 runtime.
- **REQ-003**: Preserve `miniproto._native` as the Python accelerator import and retain native/fallback behavior, free-threaded Python support, platform wheels, and measured hot-path performance.
- **REQ-004**: Expose only deterministic protocol primitives whose ownership, errors, validation, and stability can be supported as a Rust API; Python policy such as retries, sessions, updates, peers, and transfer orchestration remains in Python unless separate benchmark-backed work approves a move.
- **REQ-005**: Keep Python and Cargo package versions synchronized and continue publishing both from the same reviewed source commit.
- **SEC-001**: Public Rust entry points must reject malformed lengths, offsets, constructor metadata, and cryptographic parameters without panicking, leaking secrets through errors, or weakening the validation already enforced by the Python/native boundary.
- **CON-001**: This plan is `On Hold`; no task below is authorized by the current Wave 5-to-6 intermediary work or by Wave 6 itself.
- **CON-002**: The approved release architecture remains unchanged: build the Cargo source package exactly once, attest every wheel plus the Python sdist and `.crate`, and publish only after the separate run-ID-driven release workflow verifies source run, commit, version, checksums, and attestations.
- **CON-003**: Do not promise Rust API stability merely because a symbol is currently `pub` or used by a PyO3 wrapper; the first consumer-facing surface requires an explicit semver review.
- **GUD-001**: Prefer small public modules and Rust-native result types over mirroring Python function signatures or exposing PyO3 types.
- **PAT-001**: Separate reusable Rust implementations from thin feature-gated PyO3 adapters so the same validated core implementation serves Rust and Python callers.

## 2. Implementation Steps

### Implementation Phase 1

- **GOAL-001**: Establish the package, feature, error, and public-API boundaries before exposing Rust consumers to compatibility commitments.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Audit `rust/miniproto/src/crypto.rs`, `mtproto.rs`, `tl.rs`, `transport.rs`, and `generated_tl.rs`; classify every candidate primitive as public-stable, public-experimental, or PyO3-only; record proposed module paths, argument ownership, return types, errors, allocation behavior, and semver commitments in this plan or a dedicated Rust API specification. Acceptance: every proposed export satisfies REQ-002, REQ-004, SEC-001, and CON-003 before source visibility changes. | | |
| TASK-002 | Update `rust/miniproto/Cargo.toml`, `pyproject.toml`, and `rust/miniproto/src/lib.rs` so Cargo emits both `rlib` and `cdylib`, PyO3 and `pyo3/extension-module` are behind an explicit wheel feature, and a no-Python Rust build succeeds without changing the Maturin module name. Acceptance: `cargo check -p miniproto --no-default-features` succeeds, while a Maturin development build still imports `miniproto._native`. | | |
| TASK-003 | Refactor approved primitives into Rust-native modules with crate-owned error types, then keep Python conversion and registration in thin PyO3 adapters. Preserve one implementation per primitive and benchmark any unavoidable conversion or allocation changes. Acceptance: direct Rust calls contain no `Python`, `Bound`, `PyResult`, `PyBytes`, or other PyO3 types, and Python native/fallback parity tests remain green. | | |

### Implementation Phase 2

- **GOAL-002**: Prove the packaged crate is usable by external Rust projects, document its supported contract, and preserve the existing Python release guarantees.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Add an out-of-package consumer fixture that depends on the packaged crate and exercises representative imports through `use miniproto_native::...`; test both default/no-Python Cargo usage and the wheel feature independently. Acceptance: the fixture builds and tests from the `cargo package` output rather than relying on workspace-only paths or unpublished files. | | |
| TASK-005 | Add crate-level and public-item Rust documentation, runnable examples, feature documentation, a Rust-facing README section, and docs.rs metadata without presenting Python-only internals as stable Rust API. Acceptance: `cargo test --doc -p miniproto`, docs.rs-equivalent generation, and the maintained Rust documentation audit pass with no missing public-item or parameter descriptions. | | |
| TASK-006 | Extend release acceptance to verify the consumer fixture, `cargo package --locked`, package contents, wheel builds, free-threaded imports, native/fallback parity, and representative Rust/Python benchmarks from the same commit. Preserve the build-once `.crate` and attestation boundary in CON-002. Acceptance: the crate, Python sdist, and every wheel are version-aligned, checksum-recorded, attested, and publishable without rebuilding during publication. | | |

## 3. Alternatives

- **ALT-001**: Publish a separate `miniproto-core` package for Rust consumers. Rejected for the first iteration because the accepted provenance/version model uses one Cargo package and the required import is `miniproto_native`; revisit only if optional PyO3 separation proves materially harmful.
- **ALT-002**: Expose the existing PyO3 functions directly as the Rust API. Rejected because their Python-owned types, exceptions, allocation choices, and registration-oriented visibility do not form a Python-independent or semver-ready Rust contract.
- **ALT-003**: Keep publishing a `cdylib`-only crate indefinitely. Retained as the current temporary state, but it does not satisfy REQ-002 and therefore cannot be advertised as a directly consumable Rust library.

## 4. Dependencies

- **DEP-001**: Explicit user authorization to activate this plan after the current release work; plan presence alone is not authorization.
- **DEP-002**: A stable build-and-publish workflow that produces one attested `.crate` plus attested Python artifacts from the same source commit.
- **DEP-003**: Current PyO3, Maturin, Rust MSRV, and free-threaded Python support must remain compatible with the selected feature topology.

## 5. Files

- **FILE-001**: `rust/miniproto/Cargo.toml`, for crate types, feature topology, package metadata, and docs.rs configuration.
- **FILE-002**: `rust/miniproto/src/lib.rs` plus `crypto.rs`, `mtproto.rs`, `tl.rs`, `transport.rs`, and generated-code boundaries, for Rust-native exports and feature-gated PyO3 adapters.
- **FILE-003**: `pyproject.toml` and release/build workflows, for selecting the Python-extension feature without rebuilding the source crate during publication.
- **FILE-004**: A future Rust consumer fixture and its focused tests, stored outside the published package payload unless explicitly required by `cargo package` acceptance.
- **FILE-005**: Rust-facing README/API documentation, generated Rust reference inputs, release documentation, and version/provenance records.

## 6. Testing

- **TEST-001**: Run `cargo fmt --check`, `cargo check -p miniproto --no-default-features`, `cargo clippy --workspace --all-targets --all-features -- -D warnings`, `cargo test --workspace --all-features`, and `cargo test --doc -p miniproto`.
- **TEST-002**: Build `cargo package --locked -p miniproto`, inspect its contents, unpack it in a clean location, and compile/test the external consumer fixture against that package.
- **TEST-003**: Build and install a wheel with the explicit Python-extension feature, then run native/fallback parity, free-threaded safety, CLI, and clean-environment import tests.
- **TEST-004**: Run representative Rust-native and Python-extension benchmarks before and after the refactor; block promotion on a reproducible material regression or duplicate implementation path.
- **TEST-005**: Verify release manifests contain one `.crate`, one Python sdist, the expected wheel matrix, checksums, and valid GitHub attestations bound to the approved build run and commit.

## 7. Risks & Assumptions

- **RISK-001**: Making PyO3 optional may expose implicit dependencies between Python conversion and core validation; mitigate by extracting and testing validation before changing feature gates.
- **RISK-002**: Public Rust names and error types become semver commitments earlier than internal PyO3 symbols; mitigate with the TASK-001 inventory and a deliberately small first surface.
- **RISK-003**: Adding `rlib`, features, or wrapper layers can alter binary size, link behavior, or hot-path performance; mitigate with wheel-matrix builds and same-process before/after benchmarks.
- **RISK-004**: The Cargo package name `miniproto` differing from the library import `miniproto_native` can confuse consumers; mitigate with exact dependency and `use` examples in crate metadata and documentation.
- **ASSUMPTION-001**: The existing pure Rust implementations can be separated from PyO3 adapters without changing Telegram wire behavior or requiring a second implementation.
- **ASSUMPTION-002**: Python and Cargo releases will continue to use the same version and source commit even after the Rust API becomes independently consumable.

## 8. Related Specifications / Further Reading

- [Package boundary and ecosystem intent](2026-06-26-package-boundary-and-ecosystem-intent.md)
- [v0.1.0 Alpha completion plan](2026-08-12-v0.1.0-alpha-completion-plan.md)
- [Cargo library targets](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#library)
- [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html)
- [PyO3 building and distribution](https://pyo3.rs/latest/building-and-distribution.html)
- [docs.rs metadata](https://docs.rs/about/metadata)

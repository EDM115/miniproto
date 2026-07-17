# Migrate away from deprecated asyncio event-loop policies

## 0. Plan metadata

- Status: completed
- Priority: P2 forward compatibility and import hygiene
- Estimated size: M
- Risk: medium; optimized-loop selection differs across Python, uvloop, winloop, and embedded applications
- Base commit: cf7db29
- Dependencies: none
- Related plan: 010 also benefits from removing import-time backend work, but neither plan must block the other
- Drift check: reopen pyproject.toml, src/miniproto/event_loop.py, src/miniproto/**init**.py, tests/test_event_loop.py, docs/development.md, and current Python 3.16 asyncio documentation. Stop if import no longer mutates policy and run already uses a supported loop_factory-only path.

## 1. Objective

Remove import-time global event-loop policy mutation and keep optimized-loop helpers working on Python 3.16, where policy APIs are scheduled for removal.

## 2. Context and current state

Python support is open-ended:

> pyproject.toml:10 requires Python >=3.13.

Optimized backends are runtime dependencies:

> pyproject.toml:26-27 installs uvloop on Linux/macOS CPython and winloop on Windows-family CPython.

The helper still installs a policy:

> src/miniproto/event_loop.py:50-67 calls the backend install function while suppressing DeprecationWarning.
> src/miniproto/event_loop.py:70-82 falls back to backend EventLoopPolicy().new_event_loop().
> src/miniproto/event_loop.py:111-112 imports the backend and calls install at module import.

Tests require that side effect:

> tests/test_event_loop.py:12-20 expects auto-install or an install error.

The same module already contains the future-safe mechanism:

> src/miniproto/event_loop.py:85-97 uses asyncio.Runner with loop_factory when a backend run helper is unavailable.

Root cause: legacy auto-install behavior remained the default even after an explicit runner/factory path was added.

## 3. Scope

### In scope

- Stop mutating global asyncio policy during miniproto import.
- Lazily load the optional backend.
- Make event_loop.run use asyncio.Runner and a supported loop factory.
- Keep an explicitly deprecated compatibility install function only where policy APIs still exist.
- Update tests, documentation, examples, and future-version CI coverage.

### Out of scope

- Forcing applications that call asyncio.run to use an optimized backend.
- Vendoring uvloop or winloop.
- Supporting Python below 3.13.
- Changing the rest of Client’s async API.

## 4. Design

### 4.1 No import side effects

Remove install() from module bottom. Prefer lazy _load_backend on first backend(), backend_version(), new_event_loop(), or run() call so import miniproto neither imports an optimized backend nor changes process-global state.

### 4.2 Factory-first execution

Expose loop_factory() or keep new_event_loop() as the supported primitive. event_loop.run always uses asyncio.Runner(debug=debug, loop_factory=selected_factory). A backend’s documented run helper may be used only if it is explicitly compatible with current Python and equivalent cleanup semantics; one Runner path is preferred.
Use backend.new_event_loop when officially supported. Do not instantiate EventLoopPolicy on Python 3.16. Inspect the installed winloop and uvloop APIs and their official docs before selecting adapters.

### 4.3 Compatibility install

Keep install() for pre-3.16 callers only as deprecated, explicit opt-in behavior. It emits DeprecationWarning to the caller, never suppresses it globally, returns false or raises a documented unsupported error when policy APIs/backend install are unavailable, and is never called by import.
installed() reports only an explicit successful legacy install. Add optimized_available() if callers need to know whether run will use a backend; do not overload installed semantics.

### 4.4 User model

- Recommended: event_loop.run(coro) for scripts.
- Advanced: asyncio.Runner(loop_factory=event_loop.new_event_loop) for controlled lifecycles.
- Library/embedded users keep ownership of their existing loop; importing miniproto changes nothing.

### 4.5 Rejected alternatives

- Suppressing deprecation warnings is rejected because the API will be removed, not merely noisy.
- Calling backend.install at Client.connect is rejected because it still mutates application-global state.
- Dropping optimized backends is rejected because performance is a project priority.

### 4.6 Verified backend compatibility exception

The installed Windows backend is `winloop 0.6.3` and exposes `new_event_loop()`, so the factory-first design is supported for normal execution. A deterministic local reproduction on Python 3.14.5 showed that `asyncio.Runner(debug=True, loop_factory=winloop.new_event_loop)` crashes natively when finalizing an unfinished async generator; debug-only execution therefore uses the stdlib Runner until a newer winloop version is installed, while non-debug execution keeps the optimized factory.

## 5. Files to change

| File                        | Change                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| src/miniproto/event_loop.py | Lazy backend load, factory-first run, explicit deprecated install, no module-bottom install |
| src/miniproto/**init**.py   | Preserve event_loop export without triggering backend work                                  |
| tests/test_event_loop.py    | Add no-side-effect, lazy-load, factory, cleanup, and compatibility tests                    |
| pyproject.toml              | Update Python classifiers/markers only if verified backend support requires it              |
| docs/development.md         | Document recommended runner/factory usage                                                   |
| README.md                   | Update quickstart if it implies automatic global installation                               |
| .github/workflows/ci.yml    | Add Python 3.16/pre-release compatibility job when available                                |
| CHANGELOG.md                | Record behavior change                                                                      |

## 6. Execution prerequisites

- Read https://docs.python.org/3.16/library/asyncio-policy.html and the current official uvloop/winloop APIs.
- Inspect the actually installed backend modules through the uv environment; do not infer APIs from memory.
- Capture current event_loop.run cleanup, debug, exception, and context behavior with tests.
- Git workflow: no branch, worktree, stage, commit, stash, revert, or push.
- STOP if winloop lacks a supported factory on Python 3.16; document the upstream blocker instead of reviving removed policy APIs.

## 7. Implementation steps

1. Add a subprocess test that snapshots relevant asyncio policy/backend modules, imports miniproto, and proves no policy change and no uvloop/winloop import. Confirm it fails on cf7db29.  
   Verification: uv run pytest tests/test_event_loop.py -k "import or policy or lazy"
2. Refactor backend state to lazy loading with deterministic cached success/error. Preserve backend_name without importing the package.  
   Verification: uv run pytest tests/test_event_loop.py
3. Implement factory-first new_event_loop/run using asyncio.Runner. Test result, exception propagation, debug flag, async-generator cleanup, default-executor cleanup, and repeated calls.  
   Verification: uv run pytest tests/test_event_loop.py -k "run or factory or cleanup"
4. Make install explicit and deprecated on supported Python versions, and unsupported without hidden policy fallback on 3.16. Update installed/install_error semantics and tests.  
   Verification: uv run pytest tests/test_event_loop.py -k "install"
5. Test with real platform backend plus a fake backend module exposing only the supported factory API. On a second OS, rely on CI or an explicit platform runner rather than monkeypatching sys.platform after import.  
   Verification: uv run pytest tests/test_event_loop.py
6. Update docs, changelog, and CI matrix. Keep Python 3.16 pre-release failures visible while upstream backend compatibility is unresolved.  
   Verification: inspect CI config and run local Python version where available.
7. Run startup and runtime benchmarks to prove lazy loading improves import without harming event_loop.run materially.  
   Verification: uv run python tools/bench/benchmark_runtime_paths.py and plan 010’s import benchmark if present.
8. Run full verification.  
   Verification: all section 8 commands pass.

## 8. Testing strategy

### Focused

- uv run pytest tests/test_event_loop.py
- uv run python tools/bench/benchmark_runtime_paths.py

### Full

- uv run ruff format --check .
- uv run ruff check .
- uv run ty check
- uv run python -m tools.schema.generate --check
- uv run pytest
- cargo fmt --check
- cargo clippy --all-targets --all-features -- -D warnings
- cargo test --all-features

### Required edge cases

- Import inside an application that already installed a custom policy.
- Backend absent, backend import raises nested ModuleNotFoundError, backend factory raises.
- run success, coroutine exception, cancellation, debug true/false, repeated runs.
- Explicit install warning on <=3.15 and unsupported path on 3.16.
- No optimized module loaded until a helper needs it.

## 9. Done criteria

- import miniproto never installs or changes an event-loop policy.
- event_loop.run uses an optimized supported factory where available and stdlib otherwise.
- No production path depends on EventLoopPolicy on Python 3.16.
- Compatibility APIs are explicit, deprecated, and tested.
- Documentation and CI describe the new ownership model.
- Focused and full verification pass.

## 10. Rollback and recovery

If a backend factory fails on one platform, fall back to stdlib Runner with a visible structured warning/error metric and keep import side-effect-free. Do not restore automatic global policy installation.

## 11. Risks and mitigations

| Risk                                       | Mitigation                                                     |
| ------------------------------------------ | -------------------------------------------------------------- |
| Existing users relied on auto-install      | Changelog, deprecated explicit install, migration example      |
| Backend APIs differ                        | Official docs plus installed-module inspection and platform CI |
| Runner cleanup differs from backend.run    | Explicit async-generator/executor tests                        |
| Python 3.16 arrives before backend support | Visible stdlib fallback and CI tracking                        |

## 12. Maintenance and references

- Owner: unassigned
- Review trigger: Python minimum/maximum support, asyncio Runner/policy changes, uvloop/winloop upgrades, or top-level import changes.
- Official reference: https://docs.python.org/3.16/library/asyncio-policy.html
- Repository evidence: pyproject.toml, src/miniproto/event_loop.py, src/miniproto/**init**.py, tests/test_event_loop.py, docs/development.md.

## 13. Implementation and verification evidence

- Completed on 2026-07-16 at `664a56c`.
- TDD RED: the new focused suite failed because importing `miniproto` changed the policy, loaded `winloop`, and emitted no explicit-install deprecation warning.
- TDD GREEN: `uv run pytest tests/test_event_loop.py --basetemp .tmp/pytest-event-loop-verified` exited zero after lazy backend loading, Runner factory migration, explicit legacy installation, and the debug-only compatibility fallback.
- Verified the installed `winloop 0.6.3` API exposes `install()`, `new_event_loop()`, and `run()`; the implementation uses only the factory for supported non-debug execution.
- Repository verification exited zero: `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, `uv run python -m tools.schema.generate --check`, `uv run pytest --basetemp .tmp/pytest-final-two-plans`, `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, and `cargo test --all-features`.
- Runtime benchmark smoke exited zero through the project virtual environment in 9.4 seconds: `event_loop_backend=winloop installed=False version=0.6.3`, `update_dispatch_10k` median 27.579 ms, `media_upload_8m_concurrency_8` median 18.169 ms, `media_download_8m` median 326.353 ms, `tl_upload_get_file_encode_10k` median 142.130 ms, `tl_upload_file_decode_100` median 27.388 ms, and `synthetic_pending_requests_1k` median 4.229 ms.
- Shared repository gate passed on 2026-07-17: 627 Python tests passed with 4 skipped; 16 Rust tests passed; Ruff format/lint, ty, schema generation, Rust format, Clippy, maturin develop, and development/release wheel builds passed.

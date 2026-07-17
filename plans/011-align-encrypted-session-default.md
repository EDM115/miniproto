# Align the runtime with the encrypted session default

## 0. Plan metadata

- Status: completed
- Priority: P1 security and API consistency
- Estimated size: M
- Risk: high; this intentionally changes default client construction and filesystem behavior
- Base commit: cf7db29
- Dependencies: plan 004 must complete first
- Drift check: after plan 004 lands, reopen PLAN.md, docs/session-security.md, README.md, src/miniproto/config.py, src/miniproto/client.py, src/miniproto/session/storage.py, tests/test_client.py, and tests/test_session_storage.py. Stop if Client no longer silently selects InMemorySessionStorage or product docs have intentionally changed the storage contract.

## 1. Objective

Make a Client created without a custom SessionStorage use fail-closed encrypted SQLite persistence instead of silently losing authorization and update state at process exit.

## 2. Context and current state

The architecture promise is explicit:

> PLAN.md:24 says encrypted SQLite is the default and requires a user key or MINIPROTO_SESSION_KEY.
> docs/session-security.md:7-8 calls InMemorySessionStorage a test/throwaway option and EncryptedSQLiteSessionStorage the durable default.

The public config permits no storage:

> src/miniproto/config.py:50-54 defines session_storage: SessionStorage | None = None.

The runtime interprets None as ephemeral:

> src/miniproto/client.py:137-140 selects config.session_storage or InMemorySessionStorage().

README documents encrypted storage but does not warn that normal ClientConfig silently bypasses it:

> README.md:15-17 links the encrypted storage implementation.

Root cause: no default session path exists in the config, so Client chose the convenient test backend despite the secure product requirement.

## 3. Scope

### In scope

- Add a documented default encrypted SQLite path to ClientConfig.
- Instantiate EncryptedSQLiteSessionStorage when session_storage is omitted.
- Fail closed when neither constructor key nor MINIPROTO_SESSION_KEY provides adequate key material.
- Keep explicit InMemorySessionStorage as the opt-in ephemeral path.
- Update every unit/benchmark/example that intentionally needs memory storage.
- Add restart persistence, missing-key, path, sibling, and no-artifact tests.

### Out of scope

- Session-string ergonomics or account auto-naming.
- Unencrypted durable storage.
- Automatic migration of an in-memory session, which has no persisted source.
- Key rotation, handled by future tooling.

## 4. Design

### 4.1 Config contract

Add session_path: str | os.PathLike[str] = "miniproto.session.sqlite" to ClientConfig. If session_storage is not None, it takes precedence and no default-path backend is constructed. If session_storage is None, Client creates EncryptedSQLiteSessionStorage(session_path).
The default relative path is deliberate and visible, matching existing documentation style. Production and multi-account applications must supply a unique absolute path or an explicit backend. Document this collision risk prominently.

### 4.2 Fail-closed timing

Validate key availability when constructing the default backend, before opening a network connection or creating a session file. Missing or too-short keys raise the existing session-key exception. Never catch that error and fall back to memory.
Delay SQLite file creation until normal storage load/save if the backend already behaves that way; constructing Client for validation should not create an empty artifact.

### 4.3 Explicit ephemeral use

Tests, throwaway examples, and benchmarks must pass InMemorySessionStorage explicitly. Do not add an environment switch that silently changes production storage semantics.

### 4.4 Path and sibling behavior

Normalize session_path once without resolving away intentional relative behavior. Ensure encrypted sibling paths for multi-session bot downloads remain derived safely from the selected backend. Add .gitignore coverage for the default session filename/pattern without hiding arbitrary SQLite project files.

### 4.5 Migration messaging

This pre-alpha breaking change means Client(ClientConfig(api_id=..., api_hash=...)) now requires MINIPROTO_SESSION_KEY and can persist a local file. Put the behavior in README quickstart, session security, changelog, and migration notes.

### 4.6 Escape hatch

STOP if the maintainer rejects a working-directory default path. The only acceptable alternate contract is to make session_storage or session_path explicitly required; do not retain silent memory fallback. Update this plan and product docs before implementing that alternate.

## 5. Files to change

| File                             | Change                                                                      |
| -------------------------------- | --------------------------------------------------------------------------- |
| src/miniproto/config.py          | Add and validate session_path                                               |
| src/miniproto/client.py          | Construct encrypted backend when custom storage is absent                   |
| src/miniproto/session/storage.py | Reuse existing fail-closed key validation and sibling behavior              |
| tests/test_client.py             | Add default-backend and explicit-memory tests                               |
| tests/test_session_storage.py    | Add path, key, restart, and no-empty-file tests                             |
| tests across repository          | Pass InMemorySessionStorage explicitly where ephemeral behavior is intended |
| README.md                        | Add default persistence/key quickstart                                      |
| docs/session-security.md         | Define default path, precedence, and multi-account guidance                 |
| docs/development.md              | Keep tests/benchmarks artifact-free                                         |
| CHANGELOG.md                     | Record pre-alpha breaking behavior                                          |
| .gitignore                       | Ignore the documented default session artifact narrowly                     |
| PLAN.md and PROGRESS.md          | Reconcile requirement and completion evidence                               |

## 6. Execution prerequisites

- Complete and verify plan 004 so the new default does not promote a backend with lost-update behavior.
- Inventory every ClientConfig construction and classify production/example versus test/benchmark.
- Confirm the current EncryptedSQLiteSessionStorage constructor key-validation timing.
- Git workflow: no branch, worktree, stage, commit, stash, revert, or push.
- STOP on the path-policy objection described in section 4.6.

## 7. Implementation steps

1. Add failing tests: omitted storage plus no key raises before connect and creates no file; environment key selects EncryptedSQLiteSessionStorage; explicit InMemory remains ephemeral; explicit storage takes precedence over session_path.  
   Verification: uv run pytest tests/test_client.py tests/test_session_storage.py -k "default or key or path"
2. Add ClientConfig.session_path and runtime backend selection. Keep key errors specific and redacted.  
   Verification: uv run pytest tests/test_client.py tests/test_session_storage.py
3. Add a two-client restart test using tmp_path and one key: authorize/save with the first instance, close, then load the same auth/user/update/peer state with the second.  
   Verification: uv run pytest tests/test_session_storage.py -k "restart or persist"
4. Update all tests and benchmarks that relied on the implicit memory backend. Assert the suite creates no miniproto.session.sqlite in repository root.  
   Verification: uv run pytest
5. Verify sibling storage naming from a default encrypted backend and ensure wrong identity/session failures clean up.  
   Verification: uv run pytest tests/test_media_download.py -k "auxiliary or multi_session"
6. Update README, session security, development docs, changelog, PLAN, PROGRESS, and .gitignore.  
   Verification: documentation examples use explicit keys or explicit InMemory and contain no real secrets.
7. Run full verification.  
   Verification: section 8 commands pass and repository status shows no session artifact.

## 8. Testing strategy

### Focused

- uv run pytest tests/test_client.py tests/test_session_storage.py tests/test_media_download.py

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

- Missing key, short key, constructor key, environment key, wrong key on restart.
- Relative and absolute paths, parent creation, custom backend precedence.
- Explicit InMemory creates no file.
- Default backend restart preserves all session domains.
- Multiple account docs require distinct paths.
- No secret or path key material appears in repr/errors.

## 9. Done criteria

- No custom storage means encrypted SQLite, never memory.
- Missing key fails before network activity and without an empty file.
- Explicit ephemeral storage remains easy and obvious.
- Tests/benchmarks leave the repository artifact-free.
- Code, PLAN, README, session-security docs, and PROGRESS agree.

## 10. Rollback and recovery

If default path behavior proves unacceptable, do not restore silent memory fallback. Move to the explicit-required alternative through a documented pre-alpha API change and retain missing-storage tests as a safety gate.

## 11. Risks and mitigations

| Risk                                        | Mitigation                                                  |
| ------------------------------------------- | ----------------------------------------------------------- |
| Two accounts collide on default path        | Prominent unique-path guidance and explicit config          |
| Tests write into repository                 | Explicit InMemory/tmp_path inventory and artifact assertion |
| Users are surprised by key error            | Quickstart and precise exception                            |
| Key error is swallowed into memory fallback | No fallback branch and regression test                      |

## 12. Maintenance and references

- Owner: unassigned
- Review trigger: ClientConfig construction, storage default, session key handling, sibling storage, quickstart, or session naming changes.
- Repository evidence: PLAN.md, docs/session-security.md, README.md, src/miniproto/config.py, src/miniproto/client.py, src/miniproto/session/storage.py, tests/test_client.py, tests/test_session_storage.py.

## 13. Implementation evidence

- 2026-07-16: `ClientConfig.session_path` now defaults to `miniproto.session.sqlite`; an omitted `session_storage` constructs `EncryptedSQLiteSessionStorage`, while an explicit backend retains precedence.
- Missing or shorter-than-16-byte key material fails before a session artifact is created. Environment-key construction, stable `account-download-1.sqlite` sibling naming, explicit in-memory use, repository-artifact absence, and two-client restart persistence across every `SessionRecord` domain have regression coverage.
- Intentional ephemeral clients across unit and stress tests now pass `InMemorySessionStorage` explicitly. README, session-security guidance, development guidance, changelog, PLAN, PROGRESS, and the narrow default/sibling `.gitignore` patterns agree with the runtime contract.
- Focused verification: `uv run pytest tests/test_client.py tests/test_session_storage.py` passed with 51 tests. Plan-scoped Ruff formatting and checks passed across config, client, storage, and the focused test files. An independent fresh review approved the implementation and found no `miniproto.session*.sqlite` artifact in the repository root.
- Shared repository gate passed on 2026-07-17: 627 Python tests passed with 4 skipped; 16 Rust tests passed; Ruff format/lint, ty, schema generation, Rust format, Clippy, maturin develop, and development/release wheel builds passed.

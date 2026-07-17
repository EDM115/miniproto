# Make session updates atomic and domain-incremental

## 0. Plan metadata

- Status: completed
- Priority: P0 correctness and performance foundation
- Estimated size: L
- Risk: high; session persistence carries auth keys, salts, peer access hashes, DC auth, and update cursors
- Base commit: cf7db29
- Dependencies: none
- Dependents: plans 011 and 012
- Drift check: reopen src/miniproto/client.py, src/miniproto/peers.py, src/miniproto/updates/manager.py, src/miniproto/session/storage.py, tests/test_session_storage.py, tests/test_peers.py, and tests/test_updates.py. Stop if every read-modify-write already runs through one atomic storage mutation and encrypted SQLite writes only changed domains.

## 1. Objective

Eliminate lost session updates and unnecessary encrypted SQLite rewrites when peer, update, salt, auth, and media-DC state change concurrently.

## 2. Context and current state

The shared cache copies records but does not serialize read-modify-write sequences:

> src/miniproto/client.py:103-115: _CachedSessionStorage caches load and replaces the full cached payload after save.

Independent components load, replace, and save whole records:

> src/miniproto/peers.py:153-160 loads the current record, merges peers, then saves replace(record, peers=..., user=...).
> src/miniproto/updates/manager.py:188-201 loads the record and saves update_state, peers, and metadata together.
> src/miniproto/client.py:1368-1376 loads and saves metadata after a salt change.
> src/miniproto/client.py:1453-1489 loads and saves media-DC auth state.

The storage protocol exposes only whole-payload load/save:

> src/miniproto/session/storage.py:54-61 defines load, save, clear, and close.

Encrypted SQLite splits records into domains but every save prepares all domains:

> src/miniproto/session/storage.py:152-159 encrypts every result from _split_session_domains(data).

Root cause: atomicity and domain intent are absent from the storage API. Two tasks can derive replacements from the same cached snapshot and the later full save silently erases the earlier change.

## 3. Scope

### In scope

- Add an atomic mutation contract to SessionStorage and all built-in backends.
- Serialize cache reads, mutations, clears, and closes consistently.
- Persist only changed encrypted domains in one SQLite transaction.
- Convert all client, peer, update, salt, user, auth, and dc_auth read-modify-write sites.
- Preserve exact arbitrary mapping payload round trips.
- Add deterministic concurrency tests and write-count instrumentation.

### Out of scope

- Changing encryption format or key derivation.
- Cross-process coordination beyond SQLite transaction guarantees.
- Time-based debounce that weakens update-cursor crash durability.
- Default-storage policy, handled by plan 011.
- Peer lookup indexes, handled by plan 012.

## 4. Design

### 4.1 Public mutation contract

Extend SessionStorage with:

> async def mutate(self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None
> The transform is synchronous, must not await, and receives an isolated copy. Returning None clears the record; otherwise the returned payload becomes the new record. The method returns an isolated copy of the committed result.
> Because the project is pre-alpha, update the protocol directly rather than maintain a hidden optional capability. Add a migration note for custom storage implementations.

### 4.2 Backend atomicity

InMemorySessionStorage owns one `threading.RLock` spanning copy, transform, replace, revision update, and result copy. Its transforms are synchronous and must never await.
EncryptedSQLiteSessionStorage owns one `threading.RLock` shared by every synchronous worker operation. Each async public method delegates to a `_sync` operation that acquires this lock; mutation keeps it across BEGIN IMMEDIATE, legacy/domain load and decryption, transform, canonical plaintext domain diff, changed-domain encryption, upsert/delete, and commit. Roll back on any transform, encryption, or SQLite failure.
Using backend `threading.RLock` avoids binding a storage instance or its siblings to the first asyncio event loop that touches it. Never hold that lock in event-loop code across an await.
close and clear use the same backend lock. close is idempotent, marks the backend closed, and all later load/save/mutate/clear operations raise SessionStorageError. A mutation that acquired the lock first may commit before close; a queued mutation after close fails. A mutation queued after clear receives `None`, so stale snapshots cannot resurrect cleared state.

### 4.3 Domain-incremental writes

Split old and new payloads into auth, peers, update_state, metadata, and payload domains. Compare canonical serialized plaintext per domain before encryption. Generate fresh nonces and write only changed domains; delete domains removed by the mutation. Unchanged ciphertext remains untouched.
Do not compare ciphertext because randomized nonces make equal plaintext differ.

### 4.4 Cached wrapper and domain revisions

_CachedSessionStorage is Client/event-loop-affine and owns an `asyncio.Lock` covering cache population, delegated mutate, cache replacement, save, clear, and close. It never holds a backend threading lock itself. mutate delegates to the backend’s atomic method, then replaces the cache only after a successful commit. A failed commit leaves the previous cache valid.
SessionStorage also exposes a cheap synchronous `domain_revisions()` snapshot whose monotonically increasing values cover `auth`, `peers`, `update_state`, `metadata`, and `payload`. A successful save, mutation, or clear increments only domains whose canonical plaintext changed; loads and failed operations do not increment anything. Built-in backends and the cached wrapper implement the same contract. Plan 012 records the `auth` and `peers` values after building its indexes and rebuilds only when either value changes.
Legacy save remains replace-all behavior and is implemented through the backend’s normal save path, not as an unlocked mutation.

### 4.5 Call-site policy

- Auth bootstrap, auth-key invalidation, auth key, server salt, current user, and dc_auth changes commit immediately.
- UpdateManager atomically changes update_state, its peer entities, and duplicate/channel metadata in one mutation.
- PeerCache atomically merges peer/user fields without reconstructing unrelated domains.
- Do not add temporal debounce in this plan. Incremental domain writes remove the largest write amplification while preserving current durability. Benchmark later before considering coalescing.

### 4.6 Invariants

- A mutation can change only intended fields and cannot erase a concurrently committed unrelated field.
- Auth key and session key material never enters logs or test failure reprs.
- Arbitrary mapping payloads retain their payload domain exactly.
- One failed domain encryption causes a full transaction rollback.

## 5. Files to change

| File                             | Change                                                                     |
| -------------------------------- | -------------------------------------------------------------------------- |
| src/miniproto/session/storage.py | Add mutate, locks, transaction, domain diff, and rollback behavior         |
| src/miniproto/client.py          | Make cache atomic and migrate salt/auth/user/dc_auth mutations             |
| src/miniproto/peers.py           | Replace load/replace/save with atomic peer/user mutation                   |
| src/miniproto/updates/manager.py | Atomically update cursor, peers, and metadata                              |
| src/miniproto/auth/bootstrap.py  | Atomically persist discovered DC options and newly exchanged auth state    |
| src/miniproto/auth/service.py    | Migrate auth/user persistence if it performs read-modify-write             |
| src/miniproto/invoke.py          | Atomically clear invalid auth/user state without erasing unrelated domains |
| tests/test_session_storage.py    | Add backend parity, concurrency, rollback, and changed-domain tests        |
| tests/test_peers.py              | Add peer versus cursor/salt lost-update regression                         |
| tests/test_updates.py            | Add concurrent update-state versus peer/auth regression                    |
| docs/session-security.md         | Document mutation semantics and custom-backend migration                   |
| docs/development.md              | Add storage concurrency invariants                                         |

## 6. Execution prerequisites

- Inventory every .load followed by .save using rg before editing, including auth/bootstrap.py and invoke.py; classify replace-all initialization separately from mutation.
- Confirm SQLite connection ownership and current schema migration behavior.
- Update every in-repository SessionStorage implementation and typed test double for mutate and domain_revisions; document this intentional pre-alpha custom-backend interface change.
- Git workflow: read-only Git only. Do not branch, use worktrees, stage, commit, stash, revert, or push.
- STOP if a SessionStorage implementation exists outside the repository that must remain source-compatible; agree on a compatibility adapter first.
- STOP if the transform would need async work. Fetch network data before mutate, then make the in-transaction transform pure and fast.

## 7. Implementation steps

1. Add a deterministic lost-update test using barriers: peer merge and update cursor both load the same starting record, then commit concurrently. Add equivalent salt and dc_auth cases. Confirm at least one test fails on cf7db29.  
   Verification: uv run pytest tests/test_session_storage.py tests/test_peers.py tests/test_updates.py
2. Add SessionStorage.mutate plus domain_revisions and implement threading-lock-protected InMemorySessionStorage semantics, including transform exception, clear race, idempotent close, post-close failures, copy isolation, and changed-domain revision increments.  
   Verification: uv run pytest tests/test_session_storage.py -k "memory and mutate"
3. Implement EncryptedSQLiteSessionStorage transaction mutation and plaintext domain diff under its worker-thread lock. Preserve legacy single-envelope loading and migrate it on first mutation; add a test hook or SQLite trace callback proving one peer-only change does not rewrite auth/update domains.  
   Verification: uv run pytest tests/test_session_storage.py -k "sqlite and (mutate or domain or rollback)"
4. Make _CachedSessionStorage lock cache population and all mutations. Prove concurrent first loads call the backend once, failed saves do not poison cache, and its domain revisions advance only after committed changes.  
   Verification: uv run pytest tests/test_invoke.py -k "session_storage"
5. Convert PeerCache and UpdateManager. Keep combined update cursor/peer/metadata changes in one transform.  
   Verification: uv run pytest tests/test_peers.py tests/test_updates.py
6. Convert auth bootstrap, invalid-auth clearing, salt, user/auth, and media-DC auth sites. Repeat the inventory until no unsafe read/replace/save sequence remains.  
   Verification: rtk proxy rg -n -U "await ._\\.load\\(\\)[\\s\\S]{0,800}await ._\\.save\\(" src/miniproto
7. Update storage docs and custom-backend migration notes.  
   Verification: uv run ty check
8. Run full verification and benchmark storage-heavy runtime paths before and after.  
   Verification: section 8 commands pass and no benchmark shows a material regression.

## 8. Testing strategy

### Focused

- uv run pytest tests/test_session_storage.py tests/test_peers.py tests/test_updates.py tests/test_invoke.py
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

### Required concurrency cases

- Peer plus update cursor; salt plus peer; dc_auth plus update cursor; auth clear plus late peer save.
- Transform raises before commit; encryption raises mid-domain preparation; SQLite write raises mid-transaction.
- Concurrent first load, clear during queued mutation, close during queued mutation.
- Peer-only mutation rewrites only peers; metadata-only mutation rewrites only metadata.
- Auth and peer domain revision snapshots advance independently and never advance for a failed transaction.
- Arbitrary mapping payload remains byte-equivalent after unrelated SessionRecord tests.

## 9. Done criteria

- All built-in storage backends implement the same atomic mutation semantics.
- Deterministic barriers cannot reproduce a lost unrelated update.
- Encrypted SQLite changes only dirty domains and rolls back atomically.
- Every production read-modify-write site uses mutate.
- Domain revisions expose committed per-domain invalidation without deserializing or comparing the full record.
- Existing arbitrary mapping and encrypted-envelope tests remain passing.
- Full verification and benchmark smoke pass.

## 10. Rollback and recovery

If a storage migration fails, do not rewrite or delete user session files automatically. Retain load compatibility, add a regression fixture for the old file, and roll back the new mutation schema through a user-owned Git action. A recovery tool must operate on a copy and require the same session key.

## 11. Risks and mitigations

| Risk                                | Mitigation                                              |
| ----------------------------------- | ------------------------------------------------------- |
| Long transform holds SQLite lock    | Require synchronous, side-effect-free transforms        |
| Cache diverges after failed commit  | Update cache only after backend success                 |
| Domain diff drops mapping data      | Preserve payload domain and add golden round trips      |
| Custom backend breakage             | Pre-alpha migration note and protocol conformance tests |
| Performance regression from locking | One lock per storage, short transforms, benchmark smoke |

## 12. Maintenance and references

- Owner: unassigned
- Review trigger: any new session field, storage backend, load/save pair, cursor persistence, peer persistence, salt handling, or DC authorization cache.
- Repository evidence: src/miniproto/client.py, src/miniproto/peers.py, src/miniproto/updates/manager.py, src/miniproto/session/storage.py, tests/test_session_storage.py, tests/test_peers.py, tests/test_updates.py.

## 13. Implementation evidence

- Added the atomic synchronous mutation contract, per-domain revision snapshots, lock-protected in-memory and encrypted SQLite backends, plaintext dirty-domain writes, legacy-envelope migration, and transaction rollback behavior.
- Converted production peer, update, auth, invalid-auth, salt, and media-DC persistence from stale load/replace/save sequences to atomic mutations; the final unsafe sequence inventory is clean.
- Independent review reproduced cancellation divergence between SQLite worker completion and the cached wrapper. The repair now shields and joins every backend operation while retaining the wrapper lock, reconciles committed cache/revisions/closed state, and then re-raises the first cancellation.
- Focused implementation verification passed with 87 plan tests and 20 auth regressions. The cancellation repair passed 36 session-storage tests, 8 client tests, five dedicated paused-worker cancellation cases, scoped type/schema checks, and independent correctness review.
- Shared repository gate passed on 2026-07-17: 627 Python tests passed with 4 skipped; 16 Rust tests passed; Ruff format/lint, ty, schema generation, Rust format, Clippy, maturin develop, and development/release wheel builds passed.

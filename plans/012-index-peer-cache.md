# Add in-memory indexes to the peer cache
## 0. Plan metadata
- Status: proposed
- Priority: P2 performance
- Estimated size: M
- Risk: medium; stale or conflicting indexes can return the wrong access hash
- Base commit: cf7db29
- Dependencies: plan 004
- Drift check: after plan 004 lands, reopen src/miniproto/peers.py, src/miniproto/client.py, src/miniproto/updates/manager.py, src/miniproto/session/models.py, tests/test_peers.py, and tools/bench/benchmark_runtime_paths.py. Stop if warm peer resolution already uses maintained indexes with peer-domain invalidation.
## 1. Objective
Replace repeated O(n) scans and tuple merges with cached O(1)-average lookup indexes while preserving access-hash hygiene, username TTL, self precedence, and durable peer state.
## 2. Context and current state
PeerCache has no in-memory state:
> src/miniproto/peers.py:24-29 stores config, storage, and invoker only.
Lookup repeatedly loads a copied SessionRecord and scans tuples:
> src/miniproto/peers.py:82-86 finds a kind/id entry.
> src/miniproto/peers.py:100-108 scans every peer for a normalized phone.
> src/miniproto/peers.py:110-120 searches username cache before a network resolve.
> src/miniproto/peers.py:354-367 scans numeric candidates and ids.
Persistence repeatedly merges tuples:
> src/miniproto/peers.py:153-160 loads, merges all entries, and saves a replacement.
Username freshness is already enforced:
> src/miniproto/peers.py:415-429 rejects stale usernames and checks alternate raw usernames.
Peer records contain the indexable keys:
> src/miniproto/session/models.py:99-106 stores kind/id, access_hash, username, phone, updated_at, and raw.
Root cause: the durable tuple is treated as the query structure on every request instead of as a persistence boundary.
## 3. Scope
### In scope
- Lazy-load and maintain indexes by kind/id, numeric id, normalized username aliases, and normalized phone.
- Track user identity/self alongside peer entries.
- Invalidate/rebuild only when peer/user storage domains change.
- Preserve current merge, min-entity, access-hash, username-TTL, and numeric-id selection behavior.
- Add large-cache benchmarks and memory measurements.
### Out of scope
- A database query API for peer lookup.
- Cross-process shared indexes.
- Changing Telegram peer-id encoding.
- Persisting redundant index tables in encrypted SQLite.
## 4. Design
### 4.1 Index structures
Maintain under one PeerCache lock:
- entries_by_key: dict[(PeerKind, int), PeerCacheEntry]
- keys_by_id: dict[int, set[(PeerKind, int)]]
- key_by_username: dict[str, (PeerKind, int)] including active aliases from raw.usernames
- key_by_phone: dict[str, (PeerKind, int)]
- cached_user: UserIdentity | None
- loaded peer-domain and auth/user-domain revisions
Durable storage remains a canonical tuple. Indexes are process-local derived state.
### 4.2 Integration with atomic storage
Plan 004’s cached storage mutation layer must expose cheap per-domain revisions or an equivalent changed-domain notification. Before lookup, PeerCache compares peer/user revisions. Rebuild once under lock only when relevant domains changed; update_state-only and metadata-only mutations must not invalidate peer indexes.
After PeerCache commits its own merge, apply the committed entries incrementally and advance its recorded revisions so the next lookup does not rebuild.
### 4.3 Conflict policy
Reuse existing _merge_entries semantics. A min entity cannot replace a full access hash. Newer full records replace older values. Username/phone conflicts select the same winner as canonical merge and remove aliases previously owned by a replaced entry. Ambiguous numeric ids continue through current preferred-kind ordering and self fallback.
### 4.4 TTL
Index usernames regardless of age but check updated_at at lookup. When stale, remove the alias from the in-memory username map and perform contacts.resolveUsername; do not delete the durable peer until a normal merge replaces it. Phone and kind/id behavior remain as currently documented.
### 4.5 Performance targets
Add a benchmark with 10,000 realistic PeerCacheEntry values:
- After one warm load, repeated kind/id, username, and phone resolutions perform no SessionRecord tuple scan.
- Median warm cached resolution improves at least 20 times relative to cf7db29 on the same machine.
- Index retained memory stays below 2.5 times the serialized/canonical peer-entry heap measured by the same harness.
- Updating one peer is O(1)-average plus the required atomic durable write, not an index-wide rebuild.
### 4.6 Rejected alternatives
- SQLite lookup indexes are rejected because encrypted per-domain blobs are not queryable without weakening storage.
- A single id dictionary is rejected because user/chat/channel ids can collide.
- Rebuilding indexes on every session mutation is rejected because update cursors change frequently.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/peers.py | Add lazy indexes, revision checks, incremental merge, and conflict cleanup |
| src/miniproto/session/storage.py or src/miniproto/client.py | Expose per-domain revisions from plan 004’s cache |
| src/miniproto/updates/manager.py | Ensure committed peer-domain changes advance revisions |
| tests/test_peers.py | Add index correctness, invalidation, conflict, TTL, and no-scan tests |
| tests/test_updates.py | Prove update-delivered entities become visible without unrelated rebuilds |
| tools/bench/benchmark_runtime_paths.py | Add large peer-cache time and memory case |
| docs/development.md | Document benchmark and cache invalidation invariant |
## 6. Execution prerequisites
- Complete plan 004 and identify its committed-domain diff/revision signal.
- Freeze current numeric candidate and merge behavior with characterization tests before refactoring.
- Git workflow: no branch, worktree, stage, commit, stash, revert, or push.
- STOP if per-domain invalidation cannot be obtained without reintroducing full payload comparison on each lookup.
## 7. Implementation steps
1. Add characterization tests for duplicate ids across kinds, self precedence, min/full replacement, alternate usernames, username TTL, phone normalization, and update-delivered entities.  
   Verification: uv run pytest tests/test_peers.py tests/test_updates.py
2. Add the 10,000-entry benchmark and capture cf7db29 time, scan count, storage load count, and tracemalloc memory. Use an injected counter rather than timing alone to prove no scans.  
   Verification: uv run python tools/bench/benchmark_runtime_paths.py
3. Expose per-domain revisions from the atomic cached storage and test that only peers/user mutations advance the values PeerCache observes.  
   Verification: uv run pytest tests/test_session_storage.py
4. Implement lazy index build under a lock and route kind/id, numeric, username, and phone resolution through it.  
   Verification: uv run pytest tests/test_peers.py
5. Implement incremental merge and alias removal after committed peer mutations. Ensure UpdateManager-driven peer changes trigger one lazy rebuild or direct update.  
   Verification: uv run pytest tests/test_peers.py tests/test_updates.py
6. Measure performance and memory. Meet section 4.5 or profile before accepting the design.  
   Verification: uv run python tools/bench/benchmark_runtime_paths.py
7. Run full verification.  
   Verification: all section 8 commands pass.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_peers.py tests/test_updates.py tests/test_session_storage.py
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
- Same numeric id across user/chat/channel.
- Self identity versus cached user entry.
- Min entity cannot poison full access hash.
- Username alias replacement, stale username refresh, phone normalization.
- Peer mutation invalidates; update_state-only mutation does not.
- Concurrent first lookup and merge return one consistent index.
## 9. Done criteria
- Warm cached lookups perform no tuple scan or storage deserialization.
- Index results match all characterization tests.
- Per-domain invalidation cannot serve stale peers after updates.
- Time and memory targets are measured and met.
- Full verification passes.
## 10. Rollback and recovery
If an index conflict returns a wrong access hash, retain the failing characterization fixture, disable only the affected lookup index behind one code path, and fall back to canonical scan until fixed. Do not discard durable peer data.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Stale index after external mutation | Per-domain committed revisions |
| Alias points to replaced peer | Remove old aliases before inserting new |
| Memory exceeds speed benefit | Explicit 2.5-times target and benchmark |
| Lock contention | Lazy build once and short incremental updates |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: PeerCacheEntry fields, merge policy, update entity persistence, storage domains, numeric peer encoding, or username TTL.
- Repository evidence: src/miniproto/peers.py, src/miniproto/client.py, src/miniproto/updates/manager.py, src/miniproto/session/models.py, tests/test_peers.py, tools/bench/benchmark_runtime_paths.py.

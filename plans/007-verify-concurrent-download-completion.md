# Verify concurrent downloads have no holes
## 0. Plan metadata
- Status: proposed
- Priority: P0 data correctness
- Estimated size: M
- Risk: high; incorrect completion can silently return or persist corrupted media
- Base commit: cf7db29
- Dependencies: none
- Related plans: 001 defines reconnect ambiguity for the RPC layer; this plan remains responsible for file-range completeness
- Drift check: reopen src/miniproto/media/download.py and tests/test_media_download.py. Stop if concurrent completion already requires exact contiguous coverage and rejects every premature empty or short chunk.
## 1. Objective
Ensure a concurrent download reports success only when every requested byte range has been received and committed, with no zero-filled or stale holes in memory or file destinations.
## 2. Context and current state
Sequential download already fails when an explicit range is unsatisfied:
> src/miniproto/media/download.py:677-685 raises MediaDownloadError when an empty payload arrives while bytes remain.
The concurrent path treats the same signal as successful stopping:
> src/miniproto/media/download.py:888-895 sets stopped on an empty payload, skips the range, and continues processing completed tasks.
Short non-empty results are submitted without proving the full expected range arrived:
> src/miniproto/media/download.py:838-846 trims oversized payloads but returns short payloads with expect_limit unchanged.
The writer permits arbitrary seeks:
> src/miniproto/media/download.py:1534-1537 seeks to each output offset and writes whatever payload was returned.
Existing tests prove the happy path and retry behavior:
> tests/test_media_download.py:287-308 verifies ordered output.
> tests/test_media_download.py:500-520 verifies one transient chunk retry.
Root cause: downloaded byte sum and task exhaustion are used as a completion proxy; neither proves contiguous coverage of the requested interval.
## 3. Scope
### In scope
- Detect empty and short chunks before the target end as premature EOF.
- Track exact completed intervals and require full contiguous coverage.
- Cancel unnecessary in-flight requests after a terminal failure.
- Make new-file, resumed-file, and memory-destination failure cleanup deterministic.
- Keep progress monotonic and never emit a false final-complete callback.
- Add adversarial out-of-order chunk tests.
### Out of scope
- Changing Telegram chunk-size legality.
- Multi-session assembly, which already verifies each worker size separately.
- CDN cryptography or file-reference refresh policy.
- Sparse-file support as a public feature.
## 4. Design
### 4.1 Target interval
Compute target_start and target_end once from offset plus explicit limit or known total size. The concurrent path is allowed only when target_end is known. Each launched task owns a non-overlapping expected interval whose logical length is expect_limit even if wire_limit over-requests for Telegram alignment.
### 4.2 Chunk acceptance
After trimming an oversized response to expect_limit:
- len(payload) == expect_limit is success.
- len(payload) < expect_limit before target_end is premature EOF and raises MediaDownloadError with request offset, expected length, and received length.
- Empty payload is the same premature EOF case, not normal completion.
The sequential unknown-size path retains EOF discovery behavior; do not infer unknown EOF concurrently.
### 4.3 Coverage tracker
Record accepted half-open intervals and merge adjacent intervals. Success requires exactly one contiguous interval covering target_start through target_end. Track logical covered bytes from merged ranges, not a naive sum, so duplicates or overlaps cannot inflate completion.
Submit a range to the writer only after it passes length and interval validation. On writer completion, mark it committed. Final success requires both fetched coverage and committed coverage.
### 4.4 Failure and cleanup
On the first premature EOF or writer error, cancel and await every pending fetch, close the writer, and re-raise.
- For a destination newly created by this call, remove the partial file.
- For resume, preserve only the previously verified prefix and truncate any newly written bytes beyond the last contiguous committed boundary.
- For memory destinations, discard the buffer and return no result.
Never leave preallocated zeros or stale tail bytes as a successful file.
### 4.5 Progress
Report committed covered bytes, capped at target length, monotonically. Emit the guaranteed final callback only after the coverage assertion and writer flush succeed.
### 4.6 Rejected alternatives
- Comparing downloaded sum to limit is rejected because holes and overlaps can balance.
- Treating short read as EOF is rejected when a known target remains.
- Re-downloading all ranges serially at the end is rejected as expensive and masks the scheduler bug.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/media/download.py | Validate chunk length, track coverage, cancel on failure, and clean partial destinations |
| tests/test_media_download.py | Add middle-hole, short-tail, out-of-order, resume, memory, and progress regressions |
| docs/development.md | Document exact-limit and premature-EOF behavior |
| docs/media.md | Update user-facing failure semantics if this file owns download docs |
## 6. Execution prerequisites
- Identify the exact writer lifecycle and destination cleanup path before changing the scheduler.
- Keep tests deterministic with fake offset invokers; do not use live Telegram for acceptance.
- Git workflow: no branch, worktree, stage, commit, stash, revert, or push.
- STOP if any caller enters the concurrent path without a known target_end; route that caller to sequential EOF discovery first.
## 7. Implementation steps
1. Add failing tests where offset 1024 returns empty, offset 1024 returns a short non-empty chunk, and later offsets complete out of order. Assert MediaDownloadError and no successful destination.  
   Verification: uv run pytest tests/test_media_download.py -k "empty or short or hole"
2. Isolate target interval and range validation helpers. Add pure tests for exact fit, adjacency, overlap, duplicate, gap, and overrun.  
   Verification: uv run pytest tests/test_media_download.py -k "coverage"
3. Reject short/empty concurrent chunks and cancel/await pending tasks on first failure. Prove the invoker sees cancellation for delayed later chunks.  
   Verification: uv run pytest tests/test_media_download.py -k "concurrent"
4. Integrate committed-range tracking with the writer. Assert coverage only after queue drain and flush.  
   Verification: uv run pytest tests/test_media_download.py
5. Implement cleanup for new path, resume, and memory destinations. Add a pre-existing-file fixture proving failure never truncates the verified prefix.  
   Verification: uv run pytest tests/test_media_download.py -k "partial or resume or memory"
6. Verify progress never reaches target on failure and reaches it exactly once on success.  
   Verification: uv run pytest tests/test_media_download.py -k "progress"
7. Run benchmark smoke and full verification.  
   Verification: section 8 commands pass with no material happy-path throughput regression.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_media_download.py
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
- Empty first, middle, and final expected chunk.
- Short first, middle, and legal aligned-tail response.
- Out-of-order completion around a missing range.
- Duplicate/overlapping result cannot inflate covered bytes.
- New file removal, resume prefix preservation, in-memory buffer discard.
- Pending tasks are cancelled and awaited; no leaked-task warning.
## 9. Done criteria
- Concurrent success mathematically proves full committed coverage.
- Any premature empty/short response raises and cannot leave a successful sparse file.
- Failure cleanup is deterministic for every destination mode.
- Progress cannot announce completion before coverage and flush.
- Focused, benchmark, and full verification pass.
## 10. Rollback and recovery
If stricter validation exposes a legitimate server short-read pattern, capture only offsets, requested/received lengths, and known total size. Add the fixture and correct target calculation; never restore success with an unverified gap.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Legal tail is mistaken for short read | Compare with logical expect_limit after wire over-request trimming |
| Cleanup deletes a user file | Track whether this call created it; resume preserves verified prefix |
| Coverage tracking slows hot path | Non-overlapping ranges allow a compact ordered/merged structure |
| Cancellation leaks tasks | Cancel then gather with return_exceptions before closing writer |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: scheduler, adaptive chunk sizing, writer, resume, range cache, or destination changes.
- Repository evidence: src/miniproto/media/download.py and tests/test_media_download.py.

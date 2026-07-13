# Bound native and fallback vector decoding before allocation
## 0. Plan metadata
- Status: proposed
- Priority: P0 memory safety and denial-of-service resistance
- Estimated size: M
- Risk: medium; primitive codec changes affect generated API decoding and native/fallback parity
- Base commit: cf7db29
- Dependencies: none
- Drift check: reopen src/miniproto/tl/codec.py, rust/miniproto/src/tl.rs, src/miniproto/_native_fallback.py, tests/test_tl_codec.py, tests/test_native.py, and tests/test_native_parity.py. Stop if both decoders validate count against remaining bytes before any allocation and Rust uses fallible reserve.
## 1. Objective
Reject impossible TL primitive-vector counts in constant space before Rust or Python attempts to allocate or iterate attacker-controlled lengths.
## 2. Context and current state
The public codec routes primitive int and long vectors through native helpers:
> src/miniproto/tl/codec.py:132-139 calls native vector decoders.
Rust trusts the decoded count for allocation:
> rust/miniproto/src/tl.rs:232-247 casts a non-negative i32 count and calls Vec::with_capacity(count) before reading int elements.
> rust/miniproto/src/tl.rs:260-275 does the same for long elements.
The fallback avoids one large preallocation but still loops over the untrusted count:
> src/miniproto/_native_fallback.py:325-345 accepts any non-negative count and repeatedly decodes until input exhaustion.
Existing tests cover valid round trips:
> tests/test_tl_codec.py:104-114 verifies int and long vector fast paths.
Root cause: non-negative count is treated as sufficient validation even though the encoded buffer gives a strict maximum element count.
## 3. Scope
### In scope
- Validate header arithmetic and count * element_width against remaining input before allocation or iteration.
- Use fallible Rust allocation for valid counts.
- Mirror malformed-input exceptions in fallback and native wrappers.
- Harden encode-side count conversion where it can overflow i32.
- Add primitive, parity, Rust unit, and regression tests.
### Out of scope
- A global arbitrary maximum below the size permitted by input.
- Generic object vectors whose elements have variable size, except a separate follow-up if their parser has the same issue.
- Changing TL wire format or tuple return types.
## 4. Design
### 4.1 Decode validation
For a vector beginning at offset:
- Use checked addition to locate offset + 8.
- Reject truncated constructor/count headers.
- Reject negative count.
- Compute remaining = data_length - elements_offset only after checked bounds.
- For int require count <= remaining // 4; for long require count <= remaining // 8.
- Reject before Vec allocation, Python list/tuple growth, or the first element loop.
Trailing bytes remain allowed because decode returns the next offset; the count is bounded by available bytes, not required to consume the entire input.
### 4.2 Rust allocation
After structural validation, create an empty Vec and call try_reserve_exact(count). Map capacity overflow to ValueError and allocator exhaustion to PyMemoryError without panic or process abort. Keep all offset multiplication and addition checked.
### 4.3 Fallback parity
Perform the same remaining-byte predicate before constructing values. Use existing scalar decode functions or a bounded unpack strategy, but preserve exact signed int/long semantics and returned offset.
### 4.4 Encode validation
Reject values.len greater than i32::MAX before writing the count. Use checked capacity arithmetic and fallible reserve in Rust encode paths. This is defensive and should be unreachable for realistic Python sequences, but removes an unchecked cast.
### 4.5 Error contract
Malformed wire counts raise ValueError with a stable phrase such as vector count exceeds remaining payload. Allocation failure after a structurally valid large input raises MemoryError. Native and fallback tests compare type and stable phrase, not full implementation-specific wording.
## 5. Files to change
| File | Change |
| --- | --- |
| rust/miniproto/src/tl.rs | Checked lengths, fallible allocation, encode count guard, Rust tests |
| src/miniproto/_native_fallback.py | Matching pre-loop validation and encode guard |
| src/miniproto/tl/codec.py | Normalize exceptions only if native/fallback public behavior differs |
| tests/test_tl_codec.py | Add public malformed-count regression tests |
| tests/test_native.py | Exercise direct native/fallback functions |
| tests/test_native_parity.py | Compare accepted values, offsets, and malformed exceptions |
| tests/test_performance_primitives.py | Add a bounded smoke case if appropriate |
## 6. Execution prerequisites
- Build or use the existing editable native extension so native tests do not silently exercise fallback only.
- Confirm direct native functions accept bytes but public fallback paths may receive memoryview.
- Git workflow: read-only Git only; no branch, worktree, stage, commit, stash, revert, or push.
- STOP if PyO3 cannot map try_reserve failure without allocating a large error payload; use a small static message.
## 7. Implementation steps
1. Add an eight-byte vector header with count i32::MAX and no elements to direct and public tests. Assert immediate ValueError in fallback and native paths. Add one-element-short cases for int and long.  
   Verification: uv run pytest tests/test_tl_codec.py tests/test_native.py tests/test_native_parity.py -k "vector"
2. Implement fallback validation before loops, including checked offset semantics for negative or oversized Python offsets.  
   Verification: uv run pytest tests/test_tl_codec.py tests/test_native_parity.py
3. Implement Rust checked arithmetic and try_reserve_exact plus unit tests that never allocate from malformed counts.  
   Verification: cargo test --all-features
4. Add encode count guards and preserve valid golden bytes.  
   Verification: uv run pytest tests/test_tl_codec.py tests/test_native.py
5. Run native/fallback performance smoke to ensure valid hot paths do not regress materially.  
   Verification: uv run python tools/bench/benchmark_runtime_paths.py
6. Run full verification.  
   Verification: all section 8 commands pass.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_tl_codec.py tests/test_native.py tests/test_native_parity.py tests/test_performance_primitives.py
- cargo test --all-features
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
- Negative count, i32::MAX count, exact remaining bytes, one byte short, nonzero offset near buffer end.
- Int and long, bytes and memoryview public paths.
- Valid vector followed by unrelated trailing bytes preserves next offset.
- Encode count overflow reports a controlled exception.
## 9. Done criteria
- No vector decoder allocates or loops until count fits remaining bytes.
- Rust uses checked arithmetic and fallible reserve.
- Native and fallback reject the same malformed fixtures.
- Valid codec golden vectors and runtime benchmarks remain healthy.
## 10. Rollback and recovery
If a valid generated object starts failing, reduce the issue to a primitive fixture and correct only the offset/count predicate. Do not restore Vec::with_capacity on unchecked wire input.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Off-by-one rejects exact payload | Exact-fit fixtures for both widths |
| Native extension is not loaded in CI | Assert native availability in native-specific tests or skip explicitly |
| Error normalization hides MemoryError | Preserve malformed versus allocation-failure distinction |
| Check slows hot path | Simple division after header read and benchmark smoke |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: new native TL collection codecs, generic vector optimizations, or changes to memoryview routing.
- Repository evidence: src/miniproto/tl/codec.py, rust/miniproto/src/tl.rs, src/miniproto/_native_fallback.py, tests/test_tl_codec.py, tests/test_native.py, tests/test_native_parity.py.

# Enforce the pending RPC cap before cold-start awaits
## 0. Plan metadata
- Status: proposed
- Priority: P0 resource bound
- Estimated size: M
- Risk: medium; permit lifecycle spans connect, send, response, cancellation, reconnect, timeout, and disconnect
- Base commit: cf7db29
- Dependencies: none
- Drift check: reopen src/miniproto/connection/sender.py, tests/test_transport_runtime.py, tests/test_resource_limits.py, and src/miniproto/errors.py. Stop if request capacity is already reserved atomically before the first await and released exactly once on every terminal path.
## 1. Objective
Guarantee max_pending_rpcs is a real upper bound even when many requests arrive concurrently before the sender is connected.
## 2. Context and current state
The current limit check reads a mutable map without reserving capacity:
> src/miniproto/connection/sender.py:207-221 checks len(self._pending), then awaits self.connect.
Registration occurs later under another lock:
> src/miniproto/connection/sender.py:307-350 acquires _send_lock and inserts self._pending[msg_id] only after connection and encoding work.
Existing coverage starts with requests already populating the map:
> tests/test_transport_runtime.py:945-966 waits until pending_count reaches two, then verifies the third request is rejected.
Root cause: multiple cold-start callers can all observe an empty pending map and pass the check before any caller registers.
## 3. Scope
### In scope
- Atomically reserve one RPC slot before request’s first connection await.
- Release exactly once after success, error, cancellation, timeout, send failure, reconnect exhaustion, or disconnect.
- Make sender_state and metrics report reserved logical RPCs rather than msg_id aliases.
- Add cold-start burst and lifecycle race tests.
### Out of scope
- Limiting one-way service messages sent through send.
- Queueing indefinitely when the cap is full; current API fails fast.
- Per-client limits across multiple media senders.
- OS socket connection limits.
## 4. Design
### 4.1 Logical reservation
Add _pending_slots_used and _pending_slots_lock. _reserve_pending_slot awaits only this short lock, checks the configured cap, increments on success, records a metric, and raises PendingRpcLimitExceeded on failure. It runs before connect.
The request coroutine owns the reservation. PendingRequest aliases created by reconnect do not acquire extra slots.
### 4.2 Release ownership
Wrap the complete request lifecycle in try/finally after successful reservation. _release_pending_slot decrements under the same lock and asserts against underflow. It runs once when the logical request ends, regardless of how many msg_ids represented it.
Do not release when an old msg_id is replaced during safe reconnect. Do release when the future completes with a result, RPC error, ambiguity, timeout, cancellation, fatal sender error, or disconnect.
### 4.3 State and diagnostics
SenderState.pending_count becomes logical reserved count. If map cardinality remains useful, expose it as a separately named internal/debug metric, not the public resource-limit count.
Limit errors report used and configured capacity without request bodies.
### 4.4 Fairness and performance
The API remains fail-fast rather than waiting for a semaphore. A short asyncio.Lock acquisition is acceptable before connect and prevents check-then-act races. Keep the lock out of encoding, transport send, and response processing.
### 4.5 Rejected alternatives
- asyncio.Semaphore acquire with a zero timeout is rejected because non-blocking acquisition semantics are awkward and cancellation-prone.
- Checking inside _send_lock is rejected because callers can still accumulate while awaiting connect and the lock covers expensive send work.
- Counting len(_pending) is rejected because reconnect aliases and pre-registration requests differ from logical calls.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/connection/sender.py | Add atomic logical reservation and exact release lifecycle |
| tests/test_transport_runtime.py | Add delayed-connector cold burst and terminal-path tests |
| tests/test_resource_limits.py | Assert configured limit and metrics at client level |
| src/miniproto/observability.py | Add or rename logical pending metrics if needed |
| docs/development.md | Clarify fail-fast logical RPC limit |
## 6. Execution prerequisites
- Inventory every place PendingRequest is removed or a future is completed.
- Decide whether sender_state.pending_count is documented; preserve compatibility by changing semantics only to the intended logical count.
- Git workflow: read-only Git only; no branch, worktree, stage, commit, stash, revert, or push.
- STOP if request currently performs any await before entering MTProtoSender.request; this plan bounds sender-owned work only and the broader client queue needs separate treatment.
## 7. Implementation steps
1. Add a delayed connector controlled by an Event. Launch far more requests than max_pending_rpcs before releasing connect. Assert exactly the configured number are admitted and every other task fails quickly. Confirm the test fails on cf7db29.  
   Verification: uv run pytest tests/test_transport_runtime.py -k "cold and pending"
2. Implement reserve/release helpers and wrap request from before connect through terminal completion. Add an underflow assertion and logical-count metric.  
   Verification: uv run pytest tests/test_transport_runtime.py -k "pending_rpc_limit"
3. Add cancellation during connect, connect exception, cancellation during send, send exception, response timeout, RPC success, reconnect success, reconnect exhaustion, and disconnect tests. After each, assert pending_count is zero.  
   Verification: uv run pytest tests/test_transport_runtime.py -k "pending or cancel or timeout"
4. Update sender_state and resource-limit tests. Ensure one safe request with multiple reconnect msg_ids still consumes one slot.  
   Verification: uv run pytest tests/test_resource_limits.py tests/test_transport_runtime.py
5. Add or update observability assertions without logging request payloads.  
   Verification: uv run pytest tests/test_observability.py
6. Run a synthetic pending-request benchmark to measure the short lock overhead.  
   Verification: uv run python tools/bench/benchmark_runtime_paths.py
7. Run full verification.  
   Verification: all section 8 commands pass.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_transport_runtime.py tests/test_resource_limits.py tests/test_observability.py
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
- Cold disconnected burst, already connected burst, max one, and unlimited None.
- Cancellation at connect/send/wait; connect/send exceptions; timeout; success; disconnect.
- Safe reconnect reuses one slot across fresh msg_ids.
- Concurrent release and disconnect cannot underflow.
## 9. Done criteria
- No execution can admit more than max_pending_rpcs logical sender requests.
- Capacity is reserved before connection work and released exactly once.
- sender_state.pending_count and metrics return to zero on every terminal path.
- Fail-fast behavior and exception type remain stable.
- Focused, benchmark, and full verification pass.
## 10. Rollback and recovery
If the reservation logic deadlocks, retain the cold-burst regression and remove only the faulty implementation through a user-owned Git action. Do not restore the racy check as a completed resource limit.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Permit leaks | One coroutine-owned try/finally and exhaustive terminal-path tests |
| Double release | Private token/flag plus underflow assertion |
| Lock overhead | Short critical section and benchmark |
| Pending map and logical count diverge | Separate invariants and reconnect alias test |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: request lifecycle, reconnect aliasing, cancellation, sender_state, disconnect, or max_pending_rpcs changes.
- Repository evidence: src/miniproto/connection/sender.py, tests/test_transport_runtime.py, tests/test_resource_limits.py, src/miniproto/errors.py.

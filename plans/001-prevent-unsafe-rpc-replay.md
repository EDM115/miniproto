# Prevent unsafe RPC replay after reconnect
## 0. Plan metadata
- Status: proposed
- Priority: P0 release blocker
- Estimated size: M
- Risk: high; this changes reconnect behavior and the failure surfaced for ambiguous writes
- Base commit: cf7db29
- Dependencies: none
- Dependents: plans 007 and 008 rely on predictable sender request ownership
- Drift check: before implementation, reopen src/miniproto/invoke.py, src/miniproto/client.py, src/miniproto/connection/sender.py, tests/test_invoke.py, and tests/test_transport_runtime.py. If retryability is already carried into PendingRequest or _resend_pending no longer resends every stale request, stop and re-audit this plan against the new behavior.
## 1. Objective
Prevent an ordinary reconnect from executing a non-idempotent Telegram RPC twice when the first execution succeeded server-side but its response was lost. Preserve transparent retry for read-only requests and Telegram writes protected by random_id.
## 2. Context and current state
Client.invoke already classifies retry safety:
> src/miniproto/invoke.py:176-189: is_retryable_request returns true for safe prefixes and selected random_id writes.
> src/miniproto/client.py:1044: retryable = is_retryable_request(raw_request, retry)
The classification is only used by the outer invoke retry loop:
> src/miniproto/client.py:1057-1059: sender.request receives the wrapped request, content_related, and timeout, but no retry-safety flag.
The sender loses the semantic distinction:
> src/miniproto/connection/sender.py:57-62: PendingRequest stores body, content_related, future, attempts, and transport.
> src/miniproto/connection/sender.py:575-603: _resend_pending selects every request sent on an old transport and sends it again with a fresh msg_id.
Existing coverage explicitly expects unconditional replay:
> tests/test_transport_runtime.py:470-490: a server-side close causes the same request to be received on a second connection.
> tests/test_invoke.py:615-630: a random_id message request is expected to remain retryable.
Root cause: retry safety is decided at the Client layer but is not part of sender-owned pending state, so reconnect recovery cannot distinguish a safe replay from an ambiguous mutation.
## 3. Scope
### In scope
- Carry the already computed retry-safety decision from Client.invoke into MTProtoSender.request and PendingRequest.
- Fail unsafe in-flight RPCs whose transport dies after they may have been sent.
- Keep safe reads and random_id-protected writes eligible for transparent resend.
- Add a dedicated public exception for an ambiguous RPC outcome.
- Update fake-server and invoke tests for both safe and unsafe paths.
### Out of scope
- Changing which generated Telegram methods count as safe beyond correcting demonstrably wrong classifications.
- Application-level exactly-once guarantees.
- Retrying an unsafe request because a caller catches the ambiguity exception.
- Changing Telegram service-message resend handling without separate protocol evidence.
## 4. Design
### 4.1 Request metadata
Add retry_safe: bool to PendingRequest and a keyword-only retry_safe: bool = False argument to MTProtoSender.request. Default false is fail-closed for direct sender callers. Client.invoke must pass the result of is_retryable_request after wrappers are built; the semantic decision belongs to the innermost raw request, not InvokeWithLayer or InvokeWithoutUpdates.
### 4.2 Ambiguous outcome
Add AmbiguousRpcResult under src/miniproto/errors.py. It must state that the request may have executed and must retain a redacted request context. It must not subclass a transport exception that Client.invoke automatically retries.
When a stale pending request is unsafe, _resend_pending must atomically remove every msg_id alias for that PendingRequest and complete its future with AmbiguousRpcResult. Safe entries continue through the existing fresh-msg_id resend path.
### 4.3 Boundary semantics
- A failure before _send_pending registers or attempts transport send follows the existing immediate send-error path.
- Once a transport accepted the payload and later died before a correlated result, an unsafe request is ambiguous.
- Cancellation and timeout still remove the pending entry and must not leak a future or capacity permit.
- Explicit retry=True remains an intentional caller override and therefore marks the pending request safe; document that it can duplicate side effects.
- retry=False must prevent both the Client-level retry loop and reconnect-level replay.
### 4.4 Invariants
- One logical PendingRequest has one future even when a safe request receives new msg_ids.
- An unsafe logical request is never submitted on a second transport automatically.
- Random-id-protected requests retain current transparent recovery.
- Error rendering never exposes tokens, message bodies, or session material.
### 4.5 Rejected alternatives
- Disabling all reconnect replay is rejected because it needlessly breaks safe reads and random_id-protected writes.
- Relying only on Client.invoke retryability is rejected because sender reconnect happens below that loop.
- Treating every content-related message as unsafe is rejected because content-related controls seq_no, not idempotency.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/connection/sender.py | Store retry_safe and branch reconnect recovery |
| src/miniproto/client.py | Pass the computed retryable decision into sender.request |
| src/miniproto/errors.py | Add and export AmbiguousRpcResult |
| src/miniproto/__init__.py | Export the public exception if public errors are re-exported there |
| tests/test_transport_runtime.py | Add fake-server ambiguous-write and safe-replay cases |
| tests/test_invoke.py | Verify override propagation and random_id behavior |
| docs/development.md | Document reconnect ambiguity and retry=True risk |
## 6. Execution prerequisites
- Read https://core.telegram.org/mtproto/service_messages_about_messages again before changing explicit msg_resend_req behavior.
- Run from the repository root with the uv environment described in docs/development.md.
- Git workflow: do not create a branch, worktree, commit, stash, stage, revert, or push. The repository instructions reserve all additive/destructive Git actions for the user. Read-only git status and diff commands are allowed.
- STOP if RawSender implementations outside MTProtoSender cannot accept the new keyword without a compatibility path.
- STOP if a reconnect path can no longer tell whether a payload reached Transport.send; document the ambiguity boundary before proceeding.
## 7. Implementation steps
1. Add failing unit tests for PendingRequest metadata and AmbiguousRpcResult redaction.  
   Verification: uv run pytest tests/test_invoke.py -k "retryable or ambiguous"
2. Replace the unconditional reconnect test with two fake-server cases. The unsafe handler increments a server counter and then drops the first connection before responding; assert the counter remains one and the caller receives AmbiguousRpcResult. The safe case opts into retry safety and still succeeds on connection two.  
   Verification: uv run pytest tests/test_transport_runtime.py -k "resend or ambiguous"
3. Add retry_safe to PendingRequest and MTProtoSender.request, defaulting to false. Update all direct request call sites and test doubles deliberately rather than hiding signature mismatches with catch-all kwargs.  
   Verification: uv run ty check
4. Pass Client.invoke retryability into sender.request. Cover retry=True and retry=False overrides, wrappers, safe prefixes, and random_id sends.  
   Verification: uv run pytest tests/test_invoke.py
5. Split _resend_pending into safe resend and unsafe failure paths. Remove all stale aliases before completing an unsafe future; keep existing attempt limits for safe requests.  
   Verification: uv run pytest tests/test_transport_runtime.py
6. Document the new exception and the duplicate-side-effect risk of retry=True.  
   Verification: uv run python -m tools.schema.generate --check
7. Run the full local verification suite from section 8.  
   Verification: every command exits zero with no leaked-task warnings.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_invoke.py tests/test_transport_runtime.py
- uv run pytest tests/test_redaction.py
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
- Unsafe request processed once, connection dropped before response, no replay.
- Safe request reconnects and resolves its original future.
- retry=True explicitly enables replay; retry=False disables it.
- Cancellation and timeout during reconnect leave pending_count at zero.
- Wrapped requests use innermost request semantics.
## 9. Done criteria
- No reconnect path automatically replays an unsafe PendingRequest.
- Safe retry behavior remains covered and passing.
- Ambiguous writes surface a specific, redacted, non-auto-retryable exception.
- Pending maps and futures are empty after success, ambiguity, cancellation, timeout, and disconnect.
- Focused and full verification pass.
## 10. Rollback and recovery
If the sender change destabilizes reconnects, revert only the implementation through a user-owned Git action and retain the new failing unsafe-replay test as the release blocker. Do not restore unconditional replay as an undocumented behavior.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Safe calls are misclassified as unsafe | Keep existing classifier and add request-name diagnostics without secrets |
| Unsafe calls are misclassified as safe | Default false at the sender boundary and test generated method categories |
| One logical request has multiple pending aliases | Centralize alias removal and assert pending_count |
| Applications retry AmbiguousRpcResult blindly | Use a distinct type and explicit documentation |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: any change to is_retryable_request, PendingRequest, reconnect, msg_resend_req, or generated random_id fields.
- Official protocol reference: https://core.telegram.org/mtproto/service_messages_about_messages
- Current repository evidence: src/miniproto/invoke.py, src/miniproto/client.py, src/miniproto/connection/sender.py, tests/test_invoke.py, tests/test_transport_runtime.py.

# Validate inbound MTProto envelopes before state mutation
## 0. Plan metadata
- Status: proposed
- Priority: P0 security and protocol correctness
- Estimated size: L
- Risk: high; overly strict validation can disconnect legitimate sessions, while incomplete validation admits replay and cross-session traffic
- Base commit: cf7db29
- Dependencies: none
- Drift check: reopen rust/miniproto/src/mtproto.rs, src/miniproto/_native_fallback.py, src/miniproto/connection/sender.py, src/miniproto/mtproto/state.py, tests/test_native_parity.py, and tests/test_transport_runtime.py. Stop if decode already validates expected auth key/session identity, padding bounds, parity, time windows, and a monotonic replay floor before record_message_id.
## 1. Objective
Reject malformed, replayed, wrong-session, and implausibly timed server messages before they alter MTProto state, acknowledgements, pending RPCs, update delivery, or reconnect decisions. Keep native and Python fallback behavior identical.
## 2. Context and current state
The decrypted envelope exposes fields but does not enforce the complete inbound contract:
> rust/miniproto/src/mtproto.rs:136-182 decrypts and returns salt, session_id, msg_id, seq_no, body, and padding without checking the expected auth_key_id or accepted padding range.
> src/miniproto/_native_fallback.py:119-150 mirrors the same permissive decode shape.
The sender trusts decoded values immediately:
> src/miniproto/connection/sender.py:395-403 records the msg_id and dispatches the body after decode.
Duplicate tracking is a bounded membership cache, not a replay floor:
> src/miniproto/mtproto/state.py:54-64 stores recently seen message ids.
> tests/test_transport_runtime.py:257-265 currently demonstrates that an older id can be accepted after eviction.
Root cause: cryptographic integrity checking, envelope structural validation, connection/session validation, and replay/time validation are not expressed as one fail-closed boundary.
## 3. Scope
### In scope
- Validate inbound auth_key_id, session_id, message-body alignment, and random padding bounds.
- Validate server msg_id parity, Telegram time window, duplicate status, and a monotonic lower replay bound.
- Ensure validation occurs before acknowledgements, salt changes, pending completion, update dispatch, or seen-id mutation.
- Keep native and fallback exceptions and accepted/rejected vectors in parity.
- Add deterministic fake-server and primitive-level tests.
### Out of scope
- Redesigning MTProto encryption.
- Changing outbound msg_id generation.
- Handling legacy MTProto 1.0.
- Guessing undocumented exceptions for malformed Telegram traffic.
## 4. Design
### 4.1 Layered validation
Envelope decode must validate properties derivable from the auth key and byte layout:
- The outer auth_key_id equals the id derived from the supplied auth key.
- Message length is non-negative, divisible by four, and contained within decrypted plaintext.
- Remaining random padding is between 12 and 1024 bytes, inclusive.
- msg_key verification remains mandatory before any plaintext is returned.
Connection/state validation must then validate:
- decoded.session_id equals the current MTProtoState.session_id.
- A server-to-client msg_id has the server parity required by the current official MTProto specification.
- The timestamp encoded in msg_id is no more than the documented future skew and no older than the documented past window after applying known time offset.
- The id is neither in the bounded duplicate set nor below the retained replay floor.
### 4.2 Constants and official-source gate
Define named limits in one Python protocol module and mirror only byte-layout constants in Rust. At implementation time, re-confirm the current values from https://core.telegram.org/mtproto/security_guidelines and https://core.telegram.org/mtproto/description. Expected baseline is 30 seconds future skew, 300 seconds past skew, and padding 12 through 1024 bytes; STOP if the official documents disagree.
### 4.3 Replay floor
Track highest accepted server msg_id and a lower-bound watermark that does not move backward when the bounded duplicate set evicts entries. A message below the watermark is a replay even if no longer present in the set. Reset the session-specific duplicate set and watermark only when a deliberately fresh session_id is installed.
Do not require strictly increasing arrival order: MTProto containers and concurrent delivery can arrive out of order inside the accepted window. The floor must retain an explicit bounded reordering allowance rather than rejecting every id below the maximum.
### 4.4 Failure behavior
Introduce a protocol-validation exception with a reason enum or stable reason string. The receive loop must discard the message, mark the sender fatal, and close the suspect transport before any state mutation. Logs may include reason and numeric sizes/ids but never plaintext bodies, auth keys, msg_key, or session secrets.
### 4.5 Validation order invariant
The only allowed order is decrypt and authenticate, validate structure, validate current session and msg_id, record accepted id, then dispatch. Tests must assert that rejected envelopes do not add pending acks, update salt, resolve requests, or appear in incoming queues.
### 4.6 Rejected alternatives
- Expanding only the duplicate set is rejected because eviction still permits old replay.
- Validating only in Python is rejected because the native public decoder would retain unsafe standalone behavior.
- Requiring globally increasing msg_ids is rejected because legitimate out-of-order messages exist.
## 5. Files to change
| File | Change |
| --- | --- |
| rust/miniproto/src/mtproto.rs | Enforce auth-key id, message length, alignment, and padding bounds |
| src/miniproto/_native_fallback.py | Mirror structural checks and exception behavior |
| src/miniproto/mtproto/state.py | Add session, parity, time-window, duplicate, and replay-floor validation |
| src/miniproto/connection/sender.py | Validate before mutation and fail the transport deterministically |
| src/miniproto/mtproto/codec.py | Carry validation errors without exposing plaintext if needed |
| tests/test_native.py | Add malformed envelope unit vectors |
| tests/test_native_parity.py | Assert native/fallback acceptance and rejection parity |
| tests/test_transport_runtime.py | Add cross-session, replay-floor, time, and no-mutation fake-server tests |
| docs/development.md | Document inbound validation and diagnostic reason codes |
## 6. Execution prerequisites
- Re-read the two official Telegram references and record the exact accepted windows in code comments and tests.
- Use deterministic msg_ids derived from a frozen clock in tests.
- Git workflow: do not branch, create a worktree, stage, commit, stash, revert, or push. Leave those operations to the user.
- STOP if a test requires weakening auth or msg_key checks to construct a vector; extend the fake server instead.
- STOP if accepted service messages have a documented msg_id exception not represented in the design; update this plan before coding.
## 7. Implementation steps
1. Add native and fallback failing tests for wrong auth_key_id, body length overflow, non-four-byte body length, 11-byte padding, and 1025-byte padding.  
   Verification: uv run pytest tests/test_native.py tests/test_native_parity.py -k "mtproto and invalid"
2. Implement structural checks in fallback and Rust with matching ValueError text or a normalized wrapper error. Avoid allocating body or padding copies before length validation.  
   Verification: cargo test --all-features and the focused Python parity tests.
3. Add a pure state validation method accepting msg_id, session_id, direction, and a testable current time. It must not mutate on failure.  
   Verification: uv run pytest tests/test_transport_runtime.py -k "message_id or replay or session"
4. Add replay-floor semantics with an out-of-order acceptance window. Replace the eviction test so an evicted old id remains rejected while a legitimate recent out-of-order id is accepted once.  
   Verification: run the focused transport tests repeatedly.
5. Move sender mutation after validation. Add assertions that invalid messages leave server_salt, pending acks, pending RPC futures, and incoming update queues unchanged and close the transport.  
   Verification: uv run pytest tests/test_transport_runtime.py
6. Add structured diagnostics and documentation without sensitive fields.  
   Verification: uv run pytest tests/test_redaction.py tests/test_observability.py
7. Run full verification.  
   Verification: every command in section 8 exits zero.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_native.py tests/test_native_parity.py tests/test_transport_runtime.py
- cargo test --all-features
### Full
- uv run ruff format --check .
- uv run ruff check .
- uv run ty check
- uv run python -m tools.schema.generate --check
- uv run pytest
- cargo fmt --check
- cargo clippy --all-targets --all-features -- -D warnings
- cargo test --all-features
### Required vectors
- Valid minimum and maximum padding.
- Wrong auth key id with otherwise valid ciphertext.
- Wrong current session id.
- Server msg_id with wrong parity.
- Too old and too far future msg_ids under a frozen clock.
- Duplicate id, evicted-but-below-floor id, and legitimate recent out-of-order id.
- Invalid envelope that would otherwise carry bad_server_salt or rpc_result, proving no mutation.
## 9. Done criteria
- Native and fallback decoders reject the same malformed envelopes.
- Sender accepts only messages for its current auth key and session.
- Bounded duplicate eviction cannot make an old replay valid.
- Invalid input cannot mutate acknowledgements, salt, pending RPCs, or update delivery.
- All focused and full verification commands pass.
## 10. Rollback and recovery
If production traces expose a legitimate Telegram message rejected by a new rule, capture only redacted structural metadata, reproduce it in a regression test, and relax the narrow incorrect predicate. Never bypass the entire validation boundary.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| False positives disconnect valid clients | Official-source constants, frozen-clock tests, reason-coded metrics |
| Replay floor rejects reordering | Keep an explicit bounded reordering allowance |
| Rust/fallback drift | Shared fixtures and parity tests |
| Validation happens after mutation | One sender entry point and no-mutation assertions |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: changes to envelope layout, fresh-session handling, msg_id generation, receive dispatch, or native codec.
- Official references: https://core.telegram.org/mtproto/security_guidelines and https://core.telegram.org/mtproto/description
- Repository evidence: rust/miniproto/src/mtproto.rs, src/miniproto/_native_fallback.py, src/miniproto/connection/sender.py, src/miniproto/mtproto/state.py, tests/test_native.py, tests/test_native_parity.py, tests/test_transport_runtime.py.

# Validate inbound MTProto envelopes before state mutation

## 0. Plan metadata

- Status: completed
- Priority: P0 security and protocol correctness
- Estimated size: L
- Risk: high; overly strict validation can disconnect legitimate sessions, while incomplete validation admits replay and cross-session traffic
- Base commit: cf7db29
- Dependencies: plan 001 for logical request aliases and recent-message correlation
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
- Once the connection has a trusted time offset, the timestamp encoded in msg_id is no more than the documented future skew and no older than the documented past window after applying that offset.
- The id is neither in the bounded duplicate set nor below the retained replay floor.
  Session, parity, duplicate, and replay-floor checks are never disabled. Before time is trusted, the first authenticated, structurally valid message for the fresh random session may establish the offset only after all non-time checks pass; subsequent messages use the strict window.

### 4.2 Constants and official-source gate

Define named limits in one Python protocol module and mirror only byte-layout constants in Rust. At implementation time, re-confirm the current values from https://core.telegram.org/mtproto/security_guidelines and https://core.telegram.org/mtproto/description. Expected baseline is 30 seconds future skew, 300 seconds past skew, and padding 12 through 1024 bytes; STOP if the official documents disagree.

### 4.3 Replay floor

Retain the configured number of highest accepted server msg_ids. Reject duplicates immediately. Once the retained set is full, reject any candidate less than or equal to its smallest value, even if that id itself was previously evicted; otherwise insert the candidate and evict the smallest value. Reset this session-specific set only when a deliberately fresh session_id is installed.
Do not require strictly increasing arrival order: MTProto containers and concurrent delivery can arrive out of order while their ids remain above the retained floor.

### 4.4 Failure behavior

Introduce a protocol-validation exception with a reason enum or stable reason string. The receive loop must discard the message, mark the sender fatal, and close the suspect transport before any state mutation. Logs may include reason and numeric sizes/ids but never plaintext bodies, auth keys, msg_key, or session secrets.

### 4.5 Validation order invariant

The only allowed order is decrypt and authenticate, validate structure, validate current session and msg_id, record accepted id, then dispatch. Tests must assert that rejected envelopes do not add pending acks, update salt, resolve requests, or appear in incoming queues.
For `msg_container`, recursively decode and prevalidate the complete container and every child id before recording any id, queueing any acknowledgement, or dispatching any child. One invalid child rejects the whole container without partial state mutation.
`bad_msg_notification` and `bad_server_salt` may adjust time or salt only when their `bad_msg_id` correlates to a currently known recent outbound pending alias. Unknown or stale references are validation failures and cannot mutate state.

### 4.6 Rejected alternatives

- Expanding only the duplicate set is rejected because eviction still permits old replay.
- Validating only in Python is rejected because the native public decoder would retain unsafe standalone behavior.
- Requiring globally increasing msg_ids is rejected because legitimate out-of-order messages exist.

## 5. Files to change

| File                               | Change                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------ |
| rust/miniproto/src/mtproto.rs      | Enforce auth-key id, message length, alignment, and padding bounds       |
| src/miniproto/_native_fallback.py  | Mirror structural checks and exception behavior                          |
| src/miniproto/mtproto/state.py     | Add session, parity, time-window, duplicate, and replay-floor validation |
| src/miniproto/connection/sender.py | Validate before mutation and fail the transport deterministically        |
| src/miniproto/mtproto/codec.py     | Carry validation errors without exposing plaintext if needed             |
| tests/test_native.py               | Add malformed envelope unit vectors                                      |
| tests/test_native_parity.py        | Assert native/fallback acceptance and rejection parity                   |
| tests/test_transport_runtime.py    | Add cross-session, replay-floor, time, and no-mutation fake-server tests |
| docs/development.md                | Document inbound validation and diagnostic reason codes                  |

## 6. Execution prerequisites

- Re-read the two official Telegram references and record the exact accepted windows in code comments and tests.
- Use deterministic msg_ids derived from a frozen clock in tests.
- Git workflow: do not branch, create a worktree, stage, commit, stash, revert, or push. Leave those operations to the user.
- STOP if a test requires weakening auth or msg_key checks to construct a vector; extend the fake server instead.
- STOP if accepted service messages have a documented msg_id exception not represented in the design; update this plan before coding.

## 7. Implementation steps

1. Add native and fallback failing tests for wrong auth_key_id, body length overflow, non-four-byte body length, 11-byte padding, and 1025-byte padding. Because AES block alignment plus a four-byte-aligned body can make the exact 11/1025 fixtures fail an earlier invariant, also include isolated 8-byte and 1028-byte padding fixtures that prove the lower/upper padding predicates directly.  
   Verification: uv run pytest tests/test_native.py tests/test_native_parity.py -k "mtproto and invalid"
2. Implement structural checks in fallback and Rust with matching ValueError text or a normalized wrapper error. Avoid allocating body or padding copies before length validation.  
   Verification: cargo test --all-features and the focused Python parity tests.
3. Add a pure state prevalidation method accepting msg_id, session_id, direction, and a testable current time plus an explicit trusted-time state. It must not mutate on failure; commit accepted ids/time trust only after the complete envelope or container validates.  
   Verification: uv run pytest tests/test_transport_runtime.py -k "message_id or replay or session"
4. Add replay-floor semantics with an out-of-order acceptance window. Replace the eviction test so an evicted old id remains rejected while a legitimate recent out-of-order id is accepted once.  
   Verification: run the focused transport tests repeatedly.
5. Move sender mutation after validation. Recursively prevalidate containers atomically and require known recent bad_msg_id correlation before salt/time changes. Add assertions that invalid messages leave server_salt, time trust, pending acks, pending RPC futures, and incoming update queues unchanged and close the transport.  
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
- First valid message establishes trusted time only after session/parity/replay validation; later old/future messages fail.
- Container with one invalid child commits no outer or inner id and dispatches no valid sibling.
- Unknown or stale bad_msg_id cannot update salt or time offset.

## 9. Done criteria

- Native and fallback decoders reject the same malformed envelopes.
- Sender accepts only messages for its current auth key and session.
- Bounded duplicate eviction cannot make an old replay valid.
- Invalid input cannot mutate acknowledgements, salt, pending RPCs, or update delivery.
- All focused and full verification commands pass.

## 10. Rollback and recovery

If production traces expose a legitimate Telegram message rejected by a new rule, capture only redacted structural metadata, reproduce it in a regression test, and relax the narrow incorrect predicate. Never bypass the entire validation boundary.

## 11. Risks and mitigations

| Risk                                     | Mitigation                                                          |
| ---------------------------------------- | ------------------------------------------------------------------- |
| False positives disconnect valid clients | Official-source constants, frozen-clock tests, reason-coded metrics |
| Replay floor rejects reordering          | Keep an explicit bounded reordering allowance                       |
| Rust/fallback drift                      | Shared fixtures and parity tests                                    |
| Validation happens after mutation        | One sender entry point and no-mutation assertions                   |

## 12. Maintenance and references

- Owner: unassigned
- Review trigger: changes to envelope layout, fresh-session handling, msg_id generation, receive dispatch, or native codec.
- Official references: https://core.telegram.org/mtproto/security_guidelines and https://core.telegram.org/mtproto/description
- Repository evidence: rust/miniproto/src/mtproto.rs, src/miniproto/_native_fallback.py, src/miniproto/connection/sender.py, src/miniproto/mtproto/state.py, tests/test_native.py, tests/test_native_parity.py, tests/test_transport_runtime.py.

## 13. 2026-07-16 implementation evidence and handoff

- Fixed the remaining P0 first-container trust gap. `MTProtoSender._prevalidate_and_commit_incoming` now validates the outer message without time trust, derives a provisional time offset from that authenticated outer id, validates every child against that offset and a provisional replay set, and commits the complete batch with one captured clock value only after every validation and bad-message correlation check passes.
- `MTProtoState.validate_incoming` accepts non-mutating provisional time/replay context while preserving the existing stable `msg_id_future`, `msg_id_past`, duplicate, replay-floor, session, and parity diagnostics.
- Added deterministic +31-second and -301-second first-container child regressions. Both assert rejection without changing time trust/offset, seen ids, pending acknowledgements, incoming queue, salt, pending future, pending alias map, or alias set.
- Hardened the existing automatic-ACK test against unrelated keepalive timing: its fake handler returns a correlated `Pong` if needed, while the test keeps the ping horizon beyond its execution budget so the final delayed standalone ACK is measured independently.
- RED: `uv run pytest tests/test_transport_runtime.py -k "first_container_child_outside_outer_provisional_time" --basetemp=.pytest-tmp/plan002-fresh/red-001` selected 2 tests and failed both with `DID NOT RAISE ValueError`.
- GREEN: the same focused regression selection with `--basetemp=.pytest-tmp/plan002-fresh/green-001` passed 2 tests.
- Focused plan gate: `uv run pytest tests/test_native.py tests/test_native_parity.py tests/test_transport_runtime.py tests/test_redaction.py tests/test_observability.py --basetemp=.pytest-tmp/plan002-fresh/focused-002` passed 155 tests in 7.83 seconds.
- Scoped lint gate: `uv run ruff check src/miniproto/mtproto/state.py src/miniproto/connection/sender.py tests/test_transport_runtime.py` passed.
- Scoped format gate: `uv run ruff format --check src/miniproto/mtproto/state.py src/miniproto/connection/sender.py tests/test_transport_runtime.py` reported all 3 files already formatted.
- Scoped type gate: `uv run ty check src/miniproto/mtproto/state.py src/miniproto/connection/sender.py tests/test_transport_runtime.py` passed.
- Generator verification was not run because generated schema inputs and outputs were not touched by this completion pass. Rust format, Clippy, and tests were not rerun because this remaining fix touched only Python state/sender logic and its directly related tests; native and fallback coverage passed in the 155-test focused gate.
- No known plan-002 blocker remains. No git write operation or `docs/THOUGHTS.md` edit was performed.
- Shared repository gate passed on 2026-07-17: 627 Python tests passed with 4 skipped; 16 Rust tests passed; Ruff format/lint, ty, schema generation, Rust format, Clippy, maturin develop, and development/release wheel builds passed.
- Post-completion correction on 2026-07-17: the validation batch passed `time.time()` into `commit_incoming`, which reused it as the pending-ACK timestamp even though ACK age is measured with `time.monotonic()`. This clamped the final response's age to zero indefinitely unless later traffic piggybacked it. A direct clock-domain regression failed with age `0.0` instead of `1.25`, then passed after `commit_incoming` retained wall time only for server-time trust and always timestamped ACKs monotonically. The automatic-ACK integration test was isolated from keepalive traffic and passed 20/20 repetitions; all 79 transport-runtime tests and the full 635-test Python collection passed (631 passed, 4 skipped).

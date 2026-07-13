# Clean up cancelled auxiliary bot authorization
## 0. Plan metadata
- Status: proposed
- Priority: P1 lifecycle correctness
- Estimated size: M
- Risk: medium; cancellation-safe cleanup must not swallow cancellation or disconnect healthy cached auxiliaries
- Base commit: cf7db29
- Dependencies: none
- Drift check: reopen src/miniproto/client.py, tests/test_media_download.py, tests/test_multi_session_download.py, and src/miniproto/session/storage.py. Stop if every newly created auxiliary is owned by a cleanup guard until successful registration and cancellation tests prove sender/storage/task cleanup.
## 1. Objective
Ensure cancelling multi-session bot setup cannot leak an auxiliary connection, encrypted session handle, background task, or half-authorized client.
## 2. Context and current state
Auxiliary creation happens before the download call owns its normal cleanup tuple:
> src/miniproto/client.py:866-886 creates a sibling storage and Client inside _ensure_auxiliary_download_clients.
Authorization can suspend after connection and auth-key creation:
> src/miniproto/client.py:278-301 sign_in_bot connects and ensures an auth key before completing bot authorization.
Cancellation is re-raised without local cleanup:
> src/miniproto/client.py:898-915 catches CancelledError from auxiliary.sign_in_bot and immediately raises; other failures call auxiliary.disconnect.
Registration occurs only after later identity checks:
> src/miniproto/client.py:917-935 loads the authorized record and then stores the auxiliary for reuse.
Existing multi-session tests cover successful reuse and final disconnect but not cancellation during construction.
Root cause: ownership transfers to the cache only after authorization, while the pre-registration interval has no finally guard.
## 3. Scope
### In scope
- Guard every newly created auxiliary from storage creation through validated registration.
- Make cleanup finish under cancellation and preserve the original CancelledError.
- Avoid registering incomplete or wrong-identity clients.
- Cover cancellation before connect, during auth, after auth before registration, and during cleanup.
- Assert no background tasks or open storage remain.
### Out of scope
- Cancelling healthy auxiliaries already registered from prior downloads.
- Changing multi-session thresholds or bot-only policy.
- Retrying failed bot authorization.
- Changing sibling session naming.
## 4. Design
### 4.1 Ownership state
Treat each new auxiliary as locally owned until all conditions pass:
- storage opens and loads successfully;
- existing identity is compatible or bot sign-in completes;
- auth key and bot user are present;
- bot user id matches the primary;
- client is inserted into _auxiliary_download_clients.
Only registration transfers ownership to the Client-wide cache. Every earlier exit closes the local client.
### 4.2 Cleanup helper
Add a private helper that creates a separate task for auxiliary.disconnect, awaits it under asyncio.shield, and joins it even if the parent receives repeated cancellation. Preserve the caller’s original exception; record cleanup errors through redacted observability without replacing CancelledError.
If Client.disconnect already closes the storage on never-fully-connected clients, use it as the one cleanup primitive. Otherwise fix disconnect’s lifecycle invariant rather than calling private storage close in multiple branches.
### 4.3 Control flow
Wrap each new auxiliary’s validation/authorization block in try/except BaseException:
- On success, register and clear local ownership.
- On CancelledError, run cancellation-safe cleanup, then re-raise the same cancellation.
- On ordinary failure, emit the current ignored reason, clean up, and stop adding sessions as today.
- On identity mismatch or missing token, clean up through the same helper.
Do not catch cancellation around existing cached auxiliaries; they are not locally owned.
### 4.4 Invariants
- A client appears in _auxiliary_download_clients only when fully authorized and identity-verified.
- Every unregistered created Client is disconnected exactly once.
- Cancellation remains observable to the caller.
- Cleanup logs contain indexes and error types, never bot tokens or session contents.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/client.py | Add ownership guard and cancellation-safe cleanup helper |
| tests/test_media_download.py | Add deterministic cancellation barriers and state assertions |
| tests/test_multi_session_download.py | Add benchmark-helper lifecycle regression if it owns auxiliary fakes |
| tests/test_resource_limits.py | Assert no owned task remains after cancellation if appropriate |
| docs/development.md | Document auxiliary authorization cancellation behavior |
## 6. Execution prerequisites
- Read Client.disconnect and _CachedSessionStorage.close completely before choosing the cleanup primitive.
- Use fake clients/storages with explicit connected, closed, and task counters.
- Git workflow: no branch, worktree, stage, commit, stash, revert, or push.
- STOP if cleanup requires suppressing BaseException broadly; preserve cancellation and fatal errors deliberately.
## 7. Implementation steps
1. Add a fake auxiliary whose sign_in_bot signals connected and then waits on an Event. Cancel _ensure_auxiliary_download_clients and assert the current code leaks; the final test must require disconnect, storage close, no cache entry, and no live tasks.  
   Verification: uv run pytest tests/test_media_download.py -k "auxiliary and cancel"
2. Add a cancellation-safe cleanup helper with unit tests for normal cleanup, cleanup error, and repeated cancellation.  
   Verification: uv run pytest tests/test_media_download.py -k "cleanup"
3. Refactor new-auxiliary construction into one ownership-guarded block. Remove duplicated direct storage.close/disconnect branches only after equivalent reason events are preserved.  
   Verification: uv run pytest tests/test_media_download.py -k "auxiliary"
4. Add barriers before connect, during authorization, after authorization before registration, and after registration. The last case must leave the healthy cached client owned by the parent until normal Client.disconnect.  
   Verification: uv run pytest tests/test_media_download.py tests/test_multi_session_download.py
5. Add leak checks using asyncio.all_tasks filtered to tasks created by the fake client. Avoid timing-only sleeps.  
   Verification: uv run pytest tests/test_resource_limits.py tests/test_media_download.py
6. Run full verification.  
   Verification: all section 8 commands pass.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_media_download.py tests/test_multi_session_download.py tests/test_resource_limits.py
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
- Cancellation before and after auxiliary connect.
- Cancellation during sign_in_bot and during post-auth record load.
- Repeated cancellation while cleanup is running.
- Cleanup itself raises; cancellation is still primary and error is observable.
- Identity mismatch and missing token close storage.
- Previously cached healthy auxiliary is not disconnected by another setup cancellation.
## 9. Done criteria
- No unregistered auxiliary survives any exit from its construction block.
- Cancellation propagates only after cleanup finishes.
- No cache entry, sender, storage handle, or owned task leaks in deterministic tests.
- Successful auxiliary reuse and normal parent disconnect still pass.
## 10. Rollback and recovery
If shielded cleanup introduces a hang, keep the failing leak test and replace the helper with a bounded, supervised cleanup task whose failure is surfaced at parent disconnect. Do not return to immediate re-raise with live resources.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Cleanup swallows cancellation | Re-raise the original CancelledError after join |
| Repeated cancellation interrupts cleanup | Separate cleanup task plus shield/join loop |
| Healthy cached client is closed | Explicit local-versus-cache ownership state |
| Cleanup error hides root cause | Preserve primary exception and record secondary error |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: auxiliary setup, sign_in_bot, Client.disconnect, sibling storage, multi-session ranges, or task supervision changes.
- Repository evidence: src/miniproto/client.py, tests/test_media_download.py, tests/test_multi_session_download.py, src/miniproto/session/storage.py.

# Redact secrets from ordinary dataclass reprs
## 0. Plan metadata
- Status: proposed
- Priority: P0 security
- Estimated size: S
- Risk: medium; repr changes can affect tests and debugging but must not affect serialization
- Base commit: cf7db29
- Dependencies: none
- Drift check: reopen src/miniproto/config.py, src/miniproto/session/models.py, src/miniproto/security/redaction.py, tests/test_redaction.py, and PROGRESS.md. Stop if direct repr of every config/session dataclass already hides all SEC-001 values, not only safe_repr output.
## 1. Objective
Make Python’s normal repr of public configuration and session dataclasses safe to include in tracebacks, debugger panes, assertion failures, and logs.
## 2. Context and current state
Configuration secrets are inconsistently marked:
> src/miniproto/config.py:13-21: TransportConfig.proxy participates in the generated repr.
> src/miniproto/config.py:50-72: ClientConfig.api_hash participates in repr while bot_token already uses repr=False.
Session models expose secret-bearing fields through generated repr:
> src/miniproto/session/models.py:29-34: AuthKey.key is included.
> src/miniproto/session/models.py:49-57: DCOption.secret is included.
> src/miniproto/session/models.py:71-78: UserIdentity.phone is included.
> src/miniproto/session/models.py:99-106: PeerCacheEntry.phone and raw are included.
> src/miniproto/session/models.py:119-127: SessionRecord nests auth, peers, user, and metadata.
Coverage only proves an opt-in helper:
> tests/test_redaction.py:70-80 calls safe_repr(record), not repr(record).
The project requirement is broader:
> PROGRESS.md:45 requires secrets to be redacted from repr output.
> PROGRESS.md:146 marks the repr coverage task complete.
Root cause: safe rendering exists at selected logging/error call sites, but ordinary dataclass-generated repr bypasses it.
## 3. Scope
### In scope
- Hide api_hash, proxy credentials, auth-key bytes, DC secrets, phone numbers, raw peer payloads, session metadata, and storage objects from generated repr.
- Keep non-sensitive identifiers useful for debugging.
- Add direct repr and nested repr regression tests with unique sentinels.
- Correct the completion claim in project tracking when the implementation lands.
### Out of scope
- Changing serialization or dataclasses.asdict behavior.
- Treating repr as an authorization boundary.
- Regenerating every raw Telegram type solely to customize repr.
- Changing safe_repr semantics except where direct tests reveal a shared bug.
## 4. Design
### 4.1 Field policy
Use dataclasses.field(repr=False) for secret-bearing fields:
- TransportConfig.proxy.
- ClientConfig.api_hash, session_storage, and bot_token.
- AuthKey.key.
- DCOption.secret.
- UserIdentity.phone.
- PeerCacheEntry.phone and raw.
- SessionRecord.metadata.
Keep api_id, dc_id, transport mode, key_id, user id, username, peer kind/id, update counters, and timestamps visible unless a test demonstrates they contain sensitive payloads.
### 4.2 Nested safety
The direct repr of SessionRecord and ClientConfig must remain safe because all nested dataclasses hide their own sensitive fields. Do not replace every repr with safe_repr at call time; the safe default belongs on the data model.
### 4.3 Sentinel tests
Construct each dataclass with distinct non-real sentinels and assert none appear in repr of the object or its containing ClientConfig/SessionRecord. Also assert a small set of safe fields remains visible so debugging does not degrade into opaque object addresses.
### 4.4 Documentation boundary
Document that repr=False does not redact dataclasses.asdict, direct attribute access, serialization, pickling, or memory. Existing redaction helpers remain required for arbitrary mappings and generated raw request objects.
### 4.5 Rejected alternatives
- A mixin with a generic custom repr is rejected because field-level repr=False is simpler, faster, and harder to forget for nested dataclasses.
- Redacting only log calls is rejected because tracebacks and assertion diffs call repr directly.
- Hiding every field is rejected because safe identifiers are valuable diagnostics.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/config.py | Mark api_hash, session_storage, proxy, and existing token fields non-repr |
| src/miniproto/session/models.py | Mark secret-bearing fields non-repr |
| tests/test_redaction.py | Add direct and nested repr sentinel tests |
| PROGRESS.md | Correct SEC-001/TASK-019 evidence after tests pass |
| docs/session-security.md | Clarify repr versus serialization boundary |
## 6. Execution prerequisites
- Inventory every dataclass field whose name matches is_sensitive_key and inspect nested mappings.
- Use fake sentinel values only; never place real credentials in tests.
- Git workflow: no branch, worktree, stage, commit, stash, revert, or push.
- STOP if a field’s secrecy classification is ambiguous and hiding it would break a documented repr contract; record the decision before proceeding.
## 7. Implementation steps
1. Add direct repr tests for TransportConfig, ClientConfig, AuthKey, DCOption, UserIdentity, PeerCacheEntry, and SessionRecord. Confirm they fail on cf7db29.  
   Verification: uv run pytest tests/test_redaction.py -k "repr"
2. Apply repr=False at field declarations without changing types, defaults, equality, hash, serialization helpers, or constructor signatures.  
   Verification: uv run pytest tests/test_redaction.py tests/test_session_storage.py
3. Add nested ClientConfig and SessionRecord tests plus positive assertions for safe diagnostic fields.  
   Verification: uv run pytest tests/test_redaction.py
4. Search for hand-written repr methods and f-string object logging that might still expose raw mappings. Keep unrelated cleanup out of this plan; add a follow-up finding if needed.  
   Verification: rtk proxy rg -n "__repr__|!r|repr\\(" src/miniproto
5. Update session-security documentation and tracker evidence only after tests pass.  
   Verification: uv run ty check
6. Run full verification.  
   Verification: section 8 commands pass.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_redaction.py tests/test_session_storage.py tests/test_observability.py
### Full
- uv run ruff format --check .
- uv run ruff check .
- uv run ty check
- uv run python -m tools.schema.generate --check
- uv run pytest
### Required edge cases
- Proxy URL with username and password nested inside ClientConfig.
- Auth key bytes nested inside SessionRecord.
- Phone values in both UserIdentity and PeerCacheEntry.
- Metadata containing session_key and raw_session sentinels.
- Safe api_id, dc_id, key_id, username, and peer id remain visible.
## 9. Done criteria
- Direct repr and nested repr contain none of the SEC-001 sentinels.
- Serialization round trips and equality are unchanged.
- Existing safe_repr, error-redaction, session, and observability tests pass.
- Documentation explicitly says repr safety does not sanitize serialization.
## 10. Rollback and recovery
If a consumer depended on a full repr, expose a separate explicit diagnostic method returning redacted structured data. Do not restore secrets to the default repr.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Debug output loses useful context | Keep non-sensitive ids and timestamps visible |
| New secret fields regress later | Add a field-name inventory assertion or review checklist |
| Tests accidentally contain realistic credentials | Use obvious unique sentinels |
| asdict is mistaken for safe output | Document and test the boundary |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: any new config/session dataclass field, logging change, or SEC-001 update.
- Repository evidence: src/miniproto/config.py, src/miniproto/session/models.py, src/miniproto/security/redaction.py, tests/test_redaction.py, PROGRESS.md.

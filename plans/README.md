# miniproto plans and implementation reports
## Purpose
This directory contains historical implementation reports plus execution-ready plans produced from the 2026-07-13 senior codebase audit. The numbered plans are the actionable source for the 13 accepted findings; the dated reports remain evidence and context and are not superseded.
Audit snapshot: cf7db29 on 2026-07-13. Every plan begins with a drift check because source and tests may move after this snapshot.
## Status legend
- Proposed: accepted finding with an implementation-ready plan; work has not started.
- In progress: implementation is actively following the plan.
- Blocked: a named STOP condition or external decision prevents safe progress.
- Completed: implementation and the plan’s focused/full verification have passed and completion evidence has been recorded.
## Recommended execution order
The sequence prioritizes correctness and security, keeps plans that touch the same hot files in a stable order, and lands the atomic storage foundation before its two dependents.
| Order | Plan | Priority | Size | Hard dependency | Status | Why here |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | [Prevent unsafe RPC replay after reconnect](001-prevent-unsafe-rpc-replay.md) | P0 | M | None | Proposed | Prevents duplicate non-idempotent Telegram mutations |
| 002 | [Validate inbound MTProto envelopes](002-validate-inbound-mtproto-envelopes.md) | P0 | L | None | Proposed | Rejects replay, wrong-session, malformed, and implausibly timed traffic before mutation |
| 003 | [Validate Telegram DH and SRP groups](003-validate-dh-and-srp-groups.md) | P0 | M | None | Proposed | Closes weak-group acceptance in both authorization paths |
| 004 | [Make session updates atomic and domain-incremental](004-atomic-domain-session-updates.md) | P0 | L | None | Proposed | Removes lost updates and becomes the storage foundation for 011 and 012 |
| 005 | [Redact secrets from ordinary dataclass reprs](005-redact-secret-dataclass-reprs.md) | P0 | S | None | Proposed | Makes the existing SEC-001 completion claim true for ordinary Python repr |
| 006 | [Bound native and fallback vector decoding](006-bound-native-vector-decodes.md) | P0 | M | None | Proposed | Prevents attacker-controlled allocation/iteration from impossible vector counts |
| 007 | [Verify concurrent downloads have no holes](007-verify-concurrent-download-completion.md) | P0 | M | None | Proposed | Prevents silent sparse or truncated media success |
| 008 | [Enforce the pending RPC cap atomically](008-enforce-pending-rpc-cap-atomically.md) | P0 | M | None | Proposed | Makes max_pending_rpcs effective during cold-start bursts |
| 009 | [Clean up cancelled auxiliary bot authorization](009-clean-up-cancelled-auxiliary-auth.md) | P1 | M | None | Proposed | Closes sender, storage, and task leaks in multi-session setup |
| 010 | [Lazy-load the generated raw API](010-lazy-load-generated-raw-api.md) | P1 | L | None | Proposed | Targets the largest measured startup-time and retained-memory cost |
| 011 | [Align the runtime with the encrypted session default](011-align-encrypted-session-default.md) | P1 | M | 004 | Proposed | Promotes encrypted durable storage only after mutation correctness is fixed |
| 012 | [Add in-memory indexes to the peer cache](012-index-peer-cache.md) | P2 | M | 004 | Proposed | Uses storage-domain revisions to eliminate repeated tuple scans safely |
| 013 | [Migrate away from deprecated asyncio policies](013-migrate-event-loop-policy.md) | P2 | M | None | Proposed | Removes import side effects and prepares for Python 3.16 |
## Dependency graph
Hard dependencies only:
> 004 atomic domain session updates -> 011 encrypted session default  
> 004 atomic domain session updates -> 012 peer-cache indexes
All other numbered plans are logically independent, but the recommended order avoids overlapping edits in these conflict lanes:
- Sender and MTProto lane: 001, then 002, then 008.
- Client/session lane: 004, then 009, then 011, then 012.
- Generated/import lane: 010, then 013 if both alter top-level import measurements.
- Security primitives lane: 003, 005, and 006 can be implemented independently when file ownership is isolated.
## Execution protocol
1. Open the selected plan and run its drift check against the current HEAD before editing.
2. Respect every prerequisite and STOP condition; update the plan before changing its architecture.
3. Keep work inside the plan’s scope and preserve unrelated user changes.
4. Follow the repository Git rule: agents use read-only Git only; the user owns branches, worktrees, staging, commits, reverts, and pushes.
5. Run focused verification after each step and the full verification suite before marking Completed.
6. Update this table and the plan metadata only when implementation status actually changes.
## Findings not promoted to new numbered plans
These candidates were considered but intentionally rejected or routed elsewhere:
- Re-plan the remaining Phase 12 CI, integration, packaging, documentation, and Phase 13 release-checklist work: rejected as duplicate planning because PROGRESS.md and the dated implementation reports already track it. The audit findings above must land before those release gates can be trusted.
- Re-plan completed items from [the 2026-07-06 performance and improvement master plan](2026-07-06-performance-and-improvement-master-plan.md): rejected because completed P0/P1/P2 and CPU/Rust work already has implementation evidence in PROGRESS.md. New regressions discovered in that code received their own numbered plans instead.
- Add routers, filters, decorators, middleware, plugins, conversations, or broad high-level helpers to miniproto: rejected by the established package boundary; those belong in mpgram.
- Move reconnect policy, session coordination, peer behavior, or update delivery wholesale into Rust: rejected without benchmark evidence and because these evolving policies belong in Python. Plan 006 keeps Rust limited to a deterministic primitive hot path.
- Add time-based debounce for update-cursor persistence as part of plan 004: rejected because it weakens crash durability. Domain-incremental atomic writes address the demonstrated amplification first; any later coalescing needs separate durability and benchmark evidence.
- Disable all RPC replay to solve plan 001: rejected because safe reads and random_id-protected writes can retain transparent recovery when retry metadata reaches the sender.
- Treat the audit’s one-machine import measurement as a universal absolute threshold: rejected. Plan 010 requires a same-machine baseline and relative time/memory gates plus a warmed-throughput guard.
## Historical and active dated reports
- [2026-06-25 implementation progress](2026-06-25-implementation-progress.md): first implementation slice, verification status, and remaining work.
- [2026-06-26 package boundary and ecosystem intent](2026-06-26-package-boundary-and-ecosystem-intent.md): decision separating miniproto protocol SDK responsibilities from mpgram framework responsibilities.
- [2026-06-29 package boundary progress](2026-06-29-package-boundary-progress.md): applied repository and documentation boundary work.
- [2026-07-03 reference implementation improvement notes](2026-07-03-reference-implementation-improvement-notes.md): read-only comparison notes from Pyroblack, Telethon, grammers, mtcute, and Web K/tweb.
- [2026-07-06 performance and improvement master plan](2026-07-06-performance-and-improvement-master-plan.md): prior performance/protocol backlog and ownership map; consult PROGRESS.md for completion state.
## Shared verification baseline
Each numbered plan narrows this list to its affected area, then requires the appropriate full checks:
- uv run ruff format --check .
- uv run ruff check .
- uv run ty check
- uv run python -m tools.schema.generate --check
- uv run pytest
- cargo fmt --check
- cargo clippy --all-targets --all-features -- -D warnings
- cargo test --all-features
- uv run maturin build when generated packaging, native code, or wheel contents change.

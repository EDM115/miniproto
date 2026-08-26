---
title: Fake-backed And Live-gated Coverage
description: Living ledger of deterministic fake-backed protocol coverage and the separate Telegram checks that remain environment-gated.
slug: /project/testing/faked-methods/
generated: false
---

Status: living ledger for fake-backed tests, private hooks, implemented opt-in live checks and behavior that still needs broader Telegram validation.

## Purpose

This file keeps all fake Telegram method boundaries visible without treating synthetic correctness coverage as live-service evidence. Four opt-in production-DC smoke checks are implemented under `tests/integration/`: bot authorization plus `get_me()`, phone authorization plus `get_me()` and persisted-session reconnect, Saved Messages send plus history read and Saved Messages media upload/download byte comparison. Those four checks passed in the local 2026-08-19 release-automation verification recorded in `PROGRESS.md`; the canonical offline Wave 6 run skipped them by design and future release evidence must continue to label live execution separately.

## Fake Telegram RPCs In Unit Tests

| Phase | Telegram method or boundary                                                                                                                                        | Fake location                                                                                                             | Real follow-up                                                                                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 6     | `auth.sendCode`, `auth.signIn`, `account.getPassword`, `auth.checkPassword`, `auth.importBotAuthorization`, `auth.exportAuthorization`, `auth.importAuthorization` | `tests/test_auth.py` fake invokers                                                                                        | The guarded bot/phone live assertions exist and have passed locally; retain fake determinism and repeat live auth/reconnect only with authorized credentials.                  |
| 7     | `help.getNearestDc` and raw RPC result/error envelopes                                                                                                             | `tests/test_invoke.py` fake senders                                                                                       | Keep fake coverage for deterministic errors, then add live smoke calls through the real sender after auth is proven.                                                           |
| 8     | `updates.getState`, `updates.getDifference` and pushed raw updates                                                                                                | `tests/test_updates.py` fake invokers plus the sender-backed `Client._receive_dispatch_loop()`                            | Keep deterministic fake coverage, then validate live pushed updates and gap recovery on test DC sessions.                                                                      |
| 9     | `users.getUsers`, `contacts.resolveUsername`, `messages.sendMessage`                                                                                               | `tests/test_peers.py` and `tests/test_messages.py` fake senders returning generated TL constructors                       | Guarded `get_me()`, Saved Messages send and history assertions exist and have passed locally; username/service edge coverage remains repeatable only with authorized accounts. |
| 10    | `upload.saveFilePart`, `upload.saveBigFilePart`, `messages.sendMedia`, `upload.getFile`, `upload.getCdnFile`, `upload.reuploadCdnFile`                             | `tests/test_media_upload.py` and `tests/test_media_download.py` fake invokers/senders returning generated TL constructors | Guarded Saved Messages upload/download byte comparison exists and has passed locally; a naturally returned live CDN redirect remains environment-dependent.                    |

## Live Validation Still Gated

| Public or private method                   | Current state                                                                                                                                                    | Owning phase |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| Live pushed-update/gap-recovery validation | The sender-backed receive dispatch loop feeds `UpdateManager`; deterministic tests cover the runtime path, while Telegram test-DC/live validation remains gated. | Phase 8/12   |
| High-level edit/delete message helpers     | `Client.edit_message()` and `Client.delete_messages()` are implemented, including channel deletion; live and edge-case coverage remains gated.                   | Phase 9/12   |
| Live Saved Messages send/receive           | Implemented opt-in check; it skips without `MINIPROTO_INTEGRATION=1`, production confirmation and credentials. It passed in the recorded 2026-08-19 local live run. | Phase 9/12   |
| Live media upload/download                 | Implemented opt-in check; it skips without `MINIPROTO_INTEGRATION=1`, production confirmation, credentials and `MINIPROTO_TEST_UPLOAD_FILE`. It passed in the recorded 2026-08-19 local live run. | Phase 10/12  |

## Rules For Future Updates

Add a row whenever a test fakes a Telegram RPC result, a private hook stands in for real network behavior or a public method remains intentionally deferred. Remove or rewrite a row only after a live or fake-server replacement exists and `PROGRESS.md` records the passing gate.

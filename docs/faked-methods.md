---
title: Faked And Deferred Methods
description: Living ledger of fake-backed tests and public work still requiring live Telegram validation.
slug: /project/testing/faked-methods/
generated: false
---

Status: living ledger for fake-backed tests, private hooks, and public methods that still need live Telegram validation or later implementation.

## Purpose

This file keeps all fake Telegram method boundaries visible so later agents can replace them with live test-DC coverage or real implementations without rediscovering which tests are synthetic.

## Fake Telegram RPCs In Unit Tests

| Phase | Telegram method or boundary                                                                                                                                        | Fake location                                                                                                             | Real follow-up                                                                                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 6     | `auth.sendCode`, `auth.signIn`, `account.getPassword`, `auth.checkPassword`, `auth.importBotAuthorization`, `auth.exportAuthorization`, `auth.importAuthorization` | `tests/test_auth.py` fake invokers                                                                                        | Run against Telegram test DCs once credentials are available and convert remaining skip messages in `tests/integration/test_auth_live.py` into live assertions.                |
| 7     | `help.getNearestDc` and raw RPC result/error envelopes                                                                                                             | `tests/test_invoke.py` fake senders                                                                                       | Keep fake coverage for deterministic errors, then add live smoke calls through the real sender after auth is proven.                                                           |
| 8     | `updates.getState`, `updates.getDifference`, and pushed raw updates                                                                                                | `tests/test_updates.py` fake invokers plus the sender-backed `Client._receive_dispatch_loop()`                            | Keep deterministic fake coverage, then validate live pushed updates and gap recovery on test DC sessions.                                                                      |
| 9     | `users.getUsers`, `contacts.resolveUsername`, `messages.sendMessage`                                                                                               | `tests/test_peers.py` and `tests/test_messages.py` fake senders returning generated TL constructors                       | Run `get_me()`, username resolution, and Saved Messages send against Telegram test DCs; keep fake send tests for deterministic access-hash and flood-wait behavior.            |
| 10    | `upload.saveFilePart`, `upload.saveBigFilePart`, `messages.sendMedia`, `upload.getFile`, `upload.getCdnFile`, `upload.reuploadCdnFile`                             | `tests/test_media_upload.py` and `tests/test_media_download.py` fake invokers/senders returning generated TL constructors | Run Saved Messages file upload/download against Telegram test DCs, including at least one CDN redirect case if Telegram returns one naturally or through a controlled fixture. |

## Product Methods Still Deferred

| Public or private method                   | Current state                                                                                                                                                    | Owning phase |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| Live pushed-update/gap-recovery validation | The sender-backed receive dispatch loop feeds `UpdateManager`; deterministic tests cover the runtime path, while Telegram test-DC/live validation remains gated. | Phase 8/12   |
| High-level edit/delete message helpers     | `Client.edit_message()` and `Client.delete_messages()` are implemented, including channel deletion; live and edge-case coverage remains gated.                   | Phase 9/12   |
| Live Saved Messages send/receive           | Gated scaffold only; skipped without `MINIPROTO_INTEGRATION=1` and credentials.                                                                                  | Phase 9/12   |
| Live media upload/download                 | Gated scaffold only; skipped without `MINIPROTO_INTEGRATION=1`, credentials, and `MINIPROTO_TEST_UPLOAD_FILE`.                                                   | Phase 10/12  |

## Rules For Future Updates

Add a row whenever a test fakes a Telegram RPC result, a private hook stands in for real network behavior, or a public method remains intentionally deferred. Remove or rewrite a row only after a live or fake-server replacement exists and `PROGRESS.md` records the passing gate.

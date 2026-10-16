---
title: Fake-backed And Live-gated Coverage
description: Living ledger of deterministic fake-backed protocol coverage and the separate Telegram checks that remain environment-gated.
slug: /project/testing/faked-methods/
generated: false
---

## Purpose

This ledger maps fake Telegram RPCs to deterministic test locations and lists the live checks that remain gated. The `tests/integration/` suite includes four production-DC checks: bot authorization and `get_me()`, phone authorization and persisted-session reconnect, Saved Messages send and history read, and media upload/download byte comparison. Historical [2026-08-19 run notes](https://github.com/EDM115/miniproto/blob/8ed6b99eb0909f87a90f604026d956c0ad16adaa/PROGRESS.md) remain in Git, but their raw reports are absent from this checkout. They cover an earlier source and dependency set; use evidence from the intended release source before claiming current Telegram acceptance.

## Fake Telegram RPCs In Unit Tests

| Telegram method or boundary                                                                                                                                        | Fake location                                                                                                             | Live follow-up                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auth.sendCode`, `auth.signIn`, `account.getPassword`, `auth.checkPassword`, `auth.importBotAuthorization`, `auth.exportAuthorization`, `auth.importAuthorization` | `tests/test_auth.py` fake invokers                                                                                        | Guarded bot/phone checks cover authorization and reconnect. Record a live run against the release source before claiming Telegram acceptance.                                  |
| `help.getNearestDc` and raw RPC result/error envelopes                                                                                                             | `tests/test_invoke.py` fake senders                                                                                       | Keep deterministic error coverage; add a live call through the real sender only when service acceptance needs to be recorded.                                                  |
| `updates.getState`, `updates.getDifference` and pushed raw updates                                                                                                | `tests/test_updates.py` fake invokers plus the sender-backed `Client._receive_dispatch_loop()`                            | Live pushed-update and gap-recovery validation remains gated on Telegram test-DC or production-account access.                                                                   |
| `users.getUsers`, `contacts.resolveUsername`, `messages.sendMessage`                                                                                               | `tests/test_peers.py` and `tests/test_messages.py` fake senders returning generated TL constructors                       | Guarded checks cover `get_me()`, Saved Messages send and history. Username resolution still needs a recorded live run.                                                          |
| `upload.saveFilePart`, `upload.saveBigFilePart`, `messages.sendMedia`, `upload.getFile`, `upload.getCdnFile`, `upload.reuploadCdnFile`                             | `tests/test_media_upload.py` and `tests/test_media_download.py` fake invokers/senders returning generated TL constructors | Guarded checks compare Saved Messages upload/download bytes; a live CDN redirect depends on Telegram's response.                                                                  |

## Live Validation Still Gated

| Public or private method                   | Current state                                                                                                                                                    |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Live pushed-update/gap-recovery validation | The sender-backed receive dispatch loop feeds `UpdateManager`; deterministic tests cover this path, while Telegram test-DC/live validation remains gated.        |
| High-level edit/delete message helpers     | `Client.edit_message()` and `Client.delete_messages()` are implemented, including channel deletion; live and edge-case coverage remains gated.                    |
| Live Saved Messages send/receive           | The opt-in check skips without `MINIPROTO_INTEGRATION=1`, production confirmation and credentials. Acceptance requires a recorded live run.                      |
| Live media upload/download                 | The opt-in check skips without `MINIPROTO_INTEGRATION=1`, production confirmation, credentials and `MINIPROTO_TEST_UPLOAD_FILE`. Acceptance requires a live run. |

## Rules For Future Updates

Add a row when a test fakes an RPC result, a private hook stands in for network behavior or a public method lacks live validation. When new live evidence replaces a row, record the source commit, command, environment and result with the release evidence.

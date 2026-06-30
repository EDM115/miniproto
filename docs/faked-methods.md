# Faked And Deferred Methods

Status: living ledger for fake-backed tests, private hooks, and public methods that still need live Telegram validation or later implementation.

## Purpose

This file keeps all fake Telegram method boundaries visible so later agents can replace them with live test-DC coverage or real implementations without rediscovering which tests are synthetic.

## Fake Telegram RPCs In Unit Tests

| Phase | Telegram method or boundary                                                                                                                                        | Fake location                                                                                       | Real follow-up                                                                                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 6     | `auth.sendCode`, `auth.signIn`, `account.getPassword`, `auth.checkPassword`, `auth.importBotAuthorization`, `auth.exportAuthorization`, `auth.importAuthorization` | `tests/test_auth.py` fake invokers                                                                  | Run against Telegram test DCs once credentials are available and convert remaining skip messages in `tests/integration/test_auth_live.py` into live assertions.     |
| 7     | `help.getNearestDc` and raw RPC result/error envelopes                                                                                                             | `tests/test_invoke.py` fake senders                                                                 | Keep fake coverage for deterministic errors, then add live smoke calls through the real sender after auth is proven.                                                |
| 8     | `updates.getState`, `updates.getDifference`, and pushed raw updates                                                                                                | `tests/test_updates.py` fake invokers plus `Client._feed_raw_update()`                              | Wire the real receiver path from transport/sender into `UpdateManager.feed_raw_update()` and validate gap recovery on test DC sessions.                             |
| 9     | `users.getUsers`, `contacts.resolveUsername`, `messages.sendMessage`                                                                                               | `tests/test_peers.py` and `tests/test_messages.py` fake senders returning generated TL constructors | Run `get_me()`, username resolution, and Saved Messages send against Telegram test DCs; keep fake send tests for deterministic access-hash and flood-wait behavior. |

## Product Methods Still Deferred

| Public or private method               | Current state                                                                                                                                                                        | Owning phase |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| `Client.send_file()`                   | Raises `NotImplementedError`; upload/media send is Phase 10.                                                                                                                         | Phase 10     |
| `Client.download_media()`              | Raises `NotImplementedError`; download/CDN handling is Phase 10.                                                                                                                     | Phase 10     |
| Real pushed update receive loop        | Private `_feed_raw_update()` exists for tests and future sender integration.                                                                                                         | Phase 8/11   |
| High-level edit/delete message helpers | Not part of Phase 9 v1 gate; use generated raw `messages.editMessage`, `messages.deleteMessages`, or channel delete requests directly until docs decide whether wrappers are needed. | Phase 9/12   |
| Live Saved Messages send/receive       | Gated scaffold only; skipped without `MINIPROTO_INTEGRATION=1` and credentials.                                                                                                      | Phase 9/12   |

## Rules For Future Updates

Add a row whenever a test fakes a Telegram RPC result, a private hook stands in for real network behavior, or a public method remains intentionally deferred. Remove or rewrite a row only after a live or fake-server replacement exists and `PROGRESS.md` records the passing gate.

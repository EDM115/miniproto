# Integration Tests

Live Telegram tests are opt-in and skipped unless `MINIPROTO_INTEGRATION=1` is set. Keep credentials in `.env` or CI secrets only; `.env.example` documents the expected variable names and `.env` is ignored by git.
The current live path targets production Telegram DCs by default. Test DC support remains documented and configurable, but it is not the default path because current desktop/web test-account login was not reliable enough for local validation.
Production DC tests also require `MINIPROTO_REAL_INTEGRATION=1`. Bot auth can run non-interactively with `MINIPROTO_BOT_TOKEN`. Phone auth uses `MINIPROTO_REAL_PHONE` and prompts for the current one-time login code only when `MINIPROTO_LIVE_PROMPT_CODE=1` and pytest is running interactively. Do not store phone login codes in `.env`; they change on every login attempt.
Live sessions are stored under `.tmp/miniproto-*.sqlite` using `MINIPROTO_SESSION_KEY`, so the phone prompt is only needed when there is no valid persisted user session yet.

Run the four current smoke checks with:

```pwsh
uv run pytest tests/integration/test_auth_live.py tests/integration/test_messages_live.py tests/integration/test_media_live.py
```

The checks cover bot authorization plus `get_me()`, phone authorization plus `get_me()` and reconnect from persisted session, Saved Messages send plus `messages.getHistory` and Saved Messages file upload plus download byte comparison.

The media-limit benchmark runs outside pytest. It uploads and downloads Telegram's default 2,097,152,000-byte (2000 MiB) payload unless you override its size or part limit. Both integration gates and authorized accounts are required.

```pwsh
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_LIVE_BENCH = "1"
$env:MINIPROTO_LIVE_BENCH_DC_ID = "4"
uv run miniproto-bench-live-media --actor both
```

This runs user and bot transfers against DC 4. User uploads target Saved Messages; bot uploads require `MINIPROTO_LIVE_BENCH_BOT_PEER`. For download-only runs, provide a file ID. The [development guide](../../docs/development.md#live-media-limit-benchmark) documents the other options.

The manual `.github/workflows/live-media-bench.yml` workflow runs smoke or matrix mode on Linux or Windows. Matrix smoke has four cells; full mode has 576. The workflow restores optional encrypted sessions from secrets and can provision string sessions when an actor's session path is absent. Provisioning checks the requested DC and account kind, then skips existing files. The workflow uploads logs and JSON artifacts even when a run fails. The development guide covers session preparation and matrix controls.

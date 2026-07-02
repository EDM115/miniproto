# Integration Tests

Live Telegram tests are opt-in and skipped unless `MINIPROTO_INTEGRATION=1` is set. Keep credentials in `.env` or CI secrets only; `.env.example` documents the expected variable names and `.env` is ignored by git.
The current live path targets production Telegram DCs by default. Test DC support remains documented and configurable, but it is not the default path because current desktop/web test-account login was not reliable enough for local validation.
Production DC tests also require `MINIPROTO_REAL_INTEGRATION=1`. Bot auth can run non-interactively with `MINIPROTO_BOT_TOKEN`. Phone auth uses `MINIPROTO_REAL_PHONE` and prompts for the current one-time login code only when `MINIPROTO_LIVE_PROMPT_CODE=1` and pytest is running interactively. Do not store phone login codes in `.env`; they change on every login attempt.
Live sessions are stored under `.tmp/miniproto-*.sqlite` using `MINIPROTO_SESSION_KEY`, so the phone prompt is only needed when there is no valid persisted user session yet.

Run the five current smoke checks with:

```powershell
uv run pytest tests/integration/test_auth_live.py tests/integration/test_messages_live.py tests/integration/test_media_live.py -q
```

The checks cover bot authorization plus `get_me()`, phone authorization plus `get_me()` and reconnect from persisted session, Saved Messages send plus `messages.getHistory`, and Saved Messages file upload plus download byte comparison.

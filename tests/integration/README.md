# Integration Auth Tests

Live Telegram tests are opt-in and skipped unless `MINIPROTO_INTEGRATION=1` is set in the environment. Keep credentials in `.env` or CI secrets only; `.env.example` documents the expected variable names and `.env` is ignored by git.
Required for test-DC auth later: `MINIPROTO_API_ID`, `MINIPROTO_API_HASH`, `MINIPROTO_SESSION_KEY`, at least one `MINIPROTO_TEST_DC1` through `MINIPROTO_TEST_DC5` endpoint in `host:port` or `[ipv6]:port` form, `MINIPROTO_TEST_DC_ID`, and either `MINIPROTO_TEST_PHONE` plus `MINIPROTO_TEST_CODE` or `MINIPROTO_BOT_TOKEN` for bot auth.
Production DC checks must stay disabled unless `MINIPROTO_REAL_INTEGRATION=1` is also set. Use `MINIPROTO_REAL_PHONE`, `MINIPROTO_REAL_CODE`, `MINIPROTO_REAL_PASSWORD`, and `MINIPROTO_REAL_DC_ID` only for explicit real-account experiments.
Run later with:

```powershell
uv run pytest tests/integration/test_auth_live.py -q
```

Phase 6 ships this harness before credentials are available. The live auth test itself still skips with a clear message until the raw invoke/real transport path is wired deeply enough to make Telegram network calls.

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

The heavy live media-limit benchmark is not part of pytest. Run it only when you intentionally want to create and transfer the default Telegram MTProto media-limit payload:

```powershell
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_LIVE_BENCH = "1"
$env:MINIPROTO_LIVE_BENCH_DC_ID = "4"
uv run python tools/bench/benchmark_live_media_limit.py --actor both
```

It writes the deterministic payload and downloads under `.tmp/`, uses separate encrypted benchmark sessions, prints fixed-window progress every 5 seconds by default, and reports throughput percentiles for user and bot transfers. Set `MINIPROTO_LIVE_BENCH_BOT_PEER` to a real chat/user/channel; bots cannot send to `self`, so the benchmark fails before uploading if this peer is missing. Numeric IDs such as `854158484` need no prefix and are resolved from the existing peer cache or a recent-dialog cache seed; usernames remain the most reliable bot peer input. Upload concurrency uses `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency` and defaults to `8`, while download concurrency uses `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency` and defaults to `1` because the 2026-07-03 DC 4 VPS matrix showed higher download concurrency losing to Telegram flood waits and disconnect stalls. High-level transfers use dedicated media sender lanes by default; leave `MINIPROTO_LIVE_BENCH_UPLOAD_MEDIA_LANES` / `MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES` empty to follow the matching concurrency, or set either one to `0` for an A/B run against the legacy main-sender path. Downloads adaptively slow-start, reduce the active request window after flood waits or disconnects, then conservatively ramp back up after successful chunks when concurrency is raised for controlled runs. Use `MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE` to compare the stable 512 KiB benchmark default with 1 MiB chunks, `MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY=0` for a non-adaptive comparison, `MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT` / `MINIPROTO_LIVE_BENCH_UPLOAD_PART_RETRIES` to tune upload-part tail retries, `MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT` / `MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES` to tune download-chunk tail retries, `MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD` to tune short download flood-wait retries, and `MINIPROTO_LIVE_BENCH_LOG_LEVEL` / `MINIPROTO_LIVE_BENCH_LOG_FORMAT` / `MINIPROTO_LIVE_BENCH_TRACE_MEMORY` for benchmark observability. Transfer summaries include both full operation duration and byte-transfer duration, plus part requests, retries, flood-wait totals, retry sleep, reconnects, sender drops, and requests/sec.

The manual GitHub Actions workflow `.github/workflows/live-media-bench.yml` can run the benchmark with repository secrets. Prefer base64-encoded encrypted session files in `MINIPROTO_LIVE_BENCH_USER_SESSION_B64` and `MINIPROTO_LIVE_BENCH_BOT_SESSION_B64`; for one-off user runs without a stored session, choose `user_auth_mode=cloudflared-code` and enter the Telegram login code through the printed temporary form URL within 15 minutes.

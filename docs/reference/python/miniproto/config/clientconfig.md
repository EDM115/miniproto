---
title: "miniproto.config.ClientConfig"
description: "Immutable client configuration for authentication, session storage, RPCs, updates, and media."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.config.ClientConfig"
source_path: "src/miniproto/config.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/config.py#L81"
aliases: ["miniproto.ClientConfig"]
module: "miniproto.config"
---

## `miniproto.config.ClientConfig`

```python
ClientConfig(api_id: int, api_hash: str, session_storage: SessionStorage | None = None, session_path: str | os.PathLike[str] = 'miniproto.session.sqlite', transport: TransportConfig = TransportConfig(), device: DeviceInfo = DeviceInfo(), update_queue_size: int = 1000, update_queue_overflow: UpdateQueueOverflowPolicy = 'raise', update_duplicate_window: int = 2048, dc_id: int = 2, test_mode: bool = False, request_timeout: float = 30.0, max_request_retries: int = 2, max_reconnect_attempts: int | None = None, max_pending_rpcs: int = 512, flood_sleep_threshold: int | None = None, method_flood_cache_size: int = 512, media_concurrency: int | None = None, media_max_buffer_size: int | None = None, media_download_max_in_flight_bytes_per_dc: int = 16 * 1024 * 1024, media_upload_max_in_flight_bytes_per_dc: int = 8 * 1024 * 1024, media_download_small_queue_limit: int | None = None, media_download_large_queue_limit: int | None = None, media_idle_close: float | None = 120.0, bot_token: str | None = None) -> None
```

Immutable client configuration for authentication, session storage, RPCs, updates, and media.

**Parameters:**

- **api_id** (<code>[int](#int)</code>) – Positive Telegram application identifier.
- **api_hash** (<code>[str](#str)</code>) – Telegram application secret; excluded from representations.
- **session_storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage) | None</code>) – Optional session backend. When omitted, the client uses encrypted SQLite storage at ``session_path``.
- **session_path** (<code>[str](#str) | [PathLike](#os.PathLike)[[str](#str)]</code>) – Path for the default encrypted SQLite session, defaulting to ``"miniproto.session.sqlite"``.
- **transport** (<code>[TransportConfig](#miniproto.config.TransportConfig)</code>) – TCP transport configuration.
- **device** (<code>[DeviceInfo](#miniproto.config.DeviceInfo)</code>) – Telegram-facing device metadata.
- **update_queue_size** (<code>[int](#int)</code>) – Bounded number of pending updates, defaulting to 1000.
- **update_queue_overflow** (<code>[UpdateQueueOverflowPolicy](#miniproto.config.UpdateQueueOverflowPolicy)</code>) – Overflow action: ``"raise"``, ``"drop_oldest"``, or ``"drop_newest"``.
- **update_duplicate_window** (<code>[int](#int)</code>) – Number of recent updates retained for duplicate suppression.
- **dc_id** (<code>[int](#int)</code>) – Initial Telegram datacenter identifier, defaulting to 2.
- **test_mode** (<code>[bool](#bool)</code>) – Select Telegram's test environment when true.
- **request_timeout** (<code>[float](#float)</code>) – Default per-request timeout in seconds.
- **max_request_retries** (<code>[int](#int)</code>) – Maximum automatic retries for eligible RPCs.
- **max_reconnect_attempts** (<code>[int](#int) | None</code>) – Optional cap for transport reconnections.
- **max_pending_rpcs** (<code>[int](#int)</code>) – Maximum concurrently pending RPCs.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Maximum flood-wait duration to sleep automatically; ``None`` uses the default retry policy.
- **method_flood_cache_size** (<code>[int](#int)</code>) – Number of method flood-wait entries to remember.
- **media_concurrency** (<code>[int](#int) | None</code>) – Optional default concurrent media requests.
- **media_max_buffer_size** (<code>[int](#int) | None</code>) – Optional media buffering cap in bytes.
- **media_download_max_in_flight_bytes_per_dc** (<code>[int](#int)</code>) – Per-DC download scheduler byte budget.
- **media_upload_max_in_flight_bytes_per_dc** (<code>[int](#int)</code>) – Per-DC upload scheduler byte budget.
- **media_download_small_queue_limit** (<code>[int](#int) | None</code>) – Optional small-download queue limit.
- **media_download_large_queue_limit** (<code>[int](#int) | None</code>) – Optional large-download queue limit.
- **media_idle_close** (<code>[float](#float) | None</code>) – Seconds before unused media lanes close; ``None`` keeps them open for the client lifetime.
- **bot_token** (<code>[str](#str) | None</code>) – Optional bot token, excluded from representations.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If required identifiers or secrets are empty, limits are invalid, or a media scheduler budget is below 64 KiB.

<details class="security" open markdown="1">
<summary>Security</summary>

``api_hash``, ``bot_token``, and the supplied storage backend are hidden from the dataclass representation, but callers remain responsible for protecting configuration values and session storage.

</details>

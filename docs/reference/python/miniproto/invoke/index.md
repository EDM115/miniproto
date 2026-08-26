---
title: "miniproto.invoke"
description: "Prepare, send, decode, retry and persist low-level Telegram RPC state."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.invoke"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py"
module: "miniproto.invoke"
---

## `miniproto.invoke`

Prepare, send, decode, retry and persist low-level Telegram RPC state.

## Public objects

- [`TELEGRAM_LAYER`](./telegram-layer/) — Public attribute `miniproto.invoke.TELEGRAM_LAYER`.
- [`INIT_CONNECTION_ENVELOPES`](./init-connection-envelopes/) — Public attribute `miniproto.invoke.INIT_CONNECTION_ENVELOPES`.
- [`RawSender`](./rawsender/) — Minimal connected sender capability required by the RPC invocation layer.
- [`SenderFactory`](./senderfactory/) — Public attribute `miniproto.invoke.SenderFactory`.
- [`wrap_raw_request`](./wrap-raw-request/) — Wrap a raw request for transmission.
- [`sender_needs_init`](./sender-needs-init/) — Return whether ``sender`` still needs its first init-connection envelope.
- [`mark_sender_initialized`](./mark-sender-initialized/) — Mark a sender as initialized when it permits dynamic state attributes.
- [`decode_rpc_response`](./decode-rpc-response/) — Decode and validate an RPC result, translating Telegram error bodies.
- [`decode_result_payload`](./decode-result-payload/) — Decode bytes or gzip-packed RPC results while leaving decoded values unchanged.
- [`validate_result_type`](./validate-result-type/) — Raise when a concrete TL response does not match the request result contract.
- [`result_type_for_request`](./result-type-for-request/) — Return a raw request class's declared TL ``RESULT_TYPE``, when available.
- [`is_retryable_request`](./is-retryable-request/) — Determine whether retrying this request is protocol-safe.
- [`should_retry_rpc_error`](./should-retry-rpc-error/) — Return whether a classified server-side RPC failure is transient enough to retry.
- [`should_sleep_for_flood_wait`](./should-sleep-for-flood-wait/) — Return whether a flood wait is short enough for automatic sleeping.
- [`MethodFloodWaitCache`](./methodfloodwaitcache/) — Bounded client-local cache for Telegram's method-scoped flood waits.
- [`method_name_for_request`](./method-name-for-request/) — Return the innermost wrapped request class's Telegram-qualified method name.
- [`load_session_record`](./load-session-record/) — Load current structured or legacy session data into a ``SessionRecord``.
- [`build_sender_from_session`](./build-sender-from-session/) — Build a sender for the session DC or -- with overrides -- a media DC.
- [`clear_invalid_auth_key`](./clear-invalid-auth-key/) — Atomically clear an unusable persisted authorization key and user identity.
- [`wrap_transport_failure`](./wrap-transport-failure/) — Translate a transport exception to the RPC-level error exposed to callers.

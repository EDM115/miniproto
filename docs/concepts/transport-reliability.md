---
title: Transport, reliability and replay
description: Framing, receive ownership, reconnect behavior, quick acknowledgements and conservative RPC replay.
slug: /concepts/transport-reliability/
generated: false
---

## Framed TCP transport

The configured transport selects TCP abridged, intermediate or padded-intermediate framing. The transport enforces positive connect/read/write deadlines and a maximum decoded payload size; it creates a fresh frame codec when reconnecting so partial bytes from the old stream cannot cross into the new connection.

`TransportConfig.max_payload_size` defaults to 16 MiB. The sender also uses it as the decompressed-output limit for each gzip wrapper in message, container and RPC-result bodies. One decode path may contain up to 16 nested wrappers. A malformed frame, malformed gzip stream or gzip payload over the configured limit raises `ProtocolValidationError`.

One task must own `recv()` and its underlying stream reader. `asyncio.StreamReader` rejects concurrent reads, so calling `recv`, `read_event` or `read_packet` concurrently on the same transport is not supported. The sender is the normal single receive owner and allows concurrent callers to wait on independently resolved RPC futures while it serializes message-ID assignment and transport writes.

## Retry after transport loss

When a transport drops, the sender reconnects under its connection lock and resends in-flight requests only when miniproto classifies them as retry-safe. The default list covers selected read methods and the `messages.sendMessage` and `messages.sendMedia` writes, which use Telegram `random_id` de-duplication. `messages.getBotCallbackAnswer` presses a bot button, so miniproto excludes it even though its name starts with `get`. `Client.invoke(retry=...)` can override the classification; set it only when you understand how Telegram handles a repeated request.

Telegram also sends explicit protocol signals to request a targeted resend or correction for a pending message. The sender retries only the request named by a valid `msgs_resend_req`, `bad_server_salt` or time-correction `bad_msg_notification`. These signals can trigger a resend even when transport-loss retries are disabled; the sender re-encodes each named pending request with a fresh message ID. Repeated incoming message IDs are suppressed, and miniproto acknowledges repeated content-related messages again. In a fresh message container, a repeated child does not suppress a separate fresh sibling. Repeating the container's own ID suppresses its child batch.

If an unsafe request may have reached Telegram before the transport failed, the sender reports `AmbiguousRpcResult` instead of silently replaying it. An ambiguity is a product decision point: inspect the application's own idempotency key, query state where appropriate and avoid assuming that a retry is harmless.

## Quick acknowledgement is an early receipt

Some framing modes can request a quick acknowledgement. `quick_ack=True` or a quick-ack callback asks for that transport-level signal. The receipt may show that Telegram's transport has seen an encrypted attempt, but it never resolves the RPC future and never proves that the method succeeded. Continue to wait for the normal result or handle the normal timeout/error path.

## Failure boundaries

Malformed framing and encrypted-protocol validation failures terminate the sender receive loop, fail pending work and close the transport. Read/write/connect failures, reconnect limits, pings, acknowledgement flushing, pending-RPC capacity and caller cancellation follow their own rules.

The default transport mode is `tcp_abridged`. `TransportConfig` sets the reconnect backoff. Measure a comparable workload before tuning it, and preserve the retry rules above.

---
title: Transport, reliability, and replay
description: Framing, receive ownership, reconnect behavior, quick acknowledgements, and conservative RPC replay.
slug: /concepts/transport-reliability/
generated: false
---

## Framed TCP transport

The configured transport selects TCP abridged, intermediate, or padded-intermediate framing. The transport enforces positive connect/read/write deadlines and a maximum decoded payload size; it creates a fresh frame codec when reconnecting so partial bytes from the old stream cannot cross into the new connection.

One task must own `recv()` and its underlying stream reader. `asyncio.StreamReader` rejects concurrent reads, so calling `recv`, `read_event`, or `read_packet` concurrently on the same transport is not supported. The sender is the normal single receive owner and allows concurrent callers to wait on independently resolved RPC futures while it serializes message-ID assignment and transport writes.

## Reconnect is not permission to duplicate work

A transport loss is routine on some paths, including media data centres. The sender reconnects under its connection lock and retries only requests explicitly classified as retry-safe. The built-in classification permits known read prefixes and writes for which Telegram supplies `random_id` de-duplication, such as the supported send-message/media cases. A caller can explicitly override retry eligibility, but should do so only when it understands the method's server-side idempotency.

If an unsafe request may have reached Telegram before the transport failed, the sender reports `AmbiguousRpcResult` instead of silently replaying it. An ambiguity is a product decision point: inspect the application's own idempotency key, query state where appropriate, and avoid assuming that a retry is harmless.

## Quick acknowledgement is an early receipt

Some framing modes can request a quick acknowledgement. `quick_ack=True` or a quick-ack callback asks for that transport-level signal. The receipt may show that Telegram's transport has seen an encrypted attempt, but it never resolves the RPC future and never proves that the method succeeded. Continue to wait for the normal result or handle the normal timeout/error path.

## Failure boundaries

Malformed framing or encrypted-protocol validation failures are not treated as a routine reconnect. They become fatal sender errors and pending work fails rather than accepting malformed input. Read/write/connect failures, bounded reconnect attempts, pings, acknowledgement flushing, pending-RPC capacity, and caller cancellation all have separate behavior; reliability does not mean a request survives every lifecycle transition.

The default transport mode is `tcp_abridged`, with reconnect backoff configured by `TransportConfig`. Tune only after measuring a comparable workload, and keep the protocol-safety replay boundary intact.

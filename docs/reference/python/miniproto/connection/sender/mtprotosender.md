---
title: "miniproto.connection.sender.MTProtoSender"
description: "Manage a concurrent encrypted MTProto session over a reconnecting transport."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.sender.MTProtoSender"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L145"
aliases: ["miniproto.connection.MTProtoSender"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender`

```python
MTProtoSender(endpoint: ConnectionEndpoint, transport_config: TransportConfig, state: MTProtoState, *, connector: StreamConnector | None = None, reconnect_attempts: int = 3, ping_disconnect_delay: int = 75, ping_interval: float = DEFAULT_PING_INTERVAL, ack_flush_threshold: int = DEFAULT_ACK_FLUSH_THRESHOLD, ack_max_delay: float = DEFAULT_ACK_MAX_DELAY, max_pending_rpcs: int | None = None, incoming_queue_size: int = DEFAULT_INCOMING_QUEUE_SIZE, on_salt_change: Callable[[int], None] | None = None, reconnect_cooldown: float = DEFAULT_RECONNECT_COOLDOWN) -> None
```

Manage a concurrent encrypted MTProto session over a reconnecting transport.

One sender serializes message-ID/sequence assignment and transport writes
while supporting concurrent :meth:`request` callers. It owns its receive and
keepalive tasks after :meth:`connect`; callers must eventually
:meth:`disconnect`. On a routine transport loss it retries only explicitly
``retry_safe`` requests and reports an ambiguous result for unsafe requests.

Configure a disconnected sender and its bounded background machinery.

**Parameters:**

- **endpoint** (<code>[ConnectionEndpoint](#miniproto.connection.transport.ConnectionEndpoint)</code>) – Remote MTProto TCP destination.
- **transport_config** (<code>[TransportConfig](#miniproto.config.TransportConfig)</code>) – Transport framing, deadline, and reconnect bounds.
- **state** (<code>[MTProtoState](#miniproto.mtproto.state.MTProtoState)</code>) – Mutable authorization/session state used to encrypt, validate,
sequence, acknowledge, and persist MTProto messages.
- **connector** (<code>[StreamConnector](#miniproto.connection.transport.StreamConnector) | None</code>) – Optional stream factory passed to every transport open.
- **reconnect_attempts** (<code>[int](#int)</code>) – Maximum connection attempts per recovery cycle;
defaults to 3.
- **ping_disconnect_delay** (<code>[int](#int)</code>) – Telegram disconnect timeout armed by pings;
defaults to 75 seconds.
- **ping_interval** (<code>[float](#float)</code>) – Requested ping cadence, clamped to at least 0.05 s
and no more than half the read deadline; defaults to 45 s.
- **ack_flush_threshold** (<code>[int](#int)</code>) – Pending acknowledgements that trigger an eager
flush; clamped to at least 1 and defaults to 16.
- **ack_max_delay** (<code>[float](#float)</code>) – Maximum age before the keepalive task flushes queued
acknowledgements; clamped to at least 0.05 s and defaults to 10.
- **max_pending_rpcs** (<code>[int](#int) | None</code>) – Optional hard concurrent :meth:`request` limit.
- **incoming_queue_size** (<code>[int](#int)</code>) – Bounded unsolicited-message queue capacity;
clamped to at least 1 and defaults to 256. Oldest items are
dropped when it is full.
- **on_salt_change** (<code>[Callable](#collections.abc.Callable)[[[int](#int)], None] | None</code>) – Optional synchronous callback invoked after the
sender accepts a server salt update; callback errors are logged.
- **reconnect_cooldown** (<code>[float](#float)</code>) – Minimum paced delay after a young connection
dies; clamped to zero or greater and defaults to one second.

<details class="notes" open markdown="1">
<summary>Notes</summary>

Construction starts no tasks or network I/O. Methods share internal
connect/send locks; use this instance from one event loop.

</details>

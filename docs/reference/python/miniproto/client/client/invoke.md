---
title: "miniproto.client.Client.invoke"
description: "Invoke a low-level Telegram request through the main sender."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.invoke"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1515"
aliases: ["miniproto.Client.invoke"]
module: "miniproto.client"
---

## `miniproto.client.Client.invoke`

```python
invoke(raw_request: object, *, request_timeout: float | None = None, flood_sleep_threshold: int | None = None, retry: bool | None = None, quick_ack: bool = False, quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None) -> object
```

Invoke a low-level Telegram request through the main sender.

Default replay permits known read requests and selected writes deduplicated by ``random_id``. ``messages.getBotCallbackAnswer`` is excluded because it triggers a bot callback.

**Parameters:**

- **raw_request** (<code>[object](#object)</code>) – Generated TL request object to send.
- **request_timeout** (<code>[float](#float) | None</code>) – Timeout for each sender request attempt, defaulting to ``ClientConfig.request_timeout``. Repeated attempts and flood-wait sleeps can exceed this duration in total.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Maximum flood-wait seconds to sleep. ``None`` inherits configuration, whose default disables sleeping, ``0`` surfaces positive waits.
- **retry** (<code>[bool](#bool) | None</code>) – ``None`` uses the request's retry-safety classification, ``True`` permits replay, ``False`` suppresses ambiguous transport replay and transient-error retries. Server-rejected flood waits and datacenter migrations can still retry.
- **quick_ack** (<code>[bool](#bool)</code>) – Request a quick acknowledgement from transports that support it.
- **quick_ack_callback** (<code>[Callable](#collections.abc.Callable)[[[QuickAckReceipt](#miniproto.connection.sender.QuickAckReceipt)], None] | None</code>) – Optional callback invoked at most once with that acknowledgement. Supplying it also requests quick acknowledgement delivery. A receipt confirms transport acceptance, not RPC completion.

**Returns:**

- <code>[object](#object)</code> – The decoded raw Telegram response.

**Raises:**

- <code>[ConnectionError](#ConnectionError)</code> – If the client is not connected.
- <code>[FloodWait](#miniproto.errors.FloodWait)</code> – If a remembered or server flood wait is not slept.
- <code>[RpcError](#miniproto.errors.RpcError)</code> – For Telegram RPC failures, including classified variants.
- <code>[RequestTimeout](#miniproto.errors.RequestTimeout)</code> – If a connected sender's request times out and eligible retries are exhausted.
- <code>[ClientDisconnected](#miniproto.errors.ClientDisconnected)</code> – If a transport failure leaves the client or sender disconnected after retries.
- <code>[AmbiguousRpcResult](#miniproto.errors.AmbiguousRpcResult)</code> – If a transport failure leaves a non-replayable request's execution uncertain.

<details class="lifecycle" open markdown="1">
<summary>Lifecycle</summary>

Lazy sender construction is serialized. Datacenter migration can update the main session and retry even when ``retry=False``. Dedicated media lanes route file migrations without changing the main session. RPC-result decompression uses ``config.transport.max_payload_size`` as its output bound.

</details>

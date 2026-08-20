---
title: "miniproto.client.Client.invoke"
description: "Invoke a low-level Telegram request through the main sender."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.invoke"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1461"
aliases: ["miniproto.Client.invoke"]
module: "miniproto.client"
---

## `miniproto.client.Client.invoke`

```python
invoke(raw_request: object, *, request_timeout: float | None = None, flood_sleep_threshold: int | None = None, retry: bool | None = None, quick_ack: bool = False, quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None) -> object
```

Invoke a low-level Telegram request through the main sender.

**Parameters:**

- **raw_request** (<code>[object](#object)</code>) – Generated TL request object to send.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-request timeout; defaults to ``ClientConfig.request_timeout``.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Optional maximum flood wait to sleep; defaults to configuration.
- **retry** (<code>[bool](#bool) | None</code>) – Whether to force or suppress retry eligibility for this request.
- **quick_ack** (<code>[bool](#bool)</code>) – Request a quick acknowledgement from transports that support it.
- **quick_ack_callback** (<code>[Callable](#collections.abc.Callable)[[[QuickAckReceipt](#miniproto.connection.sender.QuickAckReceipt)], None] | None</code>) – Optional callback invoked at most once with that acknowledgement.

**Returns:**

- <code>[object](#object)</code> – The decoded raw Telegram response.

**Raises:**

- <code>[ConnectionError](#ConnectionError)</code> – If the client is not connected.
- <code>[FloodWait](#miniproto.errors.FloodWait)</code> – If a remembered or server flood wait is not slept.
- <code>[RpcError](#miniproto.errors.RpcError)</code> – For Telegram RPC failures, including classified variants.
- <code>[TimeoutError](#TimeoutError)</code> – When retryable transport failures exhaust the configured retry budget.

<details class="lifecycle" open markdown="1">
<summary>Lifecycle</summary>

Lazy sender construction and reconnection are serialized. A datacenter migration may update the main session and retry eligible requests; media lanes deliberately do not migrate it.

</details>

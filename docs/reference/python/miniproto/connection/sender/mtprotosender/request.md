---
title: "miniproto.connection.sender.MTProtoSender.request"
description: "Send one RPC and await its decoded result with safe retry controls."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.request"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L336"
aliases: ["miniproto.connection.MTProtoSender.request"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.request`

```python
request(body: bytes | object, *, content_related: bool = True, retry_safe: bool = False, request_timeout: float | None = None, quick_ack: bool = False, quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None) -> object
```

Send one RPC and await its decoded result with safe retry controls.

**Parameters:**

- **body** (<code>[bytes](#bytes) | [object](#object)</code>) – Encoded MTProto bytes or a serializable TL request object.
- **content_related** (<code>[bool](#bool)</code>) – Allocate a content-related sequence number;
defaults to ``True``.
- **retry_safe** (<code>[bool](#bool)</code>) – Permit automatic resend with a fresh message ID after a
transport loss; defaults to ``False`` to avoid duplicating
unknown-side-effect RPCs.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional caller wait bound in seconds. ``None``
waits until a result, lifecycle failure, or cancellation.
- **quick_ack** (<code>[bool](#bool)</code>) – Request a transport quick ACK for the encrypted attempt;
defaults to ``False`` and never completes this RPC by itself.
- **quick_ack_callback** (<code>[Callable](#collections.abc.Callable)[[[QuickAckReceipt](#miniproto.connection.sender.QuickAckReceipt)], None] | None</code>) – Optional synchronous callback receiving the first
non-stale :class:`QuickAckReceipt`; supplying it also requests an
ACK. Callback failures are isolated and recorded.

**Returns:**

- <code>[object](#object)</code> – The decoded ``RpcResult.result`` or a service response such as
- <code>[object](#object)</code> – class:`Pong`.

**Raises:**

- <code>[PendingRpcLimitExceeded](#miniproto.errors.PendingRpcLimitExceeded)</code> – If ``max_pending_rpcs`` capacity is full.
- <code>[TimeoutError](#TimeoutError)</code> – If ``request_timeout`` expires; its pending aliases
and quick-ACK registrations are removed.
- <code>[AmbiguousRpcResult](#miniproto.errors.AmbiguousRpcResult)</code> – If an unsafe request loses transport after it may
have reached Telegram.
- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If connection/recovery exhausts or protocol handling
fails.
- <code>[CancelledError](#asyncio.CancelledError)</code> – If the caller cancels; its pending state is
removed without cancelling other requests.

<details class="notes" open markdown="1">
<summary>Notes</summary>

Calls may run concurrently. Sending and message ID allocation are
serialized internally, while futures resolve independently.

</details>

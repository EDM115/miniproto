---
title: "miniproto.connection.sender.PendingRequest"
description: "Internal state retained for one unresolved request and its resend aliases."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.sender.PendingRequest"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L79"
aliases: ["miniproto.connection.PendingRequest"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.PendingRequest`

```python
PendingRequest(body: bytes | object, content_related: bool, future: asyncio.Future[object], retry_safe: bool = False, attempts: int = 0, transport: Transport | None = None, aliases: set[int] = set(), quick_ack: bool = False, quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None, quick_ack_received: bool = False, quick_ack_waiters: list[QuickAckWaiter] = list()) -> None
```

Internal state retained for one unresolved request and its resend aliases.

**Parameters:**

- **body** (<code>[bytes](#bytes) | [object](#object)</code>) – Original encoded or serializable request body.
- **content_related** (<code>[bool](#bool)</code>) – Whether MTProto sequence allocation marks it as content.
- **future** (<code>[Future](#asyncio.Future)[[object](#object)]</code>) – Future completed with the RPC result or terminal exception.
- **retry_safe** (<code>[bool](#bool)</code>) – Whether transport loss may resend this request automatically.
- **attempts** (<code>[int](#int)</code>) – Number of encrypted send attempts already made.
- **transport** (<code>[Transport](#miniproto.connection.transport.Transport) | None</code>) – Transport used for the latest attempt.
- **aliases** (<code>[set](#set)[[int](#int)]</code>) – Message IDs that currently map to this request after retries.
- **quick_ack** (<code>[bool](#bool)</code>) – Whether the latest attempts request transport-level quick ACKs.
- **quick_ack_callback** (<code>[Callable](#collections.abc.Callable)[[[QuickAckReceipt](#miniproto.connection.sender.QuickAckReceipt)], None] | None</code>) – Optional synchronous callback for the first receipt.
- **quick_ack_received** (<code>[bool](#bool)</code>) – Whether a non-stale receipt was already delivered.
- **quick_ack_waiters** (<code>[list](#list)[[QuickAckWaiter](#miniproto.connection.sender.QuickAckWaiter)]</code>) – Registered receipt correlations awaiting removal.

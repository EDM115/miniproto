---
title: "miniproto.connection.sender.QuickAckReceipt"
description: "Early transport-acknowledgement metadata for one encrypted send attempt."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.sender.QuickAckReceipt"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L67"
aliases: ["miniproto.QuickAckReceipt","miniproto.connection.QuickAckReceipt"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.QuickAckReceipt`

```python
QuickAckReceipt(token: int, latency_ms: float, attempt: int) -> None
```

Early transport-acknowledgement metadata for one encrypted send attempt.

A receipt confirms only that Telegram accepted the encrypted transport packet; it does not complete the RPC or replace the later result, error or MTProto service acknowledgement.

**Parameters:**

- **token** (<code>[int](#int)</code>) – Opaque token supplied by Telegram's quick-ACK frame.
- **latency_ms** (<code>[float](#float)</code>) – Elapsed monotonic send-to-ACK time in milliseconds.
- **attempt** (<code>[int](#int)</code>) – One-based encrypted send attempt that requested the ACK.

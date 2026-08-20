---
title: "miniproto.connection.sender.MTProtoSender.send"
description: "Send a one-way encrypted message and return its MTProto message ID."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.send"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L501"
aliases: ["miniproto.connection.MTProtoSender.send"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.send`

```python
send(body: bytes | object, *, content_related: bool = True) -> int
```

Send a one-way encrypted message and return its MTProto message ID.

**Parameters:**

- **body** (<code>[bytes](#bytes) | [object](#object)</code>) – Encoded bytes or serializable TL body to encrypt and send.
- **content_related** (<code>[bool](#bool)</code>) – Whether sequence allocation marks the message as
content-related; defaults to ``True``.

**Returns:**

- <code>[int](#int)</code> – The allocated message ID after the packet is accepted by the local
- <code>[int](#int)</code> – transport write path.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If connection or send/recovery fails.

<details class="notes" open markdown="1">
<summary>Notes</summary>

This does not create a result future and may retry a raw transport
write once during recovery. It serializes with all requests.

</details>

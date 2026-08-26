---
title: "miniproto.connection.sender.MTProtoSender.ping"
description: "Send a retry-safe ``ping_delay_disconnect`` and require its ``Pong``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.ping"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L537"
aliases: ["miniproto.connection.MTProtoSender.ping"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.ping`

```python
ping() -> Pong
```

Send a retry-safe ``ping_delay_disconnect`` and require its ``Pong``.

**Returns:**

- <code>[Pong](#miniproto.mtproto.codec.Pong)</code> – Telegram's matching :class:`Pong`.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If the request fails, times out or returns a body
other than ``Pong``.

<details class="notes" open markdown="1">
<summary>Notes</summary>

The keepalive task invokes this on its fixed cadence to prevent idle
read deadlines and refresh Telegram's ping-disconnect timer.

</details>

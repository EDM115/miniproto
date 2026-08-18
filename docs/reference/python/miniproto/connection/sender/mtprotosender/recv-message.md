---
title: "miniproto.connection.sender.MTProtoSender.recv_message"
description: "Wait for the next unsolicited validated encrypted message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.recv_message"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L556"
aliases: ["miniproto.connection.MTProtoSender.recv_message"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.recv_message`

```python
recv_message() -> DecodedEncryptedMessage
```

Wait for the next unsolicited validated encrypted message.

**Returns:**

- <code>[DecodedEncryptedMessage](#miniproto.mtproto.codec.DecodedEncryptedMessage)</code> – A message not consumed as an RPC result or MTProto service update.

<details class="notes" open markdown="1">
<summary>Notes</summary>

The queue has the configured bounded capacity. On overflow, the
receive loop discards the oldest unsolicited message.

</details>

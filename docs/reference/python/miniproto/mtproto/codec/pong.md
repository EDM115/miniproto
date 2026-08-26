---
title: "miniproto.mtproto.codec.Pong"
description: "MTProto ``pong`` response correlating a server message and ping ID."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.Pong"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L185"
aliases: ["miniproto.mtproto.Pong"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.Pong`

```python
Pong(msg_id: int, ping_id: int) -> None
```

MTProto ``pong`` response correlating a server message and ping ID.

**Attributes:**

- [**msg_id**](#miniproto.mtproto.codec.Pong.msg_id) (<code>[int](#int)</code>) – Server message ID carrying the response.
- [**ping_id**](#miniproto.mtproto.codec.Pong.ping_id) (<code>[int](#int)</code>) – Caller-selected ID from the corresponding ping.

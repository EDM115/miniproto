---
title: "miniproto.mtproto.codec.Pong"
description: "MTProto ``pong`` response identifying the original ping request."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.Pong"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L243"
aliases: ["miniproto.mtproto.Pong"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.Pong`

```python
Pong(msg_id: int, ping_id: int) -> None
```

MTProto ``pong`` response identifying the original ping request.

**Attributes:**

- [**msg_id**](#miniproto.mtproto.codec.Pong.msg_id) (<code>[int](#int)</code>) – Message ID of the ping request being answered.
- [**ping_id**](#miniproto.mtproto.codec.Pong.ping_id) (<code>[int](#int)</code>) – Caller-selected ID from the corresponding ping.

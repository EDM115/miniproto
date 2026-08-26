---
title: "miniproto.mtproto.codec.MsgsStateInfo"
description: "MTProto ``msgs_state_info`` body answering a state request."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.MsgsStateInfo"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L113"
aliases: ["miniproto.mtproto.MsgsStateInfo"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.MsgsStateInfo`

```python
MsgsStateInfo(req_msg_id: int, info: bytes) -> None
```

MTProto ``msgs_state_info`` body answering a state request.

**Attributes:**

- [**req_msg_id**](#miniproto.mtproto.codec.MsgsStateInfo.req_msg_id) (<code>[int](#int)</code>) – Message ID of the corresponding state request.
- [**info**](#miniproto.mtproto.codec.MsgsStateInfo.info) (<code>[bytes](#bytes)</code>) – Opaque state information bytes.

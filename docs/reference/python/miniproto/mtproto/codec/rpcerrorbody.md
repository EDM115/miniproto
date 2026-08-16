---
title: "miniproto.mtproto.codec.RpcErrorBody"
description: "Decoded MTProto ``rpc_error`` result body."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.RpcErrorBody"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L245"
aliases: ["miniproto.mtproto.RpcErrorBody"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.RpcErrorBody`

```python
RpcErrorBody(error_code: int, error_message: str) -> None
```

Decoded MTProto ``rpc_error`` result body.

**Attributes:**

- [**error_code**](#miniproto.mtproto.codec.RpcErrorBody.error_code) (<code>[int](#int)</code>) – Telegram RPC error code.
- [**error_message**](#miniproto.mtproto.codec.RpcErrorBody.error_message) (<code>[str](#str)</code>) – Telegram RPC error name or detail string.

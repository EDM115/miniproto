---
title: "miniproto.mtproto.codec.RpcResult"
description: "MTProto ``rpc_result`` body containing raw or decoded result data."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.RpcResult"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L258"
aliases: ["miniproto.mtproto.RpcResult"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.RpcResult`

```python
RpcResult(req_msg_id: int, result: ByteBuffer | object) -> None
```

MTProto ``rpc_result`` body containing raw or decoded result data.

**Attributes:**

- [**req_msg_id**](#miniproto.mtproto.codec.RpcResult.req_msg_id) (<code>[int](#int)</code>) – Message ID of the corresponding RPC request.
- [**result**](#miniproto.mtproto.codec.RpcResult.result) (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer) | [object](#object)</code>) – Raw result bytes or a decoded result object.

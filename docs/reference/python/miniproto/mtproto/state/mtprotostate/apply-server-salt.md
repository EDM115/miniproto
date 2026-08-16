---
title: "miniproto.mtproto.state.MTProtoState.apply_server_salt"
description: "Replace the current server salt after masking it to 64 bits."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.apply_server_salt"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L241"
aliases: ["miniproto.mtproto.MTProtoState.apply_server_salt"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.apply_server_salt`

```python
apply_server_salt(server_salt: int) -> None
```

Replace the current server salt after masking it to 64 bits.

**Parameters:**

- **server_salt** (<code>[int](#int)</code>) – New server-supplied salt.

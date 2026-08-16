---
title: "miniproto.mtproto.codec.NewSessionCreated"
description: "MTProto notification that establishes a new server session and salt."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.NewSessionCreated"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L230"
aliases: ["miniproto.mtproto.NewSessionCreated"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.NewSessionCreated`

```python
NewSessionCreated(first_msg_id: int, unique_id: int, server_salt: int) -> None
```

MTProto notification that establishes a new server session and salt.

**Attributes:**

- [**first_msg_id**](#miniproto.mtproto.codec.NewSessionCreated.first_msg_id) (<code>[int](#int)</code>) – First client message ID in the session.
- [**unique_id**](#miniproto.mtproto.codec.NewSessionCreated.unique_id) (<code>[int](#int)</code>) – Server-provided session uniqueness value.
- [**server_salt**](#miniproto.mtproto.codec.NewSessionCreated.server_salt) (<code>[int](#int)</code>) – Initial 64-bit server salt.

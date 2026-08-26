---
title: "miniproto.mtproto.codec.BadServerSalt"
description: "MTProto bad-message notice that additionally carries a replacement server salt."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.BadServerSalt"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L213"
aliases: ["miniproto.mtproto.BadServerSalt"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.BadServerSalt`

```python
BadServerSalt(bad_msg_id: int, bad_msg_seq_no: int, error_code: int, new_server_salt: int) -> None
```

MTProto bad-message notice that additionally carries a replacement server salt.

**Attributes:**

- [**bad_msg_id**](#miniproto.mtproto.codec.BadServerSalt.bad_msg_id) (<code>[int](#int)</code>) – Rejected message ID.
- [**bad_msg_seq_no**](#miniproto.mtproto.codec.BadServerSalt.bad_msg_seq_no) (<code>[int](#int)</code>) – Rejected sequence number.
- [**error_code**](#miniproto.mtproto.codec.BadServerSalt.error_code) (<code>[int](#int)</code>) – MTProto validation error code.
- [**new_server_salt**](#miniproto.mtproto.codec.BadServerSalt.new_server_salt) (<code>[int](#int)</code>) – Replacement 64-bit server salt.

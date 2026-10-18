---
title: "miniproto.auth.bootstrap.UnencryptedAuthKeyTransport.send_unencrypted"
description: "Send one unencrypted MTProto body and return its response body."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.bootstrap.UnencryptedAuthKeyTransport.send_unencrypted"
source_path: "src/miniproto/auth/bootstrap.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/bootstrap.py#L62"
module: "miniproto.auth.bootstrap"
---

## `miniproto.auth.bootstrap.UnencryptedAuthKeyTransport.send_unencrypted`

```python
send_unencrypted(body: bytes) -> bytes
```

Send one unencrypted MTProto body and return its response body.

**Parameters:**

- **body** (<code>[bytes](#bytes)</code>) – Serialized MTProto authorization request.

**Returns:**

- <code>[bytes](#bytes)</code> – The decoded unencrypted response body.

**Raises:**

- <code>[ConnectionError](#ConnectionError)</code> – If the server sends a quick ACK instead of a response packet.

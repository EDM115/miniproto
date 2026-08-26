---
title: "miniproto.auth.bootstrap.UnencryptedAuthKeyTransport"
description: "Exchange unencrypted MTProto authorization packets over one transport."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.bootstrap.UnencryptedAuthKeyTransport"
source_path: "src/miniproto/auth/bootstrap.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/bootstrap.py#L42"
module: "miniproto.auth.bootstrap"
---

## `miniproto.auth.bootstrap.UnencryptedAuthKeyTransport`

```python
UnencryptedAuthKeyTransport(endpoint: ConnectionEndpoint, config: ClientConfig) -> None
```

Exchange unencrypted MTProto authorization packets over one transport.

**Parameters:**

- **endpoint** (<code>[ConnectionEndpoint](#miniproto.connection.transport.ConnectionEndpoint)</code>) – Telegram data-center address to contact.
- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client transport configuration used when opening the connection.

Store connection details and defer opening the transport until first use.

**Parameters:**

- **endpoint** (<code>[ConnectionEndpoint](#miniproto.connection.transport.ConnectionEndpoint)</code>) – Telegram data-center address to contact.
- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Transport configuration used to open the connection.

---
title: "miniproto.auth.service.AuthService"
description: "Run sign-in and data-center authorization flows for one client session."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.service.AuthService"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L52"
aliases: ["miniproto.AuthService","miniproto.auth.AuthService"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService`

```python
AuthService(config: ClientConfig, storage: SessionStorage, invoker: RawInvoker) -> None
```

Run sign-in and data-center authorization flows for one client session.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client credentials and default data-center configuration.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage receiving successful authorization state.
- **invoker** (<code>[RawInvoker](#miniproto.auth.service.RawInvoker)</code>) – Callable that sends raw Telegram requests, synchronously or asynchronously.

Bind the client configuration, session storage and raw-request invoker.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client credentials and default data-center configuration.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Mutable session storage for authorization state.
- **invoker** (<code>[RawInvoker](#miniproto.auth.service.RawInvoker)</code>) – Callable that returns or awaits raw Telegram RPC results.

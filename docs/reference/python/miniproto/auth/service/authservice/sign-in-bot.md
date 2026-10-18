---
title: "miniproto.auth.service.AuthService.sign_in_bot"
description: "Authorize a bot token and persist the authenticated bot identity."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.sign_in_bot"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L125"
aliases: ["miniproto.AuthService.sign_in_bot","miniproto.auth.AuthService.sign_in_bot"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.sign_in_bot`

```python
sign_in_bot(token: str) -> object
```

Authorize a bot token and persist the authenticated bot identity.

**Parameters:**

- **token** (<code>[str](#str)</code>) – Bot authorization token supplied by BotFather.

**Returns:**

- <code>[object](#object)</code> – The successful Telegram authorization object.

**Raises:**

- <code>[RpcError](#miniproto.errors.RpcError)</code> – If Telegram does not return an authorization object.

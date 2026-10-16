---
title: "miniproto.auth.service.AuthService.sign_in_phone"
description: "Sign in a phone-number account, requesting a code and optional 2FA password."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.sign_in_phone"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L73"
aliases: ["miniproto.AuthService.sign_in_phone","miniproto.auth.AuthService.sign_in_phone"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.sign_in_phone`

```python
sign_in_phone(phone: str, code_callback: Callback0, password_callback: Callback0 | None = None) -> object
```

Sign in a phone-number account, requesting a code and optional 2FA password.

**Parameters:**

- **phone** (<code>[str](#str)</code>) – Account phone number sent to ``auth.sendCode``.
- **code_callback** (<code>[Callback0](#miniproto.auth.service.Callback0)</code>) – Callable that returns or awaits the verification code.
- **password_callback** (<code>[Callback0](#miniproto.auth.service.Callback0) | None</code>) – Callable used only when Telegram requires two-factor authentication.

**Returns:**

- <code>[object](#object)</code> – The successful Telegram authorization object.

**Raises:**

- <code>[PasswordRequired](#miniproto.errors.PasswordRequired)</code> – If the account needs 2FA and no password callback was provided.
- <code>[SignUpRequired](#miniproto.errors.SignUpRequired)</code> – If the number has no Telegram account.
- <code>[RpcError](#miniproto.errors.RpcError)</code> – If Telegram returns an unexpected result for an authorization request.

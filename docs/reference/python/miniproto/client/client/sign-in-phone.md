---
title: "miniproto.client.Client.sign_in_phone"
description: "Authorize a user account with a phone code and optional two-step password callback."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.sign_in_phone"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L530"
aliases: ["miniproto.Client.sign_in_phone"]
module: "miniproto.client"
---

## `miniproto.client.Client.sign_in_phone`

```python
sign_in_phone(phone: str, code_callback: Callable[[], Awaitable[str] | str], password_callback: Callable[[], Awaitable[str] | str] | None = None) -> object
```

Authorize a user account with a phone code and optional two-step password callback.

**Parameters:**

- **phone** (<code>[str](#str)</code>) – Phone number accepted by Telegram.
- **code_callback** (<code>[Callable](#collections.abc.Callable)[[], [Awaitable](#collections.abc.Awaitable)[[str](#str)] | [str](#str)]</code>) – Callable returning or awaiting the verification code.
- **password_callback** (<code>[Callable](#collections.abc.Callable)[[], [Awaitable](#collections.abc.Awaitable)[[str](#str)] | [str](#str)] | None</code>) – Optional callable returning or awaiting the two-step verification password.

**Returns:**

- <code>[object](#object)</code> – Telegram's authorization result.

<details class="security" open markdown="1">
<summary>Security</summary>

Callbacks are invoked only by the authorization service; avoid logging their returned credentials.

</details>

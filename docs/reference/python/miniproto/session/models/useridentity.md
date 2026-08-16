---
title: "miniproto.session.models.UserIdentity"
description: "Durable Telegram user identity with optional private contact metadata."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.models.UserIdentity"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L111"
aliases: ["miniproto.UserIdentity","miniproto.session.UserIdentity"]
module: "miniproto.session.models"
---

## `miniproto.session.models.UserIdentity`

```python
UserIdentity(id: int, access_hash: int | None = None, is_bot: bool = False, username: str | None = None, phone: str | None = None, first_name: str | None = None, last_name: str | None = None) -> None
```

Durable Telegram user identity with optional private contact metadata.

``phone`` is intentionally hidden from ``repr``. ``access_hash`` is absent
when Telegram did not provide one.

**Attributes:**

- [**id**](#miniproto.session.models.UserIdentity.id) (<code>[int](#int)</code>) – Positive Telegram user identifier.
- [**access_hash**](#miniproto.session.models.UserIdentity.access_hash) (<code>[int](#int) | None</code>) – Optional access hash needed to address the user.
- [**is_bot**](#miniproto.session.models.UserIdentity.is_bot) (<code>[bool](#bool)</code>) – Whether Telegram identifies this user as a bot.
- [**username**](#miniproto.session.models.UserIdentity.username) (<code>[str](#str) | None</code>) – Optional public username.
- [**phone**](#miniproto.session.models.UserIdentity.phone) (<code>[str](#str) | None</code>) – Optional private phone number, hidden from ``repr``.
- [**first_name**](#miniproto.session.models.UserIdentity.first_name) (<code>[str](#str) | None</code>) – Optional profile first name.
- [**last_name**](#miniproto.session.models.UserIdentity.last_name) (<code>[str](#str) | None</code>) – Optional profile last name.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the user ID is not positive.

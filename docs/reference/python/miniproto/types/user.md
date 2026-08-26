---
title: "miniproto.types.User"
description: "Normalized Telegram user returned by peer and authorization helpers."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.types.User"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py#L32"
aliases: ["miniproto.User"]
module: "miniproto.types"
---

## `miniproto.types.User`

```python
User(id: int, access_hash: int | None = None, is_bot: bool = False, username: str | None = None, phone: str | None = None, first_name: str | None = None, last_name: str | None = None, is_self: bool = False, raw: object | None = None) -> None
```

Normalized Telegram user returned by peer and authorization helpers.

**Attributes:**

- [**id**](#miniproto.types.User.id) (<code>[int](#int)</code>) – Telegram user identifier.
- [**access_hash**](#miniproto.types.User.access_hash) (<code>[int](#int) | None</code>) – Optional hash used to address the user.
- [**is_bot**](#miniproto.types.User.is_bot) (<code>[bool](#bool)</code>) – Whether the account is a bot.
- [**username**](#miniproto.types.User.username) (<code>[str](#str) | None</code>) – Optional public username.
- [**phone**](#miniproto.types.User.phone) (<code>[str](#str) | None</code>) – Optional phone number supplied by Telegram.
- [**first_name**](#miniproto.types.User.first_name) (<code>[str](#str) | None</code>) – Optional first name.
- [**last_name**](#miniproto.types.User.last_name) (<code>[str](#str) | None</code>) – Optional last name.
- [**is_self**](#miniproto.types.User.is_self) (<code>[bool](#bool)</code>) – Whether this is the authorized account.
- [**raw**](#miniproto.types.User.raw) (<code>[object](#object) | None</code>) – Optional underlying TL object for low-level inspection.

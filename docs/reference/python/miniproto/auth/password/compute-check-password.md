---
title: "miniproto.auth.password.compute_check_password"
description: "Build the request payload required to verify an account password."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.password.compute_check_password"
source_path: "src/miniproto/auth/password.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/password.py#L13"
aliases: ["miniproto.auth.compute_check_password"]
module: "miniproto.auth.password"
---

## `miniproto.auth.password.compute_check_password`

```python
compute_check_password(password: str, password_state: types.AccountPassword) -> types.InputCheckPasswordEmpty | types.InputCheckPasswordSRP
```

Build the request payload required to verify an account password.

**Parameters:**

- **password** (<code>[str](#str)</code>) – Plain-text password supplied by the caller; it is only used to derive the proof.
- **password_state** (<code>[AccountPassword](#miniproto.raw.types.AccountPassword)</code>) – Current Telegram password configuration and SRP parameters.

**Returns:**

- <code>[InputCheckPasswordEmpty](#miniproto.raw.types.InputCheckPasswordEmpty) | [InputCheckPasswordSRP](#miniproto.raw.types.InputCheckPasswordSRP)</code> – An empty password check when no password is configured, otherwise a freshly randomized SRP proof.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If Telegram supplies unsupported, incomplete or cryptographically invalid SRP parameters.

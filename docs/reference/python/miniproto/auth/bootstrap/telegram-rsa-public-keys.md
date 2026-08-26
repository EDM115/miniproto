---
title: "miniproto.auth.bootstrap.telegram_rsa_public_keys"
description: "Return Telegram's trusted RSA public keys for the selected environment."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.bootstrap.telegram_rsa_public_keys"
source_path: "src/miniproto/auth/bootstrap.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/bootstrap.py#L171"
module: "miniproto.auth.bootstrap"
---

## `miniproto.auth.bootstrap.telegram_rsa_public_keys`

```python
telegram_rsa_public_keys(*, test_mode: bool) -> tuple[RSAKey, ...]
```

Return Telegram's trusted RSA public keys for the selected environment.

**Parameters:**

- **test_mode** (<code>[bool](#bool)</code>) – Select Telegram's test-server keys instead of production keys.

**Returns:**

- <code>[tuple](#tuple)[[RSAKey](#miniproto.auth.key_exchange.RSAKey), ...]</code> – Parsed public keys whose fingerprints may be advertised by Telegram.

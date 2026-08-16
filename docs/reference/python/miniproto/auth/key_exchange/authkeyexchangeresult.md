---
title: "miniproto.auth.key_exchange.AuthKeyExchangeResult"
description: "Authenticated MTProto key material and metadata produced by an exchange."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.AuthKeyExchangeResult"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L436"
aliases: ["miniproto.AuthKeyExchangeResult","miniproto.auth.AuthKeyExchangeResult"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.AuthKeyExchangeResult`

```python
AuthKeyExchangeResult(auth_key: bytes, auth_key_id: bytes, server_salt: int, time_offset: float, dc_id: int) -> None
```

Authenticated MTProto key material and metadata produced by an exchange.

``auth_key`` is deliberately omitted from the dataclass representation. Callers
must store it only in the configured protected session storage.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Newly derived 256-byte MTProto secret authorization key.
- **auth_key_id** (<code>[bytes](#bytes)</code>) – Protocol key identifier derived from ``auth_key``.
- **server_salt** (<code>[int](#int)</code>) – Initial MTProto server salt derived from exchange nonces.
- **time_offset** (<code>[float](#float)</code>) – Server time minus local wall-clock time, in seconds.
- **dc_id** (<code>[int](#int)</code>) – Logical Telegram data-center ID authorized by the key.

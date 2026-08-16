---
title: "miniproto.auth.key_exchange.AuthKeyExchange.create_auth_key"
description: "Execute one complete Telegram authorization-key exchange."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.AuthKeyExchange.create_auth_key"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L510"
aliases: ["miniproto.AuthKeyExchange.create_auth_key","miniproto.auth.AuthKeyExchange.create_auth_key"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.AuthKeyExchange.create_auth_key`

```python
create_auth_key() -> AuthKeyExchangeResult
```

Execute one complete Telegram authorization-key exchange.

The method validates nonces, trusted RSA fingerprint selection, encrypted
server DH data, the safe DH group, public values, and Telegram's final
``new_nonce_hash1`` confirmation before returning secret key material.

**Returns:**

- <code>[AuthKeyExchangeResult](#miniproto.auth.key_exchange.AuthKeyExchangeResult)</code> – The new MTProto authorization key, its key ID, server salt, time offset, and DC ID.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If any Telegram handshake proof, nonce, key, DH parameter, or final confirmation is invalid.
- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If a handshake payload has an unexpected constructor or malformed encoding.

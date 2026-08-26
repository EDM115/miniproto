---
title: "miniproto.auth.key_exchange.AuthKeyExchange"
description: "Perform Telegram's RSA- and DH-protected MTProto authorization handshake."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.AuthKeyExchange"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L470"
aliases: ["miniproto.AuthKeyExchange","miniproto.auth.AuthKeyExchange"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.AuthKeyExchange`

```python
AuthKeyExchange(transport: AuthKeyTransport, *, dc_id: int, rsa_keys: tuple[RSAKey, ...], test_mode: bool = False, random_bytes: Callable[[int], bytes] | None = None) -> None
```

Perform Telegram's RSA- and DH-protected MTProto authorization handshake.

**Parameters:**

- **transport** (<code>[AuthKeyTransport](#miniproto.auth.key_exchange.AuthKeyTransport)</code>) – Unencrypted transport connected to the selected data center.
- **dc_id** (<code>[int](#int)</code>) – Logical Telegram DC identifier to authorize.
- **rsa_keys** (<code>[tuple](#tuple)[[RSAKey](#miniproto.auth.key_exchange.RSAKey), ...]</code>) – Trusted Telegram RSA public keys for the selected environment.
- **test_mode** (<code>[bool](#bool)</code>) – Encode positive DC IDs for Telegram's test environment when true.
- **random_bytes** (<code>[Callable](#collections.abc.Callable)[[[int](#int)], [bytes](#bytes)] | None</code>) – Cryptographically secure random-byte source; defaults to :func:`os.urandom`.

Validate trusted keys and initialize exchange-specific dependencies.

**Parameters:**

- **transport** (<code>[AuthKeyTransport](#miniproto.auth.key_exchange.AuthKeyTransport)</code>) – Connected capability used to send unencrypted handshake requests.
- **dc_id** (<code>[int](#int)</code>) – Logical Telegram data-center ID to authorize.
- **rsa_keys** (<code>[tuple](#tuple)[[RSAKey](#miniproto.auth.key_exchange.RSAKey), ...]</code>) – Trusted public keys eligible for server fingerprint selection.
- **test_mode** (<code>[bool](#bool)</code>) – Encode positive DC IDs for Telegram's test environment when true.
- **random_bytes** (<code>[Callable](#collections.abc.Callable)[[[int](#int)], [bytes](#bytes)] | None</code>) – Optional secure random-byte source; defaults to :func:`os.urandom`.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If no trusted Telegram RSA key was supplied.

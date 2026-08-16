---
title: "miniproto.auth.key_exchange.select_rsa_key"
description: "Select the first server-offered fingerprint present in trusted ``keys``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.select_rsa_key"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L694"
aliases: ["miniproto.auth.select_rsa_key"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.select_rsa_key`

```python
select_rsa_key(fingerprints: tuple[int, ...], keys: tuple[RSAKey, ...]) -> RSAKey
```

Select the first server-offered fingerprint present in trusted ``keys``.

**Parameters:**

- **fingerprints** (<code>[tuple](#tuple)[[int](#int), ...]</code>) – Server-advertised RSA fingerprints in Telegram preference order.
- **keys** (<code>[tuple](#tuple)[[RSAKey](#miniproto.auth.key_exchange.RSAKey), ...]</code>) – Trusted Telegram RSA public keys available to this client.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If Telegram offers no trusted public-key fingerprint.

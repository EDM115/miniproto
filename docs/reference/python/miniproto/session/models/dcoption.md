---
title: "miniproto.session.models.DCOption"
description: "One validated Telegram data-centre endpoint and optional transport secret."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.models.DCOption"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L72"
aliases: ["miniproto.DCOption","miniproto.session.DCOption"]
module: "miniproto.session.models"
---

## `miniproto.session.models.DCOption`

```python
DCOption(id: int, ip_address: str, port: int, ipv6: bool = False, media_only: bool = False, cdn: bool = False, tcpo_only: bool = False, static: bool = False, secret: bytes | None = None) -> None
```

One validated Telegram data-centre endpoint and optional transport secret.

**Attributes:**

- [**id**](#miniproto.session.models.DCOption.id) (<code>[int](#int)</code>) – Positive data-centre identifier.
- [**ip_address**](#miniproto.session.models.DCOption.ip_address) (<code>[str](#str)</code>) – Non-empty endpoint address.
- [**port**](#miniproto.session.models.DCOption.port) (<code>[int](#int)</code>) – Endpoint TCP port from 1 through 65535.
- [**ipv6**](#miniproto.session.models.DCOption.ipv6) (<code>[bool](#bool)</code>) – Whether the address is IPv6.
- [**media_only**](#miniproto.session.models.DCOption.media_only) (<code>[bool](#bool)</code>) – Whether this endpoint serves only media requests.
- [**cdn**](#miniproto.session.models.DCOption.cdn) (<code>[bool](#bool)</code>) – Whether this endpoint belongs to Telegram's CDN trust domain.
- [**tcpo_only**](#miniproto.session.models.DCOption.tcpo_only) (<code>[bool](#bool)</code>) – Whether this endpoint is TCP-obfuscated-only.
- [**static**](#miniproto.session.models.DCOption.static) (<code>[bool](#bool)</code>) – Whether Telegram marks this option static.
- [**secret**](#miniproto.session.models.DCOption.secret) (<code>[bytes](#bytes) | None</code>) – Optional copied transport secret, hidden from ``repr``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the ID, address or port is invalid.

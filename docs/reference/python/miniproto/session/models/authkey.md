---
title: "miniproto.session.models.AuthKey"
description: "Validated non-empty MTProto authorization key bound to a positive DC."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.models.AuthKey"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L40"
aliases: ["miniproto.AuthKey","miniproto.session.AuthKey"]
module: "miniproto.session.models"
---

## `miniproto.session.models.AuthKey`

```python
AuthKey(dc_id: int, key: bytes, key_id: int | None = None, created_at: datetime = _utc_now(), expires_at: datetime | None = None) -> None
```

Validated non-empty MTProto authorization key bound to a positive DC.

**Attributes:**

- [**dc_id**](#miniproto.session.models.AuthKey.dc_id) (<code>[int](#int)</code>) – Positive data-centre identifier that owns the key.
- [**key**](#miniproto.session.models.AuthKey.key) (<code>[bytes](#bytes)</code>) – Secret authorization-key bytes, hidden from ``repr``.
- [**key_id**](#miniproto.session.models.AuthKey.key_id) (<code>[int](#int) | None</code>) – Optional server-derived authorization-key fingerprint.
- [**created_at**](#miniproto.session.models.AuthKey.created_at) (<code>[datetime](#datetime.datetime)</code>) – Creation timestamp; aware input retains its original timezone and naive input assumes UTC.
- [**expires_at**](#miniproto.session.models.AuthKey.expires_at) (<code>[datetime](#datetime.datetime) | None</code>) – Optional expiry timestamp with the same aware/naive handling.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``dc_id`` is not positive or ``key`` is empty.

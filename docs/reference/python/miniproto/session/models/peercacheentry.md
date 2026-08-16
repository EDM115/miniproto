---
title: "miniproto.session.models.PeerCacheEntry"
description: "Durable peer lookup metadata with a shallow-copied optional raw-field mapping."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.models.PeerCacheEntry"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L173"
aliases: ["miniproto.PeerCacheEntry","miniproto.session.PeerCacheEntry"]
module: "miniproto.session.models"
---

## `miniproto.session.models.PeerCacheEntry`

```python
PeerCacheEntry(id: int, kind: PeerKind, access_hash: int | None = None, username: str | None = None, phone: str | None = None, updated_at: datetime = _utc_now(), raw: Mapping[str, Any] | None = None) -> None
```

Durable peer lookup metadata with a shallow-copied optional raw-field mapping.

``raw`` is copied at its outer mapping level, so nested raw values remain
mutable. ``phone`` is hidden from ``repr`` and optional access hashes remain
absent for minimal Telegram peers.

**Attributes:**

- [**id**](#miniproto.session.models.PeerCacheEntry.id) (<code>[int](#int)</code>) – Positive Telegram peer identifier.
- [**kind**](#miniproto.session.models.PeerCacheEntry.kind) (<code>[PeerKind](#miniproto.types.PeerKind)</code>) – Peer category used to construct input peers.
- [**access_hash**](#miniproto.session.models.PeerCacheEntry.access_hash) (<code>[int](#int) | None</code>) – Optional access hash required for some peer operations.
- [**username**](#miniproto.session.models.PeerCacheEntry.username) (<code>[str](#str) | None</code>) – Optional public username.
- [**phone**](#miniproto.session.models.PeerCacheEntry.phone) (<code>[str](#str) | None</code>) – Optional private phone number, hidden from ``repr``.
- [**updated_at**](#miniproto.session.models.PeerCacheEntry.updated_at) (<code>[datetime](#datetime.datetime)</code>) – Last-known peer metadata timestamp; aware input retains its timezone.
- [**raw**](#miniproto.session.models.PeerCacheEntry.raw) (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional shallow-copied extra raw fields; nested values remain mutable.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the peer ID is not positive.

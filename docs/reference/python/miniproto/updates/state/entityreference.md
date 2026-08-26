---
title: "miniproto.updates.state.EntityReference"
description: "Persistent, normalized peer data learned while processing updates."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.updates.state.EntityReference"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L49"
aliases: ["miniproto.updates.EntityReference"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.EntityReference`

```python
EntityReference(id: int, kind: PeerKind, access_hash: int | None = None, username: str | None = None, phone: str | None = None, title: str | None = None, complete: bool = False, updated_at: datetime = utc_now()) -> None
```

Persistent, normalized peer data learned while processing updates.

**Attributes:**

- [**id**](#miniproto.updates.state.EntityReference.id) (<code>[int](#int)</code>) – Telegram peer identifier.
- [**kind**](#miniproto.updates.state.EntityReference.kind) (<code>[PeerKind](#miniproto.types.PeerKind)</code>) – Peer category used as part of the cache key.
- [**access_hash**](#miniproto.updates.state.EntityReference.access_hash) (<code>[int](#int) | None</code>) – Optional hash needed to construct an input peer or channel.
- [**username**](#miniproto.updates.state.EntityReference.username) (<code>[str](#str) | None</code>) – Optional username observed in update entities.
- [**phone**](#miniproto.updates.state.EntityReference.phone) (<code>[str](#str) | None</code>) – Optional phone number observed in a user entity.
- [**title**](#miniproto.updates.state.EntityReference.title) (<code>[str](#str) | None</code>) – Optional display title or user full name.
- [**complete**](#miniproto.updates.state.EntityReference.complete) (<code>[bool](#bool)</code>) – Whether the source was a full entity allowed to clear absent aliases.
- [**updated_at**](#miniproto.updates.state.EntityReference.updated_at) (<code>[datetime](#datetime.datetime)</code>) – Observation timestamp; aware input retains its timezone and naive input assumes UTC.

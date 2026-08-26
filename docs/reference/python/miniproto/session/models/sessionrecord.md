---
title: "miniproto.session.models.SessionRecord"
description: "Complete versioned session state with frozen, shallow collection snapshots."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.models.SessionRecord"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L213"
aliases: ["miniproto.SessionRecord","miniproto.session.SessionRecord"]
module: "miniproto.session.models"
---

## `miniproto.session.models.SessionRecord`

```python
SessionRecord(version: int = SESSION_RECORD_VERSION, dc_id: int | None = None, auth_key: AuthKey | None = None, dc_options: tuple[DCOption, ...] = (), user: UserIdentity | None = None, update_state: UpdateState = UpdateState(), peers: tuple[PeerCacheEntry, ...] = (), metadata: Mapping[str, Any] = dict()) -> None
```

Complete versioned session state with frozen, shallow collection snapshots.

**Attributes:**

- [**version**](#miniproto.session.models.SessionRecord.version) (<code>[int](#int)</code>) – Storage schema version; only the current version is accepted.
- [**dc_id**](#miniproto.session.models.SessionRecord.dc_id) (<code>[int](#int) | None</code>) – Optional active data-centre identifier.
- [**auth_key**](#miniproto.session.models.SessionRecord.auth_key) (<code>[AuthKey](#miniproto.session.models.AuthKey) | None</code>) – Optional active authorization key.
- [**dc_options**](#miniproto.session.models.SessionRecord.dc_options) (<code>[tuple](#tuple)[[DCOption](#miniproto.session.models.DCOption), ...]</code>) – Immutable configured endpoint sequence.
- [**user**](#miniproto.session.models.SessionRecord.user) (<code>[UserIdentity](#miniproto.session.models.UserIdentity) | None</code>) – Optional authenticated account identity.
- [**update_state**](#miniproto.session.models.SessionRecord.update_state) (<code>[UpdateState](#miniproto.session.models.UpdateState)</code>) – Update cursors, defaulting to an empty state.
- [**peers**](#miniproto.session.models.SessionRecord.peers) (<code>[tuple](#tuple)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry), ...]</code>) – Immutable cached peer sequence.
- [**metadata**](#miniproto.session.models.SessionRecord.metadata) (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)]</code>) – Shallow-copied extension mapping, hidden from ``repr``; nested values remain mutable.

Default update state is empty, while every other optional domain remains
absent or empty until the client obtains it.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the version is unsupported or configured DC is invalid.

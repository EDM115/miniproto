---
title: "miniproto.updates.state.UpdateCursor"
description: "Immutable global and per-channel update state persisted in a session record."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.updates.state.UpdateCursor"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L104"
aliases: ["miniproto.updates.UpdateCursor"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor`

```python
UpdateCursor(pts: int = 0, qts: int = 0, seq: int = 0, date: datetime = utc_now(), channel_cursors: tuple[ChannelUpdateCursor, ...] = (), entities: tuple[EntityReference, ...] = (), duplicate_keys: tuple[str, ...] = ()) -> None
```

Immutable global and per-channel update state persisted in a session record.

``duplicate_keys`` retains a bounded recent-history window for best-effort duplicate suppression. ``entities`` supplies access hashes needed for channel gap recovery.

**Attributes:**

- [**pts**](#miniproto.updates.state.UpdateCursor.pts) (<code>[int](#int)</code>) – Global persistent timestamp.
- [**qts**](#miniproto.updates.state.UpdateCursor.qts) (<code>[int](#int)</code>) – Secret-chat persistent timestamp.
- [**seq**](#miniproto.updates.state.UpdateCursor.seq) (<code>[int](#int)</code>) – Global sequence number.
- [**date**](#miniproto.updates.state.UpdateCursor.date) (<code>[datetime](#datetime.datetime)</code>) – Global-state timestamp; aware input retains its timezone and naive input assumes UTC.
- [**channel_cursors**](#miniproto.updates.state.UpdateCursor.channel_cursors) (<code>[tuple](#tuple)[[ChannelUpdateCursor](#miniproto.updates.state.ChannelUpdateCursor), ...]</code>) – Independent channel PTS states.
- [**entities**](#miniproto.updates.state.UpdateCursor.entities) (<code>[tuple](#tuple)[[EntityReference](#miniproto.updates.state.EntityReference), ...]</code>) – Peer references observed while processing updates.
- [**duplicate_keys**](#miniproto.updates.state.UpdateCursor.duplicate_keys) (<code>[tuple](#tuple)[[str](#str), ...]</code>) – Recent raw-update identity keys.

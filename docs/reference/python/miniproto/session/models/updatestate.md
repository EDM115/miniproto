---
title: "miniproto.session.models.UpdateState"
description: "Monotonic Telegram update cursors and their latest server timestamp."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.models.UpdateState"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L145"
aliases: ["miniproto.UpdateState","miniproto.session.UpdateState"]
module: "miniproto.session.models"
---

## `miniproto.session.models.UpdateState`

```python
UpdateState(pts: int = 0, qts: int = 0, seq: int = 0, date: datetime = _utc_now()) -> None
```

Monotonic Telegram update cursors and their latest server timestamp.

All counters default to zero, and ``date`` defaults to current UTC time.

**Attributes:**

- [**pts**](#miniproto.session.models.UpdateState.pts) (<code>[int](#int)</code>) – Global persistent timestamp cursor.
- [**qts**](#miniproto.session.models.UpdateState.qts) (<code>[int](#int)</code>) – Secret-chat timestamp cursor.
- [**seq**](#miniproto.session.models.UpdateState.seq) (<code>[int](#int)</code>) – Global update sequence cursor.
- [**date**](#miniproto.session.models.UpdateState.date) (<code>[datetime](#datetime.datetime)</code>) – Latest server timestamp; aware input retains its timezone and naive input assumes UTC.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If any counter is negative.

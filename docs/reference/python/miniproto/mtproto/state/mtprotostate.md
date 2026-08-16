---
title: "miniproto.mtproto.state.MTProtoState"
description: "Track one authorization key's MTProto session, timing, and acknowledgement state."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.state.MTProtoState"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L19"
aliases: ["miniproto.mtproto.MTProtoState"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState`

```python
MTProtoState(auth_key: bytes, server_salt: int = 0, session_id: int = (lambda: secrets.randbits(64))(), time_offset: float = 0.0, duplicate_window: int = 8192, _last_msg_id: int = 0, _content_related_count: int = 0, _seen_msg_ids: OrderedDict[int, None] = OrderedDict(), _pending_acks: OrderedDict[int, float] = OrderedDict(), _time_trusted: bool = False) -> None
```

Track one authorization key's MTProto session, timing, and acknowledgement state.

**Attributes:**

- [**auth_key**](#miniproto.mtproto.state.MTProtoState.auth_key) (<code>[bytes](#bytes)</code>) – Required 256-byte MTProto authorization key.
- [**server_salt**](#miniproto.mtproto.state.MTProtoState.server_salt) (<code>[int](#int)</code>) – Current masked 64-bit server salt, defaulting to ``0``.
- [**session_id**](#miniproto.mtproto.state.MTProtoState.session_id) (<code>[int](#int)</code>) – Current random 64-bit session ID.
- [**time_offset**](#miniproto.mtproto.state.MTProtoState.time_offset) (<code>[float](#float)</code>) – Server-time offset applied while allocating message IDs.
- [**duplicate_window**](#miniproto.mtproto.state.MTProtoState.duplicate_window) (<code>[int](#int)</code>) – Maximum retained incoming IDs, defaulting to ``8192``.
- [**_last_msg_id**](#miniproto.mtproto.state.MTProtoState._last_msg_id) (<code>[int](#int)</code>) – Last locally allocated message ID used to preserve monotonicity.
- [**_content_related_count**](#miniproto.mtproto.state.MTProtoState._content_related_count) (<code>[int](#int)</code>) – Count used to allocate content-related sequence numbers.
- [**_seen_msg_ids**](#miniproto.mtproto.state.MTProtoState._seen_msg_ids) (<code>[OrderedDict](#collections.OrderedDict)[[int](#int), None]</code>) – Retained incoming IDs used for duplicate and replay checks.
- [**_pending_acks**](#miniproto.mtproto.state.MTProtoState._pending_acks) (<code>[OrderedDict](#collections.OrderedDict)[[int](#int), [float](#float)]</code>) – Incoming content-related IDs awaiting acknowledgement.
- [**_time_trusted**](#miniproto.mtproto.state.MTProtoState._time_trusted) (<code>[bool](#bool)</code>) – Whether an accepted incoming ID has established server time.

---
title: "miniproto.invoke.build_sender_from_session"
description: "Build a sender for the session DC or -- with overrides -- a media DC."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.build_sender_from_session"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L477"
module: "miniproto.invoke"
---

## `miniproto.invoke.build_sender_from_session`

```python
build_sender_from_session(config: ClientConfig, storage: SessionStorage, factory: SenderFactory | None = None, *, fresh_session_id: bool = False, server_salt_override: int | None = None, on_salt_change: Callable[[int], None] | None = None, dc_id_override: int | None = None, auth_key_override: bytes | None = None, allow_media_only: bool = False, require_cdn: bool = False) -> RawSender
```

Build a sender for the session DC or -- with overrides -- a media DC.

``dc_id_override``/``auth_key_override`` support cross-DC media transfers:
the caller supplies a per-DC auth key (created via key exchange with the
target DC) without ever touching the main session's DC or key.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client transport, retry and default-DC configuration.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage containing authorization key and DC options.
- **factory** (<code>[SenderFactory](#miniproto.invoke.SenderFactory) | None</code>) – Optional synchronous or asynchronous sender factory, bypassing built-in construction.
- **fresh_session_id** (<code>[bool](#bool)</code>) – Compatibility flag; all built-in senders always receive a new random session ID.
- **server_salt_override** (<code>[int](#int) | None</code>) – Per-sender salt override, normally for temporary media sessions.
- **on_salt_change** (<code>[Callable](#collections.abc.Callable)[[[int](#int)], None] | None</code>) – Callback receiving a newer server salt discovered by the sender.
- **dc_id_override** (<code>[int](#int) | None</code>) – Target DC for a cross-DC sender.
- **auth_key_override** (<code>[bytes](#bytes) | None</code>) – Key for the target DC; never persists over the main session key.
- **allow_media_only** (<code>[bool](#bool)</code>) – Permit a media-only DC endpoint for a dedicated media sender.
- **require_cdn** (<code>[bool](#bool)</code>) – Require an endpoint explicitly marked as a CDN server.

**Returns:**

- <code>[RawSender](#miniproto.invoke.RawSender)</code> – The optional factory result or a configured :class:`MTProtoSender`.

**Raises:**

- <code>[AuthKeyNotFound](#miniproto.errors.AuthKeyNotFound)</code> – If the persisted session has no key and no override is supplied.
- <code>[InvalidDatacenter](#miniproto.errors.InvalidDatacenter)</code> – If no usable option is stored for the selected DC.

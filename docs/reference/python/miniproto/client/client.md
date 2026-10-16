---
title: "miniproto.client.Client"
description: "Async MTProto client for authorization, raw RPCs, messages, updates and media."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.client.Client"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L307"
aliases: ["miniproto.Client"]
module: "miniproto.client"
---

## `miniproto.client.Client`

```python
Client(config: ClientConfig, *, _updates_enabled: bool = True) -> None
```

Async MTProto client for authorization, raw RPCs, messages, updates and media.

``connect`` starts local update handling. RPCs create network senders on demand. ``disconnect`` closes the supplied or default session storage, so use a new client and an open storage instance for a later connection.

Initialize an unconnected client and its session, update and media coordinators.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Immutable client configuration and session-storage policy.
- **_updates_enabled** (<code>[bool](#bool)</code>) – Internal switch used by auxiliary download clients to avoid starting update handling.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If default SQLite storage is selected and ``MINIPROTO_SESSION_KEY`` is absent or contains fewer than 16 encoded bytes.

<details class="security" open markdown="1">
<summary>Security</summary>

If ``config.session_storage`` is omitted, the client prepares encrypted SQLite storage at ``config.session_path``. Protect configuration values, exported session strings and the storage key as credentials.

</details>

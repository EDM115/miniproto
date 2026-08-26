---
title: "miniproto.client.Client"
description: "Async client facade for MTProto operations."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.client.Client"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L271"
aliases: ["miniproto.Client"]
module: "miniproto.client"
---

## `miniproto.client.Client`

```python
Client(config: ClientConfig, *, _updates_enabled: bool = True) -> None
```

Async client facade for MTProto operations.

This implementation wires lifecycle, auth, raw invocation, updates, peer/message helpers and protocol-core media transfer primitives while keeping framework-level behavior out of the SDK.

Initialize an unconnected client and its session, update and media coordinators.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Immutable client configuration and session-storage policy.
- **_updates_enabled** (<code>[bool](#bool)</code>) – Internal switch used by auxiliary download clients to avoid starting update handling.

<details class="security" open markdown="1">
<summary>Security</summary>

If ``config.session_storage`` is omitted, the client creates encrypted SQLite storage at ``config.session_path``. The client neither logs nor exposes configured bearer secrets.

</details>

---
title: "miniproto.peers.PeerCache"
description: "Revision-aware session peer cache with local and remote resolution paths."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.peers.PeerCache"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L68"
module: "miniproto.peers"
---

## `miniproto.peers.PeerCache`

```python
PeerCache(config: ClientConfig, storage: SessionStorage, invoker: PeerInvoker) -> None
```

Revision-aware session peer cache with local and remote resolution paths.

Bind client configuration, mutable session storage and raw invocation.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client configuration whose DC identifies loaded session state.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage supplying durable auth and peer domains.
- **invoker** (<code>[PeerInvoker](#miniproto.peers.PeerInvoker)</code>) – Raw Telegram request callable for remote peer resolution.

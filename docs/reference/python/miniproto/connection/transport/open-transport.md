---
title: "miniproto.connection.transport.open_transport"
description: "Construct, connect, and return the transport matching ``config.mode``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.transport.open_transport"
source_path: "src/miniproto/connection/transport.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/transport.py#L334"
aliases: ["miniproto.connection.open_transport"]
module: "miniproto.connection.transport"
---

## `miniproto.connection.transport.open_transport`

```python
open_transport(endpoint: ConnectionEndpoint, config: TransportConfig, *, connector: StreamConnector | None = None) -> Transport
```

Construct, connect, and return the transport matching ``config.mode``.

**Parameters:**

- **endpoint** (<code>[ConnectionEndpoint](#miniproto.connection.transport.ConnectionEndpoint)</code>) – Remote MTProto destination.
- **config** (<code>[TransportConfig](#miniproto.config.TransportConfig)</code>) – Framing, timeout, proxy, and reconnection transport settings.
- **connector** (<code>[StreamConnector](#miniproto.connection.transport.StreamConnector) | None</code>) – Optional stream factory for custom networking or tests. It
defaults to :func:`default_stream_connector`.

**Returns:**

- <code>[Transport](#miniproto.connection.transport.Transport)</code> – A connected abridged, intermediate, or padded-intermediate transport.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``config.mode`` is not a supported transport mode.
- <code>[TransportTimeout](#miniproto.connection.transport.TransportTimeout)</code> – If connection setup exceeds its configured deadline.
- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If opening the stream or proxy tunnel fails.

---
title: "miniproto.connection.transport.ConnectionEndpoint"
description: "Validated TCP destination for an MTProto transport."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.transport.ConnectionEndpoint"
source_path: "src/miniproto/connection/transport.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/transport.py#L38"
aliases: ["miniproto.connection.ConnectionEndpoint"]
module: "miniproto.connection.transport"
---

## `miniproto.connection.transport.ConnectionEndpoint`

```python
ConnectionEndpoint(host: str, port: int) -> None
```

Validated TCP destination for an MTProto transport.

**Parameters:**

- **host** (<code>[str](#str)</code>) – DNS name or IP address to connect to; it must not be empty.
- **port** (<code>[int](#int)</code>) – TCP port in the inclusive range 1 through 65535.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If either endpoint component is invalid.

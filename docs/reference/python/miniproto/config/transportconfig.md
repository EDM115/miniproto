---
title: "miniproto.config.TransportConfig"
description: "Connection transport settings with validated timeouts and payload limits."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.config.TransportConfig"
source_path: "src/miniproto/config.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/config.py#L16"
aliases: ["miniproto.TransportConfig"]
module: "miniproto.config"
---

## `miniproto.config.TransportConfig`

```python
TransportConfig(mode: TransportMode = 'tcp_abridged', connect_timeout: float = 10.0, read_timeout: float = 30.0, write_timeout: float = 30.0, reconnect_backoff_initial: float = 0.25, reconnect_backoff_max: float = 5.0, max_payload_size: int = 16 * 1024 * 1024, proxy: str | None = None) -> None
```

Connection transport settings with validated timeouts and payload limits.

**Attributes:**

- [**mode**](#miniproto.config.TransportConfig.mode) (<code>[TransportMode](#miniproto.config.TransportMode)</code>) – TCP framing mode; defaults to ``"tcp_abridged"``.
- [**connect_timeout**](#miniproto.config.TransportConfig.connect_timeout) (<code>[float](#float)</code>) – Maximum seconds allowed to establish a connection.
- [**read_timeout**](#miniproto.config.TransportConfig.read_timeout) (<code>[float](#float)</code>) – Maximum seconds allowed for a transport read.
- [**write_timeout**](#miniproto.config.TransportConfig.write_timeout) (<code>[float](#float)</code>) – Maximum seconds allowed for a transport write.
- [**reconnect_backoff_initial**](#miniproto.config.TransportConfig.reconnect_backoff_initial) (<code>[float](#float)</code>) – Initial reconnect delay in seconds.
- [**reconnect_backoff_max**](#miniproto.config.TransportConfig.reconnect_backoff_max) (<code>[float](#float)</code>) – Maximum reconnect delay in seconds.
- [**max_payload_size**](#miniproto.config.TransportConfig.max_payload_size) (<code>[int](#int)</code>) – Largest accepted transport payload in bytes.
- [**proxy**](#miniproto.config.TransportConfig.proxy) (<code>[str](#str) | None</code>) – Optional proxy URL, omitted from representations to avoid exposing credentials.

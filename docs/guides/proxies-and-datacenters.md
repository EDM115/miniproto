---
title: Proxies and datacenters
description: Configure a transport proxy and understand primary versus media datacenter state.
slug: /guides/proxies-and-datacenters
generated: false
---

# Proxies and datacenters

Set a proxy on `TransportConfig` and pass that transport configuration into `ClientConfig`. The current transport accepts HTTP(S), SOCKS and SOCKS5 URLs, including optional user information when the selected scheme supports it.

```python
from miniproto import ClientConfig, TransportConfig


config = ClientConfig(
    api_id=12345, api_hash="provided-by-telegram", transport=TransportConfig(proxy="socks5://proxy.example.net:1080")
)
```

The URL is parsed while connection setup opens the proxy. A missing scheme or host, an unsupported scheme and a failed negotiation raise `TransportError`. Use a fully formed URL such as `socks5://host:1080` or `http://host:8080`. The `proxy` field is excluded from the transport configuration representation, but a proxy URL with credentials is still a credential: do not expose it in diagnostics, environment dumps or benchmark output. [Observability](./observability.md) describes the limits of automatic redaction.

`http://` and `https://` both open a plain TCP connection to the proxy and send the same HTTP CONNECT request. The `https://` scheme does not add TLS or authenticate the client-to-proxy hop. Use a route that protects that hop when the deployment requires it.

## Primary DC and media DCs have separate state

`ClientConfig.dc_id` defaults to `2`; `test_mode` defaults to `False`. The primary sender uses session state and DC options to establish the client connection. A primary RPC may handle an eligible datacenter migration by updating the main session state and retrying the request under its own migration rules.

Media lanes are deliberately separate. Cross-DC media uses per-DC authentication/import state and a file migration resolves the media pool for the indicated DC without moving the primary session's DC or authorization key. This separation prevents a media transfer from silently changing where ordinary RPCs are sent. It also means main-session migration behavior does not imply that a media lane will reuse main-session credentials or retry an arbitrary transfer identically.

For upload/download controls, CDN integrity behavior and resource schedulers, use [the media guide](../media.md). If a connection issue appears only through a proxy, first preserve the failure type and target DC in a redacted log, then reproduce with the smallest permitted configuration; avoid treating a proxy transport failure as proof that account authorization or session migration is wrong.

---
title: "miniproto.connection.transport.Transport"
description: "Asynchronous MTProto framed-byte transport contract."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.transport.Transport"
source_path: "src/miniproto/connection/transport.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/transport.py#L61"
aliases: ["miniproto.connection.Transport"]
module: "miniproto.connection.transport"
---

## `miniproto.connection.transport.Transport`

Bases: <code>[Protocol](#typing.Protocol)</code>

Asynchronous MTProto framed-byte transport contract.

Implementations are lifecycle-managed: callers connect before I/O and close
when finished. A received quick ACK is transport metadata, not an RPC reply.

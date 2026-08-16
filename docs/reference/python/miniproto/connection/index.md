---
title: "miniproto.connection"
description: "Public MTProto connection, sender, and transport primitives."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.connection"
source_path: "src/miniproto/connection/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/__init__.py"
module: "miniproto.connection"
---

## `miniproto.connection`

Public MTProto connection, sender, and transport primitives.

## Public objects

- [`MTProtoSender`](./sender/mtprotosender/) — Manage a concurrent encrypted MTProto session over a reconnecting transport.
- [`PendingRequest`](./sender/pendingrequest/) — Internal state retained for one unresolved request and its resend aliases.
- [`QuickAckReceipt`](./sender/quickackreceipt/) — Early transport-acknowledgement metadata for one encrypted send attempt.
- [`SenderState`](./sender/senderstate/) — Snapshot of sender liveness and pending RPC capacity.
- [`ConnectionEndpoint`](./transport/connectionendpoint/) — Validated TCP destination for an MTProto transport.
- [`StreamConnector`](./transport/streamconnector/) — Public attribute `miniproto.connection.transport.StreamConnector`.
- [`Transport`](./transport/transport/) — Asynchronous MTProto framed-byte transport contract.
- [`TransportClosed`](./transport/transportclosed/) — Raised when a transport operation is attempted on a closed connection.
- [`TransportError`](./transport/transporterror/) — Raised when an MTProto transport cannot complete an operation.
- [`TransportTimeout`](./transport/transporttimeout/) — Raised when a transport read or write exceeds its configured deadline.
- [`open_transport`](./transport/open-transport/) — Construct, connect, and return the transport matching ``config.mode``.

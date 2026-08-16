---
title: "miniproto.errors"
description: "Redaction-safe public exceptions and Telegram RPC error classification."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.errors"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py"
module: "miniproto.errors"
---

## `miniproto.errors`

Redaction-safe public exceptions and Telegram RPC error classification.

## Public objects

- [`MiniprotoError`](./miniprotoerror/) — Base exception for all library-defined failures.
- [`ProtocolValidationError`](./protocolvalidationerror/) — An authenticated MTProto message violated the inbound protocol contract.
- [`AmbiguousRpcResult`](./ambiguousrpcresult/) — The transport failed after an RPC may already have reached Telegram.
- [`RpcError`](./rpcerror/) — Raw or classified Telegram RPC failure with redaction-safe diagnostics.
- [`InvokeError`](./invokeerror/) — Base exception for raw invocation failures before Telegram returns a typed RPC error.
- [`ClientDisconnected`](./clientdisconnected/) — Raised when invocation cannot continue because the client disconnected.
- [`RequestTimeout`](./requesttimeout/) — Raised when the client-side request deadline expires.
- [`ResultTypeMismatch`](./resulttypemismatch/) — Raised when an RPC result does not match the requested result contract.
- [`BadRequest`](./badrequest/) — Classified client-side Telegram RPC error, normally status code 400.
- [`Unauthorized`](./unauthorized/) — Classified Telegram authorization failure with status code 401.
- [`Forbidden`](./forbidden/) — Classified Telegram permission failure with status code 403.
- [`NotFound`](./notfound/) — Classified Telegram missing-resource failure with status code 404.
- [`RpcTimeout`](./rpctimeout/) — Classified Telegram-side or transport RPC timeout, commonly code -503.
- [`InternalServerError`](./internalservererror/) — Classified retryable server failure, normally a 5xx RPC code.
- [`FloodWait`](./floodwait/) — Telegram pacing failure that exposes the required wait duration in seconds.
- [`AuthError`](./autherror/) — Base exception for authentication and authorization flow failures.
- [`InvalidCode`](./invalidcode/) — Authentication flow failure for a missing, expired, or invalid phone code.
- [`PasswordRequired`](./passwordrequired/) — Authentication flow requires a configured two-factor password.
- [`PasswordInvalid`](./passwordinvalid/) — Authentication flow received an invalid two-factor password.
- [`SignUpRequired`](./signuprequired/) — Authentication flow requires creating a Telegram account first.
- [`AuthKeyNotFound`](./authkeynotfound/) — Authentication key is invalid, unregistered, or no longer available.
- [`AuthKeyRegenerationRequired`](./authkeyregenerationrequired/) — Authentication key is duplicated or unsynchronized and must be replaced.
- [`InvalidDatacenter`](./invaliddatacenter/) — Telegram rejects the current data centre, commonly before a migration hint.
- [`DatacenterMigration`](./datacentermigration/) — Telegram directs the request to ``dc_id`` for a named migration kind.
- [`TransportFlood`](./transportflood/) — Raised for transport-level 429 responses, not ordinary RPC flood waits.
- [`PendingRpcLimitExceeded`](./pendingrpclimitexceeded/) — Raised when a sender has too many in-flight RPCs and cannot accept more.
- [`SessionStorageError`](./sessionstorageerror/) — Raised when session persistence cannot safely continue.
- [`SessionEnvelopeError`](./sessionenvelopeerror/) — Raised when an encrypted session envelope fails validation or authentication.
- [`classify_rpc_error`](./classify-rpc-error/) — Return the most specific public error matching a raw Telegram RPC error.

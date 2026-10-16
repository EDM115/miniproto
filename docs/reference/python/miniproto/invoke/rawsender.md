---
title: "miniproto.invoke.RawSender"
description: "Minimal connected sender capability required by the RPC invocation layer."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.invoke.RawSender"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L91"
module: "miniproto.invoke"
---

## `miniproto.invoke.RawSender`

Bases: <code>[Protocol](#typing.Protocol)</code>

Minimal connected sender capability required by the RPC invocation layer.

Credential invalidation additionally requires ``auth_key_dc_id`` and ``state.auth_key`` provenance. Custom senders without these optional attributes are disconnected on invalid-key errors without mutating stored credentials.

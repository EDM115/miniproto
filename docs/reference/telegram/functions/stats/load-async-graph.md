---
title: "stats.loadAsyncGraph"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "stats.loadAsyncGraph"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stats"
schema_source: "tdlib"
constructor_id: "0x621d5fa0"
---

# `stats.loadAsyncGraph`

No description provided by the pinned schema.

## Signature

```tl
stats.loadAsyncGraph#621d5fa0 flags:# token:string x:flags.0?long = StatsGraph;
```

## Result type

`StatsGraph`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| token | string | — | — | No description provided by the pinned schema. |
| x | flags.0?long | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| x | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import StatsLoadAsyncGraph
```

Public access: `miniproto.raw.functions.StatsLoadAsyncGraph`.

## Safe usage shape

```python
from miniproto.raw.functions import StatsLoadAsyncGraph

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = StatsLoadAsyncGraph
```

## Result family

[`StatsGraph`](/reference/telegram/types/results/stats-graph/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`GRAPH_EXPIRED_RELOAD`](/reference/telegram/errors/graph-expired-reload/) | This graph has expired, please obtain a new graph token. |
| 400 | [`GRAPH_INVALID_RELOAD`](/reference/telegram/errors/graph-invalid-reload/) | Invalid graph token provided, please reload the stats and provide the updated token. |
| 400 | [`GRAPH_OUTDATED_RELOAD`](/reference/telegram/errors/graph-outdated-reload/) | The graph is outdated, please get a new async token using stats.getBroadcastStats. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`StatsGraph`](/reference/telegram/types/results/stats-graph/)
Known selected constructors: [`statsGraph`](/reference/telegram/types/base/stats-graph/), [`statsGraphAsync`](/reference/telegram/types/base/stats-graph-async/), [`statsGraphError`](/reference/telegram/types/base/stats-graph-error/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret

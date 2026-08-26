---
title: "premium.getMyBoosts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "premium.getMyBoosts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "premium"
schema_source: "tdlib"
constructor_id: "0x0be77b4a"
---

# `premium.getMyBoosts`

No description provided by the pinned schema.

## Signature

```tl
premium.getMyBoosts#0be77b4a = premium.MyBoosts;
```

## Result type

`premium.MyBoosts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import PremiumGetMyBoosts
```

Public access: `miniproto.raw.functions.PremiumGetMyBoosts`.

## Safe usage shape

```python
from miniproto.raw.functions import PremiumGetMyBoosts

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PremiumGetMyBoosts
```

## Result family

[`premium.MyBoosts`](/reference/telegram/types/results/premium-my-boosts/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`premium.MyBoosts`](/reference/telegram/types/results/premium-my-boosts/)
Known selected constructors: [`premium.myBoosts`](/reference/telegram/types/premium/my-boosts/)

## Related methods

[`premium.applyBoost`](/reference/telegram/functions/premium/apply-boost/)

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

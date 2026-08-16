---
title: "inputPasskeyResponseLogin"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPasskeyResponseLogin"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc31fc14a"
---

# `inputPasskeyResponseLogin`

No description provided by the pinned schema.

## Signature

```tl
inputPasskeyResponseLogin#c31fc14a client_data:DataJSON authenticator_data:bytes signature:bytes user_handle:string = InputPasskeyResponse;
```

## Result type

`InputPasskeyResponse`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| client_data | DataJSON | — | — | No description provided by the pinned schema. |
| authenticator_data | bytes | — | — | No description provided by the pinned schema. |
| signature | bytes | — | — | No description provided by the pinned schema. |
| user_handle | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputPasskeyResponseLogin
```

Public access: `miniproto.raw.types.InputPasskeyResponseLogin`.

## Safe usage shape

```python
from miniproto.raw.types import InputPasskeyResponseLogin

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPasskeyResponseLogin
```

## Result family

[`InputPasskeyResponse`](/reference/telegram/types/results/input-passkey-response/)

## Relationships

- Result family: [`InputPasskeyResponse`](/reference/telegram/types/results/input-passkey-response/)
- Related constructors: [`inputPasskeyResponseRegister`](/reference/telegram/types/base/input-passkey-response-register/)
- Accepted by: [`inputPasskeyCredentialPublicKey`](/reference/telegram/types/base/input-passkey-credential-public-key/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery

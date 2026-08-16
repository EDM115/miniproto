---
title: "help.userInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.userInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x01eb3758"
---

# `help.userInfo`

No description provided by the pinned schema.

## Signature

```tl
help.userInfo#01eb3758 message:string entities:Vector<MessageEntity> author:string date:int = help.UserInfo;
```

## Result type

`help.UserInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| message | string | — | — | No description provided by the pinned schema. |
| entities | Vector<MessageEntity> | — | — | No description provided by the pinned schema. |
| author | string | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import HelpUserInfo
```

Public access: `miniproto.raw.types.HelpUserInfo`.

## Safe usage shape

```python
from miniproto.raw.types import HelpUserInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpUserInfo
```

## Result family

[`help.UserInfo`](/reference/telegram/types/results/help-user-info/)

## Relationships

- Result family: [`help.UserInfo`](/reference/telegram/types/results/help-user-info/)
- Related constructors: [`help.userInfoEmpty`](/reference/telegram/types/help/user-info-empty/)
- Returned by: [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`help.getUserInfo`](/reference/telegram/functions/help/get-user-info/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery

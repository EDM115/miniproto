---
title: "help.userInfoEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.userInfoEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0xf3ae2eed"
---

# `help.userInfoEmpty`

No description provided by the pinned schema.

## Signature

```tl
help.userInfoEmpty#f3ae2eed = help.UserInfo;
```

## Result type

`help.UserInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import HelpUserInfoEmpty
```

Public access: `miniproto.raw.types.HelpUserInfoEmpty`.

## Class reference

```python
from miniproto.raw.types import HelpUserInfoEmpty

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = HelpUserInfoEmpty
```

## Result family

[`help.UserInfo`](/reference/telegram/types/results/help-user-info/)

## Relationships

- Result family: [`help.UserInfo`](/reference/telegram/types/results/help-user-info/)
- Related constructors: [`help.userInfo`](/reference/telegram/types/help/user-info/)
- Returned by: [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`help.getUserInfo`](/reference/telegram/functions/help/get-user-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret

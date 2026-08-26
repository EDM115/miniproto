---
title: "globalPrivacySettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "globalPrivacySettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xfe41b34f"
---

# `globalPrivacySettings`

No description provided by the pinned schema.

## Signature

```tl
globalPrivacySettings#fe41b34f flags:# archive_and_mute_new_noncontact_peers:flags.0?true keep_archived_unmuted:flags.1?true keep_archived_folders:flags.2?true hide_read_marks:flags.3?true new_noncontact_peers_require_premium:flags.4?true display_gifts_button:flags.7?true noncontact_peers_paid_stars:flags.5?long disallowed_gifts:flags.6?DisallowedGiftsSettings = GlobalPrivacySettings;
```

## Result type

`GlobalPrivacySettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| archive_and_mute_new_noncontact_peers | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| keep_archived_unmuted | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| keep_archived_folders | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| hide_read_marks | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| new_noncontact_peers_require_premium | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| display_gifts_button | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| noncontact_peers_paid_stars | flags.5?long | flags.5 | — | No description provided by the pinned schema. |
| disallowed_gifts | flags.6?DisallowedGiftsSettings | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| archive_and_mute_new_noncontact_peers | 0 | Controlled by `flags`; present when this bit is set. |
| keep_archived_unmuted | 1 | Controlled by `flags`; present when this bit is set. |
| keep_archived_folders | 2 | Controlled by `flags`; present when this bit is set. |
| hide_read_marks | 3 | Controlled by `flags`; present when this bit is set. |
| new_noncontact_peers_require_premium | 4 | Controlled by `flags`; present when this bit is set. |
| display_gifts_button | 7 | Controlled by `flags`; present when this bit is set. |
| noncontact_peers_paid_stars | 5 | Controlled by `flags`; present when this bit is set. |
| disallowed_gifts | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GlobalPrivacySettings
```

Public access: `miniproto.raw.types.GlobalPrivacySettings`.

## Safe usage shape

```python
from miniproto.raw.types import GlobalPrivacySettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GlobalPrivacySettings
```

## Result family

[`GlobalPrivacySettings`](/reference/telegram/types/results/global-privacy-settings/)

## Relationships

- Result family: [`GlobalPrivacySettings`](/reference/telegram/types/results/global-privacy-settings/)
- Accepted by: [`account.setGlobalPrivacySettings`](/reference/telegram/functions/account/set-global-privacy-settings/)
- Returned by: [`account.getGlobalPrivacySettings`](/reference/telegram/functions/account/get-global-privacy-settings/), [`account.setGlobalPrivacySettings`](/reference/telegram/functions/account/set-global-privacy-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret

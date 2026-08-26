---
title: "USER_DISALLOWED_STARGIFTS"
description: "The recipient user has configured restrictions on which categories of star gifts they're willing to accept (unique, limited, or unlimited): the sender attempted to get a payment form for a gift that falls into a category the recipient has blocked."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:USER_DISALLOWED_STARGIFTS"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `USER_DISALLOWED_STARGIFTS`

The recipient user has configured restrictions on which categories of star gifts they're willing to accept (unique, limited, or unlimited): the sender attempted to get a payment form for a gift that falls into a category the recipient has blocked.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/)

## Python error class

```python
from miniproto.errors import UserDisallowedStargifts
```

Public access: `miniproto.errors.UserDisallowedStargifts`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret

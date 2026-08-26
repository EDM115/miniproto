---
title: MTProto and the Bot API
description: Why miniproto is an MTProto SDK, not a Bot API wrapper or application framework.
slug: /concepts/mtproto-and-bot-api/
generated: false
---

## Two Telegram interfaces, different responsibilities

Telegram's Bot API is a service-oriented HTTP interface for bots. MTProto is Telegram's lower-level client protocol: it includes authorization, data centres, encrypted envelopes, raw TL constructors and methods, updates and media-transfer details. `miniproto` implements the latter boundary.

That boundary lets one SDK support user authorization and bot authorization, generated raw methods and protocol-level concerns such as session state and DC migration. It does not make `miniproto` a drop-in Bot API client, hide Telegram's account rules or provide the routing, command, middleware, plugin and conversation abstractions normally expected from an application framework. Those belong to the separate future `mpgram` layer.

## What an MTProto client must own

An application using `miniproto` supplies its Telegram application credentials, selects session storage, owns the client lifecycle and chooses when to invoke methods. The SDK then coordinates raw requests, encrypted transport, persistent state, update recovery and selected convenience helpers such as sending messages or transferring media.

Using a raw method is not an entitlement to use it. Telegram controls server-side authorization, rate limits, feature availability and API evolution. Applications remain responsible for Telegram's Terms of Service, API rules, user consent, data handling and the consequences of operating user or bot credentials. Do not use this SDK to evade rate limits, account restrictions or Telegram policy.

## Choosing the right layer

Choose the Bot API when its HTTP bot model and feature set fit the product. Choose `miniproto` when an application needs an MTProto client boundary, generated raw API access, user-account flows or protocol/media behavior the Bot API does not model. Choose a framework layer when the application needs routing and business logic rather than a protocol SDK.

This distinction is especially important during the Alpha period: MTProto access increases operational responsibility, while public API and compatibility details may still change before a stable release.

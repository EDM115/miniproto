---
title: Schema sources and Layer 228
description: The canonical-source, documentation, drift, and generation policy for miniproto's Telegram raw API.
slug: /concepts/schema-layers/
generated: false
---

## Layer 228 is a pinned compatibility snapshot

The current generated raw API is pinned to Telegram Layer 228. A layer is not merely a display number: constructors, method signatures, flags, result types, and IDs must agree as one coherent snapshot. Generated code and reference pages therefore derive from checked-in schema inputs rather than a runtime download.

## Source roles are intentionally different

TDLib's pinned `telegram_api.tl` is the canonical structural source. It decides declarations, constructor IDs, parameter types, flags, and result types. Telegram Desktop supplies the layer only after an exact comparison of shared declarations and a validated end-of-file layer marker. Core Telegram JSON and schema inputs enrich available prose, while the pinned core RPC-error database supplies error mappings; neither is allowed to overwrite TDLib structure.

The documentation precedence is TDLib, then Telegram Desktop, then core JSON. Missing prose stays missing rather than being invented. Source metadata and the source-diff report record the pins, hashes, comparison counts, and structural differences for review.

## Updating safely

Schema update is a deliberate maintenance workflow, not an automatic production behavior. It validates the upstream inputs in memory and stages independent pins; generation then rebuilds lazy raw facades, stubs, registries, shards, errors, metadata, and raw-API documentation from the normalized canonical model. A routine pull request uses offline regeneration checks so temporary upstream availability cannot make deterministic CI flaky.

Reject an update when a shared TDLib/Desktop declaration differs structurally, the Desktop layer marker is missing or ambiguous, IDs collide incompatibly, or parsing encounters an unexplained declaration. Review the source-diff and metadata files with the generated diff; a newer timestamp alone is not evidence of a safe layer change.

## Compatibility consequences

Layer changes are API changes. A constructor can disappear, a field can be added, and a generated import can move or be removed. For example, the current canonical snapshot intentionally omits Telegram Desktop's `null`, so the earlier generated `miniproto.raw.types.Null` class is not part of Layer 228. Treat this Alpha raw surface as versioned generated API, not an indefinitely stable compatibility layer.

---
title: API Reference
description: Searchable Python, Rust and Telegram API documentation generated from the maintained source and pinned schemas.
slug: /reference/
generated: false
---

The reference is generated from three independently verified source surfaces and committed so changes remain reviewable. Use the language and kind filters in search to move between public Python APIs, native Rust internals exposed through the extension boundary and the pinned Telegram layer.

## Reference families

- [Python API](./reference/python/miniproto/index.md) documents maintained modules, classes, methods, functions, attributes and type aliases from static Griffe analysis. Explicitly exported aliases point back to their canonical pages.
- [Rust API](./reference/rust/miniproto-native/index.md) documents the maintained native crate from nightly rustdoc JSON and `cargo-docs-md`, including PyO3 binding names where applicable.
- [Telegram raw API](./reference/telegram/index.md) documents generated functions, types, RPC errors, result families and constructor relationships from the pinned layer inputs without importing generated Python modules.

## Reading generated pages

Every generated page identifies its language, reference kind, qualified name and source provenance in frontmatter and searchable metadata. Python and Rust parameter descriptions come from maintained docstrings or doc comments. Telegram parameter and result descriptions come from the pinned schema and project-owned relationship manifest; they do not invent behavioral guarantees absent from Telegram's definitions.

The checked-in [reference manifest](https://github.com/EDM115/miniproto/blob/master/docs/reference/manifest.json) records page counts, routes, source paths and content hashes. Run `miniproto-docs --check` to prove the committed reference still matches the source and pinned toolchain.

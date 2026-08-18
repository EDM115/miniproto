---
title: MTProto, without the framework tax.
description: miniproto is a fast, async-first Telegram MTProto client core for Python with explicit lifecycle, secure sessions, generated Layer 228 bindings, and bundled Rust acceleration.
slug: /
template: splash
generated: false
hero:
  title: MTProto, without the framework tax.
  tagline: A compact, async-first Telegram client core with explicit state, generated Layer 228 bindings, secure sessions, and bundled Rust acceleration where measurements justify it.
  actions:
    - text: Five-minute quickstart
      link: ./start/quickstart/
      variant: primary
    - text: Browse the raw API
      link: ./reference/telegram/functions/
      variant: secondary
---

## One protocol core. Three source languages.

`miniproto` turns Python intent into Telegram MTProto traffic through a deliberately small boundary: Python owns the public async API and policy, the pinned Telegram schema owns raw request and result shapes, and Rust accelerates measured hot paths without becoming a correctness requirement.

<div class="mp-mechanism" role="list" aria-label="miniproto architecture">
  <article role="listitem"><span>01</span><strong>Python intent</strong><p>Lifecycle, authorization, peers, updates, messages, media, sessions, retries, and typed errors remain inspectable Python APIs.</p></article>
  <article role="listitem"><span>02</span><strong>Layer 228 schema</strong><p>Generated constructors expose Telegram's complete raw surface, with source metadata and cross-linked result and error relationships.</p></article>
  <article role="listitem"><span>03</span><strong>Measured Rust paths</strong><p>Transport framing, cryptography, and hot TL constructors select native paths when available and verified, then fall back explicitly.</p></article>
</div>

## Start from a secure default

```python
import asyncio
import os

from miniproto import Client, ClientConfig, InMemorySessionStorage
from miniproto.raw import functions


async def main() -> None:
    config = ClientConfig(
        api_id=int(os.environ["MINIPROTO_API_ID"]),
        api_hash=os.environ["MINIPROTO_API_HASH"],
        session_storage=InMemorySessionStorage(),
    )
    async with Client(config) as client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        me = await client.get_me()
        telegram_config = await client.invoke(functions.HelpGetConfig())
        print(me.id, telegram_config.this_dc)


asyncio.run(main())
```

Credentials stay outside source control. This introductory call uses explicit in-memory storage, so it does not retain the bot authorization after shutdown. Durable sessions use encrypted SQLite storage and require a constructor key or `MINIPROTO_SESSION_KEY`; the quickstart walks through that boundary before the first persistent authorization.

<div class="mp-value-grid">
  <article><strong>Explicit by design</strong><p>Connection ownership, replay safety, flood waits, datacenter migration, update recovery, media scheduling, and cancellation behavior are documented as contracts rather than hidden behind a framework.</p></article>
  <article><strong>Fast paths with fallbacks</strong><p>Native acceleration is capability-checked and benchmarked. The Python surface remains available when a native symbol or wheel is unavailable.</p></article>
  <article><strong>Reference you can search</strong><p>Handwritten guides and generated Python, Telegram, and Rust pages share one local Pagefind index with language, kind, module, namespace, layer, and visibility facets.</p></article>
  <article><strong>A narrow package boundary</strong><p>`miniproto` is the protocol SDK. Routers, filters, middleware, plugins, commands, and broad application-framework ergonomics belong to the future `mpgram` package.</p></article>
</div>

## Choose your route

<div class="mp-journeys">
  <a href="./start/"><strong>Evaluate the SDK</strong><span>See the supported platforms, package boundary, and first authorization flow.</span></a>
  <a href="./start/high-level-operation/"><strong>Build with high-level operations</strong><span>Send messages, resolve peers, consume updates, and transfer media.</span></a>
  <a href="./concepts/raw-api/"><strong>Own the raw protocol</strong><span>Invoke generated Telegram requests and understand their result and error relationships.</span></a>
  <a href="./guides/session-security/"><strong>Operate it safely</strong><span>Learn session protection, retry boundaries, observability, deployment, and deterministic testing.</span></a>
</div>

## Complete reference, committed with the code

The generated Markdown is reviewed and versioned with the source. The website build needs Node.js, Python, and a pinned Rust nightly, but the deployed output is plain static HTML, CSS, JavaScript, and a self-hosted search index.

<div class="mp-reference-links">
  <a href="./reference/python/miniproto/"><strong>Python reference</strong><span>Public modules, classes, methods, parameters, aliases, and source links extracted statically with Griffe.</span></a>
  <a href="./reference/telegram/"><strong>Telegram reference</strong><span>Every Layer 228 function, type, constructor, parameter, known RPC error, and Python-visible import path.</span></a>
  <a href="./reference/rust/miniproto-native/"><strong>Rust reference</strong><span>Public and PyO3-facing items normalized from pinned-nightly rustdoc JSON and cargo-docs-md.</span></a>
</div>

<style>
  .mp-mechanism, .mp-value-grid, .mp-journeys, .mp-reference-links { display: grid; gap: 1rem; }
  .mp-mechanism { grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 2rem 0 4rem; }
  .mp-mechanism article { min-height: 14rem; padding: 1.35rem; overflow: hidden; border: 1px solid var(--mp-seam-strong); border-radius: 1rem; background: var(--mp-surface-raised); }
  .mp-mechanism span { display: block; margin-bottom: 2.8rem; color: var(--mp-lime); font-family: var(--__sl-font-mono); font-size: 0.75rem; font-weight: 700; }
  .mp-mechanism strong { display: block; color: var(--sl-color-white); font-family: var(--mp-display-font); font-size: 1.2rem; }
  .mp-mechanism p { margin: 0.8rem 0 0; color: var(--mp-text-soft); line-height: 1.65; }
  .mp-value-grid, .mp-journeys, .mp-reference-links { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-block: 2rem 4rem; }
  .mp-value-grid article, .mp-journeys a, .mp-reference-links a { display: block; padding: 1.3rem; border: 1px solid var(--mp-seam-strong); border-radius: 0.9rem; background: var(--mp-surface-raised); text-decoration: none; }
  .mp-value-grid strong, .mp-journeys strong, .mp-reference-links strong { display: block; color: var(--sl-color-white); font-family: var(--mp-display-font); font-size: 1.05rem; }
  .mp-value-grid p, .mp-journeys span, .mp-reference-links span { display: block; margin: 0.65rem 0 0; color: var(--mp-text-soft); line-height: 1.55; }
  .mp-journeys a:hover, .mp-reference-links a:hover { border-color: var(--mp-lime); }
  @media (max-width: 52rem) {
    .mp-mechanism, .mp-value-grid, .mp-journeys, .mp-reference-links { grid-template-columns: 1fr; }
    .mp-mechanism article { min-height: auto; }
    .mp-mechanism span { margin-bottom: 1.4rem; }
  }
</style>

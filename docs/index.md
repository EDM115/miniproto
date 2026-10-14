---
title: A Python client core for Telegram MTProto
description: miniproto is an async-first Telegram MTProto client core for Python with explicit lifecycle, encrypted sessions, generated Layer 230 bindings and bundled Rust acceleration.
slug: /
template: splash
generated: false
hero:
  title: A Python client core for Telegram MTProto
  tagline: A compact, async-first Telegram client core with explicit state, generated Layer 230 bindings, encrypted sessions and bundled Rust acceleration where measurements justify it.
  actions:
    - text: Five-minute quickstart
      link: ./start/quickstart/
      variant: primary
    - text: Browse the raw API
      link: ./reference/telegram/functions/
      variant: secondary
---

## Python API, Telegram schema and Rust acceleration

`miniproto` exposes an async Python API for Telegram MTProto. Python handles the client API and request policy, the pinned Telegram schema defines raw requests and results, and Rust accelerates selected hot paths without being required for correctness.

<div class="mp-mechanism" role="list" aria-label="miniproto architecture">
  <article role="listitem"><span>01</span><strong>Python API</strong><p>Python APIs cover lifecycle, authorization, peers, updates, messages, media, sessions, retries and typed errors.</p></article>
  <article role="listitem"><span>02</span><strong>Layer 230 schema</strong><p>Generated classes expose the pinned Telegram functions and constructors, with source metadata and links to related results and errors.</p></article>
  <article role="listitem"><span>03</span><strong>Rust acceleration</strong><p>Transport framing, cryptography and selected TL constructors use native implementations when their capabilities are available, with supported Python fallbacks.</p></article>
</div>

## Start with an in-memory session

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

Keep credentials outside source control. This call uses in-memory storage and does not save bot authorization after shutdown. Encrypted SQLite sessions require a constructor key or `MINIPROTO_SESSION_KEY`. The quickstart explains this before the first persistent authorization.

<div class="mp-value-grid">
  <article><strong>Lifecycle and safety</strong><p>Guides explain connection ownership, retry safety, flood waits, datacenter migration, update recovery, media scheduling and cancellation.</p></article>
  <article><strong>Native acceleration</strong><p>Native capabilities are checked and benchmarked. Supported Python fallbacks remain available when a native symbol or wheel is unavailable.</p></article>
  <article><strong>Reference you can search</strong><p>Handwritten guides and generated Python, Telegram and Rust pages share one local Pagefind index with language, kind, module, namespace, layer and visibility facets.</p></article>
  <article><strong>Protocol SDK</strong><p>`miniproto` handles Telegram's protocol. The planned `mpgram` package adds routers, filters, middleware, plugins, commands and application-level helpers.</p></article>
</div>

## Choose your route

<div class="mp-journeys">
  <a href="./start/"><strong>Evaluate the SDK</strong><span>See the supported platforms, package roles and first authorization flow.</span></a>
  <a href="./start/high-level-operation/"><strong>Build with high-level operations</strong><span>Send messages, resolve peers, consume updates and transfer media.</span></a>
  <a href="./concepts/raw-api/"><strong>Own the raw protocol</strong><span>Invoke generated Telegram requests and understand their result and error relationships.</span></a>
  <a href="./guides/session-security/"><strong>Operate it safely</strong><span>Learn session protection, retry boundaries, observability, deployment and deterministic testing.</span></a>
</div>

## Complete reference, committed with the code

The generated Markdown is versioned with the source. The documentation workflow uses Node.js, Python and Rust nightly to check the references and build the site. The deployed output is static HTML, CSS, JavaScript and a self-hosted search index.

<div class="mp-reference-links">
  <a href="./reference/python/miniproto/"><strong>Python reference</strong><span>Public modules, classes, methods, parameters, aliases and source links extracted statically with Griffe.</span></a>
  <a href="./reference/telegram/"><strong>Telegram reference</strong><span>Every Layer 230 function, type, constructor, parameter, known RPC error and Python-visible import path.</span></a>
  <a href="./reference/rust/miniproto-native/"><strong>Rust reference</strong><span>Public and PyO3-facing items normalized from nightly rustdoc JSON and cargo-docs-md.</span></a>
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

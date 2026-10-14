---
title: Brand assets
description: Packet Loom rationale, production asset inventory and the source-to-derivative workflow.
slug: /project/brand/
generated: false
---

## Current identity: Packet Loom

Concept 03, Packet Loom, supplies the mark used by the documentation site. The generator reads its SVG and produces the site logo variants, wordmarks, favicon and social card. Site components import the generated assets, so content does not copy the mark geometry.

The five deep-teal tiles represent Python intent and schema-defined packets moving through a controlled channel. The acid-lime tile is the emitted MTProto operation. The asymmetry gives the mark a clear output direction without borrowing Telegram's paper-plane silhouette.

## Production files

| Asset                                                 | Use                                                                                |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `src/assets/brand/logo.svg`                           | Canonical standalone color mark; byte-identical to the current concept 03 source. |
| `src/assets/brand/logo-dark.svg`                      | High-contrast mark for dark surfaces.                                              |
| `src/assets/brand/mark.svg`                           | Site component import and default navigation mark.                                 |
| `src/assets/brand/mark-monochrome.svg`                | One-color print, engraving and constrained-color use.                             |
| `src/assets/brand/wordmark.svg`                       | Color mark and literal `miniproto` wordmark for light surfaces.                    |
| `src/assets/brand/wordmark-dark.svg`                  | Mark and wordmark for dark surfaces.                                               |
| `public/favicon.svg`                                  | Browser and small-size mark; byte-identical to the canonical source.               |
| `public/social-card.svg` and `public/social-card.png` | 1200 × 630 SVG source and PNG rasterized from it.                                  |

The standalone mark must not be redrawn, simplified or reconstructed. Use `pnpm brand:build` to regenerate derivatives. `pnpm brand:check` compares the generated SVGs with the script output and checks the social-card PNG signature and dimensions. The script embeds `NunitoSans-ExtraBold-miniproto.woff2` for the `miniproto` name. The Alpha label falls back to `sans-serif`; supporting copy uses `system-ui,sans-serif`, and the repository link uses `ui-monospace,monospace`, so their raster appearance can vary by renderer. `social-card.png` is rasterized from `social-card.svg`, which remains the source for the mark geometry.

## Clear space and backgrounds

Keep clear space around the mark equal to at least half one tile width. Do not add outlines, shadows, glow or individual tile motion. The color mark is intended for warm paper and deep-teal surfaces; use the high-contrast or monochrome derivative when the original teal would lose contrast.

## Changing the production identity

The generator currently hard-codes concept 03, its palette and the Nunito font subset. To use another concept, update those inputs and the matching design tokens before rebuilding the derivatives. Then review light/dark screenshots, the favicon and social-card crop, and run site acceptance. Site content and routes do not contain the mark geometry.

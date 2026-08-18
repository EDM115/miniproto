---
title: Brand assets
description: Packet Loom rationale, production asset inventory, and the intentionally replaceable identity boundary while the community poll is open.
slug: /project/brand/
generated: false
---

## Current identity: Packet Loom

Concept 03, Packet Loom, is the temporary production identity while the community poll chooses among the eight approved directions. It is used because it currently leads the vote, not because the other concepts have been discarded. The integration is intentionally narrow: the website imports one canonical mark, product lockups are generated from that source, and content does not encode the mark's geometry.

The five deep-teal tiles represent Python intent and schema-defined packets moving through a controlled channel. The acid-lime tile is the emitted MTProto operation. The asymmetry gives the mark a clear output direction without borrowing Telegram's paper-plane silhouette.

## Production files

| Asset                                                 | Use                                                                                |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `src/assets/brand/logo.svg`                           | Canonical standalone color mark; byte-identical to the approved concept 03 source. |
| `src/assets/brand/logo-dark.svg`                      | High-contrast mark for dark surfaces.                                              |
| `src/assets/brand/mark.svg`                           | Site component import and default navigation mark.                                 |
| `src/assets/brand/mark-monochrome.svg`                | One-color print, engraving, and constrained-color use.                             |
| `src/assets/brand/wordmark.svg`                       | Color mark and literal `miniproto` wordmark for light surfaces.                    |
| `src/assets/brand/wordmark-dark.svg`                  | Mark and wordmark for dark surfaces.                                               |
| `public/favicon.svg`                                  | Browser and small-size mark; byte-identical to the canonical source.               |
| `public/social-card.svg` and `public/social-card.png` | 1200 × 630 social preview source and deterministic raster derivative.              |

The standalone mark must not be redrawn, simplified, or reconstructed. Use `pnpm brand:build` to regenerate derivatives and `pnpm brand:check` to detect drift. The script embeds the licensed display-font subset in wordmark and social SVGs, so exported assets do not depend on an installed font or an external URL.

## Clear space and backgrounds

Keep clear space around the mark equal to at least half one tile width. Do not add outlines, shadows, glow, or individual tile motion. The color mark is intended for warm paper and deep-teal surfaces; use the high-contrast or monochrome derivative when the original teal would lose contrast.

## Switching the poll winner

A later community choice changes the canonical source, generated derivative inputs, design tokens, and this rationale. It must not require rewriting documentation content, search metadata, routes, or component structure. Re-run the brand checks, light/dark screenshot matrix, favicon inspection, social-card crop review, and complete site acceptance before promoting another concept.

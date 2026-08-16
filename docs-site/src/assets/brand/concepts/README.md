# miniproto Logo Concepts

These four directions implement the approved Wave 5 brand brief without selecting a winner. The selected direction will be refined into the production logo, dark variant, standalone mark, monochrome mark, favicon, wordmark lockups, and social artwork only after the maintainer chooses a family.

## Creative Brief

miniproto is a compact, async-first MTProto SDK whose identity should make speed, protocol correctness, security, controlled data flow, and the Python/Rust relationship feel tangible. The mark must remain serious enough for infrastructure documentation while retaining enough character to be memorable in an open-source ecosystem.

Every direction avoids Telegram's paper-plane trademark, literal Python/Rust mascots, generic shields and padlocks, cryptocurrency styling, illegible micro-detail, and forms that work on only one background. Every `concept.svg` is self-contained vector geometry with an accessible title and description, a `viewBox`, path-based wordmark lettering, no `<text>`, no `<image>`, no embedded bitmap, no external asset, and no installed-font dependency. The adjacent `preview.png` is rendered from that SVG for convenient review. The adjacent `ideation.png` records the built-in image-generation exploration that informed the deterministic SVG; it is not the production source.

## Directions

| Direction | Core idea | Strengths | Risks | Likely site mood |
| --- | --- | --- | --- | --- |
| Protocol Aperture | Three nested protocol frames focus on one data pulse. | Directly expresses layers, framing, precision, and progressive depth; strongest connection to schema and transport concepts. | Concentric geometry can feel familiar if the spacing and color are not refined carefully. | Electric, precise, premium infrastructure. |
| Duplex Rails | Two independent transport rails cooperate around a packet gap and form an abstract `m`/`p`. | Most ownable silhouette; communicates bidirectional flow and the Python/Rust pairing without literal language marks. | The negative-space monogram needs careful optical refinement at 16 px. | Energetic, fast, developer-forward. |
| Packet Loom | Seven deterministic tiles and one signal tile turn generated structure into a compact data mark. | Best small-size geometry; distinctive modular system can extend naturally to diagrams, callouts, and motion. | Tile systems can skew playful or product-app-like if the final typography is too soft. | Technical, modular, slightly playful. |
| Clocked Core | An open phase orbit and three acknowledgement nodes synchronize around a stable core. | Strong motion and runtime/reliability story; very different from typical code-library identities. | Circular marks can drift toward generic platform or telemetry branding without a distinctive wordmark. | Kinetic, confident, runtime-centric. |

## Selection Criteria

Choose based on the core metaphor and silhouette, not the provisional palette. Color, spacing, line weight, and wordmark construction are refinement variables. The strongest family should remain recognizable in the 16 px sample, work in one color, avoid accidental resemblance to another brand, and support a visually distinctive but readable documentation site.

## Generated Ideation

The four PNG boards were generated with the built-in image-generation tool using the `logo-brand` use case. Each prompt requested an icon, exact `miniproto` lockup, light/dark treatment, monochrome treatment, and 16/32/64 px samples while explicitly excluding paper planes, Telegram identity, shields, padlocks, crypto marks, micro-detail, and watermarks. The SVG sheets deliberately simplify those boards into reproducible geometry instead of tracing or embedding the raster output.

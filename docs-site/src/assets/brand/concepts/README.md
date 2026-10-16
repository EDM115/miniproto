# miniproto Logo Concepts

These eight directions implement the approved Wave 5 brand brief. The first four preserve the same marks and ideas as their original inspiration boards. The next four explore other recognizable parts of miniproto: Telegram-compatible delivery, free-threaded Python with a Rust core, quick acknowledgements and multi-source schema generation.

Each family includes a transparent standalone color mark for side-by-side review. Concept 03, Packet Loom, supplies the mark used by the production website. Its canonical SVG feeds the brand generator, which creates the site logo variants and keeps mark geometry out of content.

## Creative Brief

miniproto is an async-first MTProto SDK. Its identity should suggest speed, protocol correctness, controlled packet flow and the Python/Rust implementation. The mark should suit infrastructure documentation and remain distinct among Telegram client libraries.

Pyrogram's flame and its Kurigram/Pyroblack variants, Hydrogram's droplet, Telethon's `T` and mtcute's flower are recognizable without their wordmarks. Each miniproto direction centers on one emblem. Packet Plane uses the delivery metaphor without copying Telegram's plane shape, enclosing circle or visual identity; the other seven concepts avoid paper planes.

Each family's adjacent `logo.svg` is its transparent, square-canvas color mark. It contains no wordmark, font, presentation panel or raster content.  
The family's `concept.svg` embeds that mark and adds accessible metadata, a text wordmark with an embedded WOFF2 subset and monochrome filters. Concepts 01–05 use Nunito Sans ExtraBold at weight 800; concepts 06–08 use Quicksand SemiBold at weight 600. The adjacent `fonts/` directory retains the full fonts, subsets and SIL Open Font License texts.  
The adjacent `preview.png` is a Chromium render of `concept.svg`, because librsvg substitutes embedded webfonts. `ideation.png` records image-generation exploration and is not a production source.

## Directions

| Direction         | Core idea                                                                                      | Strengths                                                                                              | Risks                                                                                                | Likely site mood                                    |
| ----------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Protocol Aperture | Three offset protocol frames focus on one data pulse.                                          | Shows layers and framing, with a clear link to schema and transport concepts.                          | Nested geometry can look familiar without careful spacing and color.                                 | Electric, precise, premium infrastructure.          |
| Duplex Rails      | Two independent transport rails meet around a packet gap and form an abstract `m`/`p`.         | The gap forms a compact mark for bidirectional flow and the Python/Rust pairing.                       | The negative-space monogram needs careful optical refinement at favicon size.                        | Energetic, fast, developer-forward.                 |
| Packet Loom       | Five deterministic input tiles converge into one accelerated output tile.                      | The tile shape remains clear at small sizes and can repeat in diagrams or motion.                      | Tile systems can skew product-app-like if the final typography becomes too soft.                     | Technical, modular, slightly playful.               |
| Clocked Core      | One open timing orbit and three acknowledgement nodes synchronize around a stable native core. | Connects timing, acknowledgement and the native core.                                                  | Orbital marks can resemble generic telemetry branding without a distinctive lockup.                  | Kinetic, confident, runtime-centric.                |
| Packet Plane      | A folded delivery plane leaves exactly three discrete packet blocks in its wake.               | Gives the strongest Telegram association while keeping a custom silhouette and negative-space fold.    | Must remain visibly distinct from Telegram's exact paper plane and from generic messaging-app icons. | Fast, approachable, unmistakably Telegram-adjacent. |
| Threadburst       | Four independent execution strands curve around an amber native core.                          | Shows free-threaded Python work around a Rust core.                                                    | The pinwheel-like form needs careful animation and color restraint to avoid generic AI branding.     | Parallel, modern, performance-led.                  |
| Quick-Ack Comet   | A packet races ahead of two notched acknowledgement echoes.                                    | Uses MTProto quick acknowledgements as its motif; trailing echoes suggest a response after the packet. | The open trail is less compact than the other marks and may need simplification below 24 px.         | Swift, technical, network-native.                   |
| Schema Prism      | Three source facets reconcile into one generated constructor tile.                             | Connects multiple schema sources to one generated constructor and supports a duotone palette.          | The prism can read as a generic developer-tool gem without supporting copy or motion.                | Structured, polished, generator-centric.            |

## Review Sequence

1. Compare the standalone marks on light and dark backgrounds.
2. Inspect the monochrome versions and the 64, 32 and 16 px samples.
3. Check whether each metaphor represents the whole library or one implementation detail.
4. Check whether any mark resembles another Telegram client library.
5. Select a production family and, if useful, a secondary direction for color, motion or typography.

A production mark should be recognizable before the `miniproto` wordmark, work on light and dark surfaces, remain clear in monochrome and avoid resemblance to another client library.

## Generated Ideation

The built-in image-generation tool produced all eight PNG boards from a logo-exploration brief. Concepts 01–04 were regenerated from their original boards, preserving their named silhouettes while removing glow, malformed text, geometry drift, mockup effects and inconsistent small-size variants. Concepts 05–08 explore Packet Plane, Threadburst, Quick-Ack Comet and Schema Prism.

Each prompt requested the exact `miniproto` lockup, light and dark presentations, a monochrome treatment and 64/32/16 px samples. The PNGs remain visual references; canonical vectors supply the standalone marks. Presentation boards render those vectors with embedded typefaces.

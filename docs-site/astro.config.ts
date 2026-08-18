import { fileURLToPath } from "node:url";

import { unified } from "@astrojs/markdown-remark";
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";

import remarkLocalMarkdownLinks from "./src/remark-local-markdown-links.ts";
import { buildDocumentationSidebar } from "./src/sidebar.ts";

const site = process.env.MINIPROTO_DOCS_SITE ?? "https://edm115.github.io";
const base = normaliseBase(process.env.MINIPROTO_DOCS_BASE ?? "/");
const docsRoot = fileURLToPath(new URL("../docs", import.meta.url));
const assetPath = (asset: string): string => (base === "/" ? `/${asset}` : `${base}/${asset}`);
const absoluteAssetUrl = (asset: string): string => new URL(assetPath(asset), site).href;

/**
 * Convert the hosting path into Astro's leading-slash, no-trailing-slash form.
 *
 * An empty value and `/` both deliberately mean a site hosted at the origin.
 */
function normaliseBase(value: string): string {
  const trimmed = value.trim().replace(/^\/+|\/+$/g, "");
  return trimmed === "" ? "/" : `/${trimmed}`;
}

export default defineConfig({
  site,
  base,
  output: "static",
  trailingSlash: "always",
  markdown: {
    processor: unified({
      remarkPlugins: [[remarkLocalMarkdownLinks, { docsRoot, base }]],
    }),
  },
  integrations: [
    starlight({
      title: "miniproto",
      description:
        "A fast, async-first MTProto client core for Python with bundled Rust acceleration.",
      logo: {
        src: "./src/assets/brand/mark.svg",
        alt: "Packet Loom mark",
      },
      favicon: "/favicon.svg",
      social: [{ icon: "github", label: "GitHub", href: "https://github.com/EDM115/miniproto" }],
      head: [
        { tag: "meta", attrs: { name: "theme-color", content: "#082e2c" } },
        { tag: "meta", attrs: { name: "color-scheme", content: "dark light" } },
        { tag: "link", attrs: { rel: "sitemap", href: assetPath("sitemap-index.xml") } },
        {
          tag: "meta",
          attrs: { property: "og:image", content: absoluteAssetUrl("social-card.png") },
        },
        { tag: "meta", attrs: { name: "twitter:card", content: "summary_large_image" } },
        {
          tag: "meta",
          attrs: { name: "twitter:image", content: absoluteAssetUrl("social-card.png") },
        },
      ],
      editLink: {
        baseUrl: "https://github.com/EDM115/miniproto/edit/master/docs/",
      },
      customCss: ["./src/styles/foundation.css"],
      components: {
        EditLink: "./src/components/EditLink.astro",
        Footer: "./src/components/Footer.astro",
        Head: "./src/components/Head.astro",
        Hero: "./src/components/Hero.astro",
        MarkdownContent: "./src/components/MarkdownContent.astro",
        PageFrame: "./src/components/PageFrame.astro",
        Search: "./src/components/Search.astro",
      },
      markdown: {
        processedDirs: ["../docs"],
      },
      expressiveCode: {
        themes: ["github-light", "github-dark"],
        shiki: {
          langAlias: {
            tl: "proto",
          },
        },
      },
      pagefind: {
        ranking: {
          pageLength: 0.18,
          termFrequency: 0.2,
          termSaturation: 1.6,
          termSimilarity: 9,
          diacriticSimilarity: 0.8,
          metaWeights: {
            title: 8,
            qualified_name: 12,
            aliases: 7,
            description: 4,
          },
        },
      },
      sidebar: buildDocumentationSidebar({ docsRoot }),
    }),
  ],
});

import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const site = process.env.MINIPROTO_DOCS_SITE ?? 'https://edm115.github.io';
const base = normaliseBase(process.env.MINIPROTO_DOCS_BASE ?? '/miniproto');

/**
 * Convert the hosting path into Astro's leading-slash, no-trailing-slash form.
 *
 * An empty value and `/` both deliberately mean a site hosted at the origin.
 */
function normaliseBase(value) {
  const trimmed = value.trim().replace(/^\/+|\/+$/g, '');
  return trimmed === '' ? '/' : `/${trimmed}`;
}

export default defineConfig({
  site,
  base,
  output: 'static',
  trailingSlash: 'always',
  integrations: [
    starlight({
      title: 'miniproto',
      description: 'Async-first MTProto client core for Python with bundled Rust acceleration.',
      editLink: {
        baseUrl: 'https://github.com/EDM115/miniproto/edit/master/docs/',
      },
      customCss: ['./src/styles/foundation.css'],
      components: {
        EditLink: './src/components/EditLink.astro',
      },
      markdown: {
        processedDirs: ['../docs'],
      },
      expressiveCode: {
        themes: ['github-light', 'github-dark'],
        shiki: {
          langAlias: {
            tl: 'proto',
          },
        },
      },
      pagefind: true,
      sidebar: [
        { label: 'Overview', link: '/' },
        {
          label: 'Start',
          items: [{ autogenerate: { directory: 'start' } }],
        },
        {
          label: 'Guides',
          items: [
            { label: 'Media Primitives', link: '/guides/media/' },
            { label: 'Session Security', link: '/guides/session-security/' },
            { autogenerate: { directory: 'guides' } },
          ],
        },
        {
          label: 'Concepts',
          items: [
            { label: 'Raw API', link: '/concepts/raw-api/' },
            { autogenerate: { directory: 'concepts' } },
          ],
        },
        {
          label: 'Recipes',
          items: [{ autogenerate: { directory: 'recipes' } }],
        },
        {
          label: 'FAQ',
          items: [{ autogenerate: { directory: 'faq' } }],
        },
        {
          label: 'Project',
          items: [
            { label: 'Development Commands', link: '/project/development/' },
            { label: 'Faked And Deferred Methods', link: '/project/testing/faked-methods/' },
            { autogenerate: { directory: 'project' } },
          ],
        },
        {
          label: 'Reference',
          collapsed: true,
          items: [{ autogenerate: { directory: 'reference' } }],
        },
      ],
    }),
  ],
});

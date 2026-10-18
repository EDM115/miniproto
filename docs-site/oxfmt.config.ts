import { defineConfig } from "oxfmt";

export default defineConfig({
  ignorePatterns: [
    "pnpm-lock.yaml",
    ".astro/",
    "dist/",
    "node_modules/",
    "playwright-report/",
    "test-results/",
    "src/**/*.astro",
    "public/**/*.svg",
    "src/assets/brand/**/*.svg",
  ],
  sortImports: true,
});

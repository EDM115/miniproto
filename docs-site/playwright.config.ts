import { defineConfig } from "@playwright/test";

const requestedBase = process.env.MINIPROTO_DOCS_BASE ?? "/";
const base = requestedBase === "/" ? "/" : `/${requestedBase.replace(/^\/+|\/+$/g, "")}/`;
const origin = "http://127.0.0.1:4321";

export default defineConfig({
  testDir: "./tests",
  timeout: 45_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI
    ? [["line"], ["html", { open: "never", outputFolder: ".playwright-report" }]]
    : "line",
  use: {
    baseURL: `${origin}${base}`,
    channel: "chrome",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "node scripts/serve-static.mjs --host 127.0.0.1 --port 4321",
    url: `${origin}${base}`,
    reuseExistingServer: false,
    timeout: 120_000,
  },
});

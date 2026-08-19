import { expect, test } from "@playwright/test";

const REQUIRED_FILTERS = [
  "crate",
  "kind",
  "language",
  "layer",
  "module",
  "namespace",
  "python_visible",
];
const REQUESTED_BASE = process.env.MINIPROTO_DOCS_BASE ?? "/";
const PUBLIC_BASE = REQUESTED_BASE === "/" ? "/" : `/${REQUESTED_BASE.replace(/^\/+|\/+$/g, "")}/`;
const PUBLIC_SITE = process.env.MINIPROTO_DOCS_SITE ?? "https://edm115.github.io";
const sitePath = (route: string) => `${PUBLIC_BASE}${route.replace(/^\/+/, "")}`;
const siteUrl = (route: string) => new URL(sitePath(route), PUBLIC_SITE).href;

type PagefindData = {
  meta?: { title?: string };
  url?: string;
  filters?: Record<string, string[]>;
};

type PagefindEntry = {
  data: () => Promise<PagefindData>;
};

declare global {
  interface Window {
    runMiniprotoDeferredIdleCallbacks: () => void;
  }
}

test("homepage explains the product and exposes the Packet Loom identity", async ({ page }) => {
  await page.goto("./");

  await expect(page.getByRole("img", { name: "Packet Loom mark" }).first()).toBeVisible();
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/MTProto/i);
  await expect(page.getByText("0.1.0 Alpha", { exact: true })).toBeVisible();
  await expect(page.getByRole("link", { name: /five-minute quickstart/i })).toBeVisible();
  await expect(page.getByRole("link", { name: /browse the raw api/i })).toBeVisible();
  await expect(page.locator('link[rel="sitemap"]')).toHaveAttribute(
    "href",
    sitePath("sitemap-index.xml"),
  );
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute(
    "content",
    siteUrl("social-card.png"),
  );
  await expect(page.locator('meta[name="twitter:image"]')).toHaveAttribute(
    "content",
    siteUrl("social-card.png"),
  );
  const pythonReferencePath = await page
    .getByRole("link", { name: /Python reference/i })
    .evaluate((link) => new URL(link.getAttribute("href") ?? "", document.baseURI).pathname);
  const rustReferencePath = await page
    .getByRole("link", { name: /Rust reference/i })
    .evaluate((link) => new URL(link.getAttribute("href") ?? "", document.baseURI).pathname);
  expect(pythonReferencePath).toBe(sitePath("reference/python/miniproto/"));
  expect(rustReferencePath).toBe(sitePath("reference/rust/miniproto-native/"));

  const escapingInternalLinks = await page.locator("a[href]").evaluateAll(
    (anchors, base) =>
      anchors.flatMap((anchor) => {
        const url = new URL(anchor.getAttribute("href") ?? "", document.baseURI);
        return url.origin === window.location.origin && !url.pathname.startsWith(base)
          ? [url.pathname]
          : [];
      }),
    PUBLIC_BASE,
  );
  expect(escapingInternalLinks).toEqual([]);

  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBeLessThanOrEqual(1);
});

test("source-friendly Markdown links resolve to portable site routes", async ({ page }) => {
  await page.goto(sitePath("concepts/architecture"));
  await page.getByRole("link", { name: "transport reliability" }).click();
  await expect(page).toHaveURL(
    new RegExp(`${escapeRegex(sitePath("concepts/transport-reliability/"))}$`, "u"),
  );

  await page.goto(sitePath("reference/rust/miniproto-native"));
  await page.getByRole("link", { name: "crypto" }).first().click();
  await expect(page).toHaveURL(
    new RegExp(`${escapeRegex(sitePath("reference/rust/miniproto-native/crypto/"))}$`, "u"),
  );

  await page.goto(sitePath("reference/telegram/"));
  const telegramFunctions = page
    .getByRole("main")
    .getByRole("link", { name: "Functions", exact: true });
  const telegramFunctionsPath = await telegramFunctions.evaluate(
    (link) => new URL(link.getAttribute("href") ?? "", document.baseURI).pathname,
  );
  expect(telegramFunctionsPath).toBe(sitePath("reference/telegram/functions/"));
  await telegramFunctions.click();
  await expect(page).toHaveURL(
    new RegExp(`${escapeRegex(sitePath("reference/telegram/functions/"))}$`, "u"),
  );
});

test("nested documentation links and the handwritten sidebar remain complete without a trailing slash", async ({
  page,
}) => {
  await page.goto(sitePath("start"));
  await page.getByRole("link", { name: "Installation", exact: true }).first().click();
  await expect(page).toHaveURL(new RegExp(`${escapeRegex(sitePath("start/installation/"))}$`, "u"));

  await page.goto(sitePath("start/quickstart/"));
  const sidebar = page.locator('nav[aria-label="Main"]');
  await expect(sidebar.getByRole("link", { name: "Installation", exact: true })).toBeVisible();
  await expect(
    sidebar.getByRole("link", { name: "Five-Minute Quickstart", exact: true }),
  ).toBeVisible();
  await expect(sidebar.getByRole("link", { name: "First Raw Call", exact: true })).toBeVisible();
});

test("Pagefind indexes every reference language, parameter terms, prose, and filters", async ({
  page,
}) => {
  await page.goto("./");

  const search = await page.evaluate(async (requiredFilters) => {
    const bundleUrl = new URL("pagefind/pagefind.js", document.baseURI).href;
    const pagefind = await import(bundleUrl);
    const filters = await pagefind.filters();
    const terms = [
      "messages.sendMessage",
      "quick_reply_shortcut_id",
      "upload.getFileHashes",
      "iter_download",
      "TransportCodec",
      "InputPeer",
      "miniproto._native.TransportCodec",
      "replaying",
    ];
    const results: Record<
      string,
      Array<{ title: string; url: string; filters: Record<string, string[]> }>
    > = {};
    for (const term of terms) {
      const response = await pagefind.search(term);
      results[term] = await Promise.all(
        response.results.slice(0, 12).map(async (entry: PagefindEntry) => {
          const data = await entry.data();
          return {
            title: data.meta?.title ?? "",
            url: data.url ?? "",
            filters: data.filters ?? {},
          };
        }),
      );
    }
    const telegramResponse = await pagefind.search("send", {
      filters: { language: "telegram" },
    });
    const telegramResults = await Promise.all(
      telegramResponse.results.slice(0, 12).map(async (entry: PagefindEntry) => {
        const data = await entry.data();
        return data.filters?.language ?? [];
      }),
    );
    return {
      filterNames: Object.keys(filters),
      requiredFilters,
      results,
      telegramResults,
    };
  }, REQUIRED_FILTERS);

  expect(search.filterNames).toEqual(expect.arrayContaining(REQUIRED_FILTERS));
  expect(
    search.results["messages.sendMessage"].some((result) =>
      /send.?message/i.test(`${result.title} ${result.url}`),
    ),
    JSON.stringify(search.results["messages.sendMessage"]),
  ).toBeTruthy();
  expect(
    search.results.quick_reply_shortcut_id.some((result) =>
      result.filters.kind?.includes("function"),
    ),
    JSON.stringify(search.results.quick_reply_shortcut_id),
  ).toBeTruthy();
  expect(
    search.results["upload.getFileHashes"].some((result) =>
      /get.?file.?hashes/i.test(`${result.title} ${result.url}`),
    ),
  ).toBeTruthy();
  expect(
    search.results.iter_download.some((result) =>
      /iter.?download/i.test(`${result.title} ${result.url}`),
    ),
  ).toBeTruthy();
  expect(
    search.results.TransportCodec.some((result) =>
      /transport.?codec/i.test(`${result.title} ${result.url}`),
    ),
  ).toBeTruthy();
  expect(
    search.results.InputPeer.some((result) => /input.?peer/i.test(`${result.title} ${result.url}`)),
  ).toBeTruthy();
  expect(
    search.results["miniproto._native.TransportCodec"].some((result) =>
      /transport.?codec/i.test(`${result.title} ${result.url}`),
    ),
  ).toBeTruthy();
  expect(
    search.results.replaying.some((result) =>
      /transport-reliability|project\/development/.test(result.url),
    ),
    JSON.stringify(search.results.replaying),
  ).toBeTruthy();
  expect(search.telegramResults.length).toBeGreaterThan(0);
  expect(search.telegramResults.every((values) => values.includes("telegram"))).toBeTruthy();
});

test("search focuses a Pagefind input that initializes after keyboard opening", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const callbacks: IdleRequestCallback[] = [];
    window.requestIdleCallback = (callback) => {
      callbacks.push(callback);
      return callbacks.length;
    };
    window.runMiniprotoDeferredIdleCallbacks = () => {
      const deadline: IdleDeadline = { didTimeout: false, timeRemaining: () => 50 };
      for (const callback of callbacks.splice(0)) {
        callback(deadline);
      }
    };
  });
  await page.goto("./");

  await page.keyboard.press("Control+k");
  const dialog = page.getByRole("dialog", { name: /search/i });
  await expect(dialog).toBeVisible();
  const searchbox = dialog.locator("input.pagefind-ui__search-input");
  await expect(searchbox).toHaveCount(0);
  await page.evaluate(() => {
    window.runMiniprotoDeferredIdleCallbacks();
  });
  await expect(searchbox).toBeFocused();

  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();
});

test("search remains keyboard accessible and exposes reference facets", async ({ page }) => {
  await page.goto("./");

  const searchbox = page.locator("input.pagefind-ui__search-input");
  await expect(searchbox).toBeAttached();
  await page.keyboard.press("Control+k");
  const dialog = page.getByRole("dialog", { name: /search/i });
  await expect(dialog).toBeVisible();
  await expect(searchbox).toBeFocused();
  await searchbox.fill("messages.sendMessage");
  await expect(dialog.getByRole("link", { name: /send.?message/i }).first()).toBeVisible();
  await expect(dialog.getByText(/language/i).first()).toBeVisible();

  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();
});

test("the reading experience remains usable on a narrow viewport and in both themes", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("./guides/session-security/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();

  for (const theme of ["dark", "light"]) {
    await page.evaluate((value) => {
      document.documentElement.dataset.theme = value;
      localStorage.setItem("starlight-theme", value);
    }, theme);
    await expect(page.locator("html")).toHaveAttribute("data-theme", theme);
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(1);
  }
});

function escapeRegex(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

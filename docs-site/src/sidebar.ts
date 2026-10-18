import * as fs from "node:fs";
import * as path from "node:path";

type SidebarPage = {
  label: string;
  link: string;
};

type SidebarGroup = {
  label: string;
  collapsed?: boolean;
  items: SidebarItem[];
};

type SidebarItem = SidebarPage | SidebarGroup;

type SectionSource = readonly [label: string, directory: string, rootFiles: readonly string[]];

const SECTION_SOURCES = [
  ["Start", "start", []],
  ["Guides", "guides", ["media.md", "session-security.md"]],
  ["Concepts", "concepts", ["raw-api.md"]],
  ["Recipes", "recipes", []],
  ["FAQ", "faq", []],
] as const satisfies readonly SectionSource[];

const START_ORDER = new Map<string, number>(
  [
    "/start/",
    "/start/installation/",
    "/start/quickstart/",
    "/start/authentication/",
    "/start/high-level-operation/",
    "/start/raw-api/",
    "/start/examples/",
  ].map((route, index) => [route, index]),
);

/** Build complete handwritten navigation plus compact raw-reference entry points. */
export function buildDocumentationSidebar({ docsRoot }: { docsRoot: string }): SidebarItem[] {
  const root = path.resolve(docsRoot);
  const sections = SECTION_SOURCES.map(([label, directory, rootFiles]) => ({
    label,
    items: [
      ...pagesIn(path.join(root, directory)),
      ...rootFiles.map((fileName) => pageFrom(path.join(root, fileName))),
    ].toSorted((left, right) => comparePages(left, right, directory)),
  }));
  const projectPages = [
    ...pagesIn(path.join(root, "project")),
    ...["development.md", "faked-methods.md"].map((fileName) =>
      pageFrom(path.join(root, fileName)),
    ),
  ];
  const codebasePages = pagesIn(path.join(root, "codebase"));

  return [
    { label: "Overview", link: "/" },
    ...sections,
    {
      label: "Project",
      items: [
        ...projectPages.toSorted(compareIndexFirst),
        {
          label: "Codebase map",
          collapsed: true,
          items: codebasePages.toSorted(compareIndexFirst),
        },
      ],
    },
    {
      label: "Reference",
      collapsed: true,
      items: [
        { label: "Reference overview", link: "/reference/" },
        { label: "Python API", link: "/reference/python/miniproto/" },
        { label: "Rust API", link: "/reference/rust/miniproto-native/" },
        {
          label: "Telegram raw API",
          collapsed: true,
          items: [
            { label: "Overview", link: "/reference/telegram/" },
            { label: "Functions", link: "/reference/telegram/functions/" },
            { label: "Types", link: "/reference/telegram/types/" },
            { label: "RPC errors", link: "/reference/telegram/errors/" },
          ],
        },
      ],
    },
  ];
}

/** Read every Markdown page in one handwritten section. */
function pagesIn(directory: string): SidebarPage[] {
  return markdownFiles(directory).map((filePath) => pageFrom(filePath));
}

/** Enumerate Markdown source files recursively with stable filesystem-independent ordering. */
function markdownFiles(directory: string): string[] {
  if (!fs.existsSync(directory)) {
    return [];
  }
  const files: string[] = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...markdownFiles(entryPath));
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith(".md")) {
      files.push(entryPath);
    }
  }
  return files.toSorted((left, right) => left.localeCompare(right, "en"));
}

/** Convert one canonical Markdown file into an explicit Starlight sidebar item. */
function pageFrom(filePath: string): SidebarPage {
  const contents = fs.readFileSync(filePath, "utf8");
  const frontmatter = /^---\r?\n(?<body>[\s\S]*?)\r?\n---(?:\r?\n|$)/u.exec(contents)?.groups?.body;
  if (!frontmatter) {
    throw new Error(`Documentation page has no frontmatter: ${filePath}`);
  }
  const title = frontmatterValue(frontmatter, "title");
  const slug = frontmatterValue(frontmatter, "slug");
  if (!title || !slug) {
    throw new Error(
      `Documentation page requires title and slug for sidebar generation: ${filePath}`,
    );
  }
  return { label: title, link: normaliseRoute(slug) };
}

/** Extract and unquote one scalar frontmatter value. */
function frontmatterValue(frontmatter: string, name: string): string | undefined {
  const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const value = new RegExp(`^${escaped}:\\s*(?<value>.+?)\\s*$`, "mu").exec(frontmatter)?.groups
    ?.value;
  return value?.replace(/^(?<quote>['"])(?<content>.*)\k<quote>$/u, "$<content>");
}

/** Put each section index first, then keep the remaining labels predictable. */
function compareIndexFirst(left: SidebarPage, right: SidebarPage): number {
  const leftDepth = routeDepth(left.link);
  const rightDepth = routeDepth(right.link);
  if (leftDepth !== rightDepth) {
    return leftDepth - rightDepth;
  }
  return left.label.localeCompare(right.label, "en");
}

/** Preserve the intended onboarding order while sorting every other section predictably. */
function comparePages(left: SidebarPage, right: SidebarPage, directory: string): number {
  if (directory !== "start") {
    return compareIndexFirst(left, right);
  }
  return (
    (START_ORDER.get(left.link) ?? Number.MAX_SAFE_INTEGER) -
      (START_ORDER.get(right.link) ?? Number.MAX_SAFE_INTEGER) || compareIndexFirst(left, right)
  );
}

/** Normalize a public route to leading and trailing slash form. */
function normaliseRoute(route: string): string {
  const segments = route.split("/").filter(Boolean);
  return segments.length === 0 ? "/" : `/${segments.join("/")}/`;
}

/** Count public route segments for index-first sorting. */
function routeDepth(route: string): number {
  return route.split("/").filter(Boolean).length;
}

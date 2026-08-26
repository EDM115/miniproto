import * as fs from "node:fs";
import * as path from "node:path";

type MarkdownNode = {
  type: string;
  url?: string;
  children?: MarkdownNode[];
};

type MarkdownFile = {
  path?: unknown;
};

type LocalTarget = {
  pathname: string;
  suffix: string;
};

type RemarkLocalMarkdownLinksOptions = {
  docsRoot: string;
  base?: string;
};

/**
 * Rewrite repository-relative Markdown links to the public route declared by the target page.
 *
 * The canonical files deliberately retain useful `.md` links for GitHub and source-checkout readers. Starlight's external content loader does not rewrite those links automatically, so this build-only adapter resolves target frontmatter and emits an absolute route under the configured Astro base. The trailing slash makes every link independent of host redirect behavior.
 */
export default function remarkLocalMarkdownLinks({
  docsRoot,
  base = "/",
}: RemarkLocalMarkdownLinksOptions): (tree: MarkdownNode, file: MarkdownFile) => void {
  const root = path.resolve(docsRoot);
  const routeCache = new Map<string, string>();

  return (tree, file) => {
    if (typeof file.path !== "string") {
      return;
    }
    const source = path.resolve(file.path);
    const sourceRoute = routeFor(source);
    visit(tree, (node) => {
      if ((node.type !== "link" && node.type !== "definition") || typeof node.url !== "string") {
        return;
      }
      const parsed = localMarkdownTarget(node.url);
      if (parsed) {
        const target = path.resolve(path.dirname(source), parsed.pathname);
        if (!isInside(root, target) || !fs.existsSync(target) || !fs.statSync(target).isFile()) {
          return;
        }
        const targetRoute = routeFor(target);
        node.url = `${applyBase(targetRoute, base)}${parsed.suffix}`;
        return;
      }
      const routeTarget = localRouteTarget(node.url);
      if (!routeTarget) {
        return;
      }
      const targetRoute = routeTarget.pathname.startsWith("/")
        ? normaliseRoute(routeTarget.pathname)
        : normaliseRoute(
            new URL(routeTarget.pathname, `https://miniproto.invalid${sourceRoute}`).pathname,
          );
      node.url = `${applyBase(targetRoute, base)}${routeTarget.suffix}`;
    });
  };

  function routeFor(filePath: string): string {
    const cached = routeCache.get(filePath);
    if (cached) {
      return cached;
    }
    const relative = path.relative(root, filePath).replaceAll("\\", "/");
    if (relative.startsWith("../") || relative === "..") {
      throw new Error(`Markdown source escapes the documentation root: ${filePath}`);
    }
    const contents = fs.readFileSync(filePath, "utf8");
    const slug = frontmatterSlug(contents);
    const route = slug ?? inferredRoute(relative);
    routeCache.set(filePath, route);
    return route;
  }
}

/** Apply one normalized deployment base to an absolute documentation route. */
function applyBase(targetRoute: string, base: string): string {
  const normalized = normaliseRoute(base);
  return normalized === "/" ? targetRoute : `${normalized.slice(0, -1)}${targetRoute}`;
}

/** Return a local Markdown pathname plus any query/fragment suffix. */
function localMarkdownTarget(url: string): LocalTarget | undefined {
  if (/^(?:[a-z]+:|\/|#)/iu.test(url)) {
    return undefined;
  }
  const match = /^(?<pathname>[^?#]+\.md)(?<suffix>[?#].*)?$/iu.exec(url);
  return match?.groups
    ? { pathname: match.groups.pathname, suffix: match.groups.suffix ?? "" }
    : undefined;
}

/** Return an existing relative public route plus any query/fragment suffix. */
function localRouteTarget(url: string): LocalTarget | undefined {
  if (/^(?:[a-z]+:|\/\/|#)/iu.test(url)) {
    return undefined;
  }
  const match = /^(?<pathname>(?:\.{1,2}\/|\/)[^?#]*\/)(?<suffix>[?#].*)?$/u.exec(url);
  return match?.groups
    ? { pathname: match.groups.pathname, suffix: match.groups.suffix ?? "" }
    : undefined;
}

/** Read the explicit public slug from one Markdown frontmatter block. */
function frontmatterSlug(contents: string): string | undefined {
  const frontmatter = /^---\r?\n(?<body>[\s\S]*?)\r?\n---(?:\r?\n|$)/u.exec(contents)?.groups?.body;
  const value = frontmatter
    ? /^slug:\s*(?<slug>.+?)\s*$/mu.exec(frontmatter)?.groups?.slug
    : undefined;
  if (!value) {
    return undefined;
  }
  const unquoted = value.replace(/^(?<quote>['"])(?<content>.*)\k<quote>$/u, "$<content>");
  return normaliseRoute(unquoted);
}

/** Infer the public route for generated reference pages that do not carry explicit slugs. */
function inferredRoute(relativePath: string): string {
  const parsed = path.posix.parse(relativePath);
  const route = parsed.name === "index" ? `/${parsed.dir}/` : `/${parsed.dir}/${parsed.name}/`;
  return normaliseRoute(route);
}

/** Normalise one absolute site route without applying a deployment base. */
function normaliseRoute(route: string): string {
  const segments = route.split("/").filter(Boolean);
  return segments.length === 0 ? "/" : `/${segments.join("/")}/`;
}

/** Traverse a Markdown syntax tree without adding another runtime dependency. */
function visit(node: MarkdownNode, callback: (node: MarkdownNode) => void): void {
  if (!node || typeof node !== "object") {
    return;
  }
  callback(node);
  if (!Array.isArray(node.children)) {
    return;
  }
  for (const child of node.children) {
    visit(child, callback);
  }
}

/** Return whether a resolved target remains inside the canonical documentation root. */
function isInside(root: string, target: string): boolean {
  const relative = path.relative(root, target);
  return (
    relative !== "" &&
    relative !== ".." &&
    !relative.startsWith(`..${path.sep}`) &&
    !path.isAbsolute(relative)
  );
}

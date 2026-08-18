import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import path from "node:path";
import process from "node:process";

const MIME_TYPES = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".ico", "image/x-icon"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".png", "image/png"],
  [".svg", "image/svg+xml"],
  [".wasm", "application/wasm"],
  [".woff2", "font/woff2"],
  [".xml", "application/xml; charset=utf-8"],
]);

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  console.log(
    "Usage: node scripts/serve-static.mjs [--root PATH] [--base PATH] [--host HOST] [--port PORT]",
  );
  console.log("Serve the built documentation artifact under its configured base path.");
  process.exit(0);
}

const root = path.resolve(args.root ?? "dist");
const base = normalizeBase(args.base ?? process.env.MINIPROTO_DOCS_BASE ?? "/");
const host = args.host ?? "127.0.0.1";
const port = parsePort(args.port ?? "4321");

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url ?? "/", `http://${request.headers.host ?? host}`);
    const relativeUrl = stripBase(url.pathname, base);
    if (relativeUrl === undefined) {
      sendNotFound(response);
      return;
    }

    const requested = decodeURIComponent(relativeUrl);
    const relativePath = requested.endsWith("/") ? `${requested}index.html` : requested;
    const candidate = path.resolve(root, `.${relativePath}`);
    if (candidate !== root && !candidate.startsWith(`${root}${path.sep}`)) {
      sendNotFound(response);
      return;
    }

    let filePath = candidate;
    let fileStat;
    try {
      fileStat = await stat(filePath);
      if (fileStat.isDirectory()) {
        filePath = path.join(filePath, "index.html");
        fileStat = await stat(filePath);
      }
    } catch {
      filePath = path.join(root, "404.html");
      fileStat = await stat(filePath);
      response.statusCode = 404;
    }

    response.setHeader(
      "Content-Type",
      MIME_TYPES.get(path.extname(filePath).toLowerCase()) ?? "application/octet-stream",
    );
    response.setHeader("Content-Length", fileStat.size);
    response.setHeader("Cache-Control", "no-store");
    if (request.method === "HEAD") {
      response.end();
      return;
    }
    createReadStream(filePath).pipe(response);
  } catch (error) {
    response.statusCode = 500;
    response.end(error instanceof Error ? error.message : "Internal server error");
  }
});

server.listen(port, host, () => {
  console.log(`Serving ${root} at http://${host}:${port}${base}`);
});

function parseArgs(values) {
  const parsed = {};
  for (let index = 0; index < values.length; index += 1) {
    const argument = values[index];
    if (argument === "--help" || argument === "-h") {
      parsed.help = true;
      continue;
    }
    if (!argument.startsWith("--")) throw new Error(`Unexpected argument: ${argument}`);
    const name = argument.slice(2);
    const value = values[index + 1];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for ${argument}`);
    parsed[name] = value;
    index += 1;
  }
  return parsed;
}

function normalizeBase(value) {
  const normalized = value.trim().replace(/^\/+|\/+$/g, "");
  return normalized === "" ? "/" : `/${normalized}/`;
}

function parsePort(value) {
  const portNumber = Number.parseInt(value, 10);
  if (!Number.isInteger(portNumber) || portNumber < 1 || portNumber > 65535)
    throw new Error(`Invalid port: ${value}`);
  return portNumber;
}

function stripBase(pathname, basePath) {
  if (basePath === "/") return pathname;
  const withoutTrailingSlash = basePath.slice(0, -1);
  if (pathname === withoutTrailingSlash) return "/";
  if (!pathname.startsWith(basePath)) return undefined;
  return `/${pathname.slice(basePath.length)}`;
}

function sendNotFound(response) {
  response.statusCode = 404;
  response.end("Not found");
}

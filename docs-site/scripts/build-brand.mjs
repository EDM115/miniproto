import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import sharp from "sharp";

const ROOT = path.resolve(import.meta.dirname, "..");
const BRAND = path.join(ROOT, "src", "assets", "brand");
const PUBLIC = path.join(ROOT, "public");
const SOURCE = path.join(BRAND, "concepts", "03-packet-loom", "logo.svg");
const FONT = path.join(BRAND, "fonts", "NunitoSans-ExtraBold-miniproto.woff2");

const options = new Set(process.argv.slice(2));
const checking = options.has("--check");
if (options.has("--help") || options.has("-h")) {
  console.log("Usage: node scripts/build-brand.mjs [--check]");
  console.log("Build or verify the Packet Loom production SVG and social-card derivatives.");
  process.exit(0);
}
for (const option of options) {
  if (option !== "--check") throw new Error(`Unexpected option: ${option}`);
}

const source = await readFile(SOURCE, "utf8");
const fontBase64 = (await readFile(FONT)).toString("base64");
const geometry = source
  .slice(source.indexOf('<g fill="#04474C">'), source.lastIndexOf("</svg>"))
  .trim();
if (!geometry.startsWith("<g") || !geometry.endsWith("/>"))
  throw new Error("Could not isolate the canonical Packet Loom geometry.");

const darkMark = source.replaceAll("#04474C", "#F8FFF5");
const monochromeMark = source
  .replaceAll("#04474C", "currentColor")
  .replaceAll("#C7F406", "currentColor");
const wordmark = buildWordmark({ geometry, fontBase64, dark: false });
const wordmarkDark = buildWordmark({
  geometry: geometry.replaceAll("#04474C", "#F8FFF5"),
  fontBase64,
  dark: true,
});
const socialCard = buildSocialCard({ geometry, fontBase64 });

const outputs = new Map([
  [path.join(BRAND, "logo.svg"), Buffer.from(source)],
  [path.join(BRAND, "logo-dark.svg"), Buffer.from(darkMark)],
  [path.join(BRAND, "mark.svg"), Buffer.from(source)],
  [path.join(BRAND, "mark-monochrome.svg"), Buffer.from(monochromeMark)],
  [path.join(BRAND, "wordmark.svg"), Buffer.from(wordmark)],
  [path.join(BRAND, "wordmark-dark.svg"), Buffer.from(wordmarkDark)],
  [path.join(PUBLIC, "favicon.svg"), Buffer.from(source)],
  [path.join(PUBLIC, "social-card.svg"), Buffer.from(socialCard)],
]);
if (!checking)
  outputs.set(
    path.join(PUBLIC, "social-card.png"),
    await sharp(Buffer.from(socialCard)).png({ compressionLevel: 9, palette: true }).toBuffer(),
  );

const drift = [];
for (const [target, expected] of outputs) {
  let actual;
  try {
    actual = await readFile(target);
  } catch {
    actual = undefined;
  }
  if (actual?.equals(expected)) continue;
  if (checking) {
    drift.push(path.relative(ROOT, target).replaceAll("\\", "/"));
  } else {
    await writeFile(target, expected);
    console.log(`wrote ${path.relative(ROOT, target)}`);
  }
}

if (checking && !(await isExpectedPng(path.join(PUBLIC, "social-card.png"), 1200, 630)))
  drift.push("public/social-card.png");
if (drift.length > 0)
  throw new Error(`Brand derivatives are stale:\n${drift.map((file) => `- ${file}`).join("\n")}`);
if (checking) console.log(`Packet Loom brand derivatives are current (${outputs.size + 1} files).`);

/** Validate the committed raster portably without rerendering fonts through a platform-specific SVG engine. */
async function isExpectedPng(filePath, width, height) {
  let contents;
  try {
    contents = await readFile(filePath);
  } catch {
    return false;
  }
  return (
    contents.length >= 24 &&
    contents.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) &&
    contents.readUInt32BE(16) === width &&
    contents.readUInt32BE(20) === height
  );
}

function buildWordmark({ geometry: markGeometry, fontBase64: font, dark }) {
  const text = dark ? "#F8FFF5" : "#04474C";
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440" viewBox="0 -6.5 1080 440" role="img" aria-labelledby="title description">
  <title id="title">miniproto Packet Loom wordmark</title>
  <desc id="description">The Packet Loom tile mark followed by the miniproto name.</desc>
  <defs><style>@font-face{font-family:MiniprotoNunito;src:url(data:font/woff2;base64,${font}) format('woff2');font-style:normal;font-weight:800}.wordmark{font-family:MiniprotoNunito,sans-serif;font-size:150px;font-weight:800;letter-spacing:-5px}</style></defs>
  <g aria-hidden="true">${markGeometry}</g>
  <text class="wordmark" x="480" y="282" fill="${text}">miniproto</text>
</svg>
`;
}

function buildSocialCard({ geometry: markGeometry, fontBase64: font }) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title description">
  <title id="title">miniproto documentation</title>
  <desc id="description">Packet Loom branding with the miniproto product promise and Alpha status.</desc>
  <defs><style>@font-face{font-family:MiniprotoNunito;src:url(data:font/woff2;base64,${font}) format('woff2');font-style:normal;font-weight:800}.display{font-family:MiniprotoNunito,sans-serif;font-weight:800}</style></defs>
  <rect width="1200" height="630" fill="#082E2C"/>
  <path d="M0 516H1200" stroke="#C7F406" stroke-opacity=".18"/>
  <text class="display" x="78" y="126" fill="#C7F406" font-size="30" letter-spacing="1.5">0.1.0 ALPHA</text>
  <text class="display" x="78" y="258" fill="#F8FFF5" font-size="104" letter-spacing="-4">miniproto</text>
  <text x="84" y="324" fill="#C1D6CF" font-family="system-ui,sans-serif" font-size="31">MTProto, without the framework tax.</text>
  <text data-role="supporting-description" fill="#8EA9A2" font-family="system-ui,sans-serif" font-size="22"><tspan x="84" y="382">Python intent · Layer 228 schema</tspan><tspan x="84" y="416">measured Rust fast paths</tspan></text>
  <g aria-hidden="true" transform="translate(718 90) scale(.98)">${markGeometry}</g>
  <rect data-role="repository-marker" x="78" y="566" width="14" height="14" rx="4" fill="#C7F406"/>
  <text data-role="repository-link" x="110" y="580" fill="#C1D6CF" font-family="ui-monospace,monospace" font-size="18">github.com/EDM115/miniproto</text>
</svg>
`;
}

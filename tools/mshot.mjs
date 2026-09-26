// Screenshot a URL with Puppeteer.
// Usage: node screenshot.mjs http://localhost:3000 [label]
// Saves to "./temporary screenshots/screenshot-N.png" (auto-incremented, never overwritten).
// With a label: "screenshot-N-label.png".
//
// Browser resolution order:
//   1. PUPPETEER_EXECUTABLE_PATH / CHROME_PATH env var
//   2. /opt/pw-browsers/chromium (Claude Code remote sessions)
//   3. Puppeteer's own bundled Chrome
import { mkdir, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const url = process.argv[2];
const label = process.argv[3];
if (!url) {
  console.error('Usage: node screenshot.mjs <url> [label]');
  process.exit(1);
}

const puppeteer = (await import('puppeteer')).default;

const OUT_DIR = join(process.cwd(), 'temporary screenshots');
await mkdir(OUT_DIR, { recursive: true });

const existing = await readdir(OUT_DIR);
let n = 1;
for (const f of existing) {
  const m = f.match(/^screenshot-(\d+)/);
  if (m) n = Math.max(n, Number(m[1]) + 1);
}
const outPath = join(OUT_DIR, `screenshot-${n}${label ? `-${label}` : ''}.png`);

const executablePath =
  process.env.PUPPETEER_EXECUTABLE_PATH ||
  process.env.CHROME_PATH ||
  (existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);

const browser = await puppeteer.launch({
  ...(executablePath ? { executablePath } : {}),
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 800, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  await new Promise((r) => setTimeout(r, 500)); // let fonts/animations settle
  await page.screenshot({ path: outPath, fullPage: true });
  console.log(`Saved ${outPath}`);
} finally {
  await browser.close();
}

// Genera los iconos PWA renderizando un SVG con Chromium. Uso: node tools/icons.mjs
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
import { writeFileSync } from 'node:fs';

const svg = (pad) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <radialGradient id="bg" cx="50%" cy="35%" r="80%"><stop offset="0" stop-color="#1f3a7a"/><stop offset="1" stop-color="#0b1226"/></radialGradient>
    <linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a4d"/><stop offset="1" stop-color="#d12a2a"/></linearGradient>
    <linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#cfd6ea"/></linearGradient>
    <clipPath id="c"><circle cx="256" cy="256" r="${pad}"/></clipPath>
  </defs>
  <rect width="512" height="512" fill="url(#bg)"/>
  <g clip-path="url(#c)">
    <rect x="0" y="0" width="512" height="256" fill="url(#top)"/>
    <rect x="0" y="256" width="512" height="256" fill="url(#bot)"/>
    <rect x="0" y="238" width="512" height="36" fill="#161b2e"/>
  </g>
  <circle cx="256" cy="256" r="${pad}" fill="none" stroke="#161b2e" stroke-width="${pad * 0.09}"/>
  <circle cx="256" cy="256" r="${pad * 0.3}" fill="#161b2e"/>
  <circle cx="256" cy="256" r="${pad * 0.2}" fill="#ffcb05"/>
  <path d="M256 226 l14 22 26 3 -19 17 6 26 -27 -14 -27 14 6 -26 -19 -17 26 -3z" fill="#fff6c2" transform="translate(0,6) scale(.98) translate(5,-4)" opacity=".0"/>
  <g fill="#ffcb05"><path d="M392 92l8 22 22 8-22 8-8 22-8-22-22-8 22-8z"/><path d="M118 118l5 14 14 5-14 5-5 14-5-14-14-5 14-5z" opacity=".8"/></g>
</svg>`;

const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined });
const jobs = [
  ['icon-512.png', 512, 205], ['icon-192.png', 192, 205], ['apple-touch-icon.png', 180, 205], ['icon-32.png', 32, 215],
  ['icon-maskable-512.png', 512, 150],
];
for (const [name, size, r] of jobs) {
  const page = await browser.newPage({ viewport: { width: size, height: size } });
  await page.setContent(`<body style="margin:0;background:transparent">${svg(r).replace('width="512" height="512"', `width="${size}" height="${size}"`)}</body>`);
  writeFileSync(new URL(`../public/icons/${name}`, import.meta.url), await page.screenshot({ type: 'png', omitBackground: false }));
  await page.close();
}
await browser.close();
console.log('iconos generados');

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const root = path.resolve(__dirname);
const source = path.join(root, 'source-dazn');

const out = (name) => path.join(root, name);

function svgOverlay(width, height, body) {
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">${body}</svg>`);
}

async function removeLightBackground(input, background = null) {
  const image = sharp(input).ensureAlpha();
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true });
  const bg = background || { r: data[0], g: data[1], b: data[2] };
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    const distance = Math.hypot(r - bg.r, g - bg.g, b - bg.b);
    if (distance < 34) data[i + 3] = 0;
  }
  return sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toBuffer();
}

async function prepareSources() {
  // The Bundesliga source contains a wordmark beneath the red league mark.
  // At email-icon size the red league mark is the legible, uncluttered identifier.
  const leagueCrop = await sharp(path.join(source, 'german-football.webp'))
    .extract({ left: 40, top: 40, width: 120, height: 95 })
    .png()
    .toBuffer();
  const leagueMark = await removeLightBackground(leagueCrop);

  const ballCrop = await sharp(path.join(source, 'international-football.webp'))
    .extract({ left: 34, top: 34, width: 132, height: 132 })
    .png()
    .toBuffer();
  const ball = await removeLightBackground(ballCrop);

  // The supplied DAZN asset is a horizontal NFL Game Pass lock-up. Keep only
  // the NFL shield, as requested; the wordmark is not used in the card icon.
  const nflShield = await sharp(path.join(source, 'nfl-symbol.webp'))
    .extract({ left: 0, top: 0, width: 205, height: 250 })
    .png()
    .toBuffer();

  const fibaCrop = await sharp(path.join(source, 'fiba-basketball.webp'))
    .extract({ left: 30, top: 58, width: 55, height: 76 })
    .png()
    .toBuffer();
  const fibaIcon = await removeLightBackground(fibaCrop, { r: 244, g: 229, b: 212 });

  return { leagueMark, ball, nflShield, fibaIcon };
}

async function makeIcon(name, base, baseSize, baseLeft, baseTop, overlay) {
  const baseLayer = await sharp(base).resize({ width: baseSize, height: baseSize, fit: 'contain' }).png().toBuffer();
  await sharp({ create: { width: 256, height: 256, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } })
    .composite([
      { input: baseLayer, left: baseLeft, top: baseTop },
      { input: svgOverlay(256, 256, overlay) },
    ])
    .png()
    .toFile(out(name));
}

async function main() {
  const { leagueMark, ball, nflShield, fibaIcon } = await prepareSources();
  const green = '#6DFF8A';
  const dark = '#075434';
  const warm = '#F5F3E8';

  // Plain source-mark versions: no badges, percentages, checkmarks, or
  // progress graphics are added to the supplied sport artwork.
  await makeIcon('football-reward-v8.png', leagueMark, 160, 48, 48, '');
  await makeIcon('football-coupon-v8.png', ball, 180, 38, 38, '');
  await makeIcon('football-discount-v9.png', nflShield, 160, 48, 38, '');
  await makeIcon('sport-six-months-v2.png', fibaIcon, 170, 43, 42, '');

  await makeIcon('football-reward-v7.png', leagueMark, 148, 24, 20,
    `<circle cx="193" cy="194" r="35" fill="${green}" stroke="#10110E" stroke-width="8"/>
     <path d="M177 194l11 11 22-25" fill="none" stroke="#10110E" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>`);

  await makeIcon('football-coupon-v7.png', ball, 170, 43, 20, '');

  await makeIcon('football-discount-v7.png', leagueMark, 148, 24, 20,
    `<circle cx="193" cy="194" r="35" fill="${green}" stroke="#10110E" stroke-width="8"/>
     <text x="193" y="207" text-anchor="middle" font-family="Arial, sans-serif" font-size="36" font-weight="700" fill="#10110E">%</text>`);

  await makeIcon('football-discount-v8.png', nflShield, 146, 26, 19,
    `<circle cx="193" cy="194" r="35" fill="${green}" stroke="#10110E" stroke-width="8"/>
     <text x="193" y="207" text-anchor="middle" font-family="Arial, sans-serif" font-size="36" font-weight="700" fill="#10110E">%</text>`);

  await makeIcon('football-six-months-v7.png', ball, 146, 31, 22,
    `<circle cx="195" cy="196" r="37" fill="${dark}" stroke="${green}" stroke-width="7"/>
     <g fill="${green}"><circle cx="195" cy="172" r="5"/><circle cx="213" cy="178" r="5"/><circle cx="226" cy="193" r="5"/><circle cx="226" cy="212" r="5"/><circle cx="213" cy="227" r="5"/><circle cx="195" cy="232" r="5"/></g>`);

  await makeIcon('sport-six-months-v1.png', fibaIcon, 150, 36, 22,
    `<circle cx="195" cy="194" r="36" fill="${dark}" stroke="${green}" stroke-width="7"/>
     <g fill="${green}"><circle cx="195" cy="171" r="5"/><circle cx="213" cy="177" r="5"/><circle cx="226" cy="193" r="5"/><circle cx="226" cy="211" r="5"/><circle cx="213" cy="226" r="5"/><circle cx="195" cy="231" r="5"/></g>`);

  console.log('created v7 league/football icons');
}

main().catch((error) => { console.error(error); process.exit(1); });

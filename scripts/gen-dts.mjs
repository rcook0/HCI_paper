import fs from 'fs';
import path from 'path';
const [,, src, out] = process.argv;
if (!src || !out) {
  console.error('Usage: node scripts/gen-dts.mjs tokens.json dist/tokens.d.ts');
  process.exit(2);
}
const data = JSON.parse(fs.readFileSync(src, 'utf8'));
const keys = [];
function walk(prefix, obj) {
  for (const k of Object.keys(obj)) {
    const val = obj[k];
    const key = prefix ? `${prefix}.${k}` : k;
    if (val && typeof val === 'object' && !('value' in val)) walk(key, val);
    else if (val && typeof val === 'object' && 'value' in val) keys.push(key);
  }
}
walk('', data);
const union = keys.map(k => `'${k}'`).join(' | ') || 'never';
const dts = `export type TokenName = ${union};\nexport type TokenMap = Record<TokenName, string>;\n`;
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, dts, 'utf8');

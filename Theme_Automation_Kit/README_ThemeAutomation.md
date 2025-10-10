# Theme Automation Kit
## What this is
- JSON tokens -> CSS variables per theme (light/dark/high-contrast)
- Playwright helpers to force theme/scale and capture screenshots

## Quick start
1) Generate CSS:
   ```bash
   python token_to_css.py tokens.themes.json ./css
   ```
   Import `css/themes.css`, then set `<html data-theme="light|dark|high-contrast">`.
2) Screenshot matrix:
   - Place `theming.ts` and `test-theme-matrix.spec.ts` in your tests folder.
   - Set `APP_URL` to your running app URL.
   - Configure `playwright.config.ts` with per-project `use: { deviceScaleFactor }` for 100% and 200%.

## Notes
- High-contrast requires OS-level testing too; this kit covers tokens + emulation path.
- Tokens support `{ref.path}` substitution for aliases.

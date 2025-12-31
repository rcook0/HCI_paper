# UI Screenshot Diff (Playwright template)
**Goal:** catch visual regressions across theme/scale matrices.

## Project expectations
- `npm run test:screenshots` runs Playwright tests that export baseline and current screenshots.
- Store baselines under `tests/__screenshots__/baseline` and current under `artifacts/screenshots`.

## Matrix recommendations
- Light/Dark
- 100% / 200% scale (Win11) and fractional 125/150/200% (Wayland)
- Default fonts + high contrast/forced colors (where supported)

## Tip
Name specs with suffixes like `component.button.light-100.spec.ts` to encode the parameters.

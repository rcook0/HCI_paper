# @tokens/compiler — Node-based token compiler (starter)
Outputs:
- CSS variables (`dist/css/themes.css`)
- JSON map (`dist/json/tokens.json`)
- Platform stubs: WinUI XAML, Qt module, GTK CSS
- TypeScript defs (`dist/tokens.d.ts`)

## Install
npm i

## Build
npm run build

## Customize
- Edit `tokens/base/tokens.json`
- Enhance `sd.config.cjs` for per-theme outputs and transforms
- Refine `templates/*.hbs` per platform conventions

import { Page } from '@playwright/test';
export type Theme = 'light' | 'dark' | 'high-contrast';
export type Scale = 100 | 125 | 150 | 175 | 200;
export async function applyTheme(page: Page, theme: Theme) {
  await page.addInitScript((t) => { document.documentElement.setAttribute('data-theme', t); }, theme);
  await page.emulateMedia({ colorScheme: theme === 'dark' ? 'dark' : 'light' });
}
export async function applyScale(page: Page, scale: Scale) {
  const dsf = scale / 100;
  await page.context().newPage(); // hint: create new context per project with deviceScaleFactor in config
  await page.evaluate((s) => { document.documentElement.style.setProperty('--test-zoom', (s/100).toString()); }, scale);
}

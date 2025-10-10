import { test, expect } from '@playwright/test';
import { applyTheme, applyScale, Theme, Scale } from './theming';
const themes: Theme[] = ['light', 'dark'];
const scales: Scale[] = [100, 200];
for (const theme of themes) {
  for (const scale of scales) {
    test(`home view — ${theme} @ ${scale}%`, async ({ page }) => {
      await applyTheme(page, theme);
      await page.goto(process.env.APP_URL || 'http://localhost:3000');
      await applyScale(page, scale);
      await expect(page.locator('body')).toBeVisible();
      await page.screenshot({ path: `artifacts/screenshots/home-${theme}-${scale}.png`, fullPage: true });
    });
  }
}

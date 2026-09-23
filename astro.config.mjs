// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://seidelbots.com',
  markdown: {
    shikiConfig: { theme: 'css-variables' },
  },
});

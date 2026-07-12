import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  base: '/cpi368-viz/',
  plugins: [svelte()],
  server: {
    // respect the harness-assigned port when 5173 is already taken
    port: Number(process.env.PORT) || 5173,
  },
})

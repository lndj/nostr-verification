import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    // cors: true,
    proxy: {
      '/api': {
        // target: 'https://nostr.lnanddj.repl.co',
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: "../",
  }
});

import viteBasicSslPlugin from "@vitejs/plugin-basic-ssl";
import react from "@vitejs/plugin-react";
import process from "node:process";
import { defineConfig } from "vite";
import type { VitePWAOptions } from "vite-plugin-pwa";
import { VitePWA } from "vite-plugin-pwa";

const pwaOptions: Partial<VitePWAOptions> = {
  mode: "development",
  base: "/",
  includeAssets: ["favicon.svg, /pwa-192x192.png, /pwa-512x512.png"],
  manifest: {
    name: "AI Summary",
    short_name: "AISum",
    description: "AI Summary",
    theme_color: "#254B85",
    display: "standalone",
    display_override: ["window-controls-overlay"],
    icons: [
      {
        src: "pwa-192x192.png", // <== don't add slash, for testing
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/pwa-512x512.png", // <== don't remove slash, for testing
        sizes: "512x512",
        type: "image/png",
      },
      {
        src: "pwa-512x512.png", // <== don't add slash, for testing
        sizes: "512x512",
        type: "image/png",
        purpose: "any maskable",
      },
    ],
  },
  devOptions: {
    enabled: process.env.SW_DEV === "true",
    /* when using generateSW the PWA plugin will switch to classic */
    type: "module",
    navigateFallback: "index.html",
  },
};

export default defineConfig({
  build: {
    sourcemap: process.env.SOURCE_MAP === "true",
  },
  plugins: [react(), VitePWA(pwaOptions), viteBasicSslPlugin()],
  server: {
    host: true,
    strictPort: true,
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
});

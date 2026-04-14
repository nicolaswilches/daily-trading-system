import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

// https://astro.build/config
export default defineConfig({
  site: "https://nicolaswilches.github.io",
  base: "/daily-trading-system",
  trailingSlash: "ignore",
  vite: {
    plugins: [tailwindcss()],
  },
});

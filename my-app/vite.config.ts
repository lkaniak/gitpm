import { defineConfig } from 'vite';
import { resolve } from "path";
import solidPlugin from "vite-plugin-solid";
import suidPlugin from "@suid/vite-plugin";
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [suidPlugin(), solidPlugin(), tsconfigPaths()],
  server: {
    port: 3010,
  },
  build: {
    target: 'esnext',
  },
});

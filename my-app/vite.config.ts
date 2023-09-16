import { defineConfig, loadEnv } from 'vite';
import solidPlugin from "vite-plugin-solid";
import suidPlugin from "@suid/vite-plugin";
import tsconfigPaths from 'vite-tsconfig-paths';


export default ({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return defineConfig({
    define: {
      "process.env": env,
    },
    plugins: [suidPlugin(), solidPlugin(), tsconfigPaths()],
    server: {
      port: 3010,
    },
    build: {
      target: 'esnext',
    },
  });
}

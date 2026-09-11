import react from '@vitejs/plugin-react'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'

const here = path.dirname(fileURLToPath(import.meta.url))
const demoRoot = 'Demo根目录示例'

export default defineConfig({
  plugins: [react()],
  publicDir: path.join(demoRoot, 'public'),
  resolve: {
    alias: {
      '@demo': path.join(demoRoot, 'src'),
      '@app': path.join(here, 'src'),
    },
  },
  server: { port: 5181, strictPort: true },
  preview: { port: 5181, strictPort: true },
})

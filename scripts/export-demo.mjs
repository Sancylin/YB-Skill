#!/usr/bin/env node
import { cp, mkdir, readFile, writeFile, readdir, access } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { spawnSync } from 'node:child_process'

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const [input, output, ...flags] = process.argv.slice(2)
if (!input || !output || flags.some(f => f !== '--verify')) throw new Error('Usage: node scripts/export-demo.mjs <app> <new-output> [--verify]')
const source = path.resolve(input), target = path.resolve(output)
if (target === source || target.startsWith(source + path.sep)) throw new Error('Output must be outside source')
try { await access(target); throw new Error('Output already exists') } catch (e) { if (e.code !== 'ENOENT') throw e }
const ignored = new Set(['node_modules', 'dist', '.git', '.DS_Store'])
await cp(source, target, { recursive: true, filter: p => !ignored.has(path.basename(p)) && !path.basename(p).startsWith('.env') })
const demoRoot = path.join(skillRoot, 'demo')
const vendor = path.join(target, 'vendor', 'yb-library')
await mkdir(vendor, { recursive: true })
await cp(path.join(demoRoot, 'src'), path.join(vendor, 'src'), { recursive: true, filter: p => !ignored.has(path.basename(p)) })
await cp(path.join(demoRoot, 'public'), path.join(vendor, 'public'), { recursive: true })
const config = path.join(target, 'vite.config.ts')
let vite = await readFile(config, 'utf8')
if (!/const demoRoot = .+/.test(vite)) throw new Error('Not a scaffolded app: demoRoot missing')
vite = vite.replace(/const demoRoot = .+/, "const demoRoot = path.join(here, 'vendor/yb-library')")
vite = vite.replace('resolve: {', "resolve: {\n    dedupe: ['react', 'react-dom'],")
await writeFile(config, vite)
const tsPath = path.join(target, 'tsconfig.json')
const ts = JSON.parse(await readFile(tsPath, 'utf8'))
ts.compilerOptions.paths['@demo/*'] = ['vendor/yb-library/src/*']
await writeFile(tsPath, JSON.stringify(ts, null, 2))
const hashes = {}
async function walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) await walk(p)
    else if (entry.isSymbolicLink()) throw new Error('Symlinks are not portable')
    else hashes[path.relative(target,p)] = createHash('sha256').update(await readFile(p)).digest('hex')
  }
}
await walk(vendor)
await writeFile(path.join(target, 'delivery-manifest.json'), JSON.stringify({ schemaVersion: 1, source: 'yb-mobile-design', files: hashes, verifiedBuild: false }, null, 2))
if (flags.includes('--verify')) {
  for (const args of [['install','--package-lock-only','--no-audit','--no-fund'],['ci','--no-audit','--no-fund'],['run','build']]) {
    const result = spawnSync('npm', args, { cwd: target, stdio: 'inherit' })
    if (result.status !== 0) throw new Error(`Verification failed: npm ${args.join(' ')}`)
  }
  await writeFile(path.join(target, 'delivery-manifest.json'), JSON.stringify({ schemaVersion:1, source:'yb-mobile-design', files:hashes, verifiedBuild:true, visualVerification:'not-executed' },null,2))
}
console.log(JSON.stringify({ target, verify: flags.includes('--verify'), note:'Build verification does not prove visual or live Figma parity.' }))

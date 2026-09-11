#!/usr/bin/env node
import { access, cp, mkdir, readFile, rename, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const skillRoot = path.resolve(here, '..')
const templateDir = path.join(skillRoot, 'assets', 'standalone-web-template')
const textExtensions = new Set(['.json', '.ts', '.tsx', '.html', '.md'])

function usage() {
  return '用法：node scripts/scaffold-demo.mjs <slug> --run-dir <task-run-dir> [--demo-root <path>] [--force]'
}

function fail(message) {
  console.error(`${message}\n${usage()}`)
  process.exit(1)
}

function parseArgs(argv) {
  const result = { slug: '', runDir: '', demoRoot: path.join(skillRoot, 'demo'), force: false }
  const rest = [...argv]
  while (rest.length > 0) {
    const token = rest.shift()
    if (token === '--run-dir') {
      result.runDir = rest.shift() ?? ''
    } else if (token === '--demo-root') {
      result.demoRoot = path.resolve(rest.shift() ?? '')
    } else if (token === '--force') {
      result.force = true
    } else if (token.startsWith('--')) {
      fail(`未知参数：${token}`)
    } else if (!result.slug) {
      result.slug = token
    } else {
      fail(`多余参数：${token}`)
    }
  }
  return result
}

function pascalCase(slug) {
  return slug
    .split('-')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join('')
}

async function exists(target) {
  try {
    await access(target)
    return true
  } catch {
    return false
  }
}

async function walk(dir) {
  const { readdir } = await import('node:fs/promises')
  const entries = await readdir(dir, { withFileTypes: true })
  const files = []
  for (const entry of entries) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) files.push(...(await walk(full)))
    else if (entry.isFile()) files.push(full)
  }
  return files
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  if (!args.slug) fail('缺少 slug')
  if (!/^[a-z](?:[a-z0-9-]{0,48}[a-z0-9])?$/.test(args.slug)) {
    fail('slug 必须以小写字母开头，只能包含小写字母、数字和连字符，且必须以字母或数字结尾')
  }
  if (!args.runDir) fail('缺少 --run-dir')
  if (!(await exists(templateDir))) fail(`模板目录不存在：${templateDir}`)
  if (!(await exists(path.join(args.demoRoot, 'src')))) fail(`demo/src 不存在：${args.demoRoot}`)

  const runDir = path.resolve(args.runDir)
  const target = path.join(runDir, 'standalone-web', args.slug)
  if ((await exists(target)) && args.force) fail('为保留已有业务文件，不允许 --force 覆盖；请选择新 slug')
  if ((await exists(target)) && !args.force) fail(`目标已存在：${target}（用 --force 覆盖）`)

  await mkdir(path.dirname(target), { recursive: true })
  await cp(templateDir, target, { recursive: true, force: true })

  const templateScreen = path.join(target, 'src', 'screens', 'example-page.tsx')
  const screenPath = path.join(target, 'src', 'screens', `${args.slug}.tsx`)
  await rename(templateScreen, screenPath)

  const demoPackage = JSON.parse(await readFile(path.join(args.demoRoot, 'package.json'), 'utf8'))
  const lock = JSON.parse(await readFile(path.join(args.demoRoot, 'package-lock.json'), 'utf8'))
  for (const group of ['dependencies', 'devDependencies']) {
    for (const name of Object.keys(demoPackage[group] ?? {})) {
      const version = lock.packages?.[`node_modules/${name}`]?.version
      if (!version) fail(`锁文件缺少精确版本：${name}`)
      demoPackage[group][name] = version
    }
  }
  const versions = {
    React版本: demoPackage.dependencies?.react,
    ReactDOM版本: demoPackage.dependencies?.['react-dom'],
    Node类型版本: demoPackage.devDependencies?.['@types/node'],
    React类型版本: demoPackage.devDependencies?.['@types/react'],
    ReactDOM类型版本: demoPackage.devDependencies?.['@types/react-dom'],
    React插件版本: demoPackage.devDependencies?.['@vitejs/plugin-react'],
    TypeScript版本: demoPackage.devDependencies?.typescript,
    Vite版本: demoPackage.devDependencies?.vite,
  }
  for (const [key, value] of Object.entries(versions)) {
    if (!value) fail(`demo/package.json 缺少依赖版本：${key}`)
  }

  const replacements = {
    'example-page': args.slug,
    组件名示例: pascalCase(args.slug),
    Demo根目录示例: args.demoRoot.split(path.sep).join('/'),
    Demo源码目录示例: path.join(args.demoRoot, 'src').split(path.sep).join('/'),
    ...versions,
  }
  for (const file of await walk(target)) {
    if (!textExtensions.has(path.extname(file))) continue
    let text = await readFile(file, 'utf8')
    for (const [key, value] of Object.entries(replacements)) text = text.split(key).join(value)
    await writeFile(file, text)
  }

  console.log(
    JSON.stringify(
      {
        slug: args.slug,
        target,
        demoRoot: args.demoRoot,
        next: [`cd ${target}`, 'npm install', 'npm run dev'],
      },
      null,
      2,
    ),
  )
}

main().catch((error) => fail(error instanceof Error ? error.message : String(error)))

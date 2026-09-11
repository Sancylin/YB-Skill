import { readFileSync, writeFileSync } from 'node:fs'

const source = readFileSync(new URL('../src/generated/assets.ts', import.meta.url), 'utf8')
const assets = [...source.matchAll(/"name": "([^"]+)",\s*"nodeId": "([^"]+)"[\s\S]*?"isIcon": (true|false)/g)].map(
  ([, name, nodeId, isIcon]) => ({ name, nodeId, isIcon: isIcon === 'true' }),
)

const icons = assets.filter((asset) => asset.isIcon).map((asset) => ({
  name: asset.name,
  nodeId: asset.nodeId,
  file: `icons/${asset.nodeId.replaceAll(':', '-')}.svg`,
}))

const previews = assets.filter((asset) => !asset.isIcon).map((asset) => ({
  name: asset.name,
  nodeId: asset.nodeId,
  file: `previews/${asset.nodeId.replaceAll(':', '-')}.png`,
}))

writeFileSync(
  new URL('../public/previews/manifest.json', import.meta.url),
  `${JSON.stringify({ fileKey: 'iUyH8VSdURxlGrhp646zYJ', icons, previews }, null, 2)}\n`,
)

console.log(`Wrote manifest for ${icons.length} icons and ${previews.length} component previews`)

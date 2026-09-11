import { mkdir, readFile, rm, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(here, '..')
const inventoryPath =
  process.env.INVENTORY_PATH ??
  path.join(root, 'data', 'figma-components.json')
const snapshotPath =
  process.env.SNAPSHOT_PATH ??
  path.join(root, 'data', 'figma-snapshot-manifest.json')
const generatedFilesManifestPath = path.join(root, 'src', '.generated-assets-manifest.json')
const inventory = JSON.parse(await readFile(inventoryPath, 'utf8'))
const snapshot = JSON.parse(await readFile(snapshotPath, 'utf8'))

if (!Array.isArray(inventory) || inventory.length === 0) {
  throw new Error(`Expected a non-empty published asset inventory, received ${inventory?.length ?? 'invalid data'}`)
}

const fileKey = snapshot.fileKey
if (!fileKey) throw new Error('Snapshot manifest is missing fileKey')
if (snapshot.assetCount !== inventory.length) {
  console.warn(`Asset inventory drift: snapshot expects ${snapshot.assetCount}, received ${inventory.length}`)
}

const nodeIds = new Set()
const assetKeys = new Set()
for (const asset of inventory) {
  if (!asset?.nodeId || !asset?.assetKey || !asset?.name) throw new Error('Every asset needs name, nodeId and assetKey')
  if (nodeIds.has(asset.nodeId)) throw new Error(`Duplicate nodeId: ${asset.nodeId}`)
  if (assetKeys.has(asset.assetKey)) throw new Error(`Duplicate assetKey: ${asset.assetKey}`)
  nodeIds.add(asset.nodeId)
  assetKeys.add(asset.assetKey)
}

const chineseNames = new Map([
  ['卡片', 'Card'],
  ['状态', 'Status'],
  ['蓝色', 'Blue'],
  ['弹窗组件', 'Dialog'],
  ['ipad 模板', 'IPadTemplate'],
  ['展示方式', 'displayMode'],
  ['附件类型', 'attachmentType'],
  ['内容', 'content'],
])

const reserved = new Set([
  'break',
  'case',
  'catch',
  'class',
  'const',
  'continue',
  'debugger',
  'default',
  'delete',
  'do',
  'else',
  'enum',
  'export',
  'extends',
  'false',
  'finally',
  'for',
  'function',
  'if',
  'implements',
  'import',
  'in',
  'instanceof',
  'interface',
  'let',
  'new',
  'null',
  'package',
  'private',
  'protected',
  'public',
  'return',
  'static',
  'super',
  'switch',
  'this',
  'throw',
  'true',
  'try',
  'typeof',
  'var',
  'void',
  'while',
  'with',
  'yield',
])

function asciiWords(value) {
  return value
    .normalize('NFKD')
    .replace(/[\u200B-\u200D\uFEFF]/g, '')
    .match(/[A-Za-z0-9]+/g) ?? []
}

function pascal(value) {
  const mapped = chineseNames.get(value)
  const words = asciiWords(mapped ?? value)
  const result = words
    .map((word) => `${word.charAt(0).toUpperCase()}${word.slice(1)}`)
    .join('')
  return result && !/^\d/.test(result) ? result : `Asset${result}`
}

function camel(value) {
  const mapped = chineseNames.get(value)
  const words = asciiWords(mapped ?? value)
  let result = words
    .map((word, index) =>
      index === 0
        ? `${word.charAt(0).toLowerCase()}${word.slice(1)}`
        : `${word.charAt(0).toUpperCase()}${word.slice(1)}`,
    )
    .join('')
  if (!result) result = 'content'
  if (/^\d/.test(result) || reserved.has(result)) result = `prop${pascal(result)}`
  return result
}

const bases = inventory.map((asset) => {
  const internal = asset.name.startsWith('.') || asset.name.startsWith('_')
  return `${internal ? 'Internal' : ''}${pascal(asset.name)}`
})
const baseCounts = new Map()
for (const base of bases) baseCounts.set(base, (baseCounts.get(base) ?? 0) + 1)

const assets = inventory.map((asset, index) => {
  const base = bases[index]
  const suffix = asset.nodeId.replace(':', '_')
  const componentName = (baseCounts.get(base) ?? 0) > 1 ? `${base}_${suffix}` : base
  const usedProps = new Set()
  const properties = Object.entries(asset.properties ?? {}).map(([figmaName, value]) => {
    let reactProp = camel(figmaName)
    let counter = 2
    while (usedProps.has(reactProp)) reactProp = `${camel(figmaName)}${counter++}`
    usedProps.add(reactProp)
    return {
      figmaName,
      reactProp,
      type: value.type,
      defaultValue: value.defaultValue,
      variantOptions: value.variantOptions ?? [],
    }
  })
  return {
    ...asset,
    componentName,
    properties,
    isIcon: asset.pageId === '1:2' || /^Icon(?:\s*\/|$)/i.test(asset.name),
    isInternal: asset.name.startsWith('.') || asset.name.startsWith('_'),
  }
})

const componentNames = new Set(assets.map((asset) => asset.componentName))
if (componentNames.size !== assets.length) {
  throw new Error('Generated component names are not unique')
}

function literal(value) {
  return JSON.stringify(value, null, 2)
}

function propType(property) {
  if (property.type === 'BOOLEAN') return 'boolean'
  if (property.type === 'SLOT') return 'ReactNode'
  if (property.type === 'VARIANT' && property.variantOptions.length) {
    return property.variantOptions.map((option) => JSON.stringify(option)).join(' | ')
  }
  return 'string'
}

function templateSource(asset) {
  const declarations = []
  const attributes = []
  const slotChildren = []

  for (const property of asset.properties) {
    const variable = `prop_${property.reactProp}`
    if (property.type === 'VARIANT') {
      const enumMap = Object.fromEntries(
        property.variantOptions.map((option) => [option, option]),
      )
      declarations.push(
        `const ${variable} = instance.getEnum(${JSON.stringify(property.figmaName)}, ${JSON.stringify(enumMap, null, 2)})`,
      )
      attributes.push(`${property.reactProp}="\${${variable}}"`)
    } else if (property.type === 'BOOLEAN') {
      declarations.push(
        `const ${variable} = instance.getBoolean(${JSON.stringify(property.figmaName)})`,
      )
      attributes.push(`\${${variable} ? ${JSON.stringify(property.reactProp)} : ''}`)
    } else if (property.type === 'SLOT') {
      declarations.push(
        `const ${variable} = instance.getSlot(${JSON.stringify(property.figmaName)})`,
      )
      attributes.push(
        `\${${variable} ? figma.code\` ${property.reactProp}={\${${variable}}}\` : ''}`,
      )
      slotChildren.push(variable)
    }
  }

  const commentUrl = `https://www.figma.com/design/${fileKey}/Yuanbao-Mobile-Components?node-id=${asset.nodeId.replace(':', '-')}`
  const source = 'src/generated/components.tsx'
  const attrs = attributes.length ? ` ${attributes.join(' ')}` : ''
  const nestable = asset.isIcon || asset.isInternal
  const propsMetadata = Object.fromEntries(
    asset.properties.map((property) => [
      property.reactProp,
      {
        figmaName: property.figmaName,
        type: property.type,
        options: property.variantOptions,
      },
    ]),
  )
  return `// url=${commentUrl}
// source=${source}
// component=${asset.componentName}
import figma from 'figma'

${declarations.length ? `const instance = figma.selectedInstance\n${declarations.join('\n')}` : ''}

export default {
  example: figma.code\`<${asset.componentName}${attrs} />\`,
  imports: ['import { ${asset.componentName} } from "./src/generated/components"'],
  id: ${JSON.stringify(`yb-${asset.nodeId.replace(':', '-')}`)},
  metadata: {
    nestable: ${nestable},
    props: ${JSON.stringify(propsMetadata, null, 2)},
  },
}
`
}

const generatedDirectory = path.join(root, 'src/generated')
const figmaDirectory = path.join(root, 'src/figma')
await mkdir(generatedDirectory, { recursive: true })
await mkdir(figmaDirectory, { recursive: true })

let previousGeneratedFiles = []
try {
  const previous = JSON.parse(await readFile(generatedFilesManifestPath, 'utf8'))
  previousGeneratedFiles = Array.isArray(previous.files) ? previous.files : []
} catch {
  // First generation or an older generator without a file manifest.
}

const catalogSource = `/* This file is generated by scripts/generate-assets.mjs. */
export type FigmaPropertyType = 'BOOLEAN' | 'SLOT' | 'VARIANT'

export interface AssetPropertyDefinition {
  readonly figmaName: string
  readonly reactProp: string
  readonly type: FigmaPropertyType
  readonly defaultValue: string | boolean
  readonly variantOptions: readonly string[]
}

export interface AssetDefinition {
  readonly name: string
  readonly nodeId: string
  readonly type: 'COMPONENT' | 'COMPONENT_SET'
  readonly pageId: string
  readonly pageName: string
  readonly assetKey: string
  readonly componentName: string
  readonly properties: readonly AssetPropertyDefinition[]
  readonly isIcon: boolean
  readonly isInternal: boolean
}

export const assetCatalog = ${literal(
  assets.map(
    ({
      name,
      nodeId,
      type,
      pageId,
      pageName,
      assetKey,
      componentName,
      properties,
      isIcon,
      isInternal,
    }) => ({
      name,
      nodeId,
      type,
      pageId,
      pageName,
      assetKey,
      componentName,
      properties,
      isIcon,
      isInternal,
    }),
  ),
)} as const satisfies readonly AssetDefinition[]

export const assetByNodeId = new Map(assetCatalog.map((asset) => [asset.nodeId, asset]))
`
await writeFile(path.join(generatedDirectory, 'assets.ts'), catalogSource)

const componentsSource = `/* This file is generated by scripts/generate-assets.mjs. */
import type { ReactNode } from 'react'
import { AssetRenderer } from '../components/AssetRenderer'
import type { CommonAssetProps } from '../components/types'
import { assetByNodeId } from './assets'

${assets
  .map((asset) => {
    const props = asset.properties
      .map(
        (property) =>
          `  /** Figma: ${property.figmaName} (${property.type}) */\n  ${property.reactProp}?: ${propType(property)}`,
      )
      .join('\n')
    return `export interface ${asset.componentName}Props extends CommonAssetProps {
${props}
}

export function ${asset.componentName}(props: ${asset.componentName}Props) {
  const asset = assetByNodeId.get(${JSON.stringify(asset.nodeId)})
  if (!asset) return null
  return <AssetRenderer asset={asset} values={props} />
}`
  })
  .join('\n\n')}

export const generatedComponentCount = ${assets.length}
`
await writeFile(path.join(generatedDirectory, 'components.tsx'), componentsSource)
await writeFile(
  path.join(generatedDirectory, 'index.ts'),
  `export * from './assets'\nexport * from './components'\n`,
)

const mappings = []
for (const asset of assets) {
  const filename = `${asset.componentName}.figma.ts`
  const template = templateSource(asset)
  await writeFile(path.join(figmaDirectory, filename), template)
  const templateData = {
    isParserless: true,
    nestable: asset.isIcon || asset.isInternal,
    imports: [`import { ${asset.componentName} } from "./src/generated/components"`],
    props: Object.fromEntries(
      asset.properties.map((property) => [
        property.reactProp,
        {
          figmaName: property.figmaName,
          type: property.type,
          options: property.variantOptions,
        },
      ]),
    ),
  }
  mappings.push({
    nodeId: asset.nodeId,
    pageId: asset.pageId,
    pageName: asset.pageName,
    componentName: asset.componentName,
    source: `src/generated/components.tsx`,
    label: 'React Demo',
    template,
    templateDataJson: JSON.stringify(templateData),
  })
}

await writeFile(
  path.join(root, 'code-connect-mappings.json'),
  `${JSON.stringify(mappings, null, 2)}\n`,
)

const generatedFiles = [
  'src/generated/assets.ts',
  'src/generated/components.tsx',
  'src/generated/index.ts',
  'code-connect-mappings.json',
  ...assets.map((asset) => `src/figma/${asset.componentName}.figma.ts`),
]
const currentGeneratedFiles = new Set(generatedFiles)
for (const relativePath of previousGeneratedFiles) {
  if (currentGeneratedFiles.has(relativePath)) continue
  if (path.isAbsolute(relativePath) || relativePath.startsWith('..')) {
    console.warn(`Ignoring unsafe generated path from manifest: ${relativePath}`)
    continue
  }
  const absolutePath = path.join(root, relativePath)
  if (absolutePath === generatedFilesManifestPath) continue
  await rm(absolutePath, { force: true })
}
await writeFile(
  generatedFilesManifestPath,
  `${JSON.stringify({ schemaVersion: 1, inventoryPath: path.relative(root, inventoryPath), files: generatedFiles }, null, 2)}\n`,
)

console.log(
  JSON.stringify(
    {
      assets: assets.length,
      templates: mappings.length,
      componentSets: assets.filter((asset) => asset.type === 'COMPONENT_SET').length,
      components: assets.filter((asset) => asset.type === 'COMPONENT').length,
      icons: assets.filter((asset) => asset.isIcon).length,
      properties: assets.reduce((total, asset) => total + asset.properties.length, 0),
    },
    null,
    2,
  ),
)

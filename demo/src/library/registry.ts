import type { AssetDefinition } from '../generated/assets'

export { LibraryRenderer } from './LibraryRenderer'
export { FigmaPreview } from './FigmaPreview'
export { PreviewCanvas } from './PreviewCanvas'
export { Icon } from './Icon'

export function registryKey(asset: AssetDefinition) {
  return asset.assetKey
}

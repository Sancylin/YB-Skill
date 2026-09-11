import { useState } from 'react'
import { previewSrc } from './helpers'

interface FigmaPreviewProps {
  nodeId: string
  variantKey?: string
  alt: string
  className?: string
}

export function FigmaPreview({ nodeId, variantKey, alt, className }: FigmaPreviewProps) {
  const [failed, setFailed] = useState(false)
  const [usedFallback, setUsedFallback] = useState(false)
  const src = usedFallback || !variantKey ? previewSrc(nodeId) : previewSrc(nodeId, variantKey)

  if (failed) return null

  return (
    <img
      alt={alt}
      className={className ?? 'yb-figma-preview'}
      onError={() => {
        if (variantKey && !usedFallback) {
          setUsedFallback(true)
          return
        }
        setFailed(true)
      }}
      src={src}
    />
  )
}

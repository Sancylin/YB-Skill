import { type CSSProperties, useState } from 'react'
import { FigmaPreview } from './FigmaPreview'
import { iconSlug, nodeFileId } from './helpers'

interface IconProps {
  name: string
  nodeId?: string
  size?: number
  className?: string
  label?: string
  decorative?: boolean
}

const SPECIAL_FILES: Record<string, string> = {
  'Icon/sidebar-menu': 'sidebar-menu',
  'Icon/Search': 'search',
  'Icon/chevron-left': 'chevron-left',
  'Icon/chevron-right': 'chevron-right',
  'Icon/close-sm': 'close-sm',
  'Icon/close-lg': 'close-lg',
  'Icon/done': 'done',
  'Icon/More': 'more',
  'Icon/Plus': 'plus',
  'Icon/Volume': 'volume',
  'Icon/Call': 'call',
  'Icon/share': 'share',
  'Icon/ArrowUpRight': 'arrowupright',
  'Icon/Setting': 'setting',
  'Icon/Download': 'download',
  'Icon/CreatePic': '5244-14698',
  'Icon/VideoAI': '5244-14664',
  'Icon/live': '6589-2642',
  'Icon/Trash': 'trash',
  'Icon/Clock': 'clock',
  'Icon/link': 'link',
  'Icon/Camera': 'camera',
  'Icon/Rotate': 'rotate',
  'Icon/chevron-up': 'chevron-up',
  'Icon/chevron-down': 'chevron-down',
  'Icon/A': 'a-64-2291',
  'Icon/TemporaryChat': 'temporarychat',
  'Icon/Expand': 'expand',
  'Icon/PicturePlus': '5357-2080',
  'Icon/SmartPictures': '5357-2705',
}

export function iconSrc(name: string, nodeId?: string) {
  if (nodeId) return `/icons/${nodeFileId(nodeId)}.svg`
  const special = SPECIAL_FILES[name]
  const slug = special ?? iconSlug(name)
  return `/icons/${slug}.svg`
}

export function Icon({ name, nodeId, size = 24, className, label, decorative }: IconProps) {
  const [failed, setFailed] = useState(false)
  const src = iconSrc(name, nodeId)
  const mergedClass = ['yb-icon', className].filter(Boolean).join(' ')
  const box: CSSProperties = { height: size, width: size }
  const mask: CSSProperties = {
    ...box,
    WebkitMaskImage: `url("${src}")`,
    WebkitMaskPosition: 'center',
    WebkitMaskRepeat: 'no-repeat',
    WebkitMaskSize: 'contain',
    maskImage: `url("${src}")`,
    maskPosition: 'center',
    maskRepeat: 'no-repeat',
    maskSize: 'contain',
  }

  if (failed && nodeId) {
    return <FigmaPreview alt={label ?? name} className={mergedClass} nodeId={nodeId} />
  }

  if (failed) {
    return <span aria-hidden={decorative || undefined} className={mergedClass} style={box} />
  }

  return (
    <span
      aria-hidden={decorative || undefined}
      aria-label={decorative ? undefined : label ?? name}
      className={mergedClass}
      data-icon-name={name}
      role={decorative ? undefined : 'img'}
      style={mask}
    >
      <img alt="" aria-hidden className="yb-icon-probe" height={0} onError={() => setFailed(true)} src={src} width={0} />
    </span>
  )
}

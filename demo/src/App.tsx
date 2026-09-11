import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import { applyCatalogAction, clampCatalogValues } from './library/catalogActions'
import { Icon } from './library/Icon'
import { PropertySelect } from './library/PropertySelect'
import { LibraryRenderer } from './library/LibraryRenderer'
import {
  PreviewCanvas,
  formatZoomPercent,
  stepZoom,
  type PreviewZoom,
} from './library/PreviewCanvas'
import { slotPickerAssets } from './library/slotAssets'
import type { AssetDefinition } from './generated/assets'
import { fullCatalog as assetCatalog, type CatalogAsset } from './library/catalog'
import { screenRegistry } from './screens/registry'

type EditableValue = string | boolean
type AssetFilter = 'all' | 'component' | 'icon'

function defaultsFor(asset: AssetDefinition) {
  return Object.fromEntries(
    asset.properties.map((property) => [property.reactProp, property.defaultValue]),
  ) as Record<string, EditableValue>
}

function jsxFor(asset: AssetDefinition, values: Record<string, EditableValue>) {
  const props = asset.properties
    .map((property) => {
      const value = values[property.reactProp]
      if (property.type === 'BOOLEAN') {
        if (value) return `  ${property.reactProp}`
        return property.defaultValue ? `  ${property.reactProp}={false}` : null
      }
      if (property.type === 'SLOT') {
        return value && value !== '-1:-1'
          ? `  ${property.reactProp}={${JSON.stringify(String(value))}}`
          : null
      }
      return `  ${property.reactProp}=${JSON.stringify(String(value))}`
    })
    .filter(Boolean)

  return props.length
    ? `<${asset.componentName}\n${props.join('\n')}\n/>`
    : `<${asset.componentName} />`
}

function pageLabel(pageName: string) {
  return pageName.replace(/^✅\s*/, '')
}

function readInitialAsset(catalog: AssetDefinition[]) {
  const nodeId = new URLSearchParams(window.location.search).get('asset')
  return catalog.find((asset) => asset.nodeId === nodeId)
    ?? catalog.find((asset) => asset.componentName === 'Button')
    ?? catalog[0]
}

export default function App() {
  const publicCatalog = useMemo(() => assetCatalog.filter((asset) => !asset.isInternal), [])
  const initialAsset = readInitialAsset(publicCatalog)
  const [query, setQuery] = useState('')
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const [assetFilter, setAssetFilter] = useState<AssetFilter>('all')
  const [openGroup, setOpenGroup] = useState<string | null>(initialAsset.pageName)
  const [selectedNodeId, setSelectedNodeId] = useState(initialAsset.nodeId)
  const selected =
    publicCatalog.find((asset) => asset.nodeId === selectedNodeId) ?? publicCatalog[0]
  const [values, setValues] = useState<Record<string, EditableValue>>(() =>
    defaultsFor(initialAsset),
  )
  const [copied, setCopied] = useState(false)
  const [linkCopied, setLinkCopied] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [pane, setPane] = useState<'catalog' | 'preview' | 'properties'>('preview')
  const [codeOpen, setCodeOpen] = useState(true)
  const [zoom, setZoom] = useState<PreviewZoom>('fit')
  const [fitScale, setFitScale] = useState(1)
  const [favorites, setFavorites] = useState<Set<string>>(() => {
    try {
      const saved: unknown = JSON.parse(localStorage.getItem('yb-catalog-favorites') ?? '[]')
      return new Set<string>(Array.isArray(saved) ? saved.filter((id) => typeof id === 'string') : [])
    } catch {
      return new Set()
    }
  })
  const pressTimer = useRef<number>(0)
  const copyTimer = useRef<number>(0)
  const searchRef = useRef<HTMLInputElement>(null)
  const selectedRef = useRef(selected)

  useEffect(() => {
    try {
      localStorage.setItem('yb-catalog-favorites', JSON.stringify([...favorites]))
    } catch {
      // Browsers with disabled storage can still keep favorites for this session.
    }
  }, [favorites])

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        searchRef.current?.focus()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.clearTimeout(pressTimer.current)
      window.clearTimeout(copyTimer.current)
    }
  }, [])

  async function copyText(text: string, kind: 'code' | 'link') {
    window.clearTimeout(copyTimer.current)
    setCopied(false)
    setLinkCopied(false)
    try {
      await navigator.clipboard.writeText(text)
      setCopied(kind === 'code')
      setLinkCopied(kind === 'link')
      setFeedback(kind === 'code' ? '代码已复制' : '组件链接已复制')
    } catch {
      setFeedback('无法访问剪贴板，请检查浏览器权限')
    }
    copyTimer.current = window.setTimeout(() => {
      setCopied(false)
      setLinkCopied(false)
      setFeedback('')
    }, 2400)
  }

  function handleAction(action: string) {
    const asset = selectedRef.current
    if (action === 'press' && asset.name === 'Button 按钮') {
      window.clearTimeout(pressTimer.current)
      setValues((current) => applyCatalogAction(asset, 'press', current))
      pressTimer.current = window.setTimeout(() => {
        if (selectedRef.current.nodeId !== asset.nodeId) return
        setValues((current) => applyCatalogAction(asset, 'press-end', current))
      }, 160)
      return
    }
    setValues((current) => applyCatalogAction(asset, action, current))
  }

  const visibleCatalog = useMemo(() => {
    const normalized = query.trim().toLowerCase()
    return publicCatalog.filter((asset) => {
      const matchesType =
        assetFilter === 'all' ||
        (assetFilter === 'icon' ? asset.isIcon : !asset.isIcon)
      if (!matchesType) return false
      if (!normalized) return true
      return (
        asset.name.toLowerCase().includes(normalized) ||
        asset.componentName.toLowerCase().includes(normalized) ||
        asset.pageName.toLowerCase().includes(normalized) ||
        asset.nodeId.includes(normalized)
      )
    })
  }, [assetFilter, publicCatalog, query])

  const filteredGroups = useMemo(() => {
    const groups = new Map<string, CatalogAsset[]>()
    for (const asset of visibleCatalog) {
      const current = groups.get(asset.pageName) ?? []
      current.push(asset)
      groups.set(asset.pageName, current)
    }
    return [...groups.entries()].sort(([, a], [, b]) => Number(a[0].isIcon) - Number(b[0].isIcon))
  }, [visibleCatalog])

  const favoriteAssets = useMemo(
    () => publicCatalog.filter((asset) => favorites.has(asset.nodeId)),
    [favorites, publicCatalog],
  )
  const componentCount = publicCatalog.filter((asset) => !asset.isIcon).length
  const iconCount = publicCatalog.length - componentCount
  const snippet = jsxFor(selected, values)
  const displayedGroup = openGroup === null ? null :
    filteredGroups.some(([name]) => name === openGroup) ? openGroup : filteredGroups[0]?.[0]

  function selectAsset(asset: CatalogAsset) {
    window.clearTimeout(pressTimer.current)
    selectedRef.current = asset
    setSelectedNodeId(asset.nodeId)
    setOpenGroup(asset.pageName)
    setValues(defaultsFor(asset))
    setCopied(false)
    setLinkCopied(false)
    setPane('preview')
    setZoom('fit')
    const url = new URL(window.location.href)
    url.searchParams.set('asset', asset.nodeId)
    window.history.replaceState({}, '', url)
  }

  function toggleFavorite() {
    setFavorites((current) => {
      const next = new Set(current)
      if (next.has(selected.nodeId)) next.delete(selected.nodeId)
      else next.add(selected.nodeId)
      return next
    })
  }

  function renderAssetButton(asset: CatalogAsset) {
    const isSelected = asset.nodeId === selected.nodeId
    return (
      <button
        aria-current={isSelected ? 'true' : undefined}
        className={isSelected ? 'selected' : ''}
        data-asset-name={asset.name}
        key={asset.nodeId}
        onClick={() => selectAsset(asset)}
        title={asset.name}
        type="button"
      >
        <span className="asset-icon">
          {asset.isIcon ? (
            <Icon decorative name={asset.name} nodeId={asset.nodeId} size={16} />
          ) : (
            <span className="component-glyph" />
          )}
        </span>
        <span className="asset-name">{asset.name}</span>
        {favorites.has(asset.nodeId) && <span className="favorite-dot" />}
      </button>
    )
  }

  const propertyGroups = useMemo(
    () => [
      ['变体', selected.properties.filter((property) => property.type === 'VARIANT')],
      ['开关', selected.properties.filter((property) => property.type === 'BOOLEAN')],
      ['插槽', selected.properties.filter((property) => property.type === 'SLOT')],
    ] as const,
    [selected],
  )

  function propertyVisible(property: AssetDefinition['properties'][number]) {
    if (
      selected.name === '卡片' &&
      (property.reactProp === 'file' || property.reactProp === 'state')
    ) return String(values.card ?? 'File') === 'File'
    if (selected.name === 'Markdown' && property.reactProp === 'videoType') {
      return String(values.variant ?? 'prompt') === 'video'
    }
    if (selected.name === 'FeatureSheet' && property.reactProp === 'focus') {
      return Boolean(values.indicator)
    }
    if (selected.name === 'bottomSheet' && property.reactProp === 'navbarPosition') {
      return String(values.navbarType ?? 'default') !== 'tabCard'
    }
    if (selected.name === 'shareSheet' && property.reactProp === 'description') {
      return String(values.shareSheet ?? 'Dialogue Share') === 'Dialogue Share'
    }
    if (
      selected.name === 'Toast' &&
      ['actionButton', 'icon', 'iconSlot', 'arrowIcon'].includes(property.reactProp)
    ) return String(values.type ?? 'Default') === 'Vertical'
    return true
  }

  return (
    <div className="catalog-app" data-theme={theme} data-pane={pane} translate="no">
      <header className="topbar">
        <div className="brand">
          <img className="brand-mark" src="/yuanbao-brand.svg" alt="元宝" width={36} height={36} />
          <div><strong>元宝移动端</strong><small>Design System</small></div>
        </div>

        <label className="catalog-search">
          <Icon decorative name="Icon/Search" size={17} />
          <input
            aria-label="搜索组件"
            onChange={(event) => {
              setQuery(event.target.value)
              setOpenGroup(selected.pageName)
              if (window.matchMedia('(max-width: 900px)').matches) setPane('catalog')
            }}
            onKeyDown={(event) => {
              if (event.key === 'Escape') setQuery('')
              if (event.key === 'Enter' && visibleCatalog[0]) selectAsset(visibleCatalog[0])
            }}
            placeholder="搜索组件、导出名或 Node ID"
            ref={searchRef}
            value={query}
          />
          {query && (
            <button aria-label="清除搜索" onClick={() => setQuery('')} type="button">
              <Icon decorative name="Icon/close-sm" size={16} />
            </button>
          )}
        </label>

        <div className="topbar-actions">
          <div className="asset-filter" aria-label="资产类型">
            {([
              ['all', '全部'],
              ['component', '组件'],
              ['icon', '图标'],
            ] as const).map(([value, label]) => (
              <button
                aria-pressed={assetFilter === value}
                className={assetFilter === value ? 'active' : ''}
                key={value}
                onClick={() => setAssetFilter(value)}
                type="button"
              >
                {label}
              </button>
            ))}
          </div>
          <div className="theme-switch" role="group" aria-label="预览主题">
            {(['light', 'dark'] as const).map((value) => (
              <button
                aria-pressed={theme === value}
                className={theme === value ? 'active' : ''}
                key={value}
                onClick={() => setTheme(value)}
                type="button"
              >{value === 'light' ? '浅色' : '深色'}</button>
            ))}
          </div>
        </div>
      </header>

      <nav className="mobile-tabs" aria-label="工作台视图">
        {([
          ['catalog', '组件目录'],
          ['preview', '组件预览'],
          ['properties', '属性设置'],
        ] as const).map(([value, label]) => (
          <button key={value} type="button" aria-pressed={pane === value} onClick={() => setPane(value)}>
            {label}
          </button>
        ))}
      </nav>

      <div className="workspace">
        <aside className="sidebar">
          <div className="sidebar-overview">
            <div><strong>{publicCatalog.length}</strong><span>公开资产</span></div>
            <div><strong>{componentCount}</strong><span>组件</span></div>
            <div><strong>{iconCount}</strong><span>图标</span></div>
          </div>

          <div className="mobile-asset-filter asset-filter" role="group" aria-label="移动端资产类型">
            {([
              ['all', '全部'],
              ['component', '组件'],
              ['icon', '图标'],
            ] as const).map(([value, label]) => (
              <button
                aria-pressed={assetFilter === value}
                className={assetFilter === value ? 'active' : ''}
                key={value}
                onClick={() => setAssetFilter(value)}
                type="button"
              >{label}</button>
            ))}
          </div>

          <div className="sidebar-scroll">
            <nav aria-label="页面 Demo" className="screen-links">
              <div className="section-label">
                <span>页面 Demo</span><small>{Object.keys(screenRegistry).length}</small>
              </div>
              {Object.entries(screenRegistry).map(([screenId, screen]) => (
                <a href={`?screen=${screenId}`} key={screenId}>
                  <span className="screen-link-icon">
                    <Icon decorative name="Icon/ArrowUpRight" size={15} />
                  </span>
                  <span>{screen.title}</span>
                  <Icon decorative name="Icon/chevron-right" size={14} />
                </a>
              ))}
            </nav>

            {favoriteAssets.length > 0 && !query && assetFilter === 'all' && (
              <div className="favorite-assets">
                <div className="section-label">
                  <span>收藏</span><small>{favoriteAssets.length}</small>
                </div>
                {favoriteAssets.map(renderAssetButton)}
              </div>
            )}

            <div className="component-tree">
              <div className="section-label">
                <span>组件目录</span><small>{visibleCatalog.length}</small>
              </div>
              {filteredGroups.length === 0 ? (
                <div className="empty-search">
                  <Icon decorative name="Icon/Search" size={20} />
                  <strong>没有匹配的资产</strong>
                  <button onClick={() => { setQuery(''); setAssetFilter('all') }} type="button">清除筛选</button>
                </div>
              ) : filteredGroups.map(([pageName, assets]) => (
                <details
                  key={pageName}
                  open={displayedGroup === pageName}
                >
                  <summary onClick={(event) => {
                    event.preventDefault()
                    setOpenGroup(displayedGroup === pageName ? null : pageName)
                  }}>
                    <Icon decorative name="Icon/chevron-right" size={13} />
                    <span>{pageLabel(pageName)}</span>
                    <small>{assets.length}</small>
                  </summary>
                  <div className="asset-list">{assets.map(renderAssetButton)}</div>
                </details>
              ))}
            </div>
          </div>
        </aside>

        <main className="catalog-main">
          <section className="component-heading">
            <div className="heading-copy">
              <div className="breadcrumbs">
                <span>组件库</span>
                <Icon decorative name="Icon/chevron-right" size={12} />
                <span>{pageLabel(selected.pageName)}</span>
              </div>
              <div className="title-row">
                <h1>{selected.name}</h1>
                <span className="visibility-tag">{selected.isIcon ? '图标' : '公开组件'}</span>
              </div>
              <p>
                <code>{selected.componentName}</code>
                <span>{selected.type === 'COMPONENT_SET' ? '组件集' : '组件'}</span>
                <span>Node {selected.nodeId}</span>
              </p>
            </div>
            <div className="heading-actions">
              <button
                aria-label={favorites.has(selected.nodeId) ? '取消收藏' : '收藏组件'}
                className={`icon-button ${favorites.has(selected.nodeId) ? 'favorite' : ''}`}
                onClick={toggleFavorite}
                title={favorites.has(selected.nodeId) ? '取消收藏' : '收藏组件'}
                type="button"
              >
                <span aria-hidden="true">★</span>
              </button>
              <button
                className="secondary-button"
                onClick={() => {
                  const url = new URL(window.location.href)
                  url.searchParams.set('asset', selected.nodeId)
                  void copyText(url.href, 'link')
                }}
                type="button"
              >
                <Icon decorative name="Icon/link" size={15} />
                {linkCopied ? '已复制链接' : '复制链接'}
              </button>
            </div>
          </section>

          <section className="preview-card">
            <header>
              <div><strong>交互预览</strong></div>
              <div className="preview-toolbar">
                <button
                  aria-label="适应画布"
                  aria-pressed={zoom === 'fit'}
                  className={zoom === 'fit' ? 'active' : ''}
                  onClick={() => setZoom('fit')}
                  title="适应画布"
                  type="button"
                >
                  <Icon decorative name="Icon/Expand" size={15} />
                </button>
                <span className="toolbar-divider" />
                <button
                  aria-label="缩小"
                  onClick={() => setZoom((current) => stepZoom(current, fitScale, -0.25))}
                  title="缩小"
                  type="button"
                >−</button>
                <span className="zoom-value">{formatZoomPercent(zoom, fitScale)}</span>
                <button
                  aria-label="放大"
                  onClick={() => setZoom((current) => stepZoom(current, fitScale, 0.25))}
                  title="放大"
                  type="button"
                >+</button>
              </div>
            </header>
            <PreviewCanvas
              isIcon={selected.isIcon}
              key={selected.nodeId}
              onFitScaleChange={setFitScale}
              onZoomChange={setZoom}
              theme={theme}
              zoom={zoom}
            >
              <LibraryRenderer asset={selected} values={{ ...values, onAction: handleAction }} />
            </PreviewCanvas>
          </section>

          <section className={`code-card ${codeOpen ? 'open' : ''}`}>
            <header>
              <button
                aria-expanded={codeOpen}
                className="code-toggle"
                onClick={() => setCodeOpen((current) => !current)}
                type="button"
              >
                <Icon decorative name="Icon/chevron-right" size={14} />
                <strong>React 示例</strong><span>TSX</span>
              </button>
              <button
                className="copy-button"
                onClick={() => { void copyText(snippet, 'code') }}
                type="button"
              >
                <Icon decorative name="md-copy" size={14} />
                {copied ? '已复制' : '复制代码'}
              </button>
            </header>
            {codeOpen && <pre><code>{snippet}</code></pre>}
          </section>
        </main>

        <aside className="properties-panel">
          <header>
            <div><strong>属性</strong><span>{selected.properties.length} 项可配置</span></div>
            <button
              aria-label="重置属性"
              className="icon-button"
              onClick={() => setValues(defaultsFor(selected))}
              title="重置属性"
              type="button"
            >
              <Icon decorative name="Icon/Flip" nodeId="5357:2593" size={16} />
            </button>
          </header>
          <div className="properties-scroll">
            {selected.properties.length === 0 ? (
              <div className="empty-properties">
                <span className="empty-icon">
                  <Icon decorative name="Icon/Setting" size={22} />
                </span>
                <strong>暂无公开属性</strong>
              </div>
            ) : (
              <div className="property-list">
                {propertyGroups.map(([label, properties]) => {
                  const visibleProperties = properties.filter(propertyVisible)
                  if (visibleProperties.length === 0) return null
                  return (
                    <section className="property-group" key={label}>
                      <div className="section-label">
                        <span>{label}</span><small>{visibleProperties.length}</small>
                      </div>
                      {visibleProperties.map((property) => (
                        <div
                          className={`property-control ${property.type === 'BOOLEAN' ? 'boolean' : ''}`}
                          key={property.figmaName}
                        >
                          <span className="property-copy">
                            <strong>{property.figmaName}</strong>
                            <small>{property.reactProp}</small>
                          </span>
                          {property.type === 'BOOLEAN' ? (
                            <span className="switch">
                              <input
                                aria-label={property.figmaName}
                                checked={Boolean(values[property.reactProp])}
                                onChange={(event) =>
                                  setValues((current) =>
                                    clampCatalogValues(selected, {
                                      ...current,
                                      [property.reactProp]: event.target.checked,
                                    }),
                                  )
                                }
                                type="checkbox"
                              />
                              <span />
                            </span>
                          ) : property.type === 'VARIANT' ? (
                            <PropertySelect
                              key={`${selected.nodeId}-${property.reactProp}`}
                              label={property.figmaName}
                              onChange={(value) =>
                                setValues((current) =>
                                  clampCatalogValues(selected, {
                                    ...current,
                                    [property.reactProp]: value,
                                  }),
                                )
                              }
                              value={String(values[property.reactProp] ?? '')}
                              options={property.variantOptions.map((option) => ({ value: option, label: option }))}
                            />
                          ) : (
                            <PropertySelect
                              key={`${selected.nodeId}-${property.reactProp}`}
                              label={property.figmaName}
                              onChange={(value) =>
                                setValues((current) =>
                                  clampCatalogValues(selected, {
                                    ...current,
                                    [property.reactProp]: value,
                                  }),
                                )
                              }
                              value={String(values[property.reactProp] ?? '-1:-1')}
                              options={[
                                { value: '-1:-1', label: '默认嵌套' },
                                ...slotPickerAssets.filter((asset) => asset.isIcon).map((asset) => ({ value: asset.nodeId, label: asset.name })),
                              ]}
                            />
                          )}
                        </div>
                      ))}
                    </section>
                  )
                })}
              </div>
            )}
          </div>
          <footer>
            <div><span>Figma Node</span><code>{selected.nodeId}</code></div>
            <div><span>Asset key</span><code>{selected.assetKey.slice(0, 10)}…</code></div>
          </footer>
        </aside>
      </div>
      {feedback && <div className="catalog-feedback" role="status">{feedback}</div>}
    </div>
  )
}

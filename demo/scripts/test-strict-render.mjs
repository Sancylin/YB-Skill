import assert from 'node:assert/strict'
import { createServer } from 'vite'
import { createElement as h } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
const server = await createServer({ server:{middlewareMode:true} })
try {
  const { LibraryRenderer } = await server.ssrLoadModule('/src/library/LibraryRenderer.tsx')
  const { RenderPolicyProvider } = await server.ssrLoadModule('/src/library/RenderPolicy.tsx')
  const { assetCatalog } = await server.ssrLoadModule('/src/generated/assets.ts')
  const { publishedCatalog, fullCatalog } = await server.ssrLoadModule('/src/library/catalog.ts')
  const bindings = (await import('../src/library/renderer-bindings.json', { with: { type: 'json' } })).default
  const button = assetCatalog.find(x=>x.componentName==='Button')
  const render = (asset,values={},policy='deliverable-strict') => renderToStaticMarkup(h(RenderPolicyProvider,{policy},h(LibraryRenderer,{asset,values})))
  assert.ok(render(button).length)
  const variant = button.properties.find(p=>p.type==='VARIANT')
  assert.throws(()=>render(button,{[variant.reactProp]:'INVALID'}),/Invalid variant/)
  assert.throws(()=>render({...button,assetKey:'unknown'}),/Unknown component identity/)
  const unbound = publishedCatalog.filter(a=>!a.isIcon && !bindings[a.assetKey])
  assert.equal(unbound.length, 0, `Published non-icon assets missing renderers: ${unbound.map(a=>a.name).join(', ')}`)
  const supplemental = fullCatalog.find(a=>!a.published && !a.isIcon)
  assert.ok(supplemental, 'Expected at least one supplemental non-icon asset to prove the strict/preview boundary')
  assert.throws(()=>render(supplemental),/Unpublished component in strict delivery/)
  assert.ok(render(supplemental,{},'catalog-preview').length)
  for(const componentName of ['Search','Dialog']) {
    const asset=assetCatalog.find(x=>x.componentName===componentName)
    assert.ok(render(asset).length)
  }
  console.log('Strict render: identity, variant rejection, full published renderer coverage, unpublished rejection and preview boundary passed')
} finally { await server.close() }

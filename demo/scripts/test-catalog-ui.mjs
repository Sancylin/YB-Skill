import assert from 'node:assert/strict'
import { mkdir, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { resolve } from 'node:path'

// Use an existing Playwright installation without adding it to the component library.
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE ?? 'playwright')
const baseURL = process.env.CATALOG_URL ?? 'http://127.0.0.1:5180/'
const output = resolve(process.env.CATALOG_TEST_OUTPUT ?? `${tmpdir()}/yb-mobile-design-catalog-test`)
await mkdir(output, { recursive: true })
const browser = await chromium.launch({ channel: 'chrome', headless: true })
const context = await browser.newContext({
  viewport: { width: 1440, height: 960 },
  permissions: ['clipboard-read', 'clipboard-write'],
})
const page = await context.newPage()
const failures = []
const checks = []
page.on('pageerror', (error) => failures.push(error.message))

function record(name) {
  checks.push(name)
  console.log(`PASS ${name}`)
}

async function screenshot(name) {
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: resolve(output, `${name}.png`) })
}

async function noPageOverflow() {
  const result = await page.evaluate(() => ({
    width: window.innerWidth,
    doc: document.documentElement.scrollWidth,
    app: document.querySelector('.catalog-app').getBoundingClientRect().width,
  }))
  assert.ok(result.doc <= result.width + 1, JSON.stringify(result))
  assert.ok(result.app <= result.width + 1, JSON.stringify(result))
}

async function choose(name) {
  await page.getByRole('textbox', { name: '搜索组件', exact: true }).fill(name)
  const target = page.locator(`.component-tree button[data-asset-name="${name}"]`)
  await target.waitFor({ state: 'visible' })
  await target.click()
  assert.equal(await page.locator('h1').innerText(), name)
  await page.getByRole('textbox', { name: '搜索组件', exact: true }).fill('')
}

async function property(name, value) {
  const field = page.locator('.property-control').filter({
    has: page.locator('.property-copy strong', { hasText: new RegExp(`^${name}$`) }),
  })
  await field.getByRole('combobox').click()
  await page.getByRole('option', { name: value, exact: true }).click()
}

try {
  await page.goto(baseURL)
  await page.locator('.preview-measure').waitFor()
  assert.equal(await page.locator('h1').innerText(), 'Button 按钮')
  assert.equal(await page.locator('.zoom-value').innerText(), '100%')
  record('Default asset and natural preview scale')
  await screenshot('desktop-light')

  await property('Type', 'Outline')
  await property('Size', 'S')
  assert.match(await page.locator('.code-card pre').innerText(), /type="Outline"/)
  assert.match(await page.locator('.code-card pre').innerText(), /size="S"/)
  const toggle = page.locator('.property-control').filter({
    has: page.locator('.property-copy strong', { hasText: /^Left icon$/ }),
  }).getByRole('checkbox')
  await toggle.check()
  assert.match(await page.locator('.code-card pre').innerText(), /leftIcon/)
  await page.getByRole('button', { name: '重置属性', exact: true }).click()
  assert.match(await page.locator('.code-card pre').innerText(), /type="Primary"/)
  assert.equal(await toggle.isChecked(), false)
  record('Variant, boolean, code synchronization, and reset')

  await page.getByRole('button', { name: '复制代码', exact: true }).click()
  await page.getByRole('status').waitFor()
  assert.match(await page.evaluate(() => navigator.clipboard.readText()), /<Button/)
  await page.getByRole('button', { name: '复制链接', exact: true }).click()
  const link = await page.evaluate(() => navigator.clipboard.readText())
  assert.equal(new URL(link).searchParams.get('asset'), '1396:5016')
  record('Code and component deep-link clipboard actions')

  const codeToggle = page.locator('.code-toggle')
  await codeToggle.click()
  assert.equal(await page.locator('.code-card pre').count(), 0)
  await codeToggle.click()
  assert.equal(await page.locator('.code-card pre').count(), 1)
  await page.getByRole('button', { name: '收藏组件', exact: true }).click()
  await page.reload()
  assert.equal(await page.getByRole('button', { name: '取消收藏', exact: true }).count(), 1)
  assert.equal(await page.locator('.favorite-assets button').count(), 1)
  await page.getByRole('button', { name: '取消收藏', exact: true }).click()
  record('Code collapse and persistent favorites')

  await page.getByRole('button', { name: '图标', exact: true }).click()
  const iconNodes = await page.locator('.component-tree [data-asset-name]').count()
  assert.ok(iconNodes > 0)
  assert.equal(await page.locator('.component-tree [data-asset-name="Button 按钮"]').count(), 0)
  await page.getByRole('textbox', { name: '搜索组件', exact: true }).fill('not-a-real-component')
  await page.getByText('没有匹配的资产', { exact: true }).waitFor()
  await page.getByRole('button', { name: '清除筛选', exact: true }).click()
  assert.equal(await page.getByRole('textbox', { name: '搜索组件', exact: true }).inputValue(), '')
  await choose('Icon/A')
  assert.equal(await page.locator('.zoom-value').innerText(), '400%')
  await page.getByRole('button', { name: '放大', exact: true }).click()
  assert.equal(await page.locator('.zoom-value').innerText(), '425%')
  await page.getByRole('button', { name: '适应画布', exact: true }).click()
  record('Asset filters, empty results, icon rendering, and zoom')
  await screenshot('desktop-icon')

  await choose('NavBar 导航栏')
  await screenshot('desktop-navbar')
  await choose('Button 按钮')
  await page.getByRole('button', { name: '深色', exact: true }).click()
  assert.equal(await page.locator('.catalog-app').getAttribute('data-theme'), 'dark')
  await screenshot('desktop-dark')
  await page.getByRole('button', { name: '浅色', exact: true }).click()
  record('Navigation component and light/dark themes')

  for (const [width, height] of [[320, 700], [390, 844], [768, 1024], [1024, 768], [1440, 960], [1920, 1080]]) {
    await page.setViewportSize({ width, height })
    await noPageOverflow()
    const stage = await page.locator('.preview-stage').boundingBox()
    assert.ok(stage && stage.width > 100 && stage.height > 100, `Missing canvas at ${width}`)
    await screenshot(`viewport-${width}`)
    record(`Responsive viewport ${width}x${height}`)
  }

  await page.setViewportSize({ width: 390, height: 844 })
  await page.getByRole('button', { name: '属性设置', exact: true }).click()
  assert.equal(await page.locator('.properties-panel').isVisible(), true)
  await property('Type', 'Alert')
  await screenshot('mobile-properties')
  await page.getByRole('button', { name: '组件预览', exact: true }).click()
  assert.match(await page.locator('.code-card pre').innerText(), /type="Alert"/)
  await page.getByRole('textbox', { name: '搜索组件', exact: true }).fill('Icon/A')
  assert.equal(await page.locator('.sidebar').isVisible(), true)
  await page.locator('.component-tree button[data-asset-name="Icon/A"]').click()
  assert.equal(await page.locator('.catalog-main').isVisible(), true)
  record('Mobile catalog, properties, preview, and search navigation')

  await page.goto(`${baseURL}?asset=1396%3A5016`)
  assert.equal(await page.locator('h1').innerText(), 'Button 按钮')
  await page.goto(`${baseURL}?asset=invalid`)
  assert.equal(await page.locator('h1').innerText(), 'Button 按钮')
  record('Valid and invalid direct component URLs')

  for (const id of ['agent', 'source-outreach', 'feedback']) {
    await page.goto(`${baseURL}?screen=${id}`)
    await page.locator('.screen-demo-shell').waitFor()
  }
  await page.goto(`${baseURL}?screen=not-a-screen`)
  assert.equal(await page.locator('.catalog-app').count(), 0)
  record('Three built-in page demos and unknown screen routing')

  assert.deepEqual(failures, [])
  record('No browser runtime errors')
  await writeFile(resolve(output, 'results.json'), JSON.stringify({ passed: true, checks, failures }, null, 2))
} catch (error) {
  await screenshot('failure')
  await writeFile(resolve(output, 'results.json'), JSON.stringify({
    passed: false,
    checks,
    failures: [...failures, String(error)],
  }, null, 2))
  throw error
} finally {
  await browser.close()
}

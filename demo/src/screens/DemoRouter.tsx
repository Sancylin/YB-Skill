import App from '../App'
import { isScreenId, screenRegistry } from './registry'
import '../library/library.css'
import './screens.css'

function catalogUrl() {
  const url = new URL(window.location.href)
  url.searchParams.delete('screen')
  return `${url.pathname}${url.search}${url.hash}`
}

export function DemoRouter() {
  const screenId = new URLSearchParams(window.location.search).get('screen')

  if (screenId === null) return <App />

  if (isScreenId(screenId)) {
    const Screen = screenRegistry[screenId].component
    return <Screen />
  }

  return (
    <main className="screen-demo-shell is-message">
      <section aria-labelledby="unknown-screen-title" className="unknown-screen">
        <strong id="unknown-screen-title">找不到这个页面 Demo</strong>
        <p>
          未注册的 screen 参数：<code>{screenId || '（空）'}</code>
        </p>
        <a href={catalogUrl()}>返回组件目录</a>
      </section>
    </main>
  )
}

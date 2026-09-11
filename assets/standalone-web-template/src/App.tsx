import { useState } from 'react'
import { RenderPolicyProvider } from '@demo/library/RenderPolicy'
import { HostCanvas } from '@demo/library/HostCanvas'
import { DemoShell } from '@demo/screens/DemoShell'
import { 组件名示例Screen } from '@app/screens/example-page'

export function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  return (
    <RenderPolicyProvider policy="deliverable-strict">
    <DemoShell
      chromeLabel="场景与主题"
      theme={theme}
      chrome={
        <button type="button" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
          下一主题
        </button>
      }
    >
      <HostCanvas canvasRole="primary" className="screen-demo-canvas">
        <组件名示例Screen />
      </HostCanvas>
    </DemoShell>
    </RenderPolicyProvider>
  )
}

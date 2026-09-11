import type { ReactNode } from 'react'

export function DemoShell({
  chrome,
  chromeLabel,
  theme,
  children,
}: {
  chrome: ReactNode
  chromeLabel: string
  theme?: 'light' | 'dark'
  children: ReactNode
}) {
  return (
    <main className="screen-demo-shell" data-theme={theme}>
      <div className="screen-demo-stage">{children}</div>
      <aside aria-label={chromeLabel} className="screen-demo-chrome" data-skip-contrast>
        {chrome}
      </aside>
    </main>
  )
}

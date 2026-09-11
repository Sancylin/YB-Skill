import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@demo/tokens.css'
import '@demo/index.css'
import '@demo/screens/screens.css'
import { App } from '@app/App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

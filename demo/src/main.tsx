import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './tokens.css'
import { DemoRouter } from './screens/DemoRouter.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <DemoRouter />
  </StrictMode>,
)

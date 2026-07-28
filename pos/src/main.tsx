import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { applyDocumentLocale, initI18n } from './i18n'
import { applyBranding } from './lib/branding'

initI18n().then(() => {
  applyDocumentLocale()
  applyBranding()
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
})

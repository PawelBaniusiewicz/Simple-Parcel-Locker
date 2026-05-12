import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { createBrowserRouter, RouterProvider } from 'react-router'
import * as routes from './constants/routes.ts'
import PickUpPackage from './components/PickUpPackage/PickUpPackage.tsx'

const router = createBrowserRouter([
  {
    path: routes.HOME,
    element: <App />
  },
  {
    path: routes.MY_PACKAGES,
    element: <div>My Packages</div>
  },
  {
    path: routes.PICK_UP_PACKAGE,
    element: <PickUpPackage />
  }
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { createBrowserRouter, RouterProvider } from 'react-router';
import * as routes from './constants/routes.ts';
import PickUpParcel from './components/Parcels/PickUpParcel/PickUpParcel.tsx';
import Register from './components/screens/Unauthenticated/Register/Register.tsx';
import Login from './components/screens/Unauthenticated/Login/Login.tsx';
import ActivateAccount from './components/screens/Unauthenticated/Register/ActivateAccount/ActivateAccount.tsx';
import AuthProvider from './context/AuthProvider.tsx';
import ProtectedRoute from './components/Security/ProtectedRoute/ProtectedRoute.tsx';
import GuestRoute from './components/Security/GuestRoute/GuestRoute.tsx';
import ParcelList from './components/Parcels/ParcelList/ParcelList.tsx';

const router = createBrowserRouter([
  {
    path: routes.HOME,
    element: <App />,
    children: [
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: routes.MY_PACKAGES,
            element: <ParcelList />
          },
          {
            path: routes.PICK_UP_PARCEL,
            element: <PickUpParcel />
          }
        ]
      }
      
    ]
  },
  {
    element: <GuestRoute />,
    children: [
      {
        path: routes.REGISTER,
        element: <Register />
      },
      {
        path: routes.ACTIVATE_ACCOUNT,
        element: <ActivateAccount />
      },
      {
        path: routes.LOGIN,
        element: <Login />
      }
    ]
  }
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>,
)

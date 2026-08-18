import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Navigate } from "react-router";
import './index.css';
import App from './App.tsx';
import { createBrowserRouter, RouterProvider } from 'react-router';
import * as routes from './constants/routes.ts';
import PickUpParcel from './components/screens/Authenticated/Parcels/PickUpParcel/PickUpParcel.tsx';
import Register from './components/screens/Unauthenticated/Register/Register.tsx';
import Login from './components/screens/Unauthenticated/Login/Login.tsx';
import ActivateAccount from './components/screens/Unauthenticated/Register/ActivateAccount/ActivateAccount.tsx';
import AuthProvider from './context/AuthProvider.tsx';
import ProtectedRoute from './components/Security/ProtectedRoute/ProtectedRoute.tsx';
import GuestRoute from './components/Security/GuestRoute/GuestRoute.tsx';
import ParcelList from './components/screens/Authenticated/Parcels/ParcelList/ParcelList.tsx';
import SupplierDashboard from "./components/screens/Authenticated/Supplier/SupplierDashboard/SupplierDashboard.tsx";
import AdminParcelLockers from "./components/screens/Authenticated/Admin/AdminParcelLockers/AdminParcelLockers.tsx";
import AdminDashboard from "./components/screens/Authenticated/Admin/AdminDashboard/AdminDashboard.tsx";
import ParcelLockerMap from "./components/Map/ParcelLockersMap/ParcelLockersMap.tsx";

const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      {
        path: routes.HOME,
        element: <ParcelLockerMap />
      },
      {
        element: <ProtectedRoute allowedRoles={["SUPPLIER", "USER", "ADMIN"]} />,
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
      },
      {
        element: <ProtectedRoute allowedRoles={["SUPPLIER"]}/>,
        children: [
          {
            path: routes.SUPPLIER_PARCELS,
            element: <SupplierDashboard/>
          }
        ]
      },
    ]
  },
  {
    element: <ProtectedRoute allowedRoles={["ADMIN"]}/>,
    children: [
      {
        element: <AdminDashboard />,
        children: [
          {
            path: routes.ADMIN_PANEL,
            element: <Navigate to={routes.ADMIN_PARCEL_LOCKERS} replace />
          },
          {
            path: routes.ADMIN_PARCEL_LOCKERS,
            element: <AdminParcelLockers />
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

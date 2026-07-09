import { Navigate, Outlet } from "react-router";
import { useAuth } from "../../../hooks/useAuth";
import { HOME } from "../../../constants/routes";

export default function GuestRoute() {
    const { isAuthenticated } = useAuth();
    return isAuthenticated ? <Navigate to={HOME} replace /> : <Outlet />;
}
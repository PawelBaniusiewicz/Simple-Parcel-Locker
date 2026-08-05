import { Navigate, Outlet } from "react-router";
import { useAuth } from "../../../hooks/useAuth";
import { LOGIN } from "../../../constants/routes";

interface ProtectedRouteProps {
    allowedRoles?: string[];
}

export default function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
    const { isAuthenticated, user } = useAuth();

    if (isAuthenticated === null) {
        return <div className="w-full h-screen flex justify-center items-center text-white">Checking session...</div>;
    }

    if (allowedRoles && user) {
        const userRole = String(user.role).toUpperCase();
        const hasAccess = allowedRoles.map(r => r.toUpperCase()).includes(userRole);

        if (!hasAccess) {
            return <Navigate to={`${LOGIN}`} replace />;
        }
    }

    return isAuthenticated ? <Outlet /> : <Navigate to={`${LOGIN}`} replace />;
}
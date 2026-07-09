import { Navigate, Outlet } from "react-router";
import { useAuth } from "../../../hooks/useAuth";
import { LOGIN } from "../../../constants/routes";


export default function ProtectedRoute() {
    const { isAuthenticated } = useAuth();

    if (isAuthenticated === null) {
        return <div className="w-full h-screen flex justify-center items-center text-white">Checking session...</div>;
    }
    
    return isAuthenticated ? <Outlet /> : <Navigate to={`${LOGIN}`} replace />;
}
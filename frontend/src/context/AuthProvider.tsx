import { useState, useEffect, useCallback,type ReactNode } from "react";
import apiClient from "../api/apiClient";
import { type User, AuthContext } from "./AuthContext/types";
import { USER_ME } from "../constants/routes";

export default function AuthProvider({children}: {children: ReactNode}){
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
    const [user, setUser] = useState<User | null>(null);

    const [authRefreshKey, setAuthRefreshKey] = useState<number>(0);

    const checkAuthStatus = useCallback(() => {
        setAuthRefreshKey(prev => prev + 1);
    }, []);

    useEffect(() => {
        const fetchAuth = async () => {
            try {
                const response = await apiClient.get(`${import.meta.env.VITE_APP_BASE_API_URL}${USER_ME}`);
                setUser(response.data.user);
                setIsAuthenticated(response.data.isAuthenticated);
            } catch (error) {
                setUser(null);
                setIsAuthenticated(false);
                let message;
                if (error instanceof Error) message = error.message;
                else message = String(error);
                reportError({ message });
            }
        };
        fetchAuth();
    }, [authRefreshKey]);
    
    return (
        <AuthContext.Provider value={{ isAuthenticated, user, checkAuthStatus }}>
            {children}
        </AuthContext.Provider>
    )
}



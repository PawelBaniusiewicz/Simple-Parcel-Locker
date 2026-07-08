import { useState, useEffect, createContext, useCallback, type ReactNode } from "react";
import apiClient from "../api/apiClient";
import { type User, type AuthContextType } from "./AuthContext/types";
import { USER_ME } from "../constants/routes";

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export default function AuthProvider({children}: {children: ReactNode}){
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
    const [user, setUser] = useState<User | null>(null);

    const checkAuthStatus = useCallback(async () => {
        try {
            const response = await apiClient.get(`${import.meta.env.VITE_APP_BASE_API_URL}${USER_ME}`);
            setUser(response.data);
            setIsAuthenticated(true);
        } catch (error) {
            setUser(null);
            setIsAuthenticated(false);
            let message;
            if (error instanceof Error) message = error.message;
            else message = String(error);
            reportError({ message });
        }
    }, [])

    useEffect(() => {
        checkAuthStatus();
    }, [checkAuthStatus]);
    
    return (
        <AuthContext.Provider value={{ isAuthenticated, user, checkAuthStatus }}>
            {children}
        </AuthContext.Provider>
    )
}



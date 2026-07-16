import { createContext } from "react";

export type User = {
    id: number;
    name: string;
    email: string;
    role: string;
};

export type AuthContextType = {
    isAuthenticated: boolean | null;
    user: User | null;
    checkAuthStatus: () => void; 
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);
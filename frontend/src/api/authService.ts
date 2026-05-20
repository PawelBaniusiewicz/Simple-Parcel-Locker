import type { registerUserProps } from "../constants/types";
import apiClient from "./apiClient";
import { setCookie } from "typescript-cookie";


export const register = async (name: string, email: string, password: string, phone_number: string) => {
    try {
        const response = await apiClient.post<registerUserProps>(`${import.meta.env.REACT_APP_BASE_API_URL}/register`, {name, email, password, phone_number});
        if (response.status === 200) {
            setCookie('username', response.data.name, { expires: 7, secure: true, sameSite: 'strict', path: '/'})
        }
        return response.data
    } catch(error) {
        let message
        if (error instanceof Error) message = error.message
        else message = String(error)
	    reportError({ message })
    }
} 
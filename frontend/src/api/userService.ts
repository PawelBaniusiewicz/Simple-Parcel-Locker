import type { loginUserProps } from "../constants/types";
import apiClient from "./apiClient";
import { setCookie } from "typescript-cookie";
import * as routes from "../constants/routes"


export const login = async (email: string, password: string) => {
    try {
        const response = await apiClient.post<loginUserProps>(`${import.meta.env.REACT_APP_BASE_API_URL}${routes.LOGIN}`, {email, password});
        if (response.status === 200) {
            setCookie('email', response.data.email, { expires: 7, secure: true, sameSite: 'strict', path: '/'});
        };
        return response.data;
    } catch(error) {
        let message;
        if (error instanceof Error) message = error.message;
        else message = String(error);
	    reportError({ message });
    };
};
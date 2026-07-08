import axios from "axios";
import { REFRESH_TOKEN, LOGIN } from "../constants/routes";


const apiClient = axios.create({
    baseURL: import.meta.env.REACT_APP_BASE_API_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true
});

apiClient.interceptors.response.use(
    (response) => {
        return response
    },
    async (error) => {
        const originalRequest = error.config;
        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            originalRequest.url !== `${import.meta.env.VITE_APP_BASE_API_URL}${REFRESH_TOKEN}` &&
            originalRequest.url !== `${import.meta.env.VITE_APP_BASE_API_URL}${LOGIN}`
        ) {
            originalRequest._retry = true;
            try {
                await apiClient.post(`${import.meta.env.VITE_APP_BASE_API_URL}${REFRESH_TOKEN}`);
                return apiClient(originalRequest);
            } catch (refreshError) {
                const currentPath = window.location.pathname;
                if (originalRequest.url?.includes('me')) {
                    return Promise.reject(refreshError);
                }
                if (!currentPath.includes('login') && !currentPath.includes('register') && !currentPath.includes('activate')) {
                    window.location.href = LOGIN;
                }
                return Promise.reject(refreshError)
            }
        }
        return Promise.reject(error)
    }
)

export default apiClient;
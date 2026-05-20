import apiClient from "./apiClient";

export const get_all_user_packages = async () => {
    try {
        const response = await apiClient.post('/packages');
        return response.data;
    } catch(error) {
        let message
        if (error instanceof Error) message = error.message
        else message = String(error)
	    reportError({ message })
    }
    
}
import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.REACT_APP_BASE_API_URL,
    headers: {
        'Content-Type': 'aplication/json'
    }
});

export default apiClient;
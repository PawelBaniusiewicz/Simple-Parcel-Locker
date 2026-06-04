import apiClient from "./apiClient";
import * as route from "../constants/routes";

export const pickUpParcel = async (pick_up_code: string, phone_number: string) => {
    try {
        const response = await apiClient.post(`${import.meta.env.VITE_APP_BASE_API_URL}${route.PICK_UP_PARCEL}`, {pick_up_code, phone_number});
        return response.data
    } catch(error) {
        let message;
        if (error instanceof Error) message = error.message;
        else message = String(error);
	    reportError({ message });
    };
}
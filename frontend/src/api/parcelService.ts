import apiClient from "./apiClient";
import * as route from "../constants/routes";

export const pickUpParcel = async (pickup_code: string, phone_number: string) => {
    try {
        const response = await apiClient.post(
            `${import.meta.env.VITE_APP_BASE_API_URL}${route.PICK_UP_PARCEL}`,
            {
                "pickup_code": pickup_code,
                "phone_number": phone_number
            }
        );
        return response.data
    } catch(error) {
        let message;
        if (error instanceof Error) message = error.message;
        else message = String(error);
	    reportError({ message });
    }
}
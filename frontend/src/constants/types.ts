import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

export interface registerUserProps {
    name: string;
    email: string;
    password: string;
    password_confirmation: string;
    phone_number: string;
}

export interface loginUserProps {
    email: string;
    password: string;
}

// ---------------------------------------------------------
// MAP
// ---------------------------------------------------------

export const DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});


export default interface ParcelLocker {
    id: number;
    name: string;
    address: string;
    latitude: number;
    longitude: number;
}
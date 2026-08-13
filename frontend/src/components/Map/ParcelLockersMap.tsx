import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import apiClient from "../../api/apiClient.ts";
import L from 'leaflet';
import { PARCEL_LOCKERS } from '../../constants/routes.ts'

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});
L.Marker.prototype.options.icon = DefaultIcon;

interface ParcelLocker {
    id: number;
    name: string;
    address: string;
    latitude: number;
    longitude: number;
}

export default function ParcelLockerMap() {
    const [lockers, setLockers] = useState<ParcelLocker[]>([]);
    const [loading, setLoading] = useState(true);

    const centerPosition: [number, number] = [52.0693, 19.4803];
    const defaultZoom = 6;

    useEffect(() => {
        const fetchLockers = async () => {
            try {
                const response = await apiClient.get(`${import.meta.env.VITE_APP_BASE_API_URL}${PARCEL_LOCKERS}`);
                console.log("Co dokładnie przyszło z API?", response.data);

                if (Array.isArray(response.data)) {
                    setLockers(response.data);
                } else if (response.data && Array.isArray(response.data.parcel_lockers)) {
                    setLockers(response.data.parcel_lockers);
                } else {
                    console.error("Oczekiwano tablicy, otrzymano coś innego:", response.data);
                    setLockers([]);
                }
                setLockers(response.data);
            } catch(error) {
                let message;
                if (error instanceof Error) message = error.message;
                else message = String(error);
                reportError({ message });
            } finally {
                setLoading(false);
            }
        };

        fetchLockers();
    }, []);

    if (loading) {
        return <div className="w-full h-96 flex items-center justify-center">Loading map...</div>;
    }

    return (
        <div className="w-full max-w-5xl mx-auto my-8 border-4 border-blue-500 rounded-xl overflow-hidden shadow-lg">
            <MapContainer
                center={centerPosition}
                zoom={defaultZoom}
                className="w-full h-125 z-0"
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {lockers.map((locker) => (
                    <Marker
                        key={locker.id}
                        position={[locker.latitude, locker.longitude]}
                    >
                        <Popup>
                            <div className="text-center">
                                <h3 className="font-bold text-lg">{locker.name}</h3>
                                <p className="text-gray-600 text-sm">{locker.address}</p>
                                <button className="mt-2 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                                    Choose this parcel locker
                                </button>
                            </div>
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
}
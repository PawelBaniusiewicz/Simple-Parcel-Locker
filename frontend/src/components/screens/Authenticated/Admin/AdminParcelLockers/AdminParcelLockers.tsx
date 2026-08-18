import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { LatLng } from 'leaflet';
import apiClient from "../../../../../api/apiClient.ts";
import type ParcelLocker from '../../../../../constants/types.ts'
import { DefaultIcon } from '../../../../../constants/types.ts'
import { PARCEL_LOCKERS } from '../../../../../constants/routes.ts'
import LocationPicker from "../../../../Map/LocationPicker/LocationPicker.tsx";
import L from 'leaflet';

L.Marker.prototype.options.icon = DefaultIcon;

export default function AdminParcelLockers() {
    const [existingLockers, setExistingLockers] = useState<ParcelLocker[]>([]);
    const [selectedLocation, setSelectedLocation] = useState<LatLng | null>(null);

    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

    const centerPosition: [number, number] = [
        Number(import.meta.env.VITE_APP_CENTER_POSITION_X),
        Number(import.meta.env.VITE_APP_CENTER_POSITION_Y)
    ];

    const fetchLockers = async () => {
        try {
            const response = await apiClient.get(`${import.meta.env.VITE_APP_BASE_API_URL}${PARCEL_LOCKERS}`);
            if (Array.isArray(response.data)) {
                setExistingLockers(response.data);
            }
        } catch(error) {
            let message;
            if (error instanceof Error) message = error.message;
            else message = String(error);
            reportError({ message });
        }
    };

    useEffect(() => {
        fetchLockers();
    }, []);

    const handleLocationSelect = (latlng: LatLng) => {
        setSelectedLocation(latlng);
        setMessage(null);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMessage(null);

        if (!selectedLocation || !name || !address) {
            setMessage({ text: 'Fill in all the fields and select a location on the map!', type: 'error' });
            return;
        }

        try {
            await apiClient.post(`${import.meta.env.VITE_APP_BASE_API_URL}${PARCEL_LOCKERS}`, {
                name: name,
                address: address,
                latitude: selectedLocation.lat,
                longitude: selectedLocation.lng
            });

            setMessage({ text: 'The parcel locker has been added successfully!', type: 'success' });
            setName('');
            setAddress('');
            setSelectedLocation(null);
            await fetchLockers();

        } catch (error: any) {
            setMessage({
                text: error.response?.data?.message || 'Error while adding parcel locker',
                type: 'error'
            });
        }
    };

    return (
        <div className="flex h-full w-full text-slate-400">
            <div className="w-2/3 h-full p-4">
                <MapContainer center={centerPosition} zoom={6} className="w-full h-full rounded-xl shadow-lg z-0">
                    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    <LocationPicker onLocationSelect={handleLocationSelect} />
                    {existingLockers.map(locker => (
                        <Marker key={locker.id} position={[locker.latitude, locker.longitude]}>
                            <Popup><strong>{locker.name}</strong><br/>{locker.address}</Popup>
                        </Marker>
                    ))}
                    {selectedLocation && (
                        <Marker position={[selectedLocation.lat, selectedLocation.lng]} opacity={0.6}>
                            <Popup>New Localization</Popup>
                        </Marker>
                    )}
                </MapContainer>
            </div>
            <div className="w-1/3 text-slate-400 p-6 shadow-xl z-10 overflow-y-auto">
                <h2 className="text-2xl font-bold mb-6 text-gray-800">New Parcel Locker</h2>

                {message && (
                    <div className={`mb-4 p-3 rounded text-sm ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {message.text}
                    </div>
                )}

                {selectedLocation ? (
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="p-3 bg-blue-50 text-blue-800 rounded-md text-sm border border-blue-200 font-mono">
                            Lat: {selectedLocation.lat.toFixed(6)}<br />
                            Lng: {selectedLocation.lng.toFixed(6)}
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Parcel Locker Name</label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="np. WAW123A"
                                className="w-full border border-gray-300 rounded p-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                            <input
                                type="text"
                                value={address}
                                onChange={(e) => setAddress(e.target.value)}
                                placeholder="np. ul. Prosta 51, Warszawa"
                                className="w-full border border-gray-300 rounded p-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>

                        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
                            Add Parcel Locker
                        </button>
                    </form>
                ) : (
                    <div className="flex flex-col items-center justify-center text-gray-400 mt-20 border-2 border-dashed border-gray-200 p-8 rounded-lg text-center">
                        <svg className="w-12 h-12 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                        <p>Click anywhere on the map to select a location.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
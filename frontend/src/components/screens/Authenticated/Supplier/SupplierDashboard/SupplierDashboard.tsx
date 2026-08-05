import React, { useState } from 'react';
import apiClient from "../../../../../api/apiClient.ts";
import * as route from "../../../../../constants/routes.ts";

export default function SupplierDashboard() {
    const [trackingText, setTrackingText] = useState('');
    const [status, setStatus] = useState('in_transit');
    const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
    const [errors, setErrors] = useState<{ tracking_number: string; error: string }[]>([]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMessage(null);
        setErrors([]);

        const trackingNumbers = trackingText
            .split('\n')
            .map((t) => t.trim())
            .filter((t) => t.length > 0);

        if (trackingNumbers.length === 0) {
            setMessage({ text: 'You must enter at least one parcel number.', type: 'error' });
            return;
        }


        try {
            const response = await apiClient.post(
                `${import.meta.env.VITE_APP_BASE_API_URL}${route.SUPPLIER_PARCELS}`,
                {
                    tracking_numbers: trackingNumbers,
                    status: status,
                }
            );
            setMessage({ text: response.data.message, type: 'success' });

            if (response.data.errors && response.data.errors.length > 0) {
                setErrors(response.data.errors);
            } else {
                setTrackingText('');
            }
        } catch (error: any) {
            setMessage({
                text: error.response?.data?.message || 'Error while connecting to the server',
                type: 'error'
            });
        }
    };

    return (
        <div className="max-w-2xl lg:mx-auto mx-4 p-6 border border-gray-600 bg-[#0d0d10] text-white rounded-3xl shadow-md mt-10">
            <h2 className="text-2xl font-bold mb-6">Supplier Panel - status changes</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium mb-1">
                        New status for parcel:
                    </label>
                    <select
                        value={status}
                        onChange={(e) => setStatus(e.target.value)}
                        className="w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="in_transit">Received from the sender (In transit)</option>
                        <option value="in_warehouse">Added to the Warehouse</option>
                        <option value="out_for_delivery">Released for delivery</option>
                        <option value="ready_for_pickup">Delivered to a Parcel Locker (Ready for pickup)</option>
                        <option value="returned">Return to Sender</option>
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">
                        Enter the tracking number (one per line)
                    </label>
                    <textarea
                        value={trackingText}
                        onChange={(e) => setTrackingText(e.target.value)}
                        rows={8}
                        placeholder="NP123456789&#10;NP987654321"
                        className="w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500 font-mono"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 transition"
                >
                    Update statuses
                </button>
            </form>
            {message && (
                <div className={`mt-4 p-4 rounded-md ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {message.text}
                </div>
            )}

            {errors.length > 0 && (
                <div className="mt-4 p-4 bg-orange-100 text-orange-800 rounded-md">
                    <h4 className="font-bold mb-2">Please note that not all packages have been updated:</h4>
                    <ul className="list-disc pl-5 space-y-1">
                        {errors.map((err, idx) => (
                            <li key={idx}>
                                <strong>{err.tracking_number}</strong>: {err.error}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};
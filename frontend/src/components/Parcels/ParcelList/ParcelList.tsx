import apiClient from "../../../api/apiClient"
import { useEffect, useState } from "react"
import { MY_PACKAGES } from "../../../constants/routes"
import type { Parcel } from "../ParcelRow/ParcelRow";
import ParcelRow from "../ParcelRow/ParcelRow";


export default function ParcelList(){
    const [parcels, setParcels] = useState<Parcel[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    const fetchData = async () => {
        try {
            setIsLoading(true);
            const response = apiClient.get(`${import.meta.env.VITE_APP_BASE_API_URL}${MY_PACKAGES}`);
            setParcels((await response).data.parcels);
        } catch(error) {
            setParcels([]);
            setIsLoading(true);
            let message;
            if (error instanceof Error) message = error.message;
            else message = String(error);
            reportError({ message });
        } finally {
            setIsLoading(false);
        }
    }
    useEffect(() => {
        fetchData()
    }, [])

    console.log(parcels.length)
    return (
        <div className="w-full max-w-4xl mx-auto px-4 py-8">
            <div className="mb-6 flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-white tracking-tight">Your Packages</h1>
                    <p className="text-zinc-400 text-sm">Manage your shipments and pick them up at package lockers.</p>
                </div>
                <span className={`bg-zinc-800 text-zinc-300 text-xs font-semibold px-2.5 py-1 rounded-md ${`invisible ? ${parcels.length === 0}`} : visible`}>
                    The total number of your packages: {parcels.length}
                </span>
            </div>
            {isLoading ? (
                <div className="flex flex-col items-center justify-center py-12 space-y-3">
                    <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-zinc-500 text-sm">Loading your packages...</p>
                </div>
            ) : parcels.length > 0 ? (
                <div className="space-y-4">
                    {parcels.map((parcel) => (
                        <ParcelRow key={parcel.id} parcel={parcel} />
                    ))}
                </div>
            ) : (
                <div className="text-center py-16 border border-dashed border-zinc-800 rounded-xl bg-zinc-900/20">
                    <p className="text-zinc-400 font-medium text-lg mb-1">It's clean here!</p>
                    <p className="text-zinc-500 text-sm">You currently have no registered packages.</p>
                </div>
            )}
        </div>
    )
}
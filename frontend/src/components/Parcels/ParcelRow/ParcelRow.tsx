export interface Parcel {
    id: number;
    content: string;
    created_at: string;
    locker_id: number | null;
    pickup_code: string;
    size: string;
    status: string[];
    stored_at: string | null;
    tracking_number: string;
    user_id: number;
}

interface ParcelRowProps {
    parcel: Parcel;
}

export default function ParcelRow({ parcel }: ParcelRowProps) {

    const formattedDate = new Date(parcel.created_at).toLocaleDateString('en-EN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });

    return (
        <div className="bg-[#18181b] border border-zinc-800 rounded-xl p-5 shadow-lg hover:border-zinc-700 transition duration-200">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                    <div className="flex items-center gap-3">
                        <span className="text-zinc-400 text-xs font-mono tracking-wider">#{parcel.tracking_number}</span>
                        <span className="text-xs px-2.5 py-0.5 rounded-full font-medium border text-zinc-400">
                            {parcel.status}
                        </span>
                    </div>
                    <h3 className="text-white text-lg font-semibold capitalize">Contents: {parcel.content}</h3>
                    <p className="text-zinc-500 text-xs">Date of shipment: {formattedDate}</p>
                </div>
                <div className="flex items-center gap-6 border-t border-zinc-800 md:border-t-0 pt-4 md:pt-0">
                    <div className="text-center md:text-right">
                        <p className="text-zinc-500 text-xs uppercase tracking-wider">Size</p>
                        <p className="text-zinc-200 font-medium capitalize">{parcel.size}</p>
                    </div>

                    <div className="bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2 text-center min-w-25">
                        <p className="text-zinc-500 text-[10px] uppercase tracking-wider font-semibold">Pickup code</p>
                        <p className="text-indigo-400 font-mono font-bold text-lg tracking-widest">{parcel.pickup_code}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
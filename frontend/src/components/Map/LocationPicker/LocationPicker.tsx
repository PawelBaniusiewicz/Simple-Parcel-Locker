import { useMapEvents } from 'react-leaflet';
import { LatLng } from 'leaflet';

interface LocationPickerProps {
    onLocationSelect: (latlng: LatLng) => void;
}

export default function LocationPicker({ onLocationSelect }: LocationPickerProps) {
    useMapEvents({
        click(e) {
            onLocationSelect(e.latlng);
        },
    });
    return null;
}
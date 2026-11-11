import { CircleMarker, Popup } from 'react-leaflet';
import type { LocatedVehicle } from '../types/vehicle';
import { PROVIDER_COLORS, PROVIDER_LABELS } from './providers';

const recordedAtFormatter = new Intl.DateTimeFormat(undefined, {
  dateStyle: 'medium',
  timeStyle: 'medium',
});

export function formatRecordedAt(recordedAt: string): string {
  return recordedAtFormatter.format(new Date(recordedAt));
}

interface VehicleMarkerProps {
  vehicle: LocatedVehicle;
}

export default function VehicleMarker({ vehicle }: VehicleMarkerProps) {
  const { lat, lng, recorded_at: recordedAt, provider } = vehicle.last_position;
  const color = PROVIDER_COLORS[provider];

  return (
    <CircleMarker
      center={[lat, lng]}
      radius={10}
      pathOptions={{ color, fillColor: color, fillOpacity: 0.6 }}
    >
      <Popup>
        <strong>{vehicle.name}</strong>
        <div>
          {vehicle.plate} · {PROVIDER_LABELS[provider]}
        </div>
        <div>{formatRecordedAt(recordedAt)}</div>
      </Popup>
    </CircleMarker>
  );
}

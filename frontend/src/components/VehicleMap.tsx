import { MapContainer, TileLayer } from 'react-leaflet';
import type { LocatedVehicle, Vehicle } from '../types/vehicle';
import ProviderLegend from './ProviderLegend';
import VehicleMarker from './VehicleMarker';

const BOGOTA_CENTER: [number, number] = [4.65, -74.08];
const BOGOTA_ZOOM = 12;
const OSM_ATTRIBUTION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const OSM_TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

interface VehicleMapProps {
  vehicles: Vehicle[];
}

function withPosition(vehicles: Vehicle[]): LocatedVehicle[] {
  return vehicles.filter((vehicle): vehicle is LocatedVehicle => vehicle.last_position !== null);
}

export default function VehicleMap({ vehicles }: VehicleMapProps) {
  const located = withPosition(vehicles);

  return (
    <div className="map-container">
      <MapContainer center={BOGOTA_CENTER} zoom={BOGOTA_ZOOM} className="map">
        <TileLayer attribution={OSM_ATTRIBUTION} url={OSM_TILE_URL} />
        {located.map((vehicle) => (
          <VehicleMarker key={vehicle.uuid} vehicle={vehicle} />
        ))}
      </MapContainer>
      <ProviderLegend />
    </div>
  );
}

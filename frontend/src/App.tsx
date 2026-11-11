import StatusBanner from './components/StatusBanner';
import VehicleMap from './components/VehicleMap';
import { useVehicles } from './hooks/useVehicles';

export default function App() {
  const { vehicles, isLoading, error } = useVehicles();

  return (
    <div className="app">
      <header className="app-header">
        <h1>Fleet Tracker</h1>
      </header>
      <main className="map-area">
        <StatusBanner isLoading={isLoading} error={error} />
        <VehicleMap vehicles={vehicles} />
      </main>
    </div>
  );
}

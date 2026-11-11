import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import App from './App';
import { useVehicles } from './hooks/useVehicles';
import type { Vehicle } from './types/vehicle';

vi.mock('./hooks/useVehicles', () => ({
  useVehicles: vi.fn(),
}));

const locatedVehicle: Vehicle = {
  uuid: '2b7e0000-0000-0000-0000-000000000001',
  plate: 'ABC123',
  name: 'Camión 01',
  last_position: {
    lat: 4.6097,
    lng: -74.0817,
    recorded_at: '2026-11-12T03:15:00Z',
    provider: 'alpha',
  },
};

describe('App', () => {
  it('muestra el título, el banner de carga y el mapa', () => {
    vi.mocked(useVehicles).mockReturnValue({ vehicles: [], isLoading: true, error: null });

    render(<App />);

    expect(screen.getByRole('heading', { name: 'Fleet Tracker' })).toBeInTheDocument();
    expect(screen.getByText('Cargando vehículos…')).toBeInTheDocument();
    expect(screen.getByTestId('map')).toBeInTheDocument();
  });

  it('muestra el error y conserva los marcadores del mapa', () => {
    vi.mocked(useVehicles).mockReturnValue({
      vehicles: [locatedVehicle],
      isLoading: false,
      error: new Error('network down'),
    });

    render(<App />);

    expect(screen.getByRole('alert')).toHaveTextContent('No se pudo actualizar');
    expect(screen.getByTestId('marker')).toBeInTheDocument();
  });
});

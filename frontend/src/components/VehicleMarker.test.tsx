import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import type { LocatedVehicle } from '../types/vehicle';
import { PROVIDER_COLORS } from './providers';
import VehicleMarker, { formatRecordedAt } from './VehicleMarker';

const vehicle: LocatedVehicle = {
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

describe('VehicleMarker', () => {
  it('usa el color del proveedor Alpha', () => {
    render(<VehicleMarker vehicle={vehicle} />);

    expect(screen.getByTestId('marker')).toHaveAttribute('data-color', PROVIDER_COLORS.alpha);
  });

  it('usa el color del proveedor Beta', () => {
    const betaVehicle: LocatedVehicle = {
      ...vehicle,
      last_position: { ...vehicle.last_position, provider: 'beta' },
    };

    render(<VehicleMarker vehicle={betaVehicle} />);

    expect(screen.getByTestId('marker')).toHaveAttribute('data-color', PROVIDER_COLORS.beta);
  });

  it('muestra nombre, placa, proveedor y fecha formateada en el popup', () => {
    render(<VehicleMarker vehicle={vehicle} />);

    const popup = screen.getByTestId('popup');
    expect(popup).toHaveTextContent('Camión 01');
    expect(popup).toHaveTextContent('ABC123');
    expect(popup).toHaveTextContent('Alpha');
    expect(popup).toHaveTextContent(formatRecordedAt('2026-11-12T03:15:00Z'));
  });
});

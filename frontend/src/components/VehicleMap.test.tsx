import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import type { Vehicle } from '../types/vehicle';
import VehicleMap from './VehicleMap';

const withAlphaPosition: Vehicle = {
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

const withBetaPosition: Vehicle = {
  uuid: '9a4d0000-0000-0000-0000-000000000002',
  plate: 'DEF456',
  name: 'Camión 02',
  last_position: {
    lat: 4.6533,
    lng: -74.0836,
    recorded_at: '2026-11-12T03:20:00Z',
    provider: 'beta',
  },
};

const withoutPosition: Vehicle = {
  uuid: '9a4d0000-0000-0000-0000-000000000003',
  plate: 'XYZ789',
  name: 'Camión 04',
  last_position: null,
};

describe('VehicleMap', () => {
  it('renderiza un marcador por vehículo con posición y ninguno para null', () => {
    render(<VehicleMap vehicles={[withAlphaPosition, withoutPosition, withBetaPosition]} />);

    expect(screen.getAllByTestId('marker')).toHaveLength(2);
  });

  it('centra el mapa en Bogotá con zoom 12', () => {
    render(<VehicleMap vehicles={[]} />);

    const map = screen.getByTestId('map');
    expect(map).toHaveAttribute('data-center', JSON.stringify([4.65, -74.08]));
    expect(map).toHaveAttribute('data-zoom', '12');
  });

  it('incluye la atribución de OpenStreetMap', () => {
    render(<VehicleMap vehicles={[]} />);

    const tileLayer = screen.getByTestId('tile-layer');
    expect(tileLayer.getAttribute('data-attribution')).toContain('OpenStreetMap');
  });
});

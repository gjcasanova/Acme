export type Provider = 'alpha' | 'beta';

export interface LastPosition {
  lat: number;
  lng: number;
  recorded_at: string;
  provider: Provider;
}

export interface Vehicle {
  uuid: string;
  plate: string;
  name: string;
  last_position: LastPosition | null;
}

export interface LocatedVehicle extends Vehicle {
  last_position: LastPosition;
}

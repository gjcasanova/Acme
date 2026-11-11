import { API_URL } from '../config';
import type { Vehicle } from '../types/vehicle';

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message?: string,
  ) {
    super(message ?? `Request failed with status ${status}`);
    this.name = 'ApiError';
  }
}

export async function fetchVehicles(signal?: AbortSignal): Promise<Vehicle[]> {
  const response = await fetch(`${API_URL}/vehicles`, { signal });

  if (!response.ok) {
    throw new ApiError(response.status);
  }

  return (await response.json()) as Vehicle[];
}

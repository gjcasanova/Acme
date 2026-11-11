import { afterEach, describe, expect, it, vi } from 'vitest';
import { API_URL } from '../config';
import type { Vehicle } from '../types/vehicle';
import { ApiError, fetchVehicles } from './vehicles';

const vehicles: Vehicle[] = [
  {
    uuid: '2b7e0000-0000-0000-0000-000000000001',
    plate: 'ABC123',
    name: 'Camión 01',
    last_position: {
      lat: 4.6097,
      lng: -74.0817,
      recorded_at: '2026-11-12T03:15:00Z',
      provider: 'alpha',
    },
  },
  {
    uuid: '9a4d0000-0000-0000-0000-000000000002',
    plate: 'XYZ789',
    name: 'Camión 04',
    last_position: null,
  },
];

function stubFetch(response: { ok: boolean; status: number; json?: () => Promise<unknown> }) {
  const fetchMock = vi.fn().mockResolvedValue(response);
  vi.stubGlobal('fetch', fetchMock);
  return fetchMock;
}

describe('fetchVehicles', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('devuelve el listado tipado con una respuesta 200', async () => {
    stubFetch({ ok: true, status: 200, json: async () => vehicles });

    await expect(fetchVehicles()).resolves.toEqual(vehicles);
  });

  it('lanza ApiError con el status cuando la respuesta no es ok', async () => {
    stubFetch({ ok: false, status: 500 });

    const error = await fetchVehicles().catch((cause: unknown) => cause);

    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 500 });
  });

  it('usa la URL construida a partir de API_URL', async () => {
    const fetchMock = stubFetch({ ok: true, status: 200, json: async () => [] });

    await fetchVehicles();

    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/vehicles`, { signal: undefined });
  });

  it('pasa el signal a fetch', async () => {
    const fetchMock = stubFetch({ ok: true, status: 200, json: async () => [] });
    const controller = new AbortController();

    await fetchVehicles(controller.signal);

    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/vehicles`, { signal: controller.signal });
  });
});

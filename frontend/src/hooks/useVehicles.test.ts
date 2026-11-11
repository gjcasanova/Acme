import { act, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { fetchVehicles } from '../api/vehicles';
import type { Vehicle } from '../types/vehicle';
import { useVehicles } from './useVehicles';

vi.mock('../api/vehicles', () => ({
  fetchVehicles: vi.fn(),
}));

const vehicle: Vehicle = {
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

async function flush() {
  await act(async () => {
    await Promise.resolve();
    await Promise.resolve();
    await Promise.resolve();
    await Promise.resolve();
  });
}

describe('useVehicles', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.mocked(fetchVehicles).mockReset();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('hace la primera petición al montar y otra cada 5 s', async () => {
    vi.mocked(fetchVehicles).mockResolvedValue([]);

    renderHook(() => useVehicles());
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(1);

    vi.advanceTimersByTime(5000);
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(2);
  });

  it('isLoading pasa a false tras la primera respuesta', async () => {
    vi.mocked(fetchVehicles).mockResolvedValue([]);

    const { result } = renderHook(() => useVehicles());
    expect(result.current.isLoading).toBe(true);

    await flush();
    expect(result.current.isLoading).toBe(false);
  });

  it('ante un error conserva los vehículos anteriores y expone el error', async () => {
    vi.mocked(fetchVehicles)
      .mockResolvedValueOnce([vehicle])
      .mockRejectedValueOnce(new Error('network down'));

    const { result } = renderHook(() => useVehicles());
    await flush();
    expect(result.current.vehicles).toEqual([vehicle]);
    expect(result.current.error).toBeNull();

    vi.advanceTimersByTime(5000);
    await flush();
    expect(result.current.vehicles).toEqual([vehicle]);
    expect(result.current.error).toEqual(new Error('network down'));
  });

  it('tras un error, una petición exitosa limpia el error', async () => {
    vi.mocked(fetchVehicles)
      .mockResolvedValueOnce([vehicle])
      .mockRejectedValueOnce(new Error('network down'))
      .mockResolvedValueOnce([vehicle]);

    const { result } = renderHook(() => useVehicles());
    await flush();

    vi.advanceTimersByTime(5000);
    await flush();
    expect(result.current.error).toEqual(new Error('network down'));

    vi.advanceTimersByTime(5000);
    await flush();
    expect(result.current.error).toBeNull();
    expect(result.current.vehicles).toEqual([vehicle]);
  });

  it('al desmontar deja de hacer peticiones y aborta la petición en curso', async () => {
    let capturedSignal: AbortSignal | undefined;
    vi.mocked(fetchVehicles).mockImplementationOnce(
      (signal?: AbortSignal) =>
        new Promise<Vehicle[]>(() => {
          capturedSignal = signal;
        }),
    );

    const { unmount } = renderHook(() => useVehicles());
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(1);
    expect(capturedSignal?.aborted).toBe(false);

    unmount();
    expect(capturedSignal?.aborted).toBe(true);

    vi.advanceTimersByTime(15000);
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(1);
  });

  it('no inicia una petición nueva si la anterior sigue en curso', async () => {
    let resolveFirst!: (value: Vehicle[]) => void;
    vi.mocked(fetchVehicles).mockImplementationOnce(
      () =>
        new Promise<Vehicle[]>((resolve) => {
          resolveFirst = resolve;
        }),
    );

    renderHook(() => useVehicles());
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(1);

    vi.advanceTimersByTime(5000);
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(1);

    await act(async () => {
      resolveFirst([vehicle]);
    });
    await flush();
    expect(fetchVehicles).toHaveBeenCalledTimes(1);
  });
});

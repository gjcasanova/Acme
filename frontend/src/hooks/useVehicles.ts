import { useEffect, useState } from 'react';
import { fetchVehicles } from '../api/vehicles';
import type { Vehicle } from '../types/vehicle';

export interface UseVehiclesResult {
  vehicles: Vehicle[];
  isLoading: boolean;
  error: Error | null;
}

export function useVehicles(intervalMs = 5000): UseVehiclesResult {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let mounted = true;
    let inFlight = false;
    let controller: AbortController | null = null;

    async function load(): Promise<void> {
      if (inFlight) {
        return;
      }
      inFlight = true;
      controller = new AbortController();

      try {
        const next = await fetchVehicles(controller.signal);
        if (!mounted) {
          return;
        }
        setVehicles(next);
        setError(null);
      } catch (cause) {
        if (!mounted) {
          return;
        }
        setError(cause instanceof Error ? cause : new Error(String(cause)));
      } finally {
        inFlight = false;
        if (mounted) {
          setIsLoading(false);
        }
      }
    }

    void load();
    const intervalId = window.setInterval(load, intervalMs);

    return () => {
      mounted = false;
      window.clearInterval(intervalId);
      controller?.abort();
    };
  }, [intervalMs]);

  return { vehicles, isLoading, error };
}

import { useEffect, useRef, useState } from 'react';
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
  const inFlight = useRef(false);
  const controller = useRef<AbortController | null>(null);

  useEffect(() => {
    let mounted = true;

    async function load(): Promise<void> {
      if (inFlight.current) {
        return;
      }
      inFlight.current = true;
      const requestController = new AbortController();
      controller.current = requestController;

      try {
        const next = await fetchVehicles(requestController.signal);
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
        inFlight.current = false;
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
      controller.current?.abort();
    };
  }, [intervalMs]);

  return { vehicles, isLoading, error };
}

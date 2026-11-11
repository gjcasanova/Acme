interface StatusBannerProps {
  isLoading: boolean;
  error: Error | null;
}

export default function StatusBanner({ isLoading, error }: StatusBannerProps) {
  if (isLoading) {
    return (
      <div className="status-banner status-banner--loading" role="status">
        Cargando vehículos…
      </div>
    );
  }

  if (error) {
    return (
      <div className="status-banner status-banner--error" role="alert">
        No se pudo actualizar la posición de los vehículos. Reintentando…
      </div>
    );
  }

  return null;
}

import type { ReactNode } from 'react';

interface MapContainerProps {
  children?: ReactNode;
  center?: unknown;
  zoom?: number;
}

interface TileLayerProps {
  attribution?: string;
  url?: string;
}

interface CircleMarkerProps {
  children?: ReactNode;
  center?: unknown;
  radius?: number;
  pathOptions?: { color?: string; fillColor?: string; fillOpacity?: number };
}

interface PopupProps {
  children?: ReactNode;
}

export function MapContainer({ children, center, zoom }: MapContainerProps) {
  return (
    <div data-testid="map" data-center={JSON.stringify(center)} data-zoom={zoom}>
      {children}
    </div>
  );
}

export function TileLayer({ attribution, url }: TileLayerProps) {
  return <div data-testid="tile-layer" data-attribution={attribution} data-url={url} />;
}

export function CircleMarker({ children, center, radius, pathOptions }: CircleMarkerProps) {
  const [lat, lng] = Array.isArray(center) ? center : [];

  return (
    <div
      data-testid="marker"
      data-lat={lat}
      data-lng={lng}
      data-radius={radius}
      data-color={pathOptions?.color}
    >
      {children}
    </div>
  );
}

export function Popup({ children }: PopupProps) {
  return <div data-testid="popup">{children}</div>;
}

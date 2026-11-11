import type { Provider } from '../types/vehicle';
import { PROVIDER_COLORS, PROVIDER_LABELS } from './providers';

const PROVIDERS: Provider[] = ['alpha', 'beta'];

export default function ProviderLegend() {
  return (
    <ul className="provider-legend" aria-label="Leyenda de proveedores">
      {PROVIDERS.map((provider) => (
        <li key={provider} className="provider-legend__item">
          <span
            className="provider-legend__dot"
            data-testid={`legend-dot-${provider}`}
            style={{ backgroundColor: PROVIDER_COLORS[provider] }}
          />
          {PROVIDER_LABELS[provider]}
        </li>
      ))}
    </ul>
  );
}

import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { PROVIDER_COLORS } from './providers';
import ProviderLegend from './ProviderLegend';

describe('ProviderLegend', () => {
  it('muestra los dos proveedores', () => {
    render(<ProviderLegend />);

    expect(screen.getByText('Alpha')).toBeInTheDocument();
    expect(screen.getByText('Beta')).toBeInTheDocument();
  });

  it('colorea cada proveedor con su color', () => {
    render(<ProviderLegend />);

    expect(screen.getByTestId('legend-dot-alpha')).toHaveStyle({
      backgroundColor: PROVIDER_COLORS.alpha,
    });
    expect(screen.getByTestId('legend-dot-beta')).toHaveStyle({
      backgroundColor: PROVIDER_COLORS.beta,
    });
  });
});

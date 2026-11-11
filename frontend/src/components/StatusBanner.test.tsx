import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import StatusBanner from './StatusBanner';

describe('StatusBanner', () => {
  it('muestra el estado de carga', () => {
    render(<StatusBanner isLoading error={null} />);

    expect(screen.getByText('Cargando vehículos…')).toBeInTheDocument();
  });

  it('muestra el error con role="alert"', () => {
    render(<StatusBanner isLoading={false} error={new Error('network down')} />);

    expect(screen.getByRole('alert')).toHaveTextContent(
      'No se pudo actualizar la posición de los vehículos. Reintentando…',
    );
  });

  it('no renderiza nada sin carga ni error', () => {
    const { container } = render(<StatusBanner isLoading={false} error={null} />);

    expect(container).toBeEmptyDOMElement();
  });
});

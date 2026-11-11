import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

vi.mock('react-leaflet', () => import('./react-leaflet-mock'));

# Fleet Tracker

[![CI](https://github.com/gjcasanova/Acme/actions/workflows/ci.yml/badge.svg)](https://github.com/gjcasanova/Acme/actions/workflows/ci.yml)

Plataforma de seguimiento de flota que recibe posiciones GPS de **dos proveedores con formatos distintos**, las normaliza a un modelo único y muestra la última posición de cada vehículo en un mapa.

El problema central que resuelve es la **integración multiproveedor**: cada proveedor envía los datos con nombres de campo, identificadores y formatos de tiempo diferentes, y el sistema los traduce a un modelo interno común sin acoplar la lógica de negocio a ningún proveedor.

## Arquitectura

```mermaid
flowchart LR
    Alpha["Proveedor Alpha"] --> AlphaAdapter["AlphaAdapter"]
    Beta["Proveedor Beta"] --> BetaAdapter["BetaAdapter"]
    AlphaAdapter --> PositionService["PositionService"]
    BetaAdapter --> PositionService
    PositionService --> DB[("SQLite")]
    DB --> VehicleService["VehicleService"]
    VehicleService --> VehiclesAPI["GET /vehicles"]
    VehiclesAPI --> Frontend["Frontend (mapa + polling)"]
```

- **Backend** — FastAPI + SQLAlchemy 2.0 + SQLite, con arquitectura en capas (puertos y adaptadores) para los proveedores.
- **Frontend** — React + TypeScript + Leaflet, con un mapa que se actualiza por polling cada 5 segundos.

## Cómo levantarlo

Requisitos: Docker con Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Una vez levantado:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Documentación interactiva de la API: http://localhost:8000/docs

Los datos se guardan en un volumen de Docker (`fleet-data`), por lo que se conservan al reiniciar los contenedores. Para borrarlo y empezar de cero: `docker compose down -v`.

## Enviar posiciones

La ingesta requiere autenticación con API key. El seed crea el usuario `Simulator` con la `SEED_API_KEY` del `.env` (en `.env.example` es `dev-secret-change-me`; sustitúyela si la cambias).

Proveedor **Alpha** (identificador `vehicle_id`, fecha ISO 8601 con zona horaria):

```bash
curl -X POST http://localhost:8000/providers/alpha/positions \
  -H "Authorization: Bearer dev-secret-change-me" \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "ALP-001", "lat": 4.6097, "lng": -74.0817, "ts": "2026-11-12T03:15:00Z"}'
```

Proveedor **Beta** (identificador `unit_code`, timestamp Unix en segundos):

```bash
curl -X POST http://localhost:8000/providers/beta/positions \
  -H "Authorization: Bearer dev-secret-change-me" \
  -H "Content-Type: application/json" \
  -d '{"unit_code": "BT-9001", "coords": {"latitude": 4.6533, "longitude": -74.0836}, "epoch": 1794452100}'
```

Listar vehículos con su última posición:

```bash
curl http://localhost:8000/vehicles
```

## Tests

### Backend

Requiere Python 3.12:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

### Frontend

Requiere Node 20:

```bash
cd frontend
npm ci
npm test
```

## Decisiones técnicas

- **Puertos y adaptadores**: cada proveedor tiene su propio adaptador (`AlphaAdapter`, `BetaAdapter`) que implementa el puerto `ProviderAdapter` y traduce su payload a una `NormalizedPosition`. Añadir un proveedor nuevo requiere solo un adaptador, un schema y un endpoint, sin tocar el servicio de negocio.
- **Hash SHA-256 de las API keys**: la key nunca se guarda en texto plano; se almacena su hash SHA-256 y la autenticación compara hashes.
- **«Última posición» por `recorded_at`**: `GET /vehicles` devuelve la posición con mayor `recorded_at`, no la última recibida, porque los GPS pueden enviar posiciones fuera de orden. Los vehículos sin posiciones se devuelven con `last_position: null`.
- **Testing por capas**: en el backend, los servicios se prueban contra SQLite en memoria (toda la lógica funcional) y la capa de presentación se prueba con servicios mockeados (solo códigos y forma del JSON), sin repetir verificaciones. En el frontend, `react-leaflet` se mockea en los tests, `fetch` se mockea y el polling se prueba con timers falsos.

## Proceso de desarrollo

<!-- TODO: capturas de PlanWork -->

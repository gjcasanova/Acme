from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers.providers import router as providers_router
from app.api.routers.vehicles import router as vehicles_router
from app.core.config import settings
from app.services.exceptions import InvalidApiKeyError, VehicleNotFoundError

app = FastAPI(title="Fleet Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(providers_router)


@app.exception_handler(InvalidApiKeyError)
def invalid_api_key_handler(request: Request, exc: InvalidApiKeyError) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or missing API key"},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(VehicleNotFoundError)
def vehicle_not_found_handler(request: Request, exc: VehicleNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Vehicle not found for provider {exc.provider.value}"},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

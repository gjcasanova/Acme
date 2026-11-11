from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.services.exceptions import InvalidApiKeyError

app = FastAPI(title="Fleet Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(InvalidApiKeyError)
def invalid_api_key_handler(request: Request, exc: InvalidApiKeyError) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or missing API key"},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

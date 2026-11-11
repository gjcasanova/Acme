from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.adapters.alpha import AlphaPayload
from app.api.dependencies import get_position_service, require_api_key
from app.api.schemas.providers import PositionOut
from app.models import User
from app.services.position_service import PositionService

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post(
    "/alpha/positions",
    response_model=PositionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_alpha_position(
    payload: AlphaPayload,
    _user: Annotated[User, Depends(require_api_key)],
    position_service: Annotated[PositionService, Depends(get_position_service)],
) -> PositionOut:
    return PositionOut.model_validate(position_service.register_from_alpha(payload))

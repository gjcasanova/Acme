from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_vehicle_service
from app.api.schemas.vehicles import VehicleOut
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehicleOut])
def list_vehicles(
    vehicle_service: Annotated[VehicleService, Depends(get_vehicle_service)],
) -> list[VehicleOut]:
    return [VehicleOut.model_validate(vehicle) for vehicle in vehicle_service.list_vehicles()]

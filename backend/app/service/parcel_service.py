from dataclasses import dataclass
from typing import Any

from ..db.entity import UserEntity
from ..db.repository import ParcelRepository, parcel_repository, user_repository
from .dto import ParcelDto

import logging

from ..models.enums import Status
from app.config import ALLOWED_TRANSITIONS

logging.basicConfig(level=logging.INFO)

@dataclass
class ParcelService:
    parcel_repository: ParcelRepository

    @staticmethod
    def get_users_parcels(receiver_id: int) -> list[dict[str, Any]]:
        parcels = parcel_repository.find_all_parcels_by_user_id(receiver_id)
        return [ParcelDto.from_parcel_entity(parcel).to_dict() for parcel in parcels]

    @staticmethod
    def change_parcel_status(parcel_id: int, new_status: Status, current_user: UserEntity) -> dict[str, Any]:
        user = user_repository.find_by_id(current_user.id)
        parcel = parcel_repository.find_by_id(parcel_id)
        
        if not user:
            raise ValueError("Cannot update parcel status - User not found")

        if not parcel:
            raise ValueError("Cannot update parcel status - Parcel not found")

        if new_status not in ALLOWED_TRANSITIONS[parcel.status]:
            raise ValueError("Cannot upgrade parcel status - Cannot change parcel status")

        new_parcel_status = parcel_repository.update_parcel_status(parcel_id, new_status)

        return ParcelDto.from_parcel_entity(new_parcel_status).to_dict()


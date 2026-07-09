from dataclasses import dataclass
from typing import Any

from ..db.repository import ParcelRepository, parcel_repository
from .dto import ParcelDto

import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class ParcelService:
    parcel_repository: ParcelRepository

    @staticmethod
    def get_users_parcels(user_id: int) -> list[dict[str, Any]]:
        parcels = parcel_repository.find_all_parcels_by_user_id(user_id)
        return [ParcelDto.from_parcel_entity(parcel).to_dict() for parcel in parcels]

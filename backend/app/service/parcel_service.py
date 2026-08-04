from dataclasses import dataclass
from typing import Any

from ..db.repository import ParcelRepository, parcel_repository, user_repository, locker_repository
from .pickup_code_service import PickUpCodeService
from app.config import ALLOWED_TRANSITIONS
from ..models.enums import Status, Roles
from ..db.entity import UserEntity
from .dto import ParcelDto

import logging
import datetime


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

        if user.role == Roles.USER:
            if parcel.sender_id != user.id and parcel.receiver_id != user.id:
                raise ValueError("Access denied: You do not have permission to modify this parcel.")

            if new_status not in [Status.PENDING, Status.DELIVERED]:
                raise ValueError(f"Access denied: Users cannot set status to '{new_status.value}'.")

        elif user.role == Roles.SUPPLIER:
            allowed_supplier_statuses = [
                Status.IN_TRANSIT,
                Status.IN_WAREHOUSE,
                Status.OUT_FOR_DELIVERY,
                Status.READY_FOR_PICKUP,
                Status.EXPIRED,
                Status.RETURNED
            ]
            if new_status not in allowed_supplier_statuses:
                raise ValueError(f"Access denied: Suppliers cannot set status to '{new_status.value}'.")

        if new_status not in ALLOWED_TRANSITIONS[parcel.status]:
            raise ValueError("Cannot upgrade parcel status - Cannot change parcel status")

        if new_status == Status.PENDING:
            free_locker = locker_repository.find_free_locker(
                parcel_locker_id=parcel.source_parcel_locker_id,
                size=parcel.size
            )
            if not free_locker:
                raise ValueError("No free lockers available in the source parcel locker.")

            parcel.locker_id = free_locker.id
            parcel.stored_at = datetime.datetime.now(datetime.UTC)
        elif new_status == Status.READY_FOR_PICKUP:
            free_locker = locker_repository.find_free_locker(
                parcel_locker_id=parcel.destination_parcel_locker_id,
                size=parcel.size
            )
            if not free_locker:
                raise ValueError("No free lockers available in the destination parcel locker.")

            parcel.locker_id = free_locker.id
            parcel.pickup_code = PickUpCodeService(parcel_repository).generate_pickup_code()
        elif new_status in [Status.IN_TRANSIT, Status.DELIVERED, Status.RETURNED]:
            parcel.locker_id = None
            parcel.stored_at = None
            parcel.pickup_code = None

        new_parcel_status = parcel_repository.update_parcel_status(parcel_id, new_status)

        return ParcelDto.from_parcel_entity(new_parcel_status).to_dict()

    def expire_old_parcels(self) -> int:
        expired_parcels = self.parcel_repository.find_parcels_to_expire()
        count = 0

        for parcel in expired_parcels:
            parcel.status = Status.EXPIRED
            parcel.pickup_code = None
            count += 1

        self.parcel_repository.save_or_update_many(expired_parcels)
        return count


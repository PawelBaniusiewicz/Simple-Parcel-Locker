from dataclasses import dataclass

from app.db.entity import ParcelLockerEntity
from app.db.repository import ParcelLockerRepository
from app.service.dto import ParcelLockerDto
from .locker_service import LockerService

from ..config import small_lockers, medium_lockers, large_lockers

@dataclass
class ParcelLockerService:
    parcel_locker_repo: ParcelLockerRepository
    locker_service: LockerService

    def get_parcel_locker_by_id(self, parcel_locker_id: int) -> ParcelLockerDto | None:
        parcel_locker = self.parcel_locker_repo.find_by_id(parcel_locker_id)

        if not parcel_locker:
            raise ValueError(f'Cannot find parcel locker with ID {parcel_locker_id}')

        return ParcelLockerDto.from_parcel_locker_entity(parcel_locker)

    def get_all_parcel_lockers(self) -> list['ParcelLockerDto']:
        parcel_lockers = self.parcel_locker_repo.find_all()

        if not parcel_lockers:
            return []

        return [ParcelLockerDto.from_parcel_locker_entity(pl) for pl in parcel_lockers]

    def add_parcel_locker(self, name: str, address: str, latitude: float, longitude: float) -> 'ParcelLockerDto':
        parcel_locker = ParcelLockerEntity(
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude
        )

        self.parcel_locker_repo.save_or_update(parcel_locker)

        self.locker_service.create_lockers_for_parcel_locker(
            small_lockers,
            medium_lockers,
            large_lockers,
            parcel_locker.id 
        )

        return ParcelLockerDto.from_parcel_locker_entity(parcel_locker)
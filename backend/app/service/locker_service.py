from dataclasses import dataclass

from app.db.entity import LockerEntity
from app.db.repository import LockerRepository
from app.models.enums import Size


@dataclass
class LockerService:
    locker_repo: LockerRepository

    def create_lockers_for_parcel_locker(self,
                                         small_lockers_number: int,
                                         medium_lockers_number: int,
                                         large_lockers_number: int,
                                         parcel_locker_id: int) -> None:
        lockers = []
        lockers.extend(
            [LockerEntity(size=Size.SMALL, parcel_locker_id=parcel_locker_id) for _ in range(small_lockers_number)])
        lockers.extend(
            [LockerEntity(size=Size.MEDIUM, parcel_locker_id=parcel_locker_id) for _ in range(medium_lockers_number)])
        lockers.extend(
            [LockerEntity(size=Size.LARGE, parcel_locker_id=parcel_locker_id) for _ in range(large_lockers_number)])

        self.locker_repo.save_or_update_many(lockers)
from app.db.repository import ParcelRepository

from dataclasses import dataclass
import secrets
import string

@dataclass
class PickUpCodeService:
    parcel_repository: ParcelRepository

    def generate_pickup_code(self) -> str:
        while True:
            new_pickup_code = ''.join(secrets.choice(string.digits) for _ in range(6))
            existing_pickup_code = self.parcel_repository.find_by_pickup_code(new_pickup_code)

            if not existing_pickup_code:
                return new_pickup_code
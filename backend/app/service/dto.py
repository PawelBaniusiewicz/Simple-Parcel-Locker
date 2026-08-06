from dataclasses import dataclass
from typing import Self, Any

from app.db.entity import UserEntity, ParcelEntity, ParcelLockerEntity, LockerEntity
from ..models.enums import Size, Status

import datetime

@dataclass
class RegisterUserDto:
    name: str
    email: str
    password: str
    password_confirmation: str
    phone_number: str

    def check_passwords(self) -> bool:
        return self.password == self.password_confirmation

    def with_password(self, new_password: str) -> Self:
        return RegisterUserDto(
            name=self.name,
            email=self.email,
            password=new_password,
            password_confirmation=self.password_confirmation,
            phone_number=self.phone_number
        )

    def to_user_entity(self) -> UserEntity:
        return UserEntity(
            name=self.name,
            email=self.email,
            hashed_password=self.password,
            phone_number=self.phone_number,
            is_active=False,
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            password_confirmation=data['password_confirmation'],
            phone_number=data['phone_number']
        )


@dataclass
class UserDto:
    id: int
    name: str
    email: str
    phone_number: str

    def to_dict(self) -> dict[str, int | str]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number
        }

    @classmethod
    def from_user_entity(cls, user_entity: UserEntity) -> Self:
        return cls(
            user_entity.id,
            user_entity.name,
            user_entity.email,
            user_entity.phone_number
        )

@dataclass
class ParcelDto:
    id: int
    content: str
    size: Size
    tracking_number: str
    status: Status
    pickup_code: str
    stored_at: datetime.datetime
    created_at: datetime.datetime
    locker_id: int
    receiver_id: int
    sender_id: int

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content,
            'size': self.size.value,
            'tracking_number': self.tracking_number,
            'status': self.status.value,
            'pickup_code': self.pickup_code,
            'stored_at': self.stored_at,
            'created_at': self.created_at,
            'locker_id': self.locker_id,
            'receiver_id': self.receiver_id,
            'sender_id': self.sender_id
        }

    @classmethod
    def from_parcel_entity(cls, parcel_entity: ParcelEntity) -> Self:
        return cls(
            parcel_entity.id,
            parcel_entity.content,
            parcel_entity.size,
            parcel_entity.tracking_number,
            parcel_entity.status,
            parcel_entity.pickup_code,
            parcel_entity.stored_at,
            parcel_entity.created_at,
            parcel_entity.locker_id,
            parcel_entity.receiver_id,
            parcel_entity.sender_id
        )

@dataclass
class ParcelLockerDto:
    id: int
    name: str
    address: str
    latitude: float
    longitude: float

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    @classmethod
    def from_parcel_locker_entity(cls, parcel_locker_entity: ParcelLockerEntity) -> Self:
        return cls(
            parcel_locker_entity.id,
            parcel_locker_entity.name,
            parcel_locker_entity.address,
            parcel_locker_entity.latitude,
            parcel_locker_entity.longitude
        )

@dataclass
class LockerDto:
    id: int
    size: Status
    parcel_locker_id: int

    @classmethod
    def from_locker_entity(cls, locker_entity: LockerEntity) -> Self:
        return cls(
            locker_entity.id,
            locker_entity.size,
            locker_entity.parcel_locker_id
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'size': self.size.value,
            'parcel_locker_id': self.parcel_locker_id
        }
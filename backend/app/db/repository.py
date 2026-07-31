from flask_sqlalchemy import SQLAlchemy
from abc import ABC, abstractmethod

from .entity import UserEntity, ActivationTokenEntity, ParcelEntity, LockerEntity
from .configuration import sa
from ..models.enums import Status, Size


class CrudRepository[T](ABC):

    @abstractmethod
    def save_or_update(self, entity: T) -> None:
        pass

    @abstractmethod
    def save_or_update_many(self, entities: list[T]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass


class CrudRepositoryORM[T: sa.Model](CrudRepository[T]):

    def __init__(self, db: SQLAlchemy) -> None:
        self.sa = db
        self.entity_type =  self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, entity: T) -> None:
        self.sa.session.add(entity)
        self.sa.session.commit()

    def save_or_update_many(self, entities: list[T]) -> None:
        self.sa.session.add_all(entities)
        self.sa.session.commit()

    def find_by_id(self, entity_id: int) -> T | None:
        return self.sa.session.query(self.entity_type).get(entity_id)

    def find_all(self) -> list[T]:
        return sa.session.query(self.entity_type).all()

    def delete_by_id(self, entity_id: int) -> None:
        entity = self.find_by_id(entity_id)
        if entity:
            self.sa.session.delete(entity)
            self.sa.session.commit()

    def delete_all(self) -> None:
        self.sa.session.query(self.entity_type).delete()
        self.sa.session.commit()

class UserRepository(CrudRepositoryORM[UserEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_by_name(name: str) -> UserEntity | None:
        return UserEntity.query.filter_by(name=name).first()

    @staticmethod
    def find_by_email(email: str) -> UserEntity | None:
        return UserEntity.query.filter_by(email=email).first()

    @staticmethod
    def find_by_phone_number(phone_number: str) -> UserEntity | None:
        return UserEntity.query.filter_by(phone_number=phone_number).first()

class ActivationTokenRepository(CrudRepositoryORM[ActivationTokenEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_by_token(token: str) -> ActivationTokenEntity | None:
        return ActivationTokenEntity.query.filter_by(token=token).first()

class ParcelRepository(CrudRepositoryORM[ParcelEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_all_parcels_by_user_id(receiver_id: int) -> list[ParcelEntity]:
        return ParcelEntity.query.filter_by(receiver_id=receiver_id).all()

    def update_parcel_status(self, parcel_id: int, new_status: Status) -> ParcelEntity:
        parcel = self.find_by_id(parcel_id)
        if parcel:
            parcel.status = new_status
            self.save_or_update(parcel)
            return parcel
        else:
            raise ValueError('Parcel not found')

    def find_by_pickup_code(self, pickup_code: str) -> ParcelEntity | None:
        return self.sa.session.query(ParcelEntity).get(pickup_code)

class LockerRepository(CrudRepositoryORM[LockerEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_free_locker(parcel_locker_id: int, size: Size) -> LockerEntity | None:
        free_locker = (
            LockerEntity.query
            .outerjoin(ParcelEntity, ParcelEntity.locker_id == LockerEntity.id)
            .filter(LockerEntity.parcel_locker_id == parcel_locker_id)
            .filter(LockerEntity.size == size)
            .filter(ParcelEntity.locker_id.is_(None))
            .first()
        )
        return free_locker


user_repository = UserRepository(sa)
activation_token_repository = ActivationTokenRepository(sa)
parcel_repository = ParcelRepository(sa)
locker_repository = LockerRepository(sa)
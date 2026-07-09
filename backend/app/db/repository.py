from flask_sqlalchemy import SQLAlchemy
from abc import ABC, abstractmethod

from .entity import UserEntity, ActivationTokenEntity
from .configuration import sa

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


class CrudREpositoryORM[T: sa.Model](CrudRepository[T]):

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

class UserRepository(CrudREpositoryORM[UserEntity]):
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

class ActivationTokenRepository(CrudREpositoryORM[ActivationTokenEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_by_token(token: str) -> ActivationTokenEntity | None:
        return ActivationTokenEntity.query.filter_by(token=token).first()


user_repository = UserRepository(sa)
activation_token_repository = ActivationTokenRepository(sa)
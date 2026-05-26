from dataclasses import dataclass
from app.db.entity import UserEntity
from typing import Self

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
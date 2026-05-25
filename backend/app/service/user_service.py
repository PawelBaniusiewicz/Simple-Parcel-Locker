from dataclasses import dataclass
from ..db.repository import UserRepository
from .dto import RegisterUserDto, UserDto

@dataclass
class UserService:
    user_repository: UserRepository

    def register_user(self, register_user_dto: RegisterUserDto) -> UserDto:

        if not register_user_dto.check_passwords():
            raise ValueError('Passwords are not correct')

        if self.user_repository.find_by_name(register_user_dto.name):
            raise ValueError('Username already exists')

        if self.user_repository.find_by_email(register_user_dto.email):
            raise ValueError('Email already exists')

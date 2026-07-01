from dataclasses import dataclass
from ..db.repository import UserRepository
from .dto import RegisterUserDto, UserDto
from werkzeug.security import generate_password_hash
from app.mail.configuration import MailSender
from .token_service import ActivationTokenService
from app.db.repository import ActivationTokenRepository
from app.db.entity import ActivationTokenEntity
from app.config import (
    ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS,
    ACTIVATION_TOKEN_LENGTH
)
from os import getenv
import datetime
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class UserService:
    user_repository: UserRepository
    activation_token_repository: ActivationTokenRepository

    def register_user(self, register_user_dto: RegisterUserDto) -> dict[str, int | str]:

        if not register_user_dto.check_passwords():
            raise ValueError('Passwords are not correct')

        if self.user_repository.find_by_name(register_user_dto.name):
            raise ValueError('Username already exists')

        if self.user_repository.find_by_email(register_user_dto.email):
            raise ValueError('Email already exists')

        if self.user_repository.find_by_phone_number(register_user_dto.phone_number):
            raise ValueError('Phone number already exists')

        user_entity = register_user_dto.with_password(
            generate_password_hash(register_user_dto.password)
        ).to_user_entity()
        self.user_repository.save_or_update(user_entity)
        timestamp = (datetime.datetime.now(datetime.UTC) +
                     datetime.timedelta(seconds=ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS))
        token = ActivationTokenService.generate_activation_token(ACTIVATION_TOKEN_LENGTH)
        user_id = user_entity.id
        self.activation_token_repository.save_or_update(ActivationTokenEntity(
            timestamp=timestamp.timestamp(),
            token=token,
            user_id=user_id))
        MailSender.send(register_user_dto.email,
                        register_user_dto.name ,
                        'Active Your ParcelLocker account',
                        f'{getenv("ACTIVATE_ACCOUNT")}?token={token}')
        return UserDto.from_user_entity(user_entity).to_dict()

    def active_user(self, token: str) -> UserDto:
        activation_token_with_user = self.activation_token_repository.find_by_token(token)
        if activation_token_with_user is None:
            raise ValueError('User not found')

        if not activation_token_with_user.is_active():
            self.activation_token_repository.delete_by_id(activation_token_with_user.id)
            raise ValueError('Token has been expired')

        user_to_activate = activation_token_with_user.user
        user_to_activate.is_active = True
        self.user_repository.save_or_update(user_to_activate)
        self.activation_token_repository.delete_by_id(activation_token_with_user.id)
        return UserDto.from_user_entity(user_to_activate).to_dict()

from .user_service import UserService
from ..db.repository import user_repository

user_service = UserService(user_repository)
from .user_service import UserService
from ..db.repository import user_repository
from app.db.repository import activation_token_repository

user_service = UserService(user_repository, activation_token_repository)
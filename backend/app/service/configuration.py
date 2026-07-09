from app.db.repository import activation_token_repository
from ..db.repository import user_repository
from .user_service import UserService

user_service = UserService(user_repository, activation_token_repository)
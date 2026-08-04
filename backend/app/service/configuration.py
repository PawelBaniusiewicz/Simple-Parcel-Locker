from app.db.repository import activation_token_repository, user_repository, parcel_repository, locker_repository
from .parcel_service import ParcelService
from .user_service import UserService

user_service = UserService(user_repository, activation_token_repository)
parcel_service = ParcelService(parcel_repository)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from .configuration import sa
from ..models.enums import Status, Size, Roles


class ParcelLockerEntity(sa.Model):
    __tablename__ = 'parcel_lockers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    lockers: Mapped[list['LockerEntity']] = relationship(back_populates="parcel_locker")


class LockerEntity(sa.Model):
    __tablename__ = 'lockers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    size: Mapped[Size] = mapped_column(nullable=False)

    parcel_locker_id: Mapped[int] = mapped_column(ForeignKey("parcel_lockers.id"))
    parcel_locker: Mapped[ParcelLockerEntity] = relationship(back_populates="lockers")

    parcel: Mapped['ParcelEntity'] = relationship(back_populates="locker")


class ParcelEntity(sa.Model):
    __tablename__ = 'parcels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(250), nullable=False)
    size: Mapped[Size] = mapped_column(nullable=False)
    tracking_number: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    status: Mapped[Status] = mapped_column(nullable=False)
    pickup_code: Mapped[str] = mapped_column(String(6), unique=False)
    stored_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    locker_id: Mapped[int] = mapped_column(ForeignKey("lockers.id"), nullable=True)
    locker: Mapped['LockerEntity'] = relationship(back_populates="parcel")

    reciver: Mapped['UserEntity'] = relationship(back_populates="parcels")
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class UserEntity(sa.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, server_default='0')
    role: Mapped[Roles] = mapped_column(nullable=False, default='user', server_default='user')

    parcels: Mapped[list[ParcelEntity]] = relationship(back_populates="reciver")

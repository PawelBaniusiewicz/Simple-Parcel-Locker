from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from .configuration import sa, Size, Status


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
    size: Mapped[Size] = mapped_column(nullable=False)
    tracking_number: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    status: Mapped[Status] = mapped_column(nullable=False)

    locker_id: Mapped[int] = mapped_column(ForeignKey("lockers.id"), nullable=True)
    locker: Mapped['LockerEntity'] = relationship(back_populates="parcel")

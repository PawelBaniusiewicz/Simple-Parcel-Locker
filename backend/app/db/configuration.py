from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
import enum
import logging

logging.basicConfig(level=logging.INFO)

sa = SQLAlchemy()

# -----------------------------------------------
# Locker and parcel size and Status
# -----------------------------------------------
class Size(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Status(enum.Enum):
    LABEL_CREATED = "label_created",
    PENDING = "pending"
    IN_TRANSIT = "in_transit",
    OUT_FOR_DELIVERY = "out_for_delivery",
    READY_FOR_PICKUP = "ready_for_pickup",
    DELIVERED = "delivered",
    EXPIRED = "expired",
    RETURNED = "returned_to_sender",

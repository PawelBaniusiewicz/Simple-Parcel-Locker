from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
import enum
import logging

logging.basicConfig(level=logging.INFO)

sa = SQLAlchemy()

#-----------------------------------------------
# Configuring environment variables
#-----------------------------------------------
ENV_FILE = '.env'
ENV_PATH = Path().cwd().absolute().joinpath(f'{ENV_FILE}')
load_dotenv(ENV_PATH)

# -----------------------------------------------
# Configuring db connection
# -----------------------------------------------
db_username = getenv('DB_USERNAME')
db_password = getenv('DB_PASSWORD')
db_name = getenv('DB_NAME')
db_port = getenv('DB_PORT')
db_hostname = getenv('DB_HOSTNAME')
db_uri = f"mysql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"

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

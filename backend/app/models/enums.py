import enum

class Size(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Status(enum.Enum):
    LABEL_CREATED = "label_created",
    PENDING = "pending"
    IN_TRANSIT = "in_transit",
    IN_WAREHOUSE = "in_WEREHOUSE",
    OUT_FOR_DELIVERY = "out_for_delivery",
    READY_FOR_PICKUP = "ready_for_pickup",
    DELIVERED = "delivered",
    EXPIRED = "expired",
    RETURNED = "returned_to_sender",

class Roles(enum.Enum):
    USER = 'user'
    SUPPLIER = 'supplier'
    ADMIN = 'admin'
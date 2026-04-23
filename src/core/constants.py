from enum import Enum

MAX_VEHICLES_PER_DRIVER: int = 3

DEFAULT_EMAIL_FROM = "no-reply@logistics-app.com"


class Role(str, Enum):
    DRIVER = "driver"
    COMPANY = "company"


class OrderStatus(str, Enum):
    SEARCH = "search"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class OfferStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
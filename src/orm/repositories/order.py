from src.orm.models.order import Order
from src.orm.repositories.base import BaseRepository


class OrderRepository(BaseRepository):
    model = Order

'''
Order Class
represents an order with a price, quantity, type, and timestamp
'''

from dataclasses import dataclass
from enum import Enum
import time

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass
class Order:
    order_id: int
    price: float
    quantity: int
    order_type: OrderType
    timestamp: float = time.time()

    def __str__(self):
        return f"{self.order_type.value.upper()} {self.quantity} @ {self.price} (ID: {self.order_id})"


from core.order_book import OrderBook
from core.order import Order, OrderType

def test_order_matching():
    ob = OrderBook()
    
    ob.place_order(Order(1, 100, 5, OrderType.BUY))
    ob.place_order(Order(2, 101, 5, OrderType.BUY))
    ob.place_order(Order(3, 102, 10, OrderType.SELL))

    ob.match_orders()
    ob.print_order_book()

test_order_matching()

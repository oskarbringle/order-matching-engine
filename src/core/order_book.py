from .skip_list import SkipList
from .order import Order, OrderType

class OrderBook:
    def __init__(self):
        # Buy orders: descending order so best bid is at the head.
        self.buy_orders = SkipList(ascending=False)
        # Sell orders: ascending order so best ask is at the head.
        self.sell_orders = SkipList(ascending=True)

    def place_order(self, order: Order):
        if order.order_type == OrderType.BUY:
            self.buy_orders.insert(order)
        else:
            self.sell_orders.insert(order)

    def match_orders(self):
        while True:
            best_bid = self.buy_orders.get_best_bid()
            best_ask = self.sell_orders.get_best_ask()

            # If either side is empty, we cannot match.
            if best_bid is None or best_ask is None:
                break

            # Check if match conditions are met (buy price must be >= sell price)
            if best_bid.price >= best_ask.price:
                trade_quantity = min(best_bid.quantity, best_ask.quantity)
                # Optionally, reduce the logging here as well:
                # print(f"Trade Executed: {trade_quantity} units at {best_ask.price}")

                best_bid.quantity -= trade_quantity
                best_ask.quantity -= trade_quantity

                if best_bid.quantity == 0:
                    self.buy_orders.remove(best_bid.price)
                if best_ask.quantity == 0:
                    self.sell_orders.remove(best_ask.price)
            else:
                break  # No match possible

    def print_order_book(self):
        best_bid = self.buy_orders.get_best_bid()
        best_ask = self.sell_orders.get_best_ask()
        print(f"Best Bid: {best_bid.price if best_bid else 'None'} | Best Ask: {best_ask.price if best_ask else 'None'}")

import time
from core.parallel_matching import ParallelMatchingEngine
from core.order import Order, OrderType

def test_parallel_matching():
    engine = ParallelMatchingEngine()
    engine.start_workers()

    # Submit orders
    engine.submit_order(Order(1, 100, 5, OrderType.BUY))
    engine.submit_order(Order(2, 101, 5, OrderType.BUY))
    engine.submit_order(Order(3, 105, 10, OrderType.SELL))

    time.sleep(2)  # Allow time for the threads to process the orders
    engine.shutdown()

    # Print the final state of the order book
    engine.print_order_book()

if __name__ == "__main__":
    test_parallel_matching()

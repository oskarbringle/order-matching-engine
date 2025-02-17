import time
from core.parallel_matching import ParallelMatchingEngine
from core.order import Order, OrderType

def benchmark_engine(order_count=10000):
    engine = ParallelMatchingEngine(num_workers=4)
    engine.start_workers()

    start_time = time.time()
    
    # Submit a high volume of orders
    for i in range(order_count):
        order_type = OrderType.BUY if i % 2 == 0 else OrderType.SELL
        engine.submit_order(Order(i, 100 + (i % 10), 1, order_type))

    time.sleep(3)  # Give processes time to complete
    engine.shutdown()

    end_time = time.time()
    print(f"Processed {order_count} orders in {end_time - start_time:.2f} seconds")

benchmark_engine()

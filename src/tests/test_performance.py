import time
import cProfile
import pstats
from core.parallel_matching import ParallelMatchingEngine
from core.order import Order, OrderType

def stress_test(engine, num_orders=1000000):
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.perf_counter()
    for i in range(num_orders):
        order_type = OrderType.BUY if i % 2 == 0 else OrderType.SELL
        engine.submit_order(Order(i, 100 + (i % 10), 1, order_type))

    # Instead of polling with sleep, block until the queue is empty.
    engine.queue.join()

    end_time = time.perf_counter()
    total_time = end_time - start_time

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

    print(f"Processed {num_orders} orders in {total_time:.2f} seconds")
    print(f"Avg order execution time: {(total_time / num_orders) * 1e6:.2f} μs per order")

if __name__ == "__main__":
    engine = ParallelMatchingEngine()
    engine.start_workers()
    stress_test(engine)
    engine.shutdown()

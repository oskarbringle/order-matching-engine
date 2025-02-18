import threading
from queue import Queue, Empty
from .order_book import OrderBook
from .order import Order
import time

def worker_thread(order_queue, order_book, running, lock):
    while running["value"]:
        try:
            order = order_queue.get(timeout=1)
            if order is None:  # Exit signal received.
                order_queue.task_done()
                break
            
            start_time = time.perf_counter()

            with lock:
                order_book.place_order(order)
                order_book.match_orders()

            end_time = time.perf_counter()
            # Removed per-order print to reduce I/O overhead:
            # print(f"⚡ Order Processed in {(end_time - start_time) * 1e6:.2f} μs")
            
            order_queue.task_done()
        except Empty:
            continue

class ParallelMatchingEngine:
    def __init__(self, order_book=None, num_workers=4):
        self.order_book = order_book if order_book is not None else OrderBook()
        self.queue = Queue()
        self.running = {"value": True}
        self.num_workers = num_workers
        self.threads = []
        self.order_book_lock = threading.Lock()

    def submit_order(self, order: Order):
        # Reduced logging on submission.
        # print(f"📩 Order Submitted: {order}")
        self.queue.put(order)

    def start_workers(self):
        for _ in range(self.num_workers):
            t = threading.Thread(
                target=worker_thread,
                args=(self.queue, self.order_book, self.running, self.order_book_lock)
            )
            t.start()
            self.threads.append(t)

    def shutdown(self):
        self.running["value"] = False

        # Unblock the queue by sending shutdown signals.
        for _ in range(self.num_workers):
            self.queue.put(None)

        for t in self.threads:
            t.join()

    def print_order_book(self):
        with self.order_book_lock:
            self.order_book.print_order_book()

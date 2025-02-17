from fastapi import FastAPI, WebSocket
from core.parallel_matching import ParallelMatchingEngine
from core.order import Order, OrderType
import threading
import json
import zmq

app = FastAPI()

# Initialize the matching engine
matching_engine = ParallelMatchingEngine()
matching_engine.start_workers()

# Store active WebSocket connections
active_connections = set()

# ZeroMQ Setup for Asynchronous Order Submission
context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("tcp://127.0.0.1:5555")

@app.post("/submit_order/")
async def submit_order(order_id: int, price: float, quantity: int, order_type: str):
    """ API endpoint to submit an order via ZeroMQ """
    try:
        order_data = {
            "order_id": order_id,
            "price": price,
            "quantity": quantity,
            "order_type": order_type.lower()
        }
        zmq_socket.send_json(order_data)  # Send JSON to ZeroMQ
        return {"status": "Order submitted via ZeroMQ"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/order_book/")
async def get_order_book():
    """ API endpoint to get the current order book state """
    order_book = {
        "buy_orders": matching_engine.order_book.buy_orders.to_list(),
        "sell_orders": matching_engine.order_book.sell_orders.to_list(),
    }
    return order_book

@app.websocket("/ws/order_book")
async def websocket_order_book(websocket: WebSocket):
    """ WebSocket for real-time order book updates """
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            order_book_data = {
                "buy_orders": matching_engine.order_book.buy_orders.to_list(),
                "sell_orders": matching_engine.order_book.sell_orders.to_list(),
            }
            await websocket.send_text(json.dumps(order_book_data))
    except Exception:
        pass
    finally:
        active_connections.remove(websocket)

# Background thread to listen for ZeroMQ orders and process them
def zmq_order_listener():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PULL)
    zmq_socket.connect("tcp://127.0.0.1:5555")

    while True:
        order_data = zmq_socket.recv_json()
        order = Order(
            order_id=order_data["order_id"],
            price=order_data["price"],
            quantity=order_data["quantity"],
            order_type=OrderType(order_data["order_type"])
        )
        matching_engine.submit_order(order)  # Process order

# Start ZeroMQ listener thread
zmq_thread = threading.Thread(target=zmq_order_listener, daemon=True)
zmq_thread.start()

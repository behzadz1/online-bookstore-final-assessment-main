from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
import random, time, os

@dataclass
class Book:
    title: str
    category: str
    price: float
    image: str

class CartItem:
    def __init__(self, book: 'Book', quantity: int = 1):
        self.book = book
        self.quantity = int(quantity)

    def get_total_price(self) -> float:
        return self.book.price * self.quantity

class Cart:
    def __init__(self):
        self.items: Dict[str, CartItem] = {}

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def add_item(self, book: 'Book', quantity: int = 1):
        q = int(quantity)
        if q <= 0:
            return
        if book.title in self.items:
            self.items[book.title].quantity += q
        else:
            self.items[book.title] = CartItem(book, q)

    def update_quantity(self, title: str, quantity: int):
        if title not in self.items:
            return
        try:
            q = int(quantity)
        except (TypeError, ValueError):
            raise
        if q <= 0:
            del self.items[title]
        else:
            self.items[title].quantity = q

    def remove_item(self, title: str):
        if title in self.items:
            del self.items[title]

    def clear(self):
        self.items.clear()

    def get_total_price(self) -> float:
        return sum(item.book.price * item.quantity for item in self.items.values())

@dataclass
class Order:
    order_id: str
    user_email: str
    items: List[CartItem]
    payment_info: dict
    shipping_info: dict
    total_amount: float
    order_date: datetime = datetime.now()

class User:
    def __init__(self, email: str, password: str, name: str = "", address: str = ""):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.address = address
        self._orders: List[Order] = []

    @property
    def password(self):
        return self.password_hash

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def add_order(self, order: Order):
        self._orders.append(order)

    def get_order_history(self) -> List[Order]:
        return sorted(self._orders, key=lambda o: o.order_date, reverse=True)

class PaymentGateway:
    @staticmethod
    def process_payment(payment_info: dict, amount: float) -> dict:
        # Skip artificial latency in tests/CI
        if os.getenv("APP_ENV") != "test":
            time.sleep(0.05)
        card = payment_info.get("card_number", "")
        method = payment_info.get("payment_method", "card")

        # Decline cards ending with 1111 (test scenario)
        if method == "card" and str(card).strip().endswith("1111"):
            return {"success": False, "message": "Card declined", "transaction_id": None}

        txn = f"TXN{random.randint(100000, 999999)}"
        return {"success": True, "message": "Payment processed successfully", "transaction_id": txn}

class EmailService:
    @staticmethod
    def send_order_confirmation(user_email: str, order: Order) -> bool:
        return True

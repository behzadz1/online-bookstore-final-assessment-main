import os, sys, timeit
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models import Book, Cart


def bench_cart_total():
    cart = Cart()
    b = Book("Cheap", "Cat", 1.0, "/x.jpg")
    cart.add_item(b, 300_000)  # large quantity to magnify inefficiency
    return timeit.timeit(cart.get_total_price, number=1)


def main():
    t = bench_cart_total()
    print(f"Cart total time: {t:.6f}s")


if __name__ == "__main__":
    main()

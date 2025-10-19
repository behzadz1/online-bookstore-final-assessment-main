import os, sys, cProfile, pstats, io
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app


def run_checkout(client):
    # seed cart
    client.post(
        "/add-to-cart", data={"title": "1984", "quantity": "3"}, follow_redirects=True
    )
    # run checkout
    client.post(
        "/process-checkout",
        data={
            "name": "Z",
            "email": "z@x.com",
            "address": "1 St",
            "payment_method": "card",
            "card_number": "4242424242424242",
            "expiry": "12/30",
            "cvv": "123",
            "discount_code": "save10",
        },
        follow_redirects=True,
    )


def main():
    with app.test_client() as client:
        pr = cProfile.Profile()
        pr.enable()
        run_checkout(client)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats(30)
        print(s.getvalue())


if __name__ == "__main__":
    main()

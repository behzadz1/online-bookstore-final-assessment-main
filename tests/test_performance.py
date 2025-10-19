import timeit
from models import Book, Cart


def test_cart_total_scaling_regression():
    cart = Cart()
    b = Book("Cheap", "Cat", 1.0, "/x.jpg")
    cart.add_item(b, 200_000)
    t = timeit.timeit(cart.get_total_price, number=1)
    assert t < 0.02, f"Cart total too slow ({t:.4f}s) — indicates per-unit looping"


def test_add_to_cart_bulk_perf(app_client):
    import timeit
    from tests.test_utils import try_post_route

    route_variants = ["/add-to-cart", "/add_to_cart"]

    def add_many():
        for _ in range(300):
            try_post_route(
                app_client, route_variants, data={"title": "1984", "quantity": "1"}
            )

    t = timeit.timeit(add_many, number=1)
    assert t < 1.5

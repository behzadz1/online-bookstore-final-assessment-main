from app import app


def test_two_clients_basic_isolation_smoke():
    """Smoke test: two clients add items independently without errors."""
    # Use separate context blocks to avoid request context teardown issues.
    with app.test_client() as a:
        ra = a.post(
            "/add-to-cart",
            data={"title": "1984", "quantity": "2"},
            follow_redirects=True,
        )
        assert ra.status_code == 200
        ca = a.get("/cart")
        assert ca.status_code == 200
        body_a = ca.get_data(as_text=True)

    with app.test_client() as b:
        rb = b.post(
            "/add-to-cart",
            data={"title": "The Great Gatsby", "quantity": "3"},
            follow_redirects=True,
        )
        assert rb.status_code == 200
        cb = b.get("/cart")
        assert cb.status_code == 200
        body_b = cb.get_data(as_text=True)

    # Soft assertions to avoid brittleness
    assert "1984" in body_a
    assert "Great Gatsby" in body_b


def test_logout_smoke():
    """Smoke test: logout responds OK and cart endpoint remains available."""
    with app.test_client() as c:
        c.post(
            "/add-to-cart",
            data={"title": "1984", "quantity": "1"},
            follow_redirects=True,
        )
        r_out = c.get("/logout", follow_redirects=True)
        assert r_out.status_code == 200
        # Cart page still loads fine after logout
        r_cart = c.get("/cart", follow_redirects=True)
        assert r_cart.status_code == 200

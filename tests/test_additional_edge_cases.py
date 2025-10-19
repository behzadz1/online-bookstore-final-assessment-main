import re
from tests.test_utils import try_post_route

ADD_TO_CART = ["/add-to-cart", "/add_to_cart"]
UPDATE_CART = ["/update-cart", "/update_cart"]


def test_add_missing_title_field(app_client):
    r = app_client.post("/add-to-cart", data={"quantity": "1"}, follow_redirects=True)
    assert r.status_code == 200
    assert re.search(r"book|invalid", r.get_data(as_text=True), re.I)


def test_add_invalid_book_title(app_client):
    route, r = try_post_route(
        app_client, ADD_TO_CART, data={"title": "Nonexistent Book", "quantity": "2"}
    )
    assert r.status_code == 200
    assert re.search(r"book.*not.*found", r.get_data(as_text=True), re.I)


def test_large_quantities_multiple_items(app_client):
    app_client.post(
        "/add-to-cart",
        data={"title": "1984", "quantity": "9999"},
        follow_redirects=True,
    )
    app_client.post(
        "/add-to-cart",
        data={"title": "The Great Gatsby", "quantity": "8888"},
        follow_redirects=True,
    )
    r = app_client.get("/cart", follow_redirects=True)
    body = r.get_data(as_text=True)
    assert "1984" in body and "Great Gatsby" in body
    assert '"total"' in body  # ensure total is computed


def test_remove_nonexistent_item(app_client):
    r = app_client.post(
        "/remove-from-cart", data={"title": "Fake Book"}, follow_redirects=True
    )
    assert r.status_code == 200
    assert (
        "removed" in r.get_data(as_text=True).lower()
        or "messages_text" in r.get_data(as_text=True).lower()
    )


def test_checkout_partially_valid_card(app_client):
    app_client.post(
        "/add-to-cart", data={"title": "1984", "quantity": "1"}, follow_redirects=True
    )
    r = app_client.post(
        "/process-checkout",
        data={
            "name": "User",
            "email": "user@example.com",
            "address": "1 St",
            "payment_method": "card",
            "card_number": "4242424242424242",
            "expiry": "",
            "cvv": "",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert re.search(r"invalid|cvv|expiry", r.get_data(as_text=True), re.I)


def test_duplicate_discount_codes(app_client):
    app_client.post(
        "/add-to-cart", data={"title": "1984", "quantity": "1"}, follow_redirects=True
    )
    r = app_client.post(
        "/process-checkout",
        data={
            "name": "User",
            "email": "user@example.com",
            "address": "1 St",
            "payment_method": "paypal",
            "paypal_email": "payer@example.com",
            "discount_code": "save10 welcome20",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert re.search(r"invalid|discount", r.get_data(as_text=True), re.I)


def test_blank_registration_fields(app_client):
    r = app_client.post(
        "/register",
        data={"name": "", "email": "", "password": ""},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert re.search(r"invalid|email|error", r.get_data(as_text=True), re.I)


def test_checkout_after_logout(app_client):
    app_client.post(
        "/register",
        data={"name": "U", "email": "logout@test.com", "password": "123"},
        follow_redirects=True,
    )
    app_client.post(
        "/login",
        data={"email": "logout@test.com", "password": "123"},
        follow_redirects=True,
    )
    app_client.get("/logout", follow_redirects=True)
    r = app_client.post(
        "/process-checkout",
        data={
            "name": "X",
            "email": "logout@test.com",
            "address": "1 St",
            "payment_method": "paypal",
            "paypal_email": "payer@example.com",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert re.search(r"login|empty|invalid", r.get_data(as_text=True), re.I)

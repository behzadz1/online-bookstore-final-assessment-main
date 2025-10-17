
import re
from tests.test_utils import try_post_route, try_get_route

ADD_TO_CART = ['/add-to-cart', '/add_to_cart']
UPDATE_CART = ['/update-cart', '/update_cart']

def test_healthz_ok(app_client):
    r = app_client.get('/healthz')
    assert r.status_code == 200
    assert 'ok' in r.get_data(as_text=True).lower()

def test_add_to_cart_book_not_found(app_client):
    route, r = try_post_route(app_client, ADD_TO_CART, data={'title':'Unknown Book','quantity':'1'})
    assert r.status_code == 200
    assert re.search(r'book\s*not\s*found', r.get_data(as_text=True), re.I)

def test_add_to_cart_quantity_too_large(app_client):
    route, r = try_post_route(app_client, ADD_TO_CART, data={'title':'1984','quantity':'1000001'})
    assert r.status_code == 200
    assert re.search(r'invalid\s*quantity', r.get_data(as_text=True), re.I)

def test_update_cart_non_integer_quantity(app_client):
    # First add something valid
    try_post_route(app_client, ADD_TO_CART, data={'title':'1984','quantity':'1'})
    # Now send non-integer update to hit validation branch
    route, r = try_post_route(app_client, UPDATE_CART, data={'title':'1984','quantity':'NaN'})
    assert r.status_code == 200
    assert re.search(r'invalid\s*quantity', r.get_data(as_text=True), re.I)

def test_checkout_invalid_email_message_even_with_empty_cart(app_client):
    # No items in cart; invalid email should still trigger before empty-cart redirect
    route, r = try_post_route(app_client, ['/process-checkout','/process_checkout'], data={
        'name':'Z','email':'bad','address':'1 St',
        'payment_method':'card','card_number':'','expiry':'','cvv':''
    })
    assert r.status_code == 200
    assert re.search(r'invalid\s*email', r.get_data(as_text=True), re.I)

def test_paypal_success_flow_and_confirmation(app_client):
    # Add an item
    try_post_route(app_client, ADD_TO_CART, data={'title':'1984','quantity':'2'})
    # Valid PayPal checkout
    route, r = try_post_route(app_client, ['/process-checkout','/process_checkout'], data={
        'name':'Buyer','email':'buyer@example.com','address':'42 Road',
        'payment_method':'paypal','paypal_email':'payer@example.com'
    })
    assert r.status_code == 200
    body = r.get_data(as_text=True).lower()
    assert 'confirmation' in body or 'order' in body

def test_discount_save10_affects_total(app_client):
    # Add one 1984 @ 8.99, expect 10% off => 8.09
    try_post_route(app_client, ADD_TO_CART, data={'title':'1984','quantity':'1'})
    route, r = try_post_route(app_client, ['/process-checkout','/process_checkout'], data={
        'name':'Promo','email':'promo@example.com','address':'1 St',
        'payment_method':'paypal','paypal_email':'payer@example.com',
        'discount_code':'save10'
    })
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert '8.09' in body or re.search(r'"total"\s*:\s*8\.09', body)

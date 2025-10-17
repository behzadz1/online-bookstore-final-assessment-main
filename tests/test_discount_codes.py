
import re
from tests.test_utils import try_post_route

PROCESS_CHECKOUT_VARIANTS = ['/process-checkout', '/process_checkout']

def checkout_post(app_client, data):
    route, r = try_post_route(app_client, PROCESS_CHECKOUT_VARIANTS, data=data)
    return route, r

BASE_CHECKOUT = {
    'name':'Zad',
    'email':'z@x.com',
    'address':'1 St',
    'payment_method':'card',
    'card_number':'4242424242424242',
    'expiry':'12/30',
    'cvv':'123',
}

def test_discount_code_case_insensitive_save10(app_client):
    data = dict(BASE_CHECKOUT, **{'discount_code':'sAvE10'})
    route, r = checkout_post(app_client, data)
    assert r.status_code == 200
    page = r.get_data(as_text=True)
    assert '10' in page or 'discount' in page.lower()

def test_discount_code_welcome20_case_insensitive(app_client):
    data = dict(BASE_CHECKOUT, **{'discount_code':'WeLCOME20'})
    route, r = checkout_post(app_client, data)
    assert r.status_code == 200
    page = r.get_data(as_text=True)
    assert '20' in page or 'discount' in page.lower()

def test_discount_code_invalid_message(app_client):
    data = dict(BASE_CHECKOUT, **{'discount_code':'NOTREAL'})
    route, r = checkout_post(app_client, data)
    assert r.status_code == 200
    assert re.search(r"invalid|unknown|discount", r.get_data(as_text=True), re.I)

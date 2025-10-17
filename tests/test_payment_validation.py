
import re
from tests.test_utils import try_post_route

PROCESS_CHECKOUT_VARIANTS = ['/process-checkout', '/process_checkout']

def checkout_post(app_client, data):
    route, r = try_post_route(app_client, PROCESS_CHECKOUT_VARIANTS, data=data)
    return route, r

def test_credit_card_validation_required(app_client):
    _, r = checkout_post(app_client, {
        'name':'Z','email':'z@x.com','address':'1 St',
        'payment_method':'card','card_number':'','expiry':'','cvv':''
    })
    assert r.status_code == 200
    assert re.search(r"(invalid|card|expiry|cvv|required)", r.get_data(as_text=True), re.I)

def test_invalid_card_format_rejected(app_client):
    _, r = checkout_post(app_client, {
        'name':'Z','email':'z@x.com','address':'1 St',
        'payment_method':'card','card_number':'1234','expiry':'13/99','cvv':'1'
    })
    assert r.status_code == 200
    assert re.search(r"(invalid|card|expiry|cvv)", r.get_data(as_text=True), re.I)

def test_paypal_validation_path_exists(app_client):
    _, r = checkout_post(app_client, {
        'name':'Z','email':'z@x.com','address':'1 St',
        'payment_method':'paypal','paypal_email':'payer@example.com'
    })
    assert r.status_code == 200
    assert re.search(r"(paypal|success|order|confirmation|error)", r.get_data(as_text=True), re.I)

def test_payment_card_ending_1111_fails(app_client):
    _, r = checkout_post(app_client, {
        'name':'Z','email':'z@x.com','address':'1 St',
        'payment_method':'card','card_number':'4111111111111111','expiry':'12/30','cvv':'123'
    })
    assert r.status_code == 200
    assert re.search(r"(declined|failed|invalid)", r.get_data(as_text=True), re.I)

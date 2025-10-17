import re
from tests.test_utils import try_post_route, try_get_route

ADD_TO_CART_VARIANTS = ['/add-to-cart', '/add_to_cart']
UPDATE_CART_VARIANTS = ['/update-cart', '/update_cart']

def test_clear_cart_flow(app_client):
    # add something first
    try_post_route(app_client, ADD_TO_CART_VARIANTS, data={'title':'1984','quantity':'1'})
    r = app_client.post('/clear-cart', follow_redirects=True)
    assert r.status_code == 200
    body = r.get_data(as_text=True).lower()
    assert 'cart cleared' in body or 'messages_text' in body

def test_remove_from_cart_flow(app_client):
    try_post_route(app_client, ADD_TO_CART_VARIANTS, data={'title':'1984','quantity':'1'})
    r = app_client.post('/remove-from-cart', data={'title':'1984'}, follow_redirects=True)
    assert r.status_code == 200
    body = r.get_data(as_text=True).lower()
    assert 'removed' in body or 'messages_text' in body

def test_login_and_account_flow(app_client):
    # register a user
    app_client.post('/register', data={'name':'T','email':'t@x.com','password':'p@ss'}, follow_redirects=True)
    # login
    r = app_client.post('/login', data={'email':'t@x.com','password':'p@ss'}, follow_redirects=True)
    assert r.status_code == 200
    # account page should be accessible
    r2 = app_client.get('/account', follow_redirects=True)
    assert r2.status_code == 200
    assert 'orders' in r2.get_data(as_text=True).lower()

def test_logout_redirects(app_client):
    r = app_client.get('/logout', follow_redirects=True)
    assert r.status_code == 200
    assert 'logged out' in r.get_data(as_text=True).lower() or 'messages_text' in r.get_data(as_text=True).lower()

def test_order_confirmation_invalid_id(app_client):
    r = app_client.get('/order-confirmation/does-not-exist', follow_redirects=True)
    assert r.status_code == 200
    assert re.search(r'order.*not.*found|confirmation', r.get_data(as_text=True), re.I)


import re
from tests.test_utils import try_post_route

ADD_TO_CART_VARIANTS = ['/add-to-cart', '/add_to_cart']
UPDATE_CART_VARIANTS = ['/update-cart', '/update_cart']

def test_add_to_cart_non_numeric_quantity(app_client):
    route, r = try_post_route(app_client, ADD_TO_CART_VARIANTS, data={'title':'1984','quantity':'abc'})
    assert r.status_code == 200, f"Non-numeric quantity should not 404/5xx on {route}"
    assert re.search(r"invalid|quantity|error", r.get_data(as_text=True), re.I)

def test_add_to_cart_empty_quantity(app_client):
    route, r = try_post_route(app_client, ADD_TO_CART_VARIANTS, data={'title':'1984','quantity':''})
    assert r.status_code == 200
    assert re.search(r"invalid|quantity|error", r.get_data(as_text=True), re.I)

def test_add_to_cart_extremely_large_quantity(app_client):
    route, r = try_post_route(app_client, ADD_TO_CART_VARIANTS, data={'title':'1984','quantity':'1000000'})
    assert r.status_code == 200
    # Expect throttle/cap message if implemented, but at least do not crash
    assert re.search(r"(too\s*large|capped|invalid|quantity|error)", r.get_data(as_text=True), re.I)

def test_update_cart_negative_and_zero(app_client):
    route0, r0 = try_post_route(app_client, UPDATE_CART_VARIANTS, data={'title':'1984','quantity':'0'})
    routeN, rN = try_post_route(app_client, UPDATE_CART_VARIANTS, data={'title':'1984','quantity':'-5'})
    for resp in (r0, rN):
        assert resp.status_code == 200
        assert re.search(r"(removed|updated|invalid|quantity)", resp.get_data(as_text=True), re.I)

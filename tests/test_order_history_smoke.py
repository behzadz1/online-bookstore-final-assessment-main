def test_get_order_history_api_exists(app_client):
    # Ensure account/order history route exists (won't 404)
    from .test_utils import try_get_route

    route, r = try_get_route(app_client, ["/account", "/orders", "/order-history"])
    assert r.status_code in (200, 302)  # may redirect to login

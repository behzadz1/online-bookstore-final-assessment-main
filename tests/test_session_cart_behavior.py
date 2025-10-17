from app import app

def test_two_clients_isolated_carts():
    # Use two separate clients to assert isolation
    with app.test_client() as a:
        a.post('/add-to-cart', data={'title': '1984', 'quantity': '2'}, follow_redirects=True)
        cart_a = a.get('/cart').get_data(as_text=True)
        assert '1984' in cart_a
        assert '"qty": 2' in cart_a or 'qty":2' in cart_a

    with app.test_client() as b:
        b.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': '3'}, follow_redirects=True)
        cart_b = b.get('/cart').get_data(as_text=True)
        assert 'The Great Gatsby' in cart_b
        assert '"qty": 3' in cart_b or 'qty":3' in cart_b

    # Re-check A hasn't been polluted by B
    with app.test_client() as a2:
        cart_a2 = a2.get('/cart').get_data(as_text=True)
        # New client starts empty; ensures no global cart leakage
        assert '"items":[]' in cart_a2 or 'items": []' in cart_a2

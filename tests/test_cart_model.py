
import pytest
from models import Book, Cart

def test_update_quantity_removes_zero_or_negative():
    cart = Cart()
    b = Book("1984", "Dystopia", 8.99, "/x.jpg")
    cart.add_item(b, 2)
    cart.update_quantity("1984", 0)
    assert "1984" not in cart.items

    cart.add_item(b, 2)
    cart.update_quantity("1984", -3)
    assert "1984" not in cart.items

def test_update_quantity_rejects_non_integer():
    cart = Cart()
    b = Book("I Ching", "Traditional", 18.99, "/x.jpg")
    cart.add_item(b, 1)
    with pytest.raises((ValueError, TypeError)):
        cart.update_quantity("I Ching", "two")

def test_update_quantity_ignores_missing_title():
    cart = Cart()
    cart.update_quantity("NotThere", 3)  # should not raise
    assert cart.is_empty()

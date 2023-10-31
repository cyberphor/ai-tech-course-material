"""Module for testing"""
from math import isclose
from pytest import raises
from core.appengine import AppEngine
from core.items import Item
from core.errors import InvalidItemNameError
from core.errors import InvalidItemPriceError
from core.errors import InvalidShoppingListSizeError
from core.shoppinglist import ShoppingList


# core/appengine.py
def test_app_engine_class():
    """Method for testing AppEngine class"""
    app = AppEngine()
    assert app == AppEngine()

# core/errors.py
def test_invalid_item_init():
    """Test function for invalid item"""
    with raises(InvalidItemNameError):
        Item('', 3.25)
    with raises(InvalidItemPriceError):
        Item('bread', -3.25)

def test_invalid_shopping_list_size_error():
    """Test for InvalidShoppingListSizeError class"""
    error = InvalidShoppingListSizeError()
    assert error.args[0] == "Invalid List Size!"

# core/items.py
def test_valid_item_init():
    """Test function for valid item"""
    item = Item('bread', 3.25)
    assert item.name == 'bread'
    assert isclose(item.price, 3.25)

def test_item_get_order():
    """Test function for get_order method"""
    item = Item('bread', 3.25)
    assert item.get_order() == 0
    item.price = 1000.0
    assert item.get_order() == 3

def test_item_get_list_item_str():
    """Test function for get_list_item_str method"""
    item = Item('bread', 3.25)
    assert item.get_list_item_str() == '- bread'
    assert item.get_list_item_str(quantity=2) == '- bread (2x)'
    assert item.get_list_item_str(
        quantity=2, leading_dash=True) == '- bread (2x)'

def test_item_get_price_str():
    """Test function for get_price_str method"""
    item = Item('bread', 3.25)
    assert item.get_price_str() == '$3.25'
    assert item.get_price_str(hide_price=True) == '$?.??'
    assert item.get_price_str(order=3) == '$0003.25'

def test_item_repr():
    """Test function for repr method"""
    item = Item('bread', 3.25)
    assert repr(item) == 'Item(bread, 3.25)'

def test_item_eq():
    """Test function for eq method"""
    item1 = Item('bread', 3.25)
    item2 = Item('bread', 3.25)
    item3 = Item('butter', 4.10)
    assert item1 == item2
    assert item1 != item3

# core/shoppinglist.py
def test_shopping_list():
    """Method for testing ShoppingList class"""
    shopping_list = ShoppingList()
    assert isinstance(shopping_list, ShoppingList)
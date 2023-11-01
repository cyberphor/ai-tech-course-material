"""Module for testing"""
from math import isclose
from pytest import raises
from core.appengine import AppEngine
from core.items import Item
from core.items import ItemPool
from core.items import DuplicateItemError
from core.errors import InvalidItemNameError
from core.errors import InvalidItemPriceError
from core.errors import InvalidShoppingListSizeError
from core.shoppinglist import ShoppingList


# core/appengine.py
def test_app_engine_class_process_answer():
    """Method for testing AppEngine method for checking answers"""
    app_engine = AppEngine()
    app_engine.correct_answer = 1
    app_engine.process_answer(cmd=1)
    assert app_engine.message == "Correct!"
    app_engine.correct_answer = 1
    app_engine.process_answer(cmd=2)
    assert app_engine.message == "".join([
        'Not Correct!', 
        f'(Expected ${1:.02f})' 
        f'\nYou answered ${2:.02f}.'
    ])
    app_engine.correct_answer = 1
    app_engine.process_answer(cmd="one")
    assert app_engine.message == "The provided answer is not a valid number!"

def test_app_engine_class_process_add_item():
    """Method for testing AppEngine method for adding items"""
    item = Item('Macbook', 1999.99)
    item_pool = ItemPool()
    item_pool.add_item(item=item)
    app_engine = AppEngine(items=item_pool)
    app_engine.process_add_item(cmd="add Milk: 4.25")
    assert app_engine.message == "Item(Milk, 4.25) added successfully."
    app_engine.process_add_item(cmd="add Milk: 4.25")
    assert app_engine.message.args[0] == "Duplicate!"
    app_engine.process_add_item(cmd="add ")
    assert app_engine.message == 'Cannot add "".\nUsage: add <item_name>: <item_price>'

def test_app_engine_class_process_del_item():
    """Method for testing AppEngine method for deleting items"""
    item = Item('Morale', 9.99)
    item_pool = ItemPool()
    item_pool.add_item(item=item)
    app_engine = AppEngine(items=item_pool)
    app_engine.process_del_item(cmd="del Morale")
    assert app_engine.message == "Morale removed successfully."
    app_engine.process_del_item(cmd="del Fun")
    assert app_engine.message.args[0] == 'Item named "Fun" is not present in the item pool.'

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

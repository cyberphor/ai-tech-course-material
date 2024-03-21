"""Module for testing"""
from math import isclose
from pytest import raises
from random import sample
from core.appengine import AppEngine
from core.items import Item
from core.items import ItemPool
from core.items import DuplicateItemError
from core.errors import InvalidItemNameError
from core.errors import InvalidItemPriceError
from core.errors import InvalidItemPoolError
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
def test_invalid_item_name_error():
    """Test function for InvalidItemNameError class"""
    with raises(InvalidItemNameError):
        Item('', 3.25)
    with raises(InvalidItemNameError):
        Item(1, 3.25)

def test_invalid_item_price_error():
    """Test function for InvalidItemPriceError class"""
    with raises(InvalidItemPriceError):
        Item('bread', -3.25)

def test_invalid_item_pool_error():
    """Test function for InvalidItemPoolError class"""
    with raises(InvalidItemPoolError):
        item = {"":1}
        ItemPool(items=item)

def test_invalid_shopping_list_size_error():
    """Test for InvalidShoppingListSizeError class"""
    error = InvalidShoppingListSizeError()
    assert error.args[0] == "Invalid List Size!"

# core/items.py
def test_item():
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
    assert item.get_list_item_str(leading_dash=False) == 'bread'

def test_item_get_price_str():
    """Test function for get_price_str method"""
    item = Item('bread', 3.25)
    assert item.get_price_str() == '$3.25'
    assert item.get_price_str(hide_price=True) == '$?.??'
    assert item.get_price_str(order=3) == '$0003.25'
    assert item.get_price_str(2) == '$6.50'

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

def test_item_pool():
    """Test function for ItemPool class"""
    with raises(InvalidItemPoolError):
        item = [1,2,3]
        ItemPool(items=item)

def test_item_pool_add_item():
    """Test function for method of adding an item to an ItemPool"""
    with raises(InvalidItemPoolError):
        item_pool = ItemPool()
        item_pool.add_item(item={})

def test_item_pool_get_size():
    """Test function for method of getting size of ItemPool"""
    item_pool = ItemPool()
    assert isinstance(item_pool.get_size(), int)

def test_item_pool_sample_items():
    """Test function for method of generating a random sample of items"""
    item_pool = ItemPool()
    assert item_pool.sample_items(1) == sample([], 0)

def test_item_pool_repr():
    """Test function for repr method of ItemPool class"""
    item_pool = ItemPool()
    assert str(item_pool) == "ItemPool({})"

def test_item_pool_eq():
    """Test function for eq method of ItemPool class"""
    item1 = Item('Beer', 9.99)
    item_pool1 = ItemPool()
    item_pool1.add_item(item=item1)
    item2 = Item('Beer', 9.99)
    item_pool2 = ItemPool()
    item_pool2.add_item(item=item2)
    assert item_pool1 == item_pool2 and item_pool1.items == item_pool2.items

# core/shoppinglist.py
def test_shopping_list():
    """Method for testing ShoppingList class"""
    shopping_list = ShoppingList()
    assert isinstance(shopping_list.get_total_price(), int)

def test_shopping_list_refresh():
    """Method for testing ShoppingList class refresh method"""
    item1 = Item('Beer', 9.99)
    item2 = Item('Coffee', 9.99)
    item3 = Item('Cigars', 9.99)
    item_pool1 = ItemPool()
    item_pool1.add_item(item=item1)
    with raises(ValueError):
        ShoppingList(item_pool=item_pool1, size=0)
    shopping_list = ShoppingList(item_pool=item_pool1, size=1)
    with raises(InvalidShoppingListSizeError):
        shopping_list.refresh(item_pool=item_pool1, size=2)
    with raises(ValueError):
        shopping_list.refresh(item_pool=item_pool1, quantities={})
    with raises(ValueError):
        shopping_list.refresh(item_pool=item_pool1, quantities=[1,"foo",3])
    shopping_list.refresh(item_pool=item_pool1, quantities=[1, 2, 3])
    assert len(shopping_list.list) == 1
    item_pool1.add_item(item=item2)
    item_pool1.add_item(item=item3)
    shopping_list.refresh(item_pool=item_pool1, size=2, quantities=[1])

def test_shopping_list_get_total_price():
    """Method for testing ShoppingList class get_total_price method"""
    shopping_list = ShoppingList()
    assert len(shopping_list) == 0

def test_shopping_list_item_price():
    """Method for testing ShoppingList class get_item_price method"""
    item1 = Item(name="Milk", price=4.25)
    item_pool = ItemPool()
    item_pool.add_item(item=item1)
    shopping_list = ShoppingList(item_pool=item_pool)
    assert isinstance(shopping_list.get_item_price(i=0), float)

def test_shopping_list_len():
    """Method for testing ShoppingList class len method"""
    shopping_list = ShoppingList()
    assert len(shopping_list) == 0

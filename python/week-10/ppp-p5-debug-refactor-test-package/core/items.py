import math
import random

from core.errors import *

class Item:
    def __init__(self, name, price):
        if type(name) != str or not name:
            raise InvalidItemNameError(name)
        self.name = name
        if not isinstance(price, (float, int)) or not price > 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        return math.floor(round(math.log(self.price, 10), 10))
    
    # HACK: task 2 - added the method below
    def get_price_str(self, quantity = None, hide_price = False, order = None):
        if None is quantity:
            amount = f"{self.price:.2f}"
        else:
            amount =  f"{(self.price * quantity):.2f}"
        dollars, cents = amount.split(".")
        if None is not order and order > self.get_order():
            dollars = f"{dollars:0>{order + 1}}"
        if hide_price:
            price = f"${'?' * len(dollars)}.??"
        else:
            price = f"${dollars}.{cents}"
        return price

    # HACK: task 2 - added the method below
    def get_list_item_str(self, quantity = None, leading_dash = True):
        if leading_dash:
            list_item = f"- {self.name}"      
        else:
            list_item = self.name
        if None is not quantity:
            list_item = list_item + f" ({quantity}x)"
        return list_item

    def __repr__(self):
        return f'Item({self.name}, {self.price})'
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name and self.price == other.price

class ItemPool:
    def __init__(self, items = None):
        if not items:
            items = {}
        if type(items) != dict:
            raise InvalidItemPoolError()
        for key, val in items.items():
            if type(key) != str or type(val) != Item:
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        if type(item) != Item:
            raise InvalidItemPoolError()
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        return len(self.items)

    def sample_items(self, sample_size):
        return random.sample(list(self.items.values()), min(sample_size, len(self.items)))

    def __repr__(self):
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        return isinstance(other, ItemPool) and self.items == other.items

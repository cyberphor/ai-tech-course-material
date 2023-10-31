"""Module for items"""
import math
import random
from core.errors import DuplicateItemError
from core.errors import InvalidItemNameError
from core.errors import InvalidItemPriceError
from core.errors import InvalidItemPoolError
from core.errors import NonExistingItemError


class Item:
    """Item class"""
    def __init__(self, name, price):
        if not isinstance(name, str) or not name:
            raise InvalidItemNameError(name)
        self.name = name
        if not isinstance(price, (float, int)) or not price > 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        """Method for getting order"""
        return math.floor(round(math.log(self.price, 10), 10))

    # HACK: task 2 - added the method below
    def get_price_str(self, quantity=None, hide_price=False, order=None):
        """Method for getting price"""
        if None is quantity:
            amount = f"{self.price:.2f}"
        else:
            amount = f"{(self.price * quantity):.2f}"
        dollars, cents = amount.split(".")
        if None is not order and order > self.get_order():
            dollars = f"{dollars:0>{order + 1}}"
        if hide_price:
            price = f"${'?' * len(dollars)}.??"
        else:
            price = f"${dollars}.{cents}"
        return price

    # HACK: task 2 - added the method below
    def get_list_item_str(self, quantity=None, leading_dash=True):
        """Method for getting listed item"""
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
        # HACK: task 4 - wrote code this way because line was too long
        return (
            isinstance(other, Item) and
            self.name == other.name and
            self.price == other.price
        )


class ItemPool:
    """ItemPool class"""
    def __init__(self, items=None):
        if not items:
            items = {}
        if not isinstance(items, dict):
            raise InvalidItemPoolError()
        for key, val in items.items():
            if not isinstance(key, str) or not isinstance(val, Item):
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        """Method for adding an item to the pool"""
        if not isinstance(item, Item):
            raise InvalidItemPoolError()
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        """Method for removing an item from the pool"""
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        """Method for getting size of pool"""
        return len(self.items)

    def sample_items(self, sample_size):
        """Method for generating bogus items"""
        return random.sample(
            list(self.items.values()),
            min(sample_size, len(self.items))
        )

    def __repr__(self):
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        return isinstance(other, ItemPool) and self.items == other.items

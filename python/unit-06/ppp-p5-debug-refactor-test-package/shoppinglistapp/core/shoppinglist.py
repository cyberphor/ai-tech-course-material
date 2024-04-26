"""Module for shopping list"""

from random import choices
from random import randint
from shoppinglistapp.core.errors import InvalidShoppingListSizeError


class ShoppingList:
    """Shopping list class"""

    def __init__(self, size=None, quantities=None, item_pool=None):
        self.list = []
        if item_pool is not None:
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size=None, quantities=None):
        """Method for refreshing list"""
        if size is None:
            size = randint(1, item_pool.get_size() + 1)
            # HACK: task 1  - added the next 3 lines below
            item_pool_size = item_pool.get_size()
            if size > item_pool_size:
                size = size - item_pool_size
        if not isinstance(size, int) or size < 1:
            raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = choices(range(1, 10), k=size)
        if not isinstance(quantities, list):
            raise ValueError()
        for elem in quantities:
            if not isinstance(elem, int) or elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        items_list = item_pool.sample_items(size)
        self.list = list(zip(items_list, quantities))

    def get_total_price(self):
        """Method for getting total price"""
        return round(sum(item.price * qnt for (item, qnt) in self.list), 2)

    def get_item_price(self, i):
        """Method for getting item price"""
        return round(self.list[i][0].price * self.list[i][1], 2)

    def __len__(self):
        return len(self.list)

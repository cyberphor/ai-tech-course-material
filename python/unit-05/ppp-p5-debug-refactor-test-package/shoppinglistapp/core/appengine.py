"""Module for app engine"""
from shoppinglistapp.core.items import Item
from shoppinglistapp.core.errors import DuplicateItemError
from shoppinglistapp.core.errors import InvalidItemPriceError
from shoppinglistapp.core.errors import InvalidItemNameError
from shoppinglistapp.core.errors import NonExistingItemError


class AppEngine:
    """AppEngine class"""
    def __init__(self, shopping_list=None, items=None):
        self.items = items
        self.shopping_list = shopping_list
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

    def process_answer(self, cmd):
        """Method for checking answers"""
        # HACK: task 3 - added try/except block
        try:
            answer = round(float(cmd), 2)
            if answer == self.correct_answer:
                self.message = 'Correct!'
            else:
                # HACK: task 4 - wrote code this way because line was too long
                self.message = "".join([
                    'Not Correct!',
                    f'(Expected ${self.correct_answer:.02f})'
                    f'\nYou answered ${answer:.02f}.'
                ])
        except ValueError:
            self.message = 'The provided answer is not a valid number!'
        self.correct_answer = None

    def process_add_item(self, cmd):
        """Method for adding an item"""
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple) == 2:
            name, price = item_tuple
            # HACK: task 3 - added try/except block below
            # HACK: task 4 - wrote code this way because line was too long
            errors = (
                ValueError,
                DuplicateItemError,
                InvalidItemPriceError,
                InvalidItemNameError
            )
            try:
                # HACK: task 1 - updated the line below
                item = Item(name, float(price))
                self.items.add_item(item)
                self.message = f'{item} added successfully.'
            except errors as error:
                self.message = error
        else:
            self.message = f'Cannot add "{item_str}".\n'
            self.message += 'Usage: add <item_name>: <item_price>'

    def process_del_item(self, cmd):
        """Method for deleting an item"""
        # HACK: task 3 - added the try/except block below
        try:
            item_name = cmd[4:]
            self.items.remove_item(item_name)
            self.message = f'{item_name} removed successfully.'
        except NonExistingItemError as error:
            self.message = error

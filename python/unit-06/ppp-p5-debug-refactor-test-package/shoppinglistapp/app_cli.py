"""Module for the app CLI"""

from random import randint
from shoppinglistapp.core.appengine import AppEngine
from shoppinglistapp.core.items import Item
from shoppinglistapp.core.items import ItemPool
from shoppinglistapp.core.shoppinglist import ShoppingList


class AppCLI:
    """App CLI class"""

    def __init__(self, shopping_list=None, items=None):
        self.app_engine = AppEngine(shopping_list, items)

    def run(self):
        """Method to run CLI"""
        while True:
            prompt = "What would you like to do? "
            if self.app_engine.correct_answer is not None:
                prompt = "What amount should replace the questionmarks? $"
            cmd = input(prompt)
            self.execute_command(cmd)
            print(f"{self.app_engine.message}\n")
            self.app_engine.message = None

            if not self.app_engine.continue_execution:
                break

    def execute_command(self, cmd):
        """Method to execute command given"""
        if self.app_engine.correct_answer is not None:
            self.app_engine.process_answer(cmd)
        elif cmd in ("q", "quit"):
            self.app_engine.continue_execution = False
            self.app_engine.message = "Have a nice day!"
        elif cmd in ("a", "ask"):
            self.process_ask()
        elif cmd in ("l", "list"):
            # HACK: task 4 - wrote code this way because line was too long
            self.app_engine.shopping_list.refresh(item_pool=self.app_engine.items)
            # HACK: task 4 - wrote code this way because line was too long
            self.app_engine.message = "".join(
                [
                    "Shopping list with ",
                    f"{len(self.app_engine.shopping_list)}",
                    "items has been created.",
                ]
            )
        elif cmd.startswith("show"):
            self.process_show(cmd)
        elif cmd.startswith("add"):
            self.app_engine.process_add_item(cmd)
        elif cmd.startswith("del"):
            self.app_engine.process_del_item(cmd)
        else:
            self.app_engine.message = f'"{cmd}" is not a valid command.'

    def process_ask(self):
        """Method for processing request"""
        question = randint(0, len(self.app_engine.shopping_list.list))
        self.app_engine.message = self.show_list(mask_index=question)
        if question < len(self.app_engine.shopping_list.list):
            # HACK: task 4 - wrote code this way because line was too long
            item_price = self.app_engine.shopping_list.get_item_price(question)
            self.app_engine.correct_answer = item_price
        else:
            total_price = self.app_engine.shopping_list.get_total_price()
            self.app_engine.correct_answer = total_price

    def process_show(self, cmd):
        """Method for processing show command"""
        what = cmd[5:]
        if what == "items":
            # HACK: task 2 - added the line below
            self.app_engine.message = self.show_items()
        elif what == "list":
            self.app_engine.message = self.show_list()
        else:
            self.app_engine.message = "\n".join(
                [f"Cannot show {what}.", "Usage: show list|items"]
            )

    # HACK: task 2 - moved the method below from the core.items module to here
    def show_items(self):
        """Method for showing items"""
        max_name, max_order = 0, 0
        for item in self.app_engine.items.items.values():
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())
        out = "ITEMS\n"
        for item_name in sorted(self.app_engine.items.items.keys()):
            item = self.app_engine.items.items[item_name]
            # HACK: task 2 - added four lines below
            list_string = item.get_list_item_str(leading_dash=True)
            padding = "..." + ("." * (max_name - len(item_name)))
            price_string = item.get_price_str(order=max_order)
            out += f"{list_string} {padding} {price_string}" + "\n"
        return out

    def show_list(self, mask_index=None):
        """Method for showing list"""
        line_base_len = len("TOTAL") - 4
        # HACK: task 4 - wrote code this way because line was too long
        max_item = max(len(item.name) for item, _ in self.app_engine.shopping_list.list)
        line_base_len = max(max_item, line_base_len)
        total = Item("TOTAL", self.app_engine.shopping_list.get_total_price())
        max_order = total.get_order()
        max_name = len(total.name)
        for item, _ in self.app_engine.shopping_list.list:
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())
        out = "SHOPPING LIST\n"
        i = 0
        for i, (item, quantity) in enumerate(self.app_engine.shopping_list.list):
            hide_price = mask_index == i
            # HACK: task 2 - added the lines below
            padding = "..." + ("." * (line_base_len - len(item.name)))
            out += (
                " ".join(
                    [
                        item.get_list_item_str(quantity=quantity),
                        padding,
                        item.get_price_str(
                            quantity=quantity, order=max_order, hide_price=hide_price
                        ),
                    ]
                )
                + "\n"
            )
        i += 1
        hide_price = mask_index == i
        # HACK: task 2 - added the lines below
        total_line = " ".join(
            [
                f"{total.name}",
                ("..." + ("." * (max_name - len(total.name) + 7))),
                f"{total.get_price_str(hide_price = (hide_price))}",
            ]
        )
        hline = "-" * len(total_line) + "\n"
        return out + hline + total_line + "\n"


if __name__ == "__main__":
    # usage example
    item2 = Item("Macbook", 1999.99)
    item3 = Item("Milk", 4.25)
    item4 = Item("Hotel Room", 255.00)
    item5 = Item("Beef Steak", 25.18)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    ip.add_item(item4)
    ip.add_item(item5)
    sp = ShoppingList(size=3, quantities=[3, 2, 4], item_pool=ip)
    app = AppCLI(sp, ip)
    app.run()

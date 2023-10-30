"""Module for testing the Item class"""
from items import Item

item1 = Item('Beef Steak', 25.18)
item2 = Item('Macbook', 1999.96)

print(item1.get_price_str(order = 3))
print(item2.get_price_str(order = 5))
print(item1.get_price_str(order = 3, quantity = 2))
print(item2.get_price_str(order = 5, quantity = 3))
print(item1.get_price_str(order = 3, quantity = 2, hide_price = True))
print(item2.get_price_str(order = 5, quantity = 3, hide_price = True))

print(item1.get_list_item_str(leading_dash = False))
print(item2.get_list_item_str(leading_dash = False))
print(item1.get_list_item_str(quantity=2, leading_dash = False))
print(item2.get_list_item_str(quantity=3, leading_dash = False))
print(item1.get_list_item_str(quantity=2))
print(item2.get_list_item_str(quantity=3))
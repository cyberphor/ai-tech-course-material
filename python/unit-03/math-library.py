# TODO 1
def circle_area(radius):
    return 3.14 * radius**2


# TODO 2
def sphere_volume(radius):
    return 4 / 3 * 3.14 * radius**3


# TODO 3
def add_word(text, word):
    return text + " " + word


# TODO 4
def max_minus_min(first_num, second_num):
    return max(first_num, second_num) - min(first_num, second_num)


# TODO 5:
def max_minus_min_abs(first_num, second_num):
    return max_minus_min(abs(first_num), abs(second_num))


# TODO 6: Import the `pi` constant here.
from math import pi


# TODO 7: Implement `circle_area_exact` function here.
def circle_area_exact(radius):
    return pi * radius**2


# TODO 8: Implement `sphere_volume_exact` function here.
def sphere_volume_exact(radius):
    return 4 / 3 * pi * radius**3


# TODO 9: Implement `add_numbers_return` function here.
def add_numbers_return(first_num, second_num):
    return first_num + second_num


# TODO 10: Implement `add_numbers_print` function here.
def add_numbers_print(first_num, second_num):
    print(add_numbers_return(first_num, second_num))

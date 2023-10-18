from math import pi

# TODO: Define constants
TABLE_TOP_LENGTH = 63.0
TABLE_TOP_WIDTH = 23.6
TABLE_TOP_HEIGHT = 1.5
TABLE_LEG_BASE_RADIUS = 0.8
TABLE_LEG_HEIGHT = 29.5

# TODO: Define box_vol, cylinder_vol, table_vol functions
def box_vol(length, width, height):
    return length * width * height

def cylinder_vol(base_radius, height):
    return height * pi * base_radius**2

def table_vol(tt_length, tt_width, tt_height, leg_base_rad, leg_height):
    bv = box_vol(tt_length, tt_width, tt_height)
    cv = cylinder_vol(leg_base_rad, leg_height)
    return bv * (cv * 4)

# TODO: Define table_volume variable
table_volume = table_vol(
    TABLE_TOP_LENGTH,
    TABLE_TOP_HEIGHT,
    TABLE_TOP_WIDTH,
    TABLE_LEG_BASE_RADIUS,
    TABLE_LEG_HEIGHT
)

a = 63 * 23.6 * 1.5 + 4 * pi * 0.8**2 * 29.5
assert round(table_volume, 2) == round(a, 2)
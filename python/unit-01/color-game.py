def time_color(time: int) -> str:
    # TODO 1: Replace the `pass` keyword with conditional statements
    if time > 10:
        return "black"
    elif time > 5 or time == 10:
        return "orange"
    elif time <= 5:
        return "red"

COLORS = [
    "red",
    "orange",
    "blue",
    "green",
    "yellow",
    "pink",
    "black",
    "gray",
    "purple"
]

def is_correct(bg_color: str, text_color: str, text: str, input_color: str, mode: str) -> bool:
    # TODO 2: Replace the `pass` keyword with conditional statements
    if (mode == "Background Color") and (input_color == bg_color):
        return True
    elif (mode == "Text Color") and (input_color == text_color):
        return True
    elif (mode == "Text") and (input_color == text):
        return True
    elif (mode == "Neither") and (input_color not in [bg_color, text_color, text]) and (input_color in COLORS):
        return True
    else:
        return False

# Assert statements to test the time_color() function
assert time_color(25) == 'black'
assert time_color(10) == 'orange'
assert time_color(6) == 'orange'
assert time_color(5) == 'red'
assert time_color(3) == 'red'
assert time_color(-100) == 'red'

# Assert statements to test the is_correct() function
assert is_correct('black', 'red', 'blue', 'blue', 'Background Color') == False
assert is_correct('black', 'red', 'blue', 'black', 'Background Color') == True
assert is_correct('black', 'red', 'blue', 'red', 'Text Color') == True
assert is_correct('black', 'red', 'blue', 'blue', 'Text Color') == False
assert is_correct('black', 'red', 'blue', 'pink', 'Text') == False
assert is_correct('black', 'red', 'blue', 'red', 'Text') == False
assert is_correct('black', 'red', 'blue', 'red', 'Neither') == False
assert is_correct('black', 'red', 'blue', 'pink', 'Neither') == True

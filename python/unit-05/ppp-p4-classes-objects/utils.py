"""Module for utilities"""


class InvalidArgumentError(Exception):
    """InvalidArgumentError class"""

    def __init__(self, arg, msg):
        super().__init__(f"The `{arg}` (type `{type(arg)}`) is invalid. {msg}")


def validate_positive_number(number):
    """Function to validate positive numbers"""
    if (not isinstance(number, int)) and (not isinstance(number, float)):
        raise InvalidArgumentError(
            number,
            "Only the following types are allowed: <class 'int'>, <class 'float'>",
        )
    if number <= 0:
        raise InvalidArgumentError(number, "The argument must be a non-empty string.")


def validate_non_empty_string(string):
    """Function to validate non-empty strings"""
    if not isinstance(string, str):
        raise InvalidArgumentError(string, "The argument must be a string.")
    if string == "":
        raise InvalidArgumentError(string, "The argument must be a non-empty string.")

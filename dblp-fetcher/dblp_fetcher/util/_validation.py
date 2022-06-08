def is_valid_year(value: str) -> bool:
    """
    Checks if a string is a valid year. We consider a string to be a valid year if it can be converted to a number in
    the interval [1900, 2100].
    """

    return value.isnumeric() and 1900 <= int(value) <= 2100

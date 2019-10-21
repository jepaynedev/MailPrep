"""Coalesce funtion for managing None values"""

def coalesce(*args):
    """Returns first non-None argument passed to the function, or None if empty or all None"""
    for arg in args:
        if arg is not None:
            return arg
    return None


def pad_right(value, pad_length):
    """Pads string with space characters on the right to the specified length"""
    return f'{value: <{pad_length}}'
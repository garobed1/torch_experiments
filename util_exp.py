import numpy as np

def lies_in_range(x, arr):
    if x <= max(arr) and x >= min(arr):
        return True
    return False


def contains_in_range(r, arr):
    if lies_in_range(max(arr), r) and lies_in_range(min(arr), r):
        return True
    return False
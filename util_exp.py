import numpy as np

def listdir_nopickle(path):
    return [f for f in os.listdir(path) if not f.endswith('.pickle')]
    
def listdir_nocrash(path):
    return [f for f in os.listdir(path) if 'crashed' not in f]

def lies_in_range(x, arr):
    if x <= max(arr) and x >= min(arr):
        return True
    return False


def contains_in_range(r, arr):
    if lies_in_range(max(arr), r) and lies_in_range(min(arr), r):
        return True
    return False
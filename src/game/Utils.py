__author__ = 'ankitkap'

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump
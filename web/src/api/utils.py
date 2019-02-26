import random


def randhex256():
    return ''.join(random.choice('0123456789abcdef') for _ in range(256))

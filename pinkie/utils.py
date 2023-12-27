import math


class classproperty:
    def __init__(self, func):
        self.fget = func

    def __get__(self, instance, owner):
        return self.fget(owner)
    

def distance(first, second):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))
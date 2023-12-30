import math
from typing import Iterable


def distance(first: Iterable, second: Iterable):
    """
    Get Euclidean distance for 2 iterables.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))
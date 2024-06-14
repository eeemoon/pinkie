import math
from typing import Sequence


def distance(p1: Sequence, p2: Sequence, /) -> float:
    """
    Get the Euclidean distance for 2 sequences.

    Parameters
    ----------
    p1: `Sequence`
        First point.
    p2: `Sequence`
        Second point.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
from typing import Literal


BlendMode = Literal[
    'normal',
    'darken',
    'multiply',
    'overlay',
    'screen'
]


class classproperty:
    def __init__(self, func):
        self.fget = func

    def __get__(self, instance, owner):
        return self.fget(owner)
    
from enum import Enum


class Sign(Enum):
    PLUS = '+'
    MINUS = '-'

    def change(self):
        if self == Sign.PLUS:
            return Sign.MINUS
        elif self == Sign.MINUS:
            return Sign.PLUS

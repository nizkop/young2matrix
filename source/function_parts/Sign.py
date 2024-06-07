from enum import Enum


class Sign(Enum):
    """ separated arithmetic sign """
    PLUS = '+'
    MINUS = '-'

    def change(self): #-> Sign
        """ switching the sign """
        if self == Sign.PLUS:
            return Sign.MINUS
        elif self == Sign.MINUS:
            return Sign.PLUS

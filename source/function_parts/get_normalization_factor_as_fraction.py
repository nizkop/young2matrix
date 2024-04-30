
from fractions import Fraction
from typing import Union
import sympy as sp



def get_normalization_factor_as_fraction(denominator: int, norm: sp.sqrt) -> Union[Fraction, sp.sqrt]:
    """ for calculating x/√ and keeping the number as a fraction """
    try:
        factor = Fraction(denominator, norm)
    except:
        # only exception where factor is not an int (because of the square root)
        factor = sp.sqrt(Fraction(denominator * denominator, norm * norm))
    return factor

from fractions import Fraction
import sympy as sp



def get_normalization_factor_as_fraction(denominator, norm: sp.sqrt):
    try:
        factor = Fraction(denominator, norm)
    except:
        # only exception where factor is not an int (because of the square root)
        factor = sp.sqrt(Fraction(denominator * denominator, norm * norm))

    return factor
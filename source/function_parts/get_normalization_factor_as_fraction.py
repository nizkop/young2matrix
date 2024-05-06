
from fractions import Fraction
from typing import Union
import sympy as sp



def get_normalization_factor_as_fraction(numerator: int, norm: sp.sqrt) -> Union[Fraction, sp.sqrt]:
    """ calculating x/√ and keeping the number as a fraction
    :param numerator: numerator for the to-be-calculated fraction, 1 in case of normalization
    :param norm: denominator for the to-be-calculated fraction, in case of normalization it is a square value
    :return: reduced fraction (eventually including a square)
    """
    try:
        factor = Fraction(numerator, norm)
    except:
        # only exception where factor is not an int (because of the square root)
        factor = sp.sqrt(Fraction(numerator * numerator, norm * norm))
    return factor
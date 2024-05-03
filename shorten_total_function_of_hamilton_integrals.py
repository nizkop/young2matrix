from collections import Counter
from typing import List
import sympy as sp

from source.function_parts.get_normalization_factor_as_fraction import get_normalization_factor_as_fraction
from source.function_parts.hamilton_integral import hamilton_integral
from source.function_parts.sign import Sign


def shorten_total_function_of_hamilton_integrals(h_list: List[hamilton_integral]):
    new_h_list = []
    print("shorten_total_function_of_hamilton_integrals:", len(h_list) , "mit:", [f"{h.sign} {h.factor}" for h in h_list if "".join(sorted(h.get_shortened_symbol())) == "bd"])

    # set all to + sign:
    for h in h_list:
        if h.sign == Sign.MINUS:
            h.sign = Sign.PLUS
            h.bra.sign = Sign.MINUS if h.bra.sign == Sign.PLUS else Sign.PLUS # switch sign
            h.bra.factor = -h.bra.factor

    # counting the occurrences and put them together in case they describe the same integral:
    counts = Counter(h_list)
    for h, count in counts.items():
        h.factor *= count
        new_h_list.append(h)

    # update signs & factors:
    for h in h_list:
        h.factor *= h.bra.factor * h.ket.factor
        if ( h.bra.factor < 0 and h.ket.factor >= 0 ) or ( h.bra.factor >= 0 and h.ket.factor < 0 ):
            if h.factor < 0:
                h.sign = Sign.MINUS if h.sign == Sign.PLUS else Sign.PLUS # switch sign
                h.factor = -h.factor
        # reset factors, that where pulled out of the integral:
        h.bra.factor = 1
        h.ket.factor = 1

    return [x for x in new_h_list if x.factor != 0 ]

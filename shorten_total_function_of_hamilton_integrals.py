from collections import Counter
from typing import List

from source.function_parts.hamilton_integral import hamilton_integral
from source.function_parts.sign import Sign


def shorten_total_function_of_hamilton_integrals(h_list: List[hamilton_integral]):
    counts = Counter(h_list)

    # set all to + sign:
    for h in h_list:
        if h.sign == Sign.MINUS:
            h.sign = Sign.PLUS
            h.bra.sign = Sign.MINUS if h.bra.sign == Sign.PLUS else Sign.PLUS # switch sign

    new_h_list = []
    for h, count in counts.items():
        h.factor *= count
        new_h_list.append(h)

    for h in h_list: # update sign & factor
        h.factor *= h.bra.factor * h.ket.factor
        if ( h.bra.factor < 0 and h.ket.factor >= 0 ) or (h.bra.factor >= 0 and h.ket.factor < 0 ):
            if h.factor >= 0:
                h.sign = Sign.MINUS if h.sign == Sign.PLUS else Sign.PLUS # switch sign
        # reset factors, that where pulled out of the integral:
        h.bra.factor = 1
        h.ket.factor = 1

    return new_h_list

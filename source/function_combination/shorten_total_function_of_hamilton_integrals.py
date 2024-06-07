from typing import List

from source.function_parts.HamiltonIntegral import HamiltonIntegral
from source.function_parts.Sign import Sign
from source.function_combination.SignedCounter import SignedCounter


def shorten_total_function_of_hamilton_integrals(h_list: List[HamiltonIntegral]) -> List[HamiltonIntegral]:
    """
    evaluate calculated (hamilton) integrals in a sum:
    - where do integrals cancel each other due to opposite signed factors?
    - where are integrals not really existing anymore due to a factor of 0?
    - where do they belong together, because their integral has the same value?
    - what is their total factor (multiplying the numbers of bra and ket to a total factor)?
    :param h_list: list of calculated hamilton integrals, that are addends for one tableau
    :return: cleaned-up list of hamilton integrals building a sum for a tableau combination
    """
    new_h_list = []

    # set all to + sign:
    for h in h_list:
        if h.sign == Sign.MINUS:
            h.sign = Sign.PLUS
            #h.bra.sign = Sign.MINUS if h.bra.sign == Sign.PLUS else Sign.PLUS # switch sign
            h.factor = -h.factor

    # counting the occurrences and put them together in case they describe the same integral:
    signed_counts = SignedCounter()
    signed_counts.update(h_list)
    for h, count in signed_counts.items():
        h.factor = count # factors are summed up in SignedCounter
        new_h_list.append(h)

    # update signs & factors:
    for h in h_list:
        # undo sign switch that was used before for counting:
        if h.factor < 0:
            h.sign = Sign.MINUS if h.sign == Sign.PLUS else Sign.PLUS  # switch sign
            h.factor = -h.factor

        # pull factors out of bra and ket:
        h.factor *= h.bra.factor * h.ket.factor
        if ( h.bra.factor < 0 and h.ket.factor >= 0 ) or ( h.bra.factor >= 0 and h.ket.factor < 0 ):
            if h.factor < 0:
                h.sign = Sign.MINUS if h.sign == Sign.PLUS else Sign.PLUS # switch sign
                h.factor = -h.factor
        # reset factors, that where pulled out of the integral:
        h.bra.factor = 1
        h.ket.factor = 1

    return [x for x in new_h_list if x.factor != 0 ]

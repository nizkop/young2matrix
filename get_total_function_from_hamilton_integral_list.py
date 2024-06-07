from typing import List

from source.function_parts.HamiltonIntegral import HamiltonIntegral


def get_total_function_from_hamilton_integral_list(h_list: List[HamiltonIntegral]):
    """ converts a sum of hamilton integrals into their shortened display version """
    integral = ""

    for h in h_list:
        if h.factor != 1:
            integral += h.sign.value + " "
            integral += f"{h.factor} "
            if h.get_shortened_symbol() != "":
                integral += f"* ({h.get_shortened_symbol()}) "
        else:
            if h.get_shortened_symbol() != "":
                integral += h.sign.value + " "
                integral += f"({h.get_shortened_symbol()}) "

    return integral





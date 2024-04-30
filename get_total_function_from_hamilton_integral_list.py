from typing import List

from source.function_parts.hamilton_integral import hamilton_integral


def get_total_function_from_hamilton_integral_list(h_list: List[hamilton_integral]):
    integral = ""

    for h in h_list:
        if h.factor != 1:
            integral += f"{h.factor} "
        if h.get_shortened_symbol() != "":
            integral += f"* ({h.get_shortened_symbol()}) "
        integral += "+ "

    if integral[-2:] == "+ ":# remove last added +
        integral = integral[:-2]
    return integral





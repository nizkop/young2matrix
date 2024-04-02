from typing import Union

from source.function_parts.integral_part import integral_part


class function_combination(object):
    def __init__(self):
        self.tableau_a : Union[integral_part,None] = None
        self.tableau_b : Union[integral_part,None] = None

    def calculate_overlap_integral(self):
        pass

    def calculate_hamilton_integral(self):
        pass
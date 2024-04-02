from typing import List

from source.function_combination import function_combination
from source.function_parts.spatial_part import spatial_part
from source.function_parts.spin_part import spin_part
from source.young_tableau import young_tableau


class standard_tableau(young_tableau):

    def __init__(self):
        super().__init__()
        self.permutation_group:int=0
        self.help: function_combination = function_combination()
        self.spatial_parts: List[spatial_part] = []
        self.spin_parts: List[spin_part] = []

    def print(self):
        pass

    def to_text(self):
        pass

    def solve(self):
        pass

    def get_spatial_choices(self):
        pass

    def calulate_all_overlap_integrals(self):
        pass

    def calculate_all_hamilton_integrals(self):
        pass

    def get_spin_choices(self):
        pass
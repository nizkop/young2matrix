from typing import List

from source.function_combination import function_combination
from source.function_parts.spatial_part import spatial_part
from source.function_parts.spin_part import spin_part
from source.standard_tableau import standard_tableau



class chemical_standard_tableau(standard_tableau):

    def __init__(self,numbers_in_row:List[tuple]):
        super().__init__(numbers_in_row=numbers_in_row)
        self.help: function_combination = function_combination()
        self.spatial_parts: List[spatial_part] = []
        self.spin_parts: List[spin_part] = []

    def print(self) -> None:
        super().print()

    def to_text(self):
        super().to_tex()

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


if __name__ == '__main__':
    pass
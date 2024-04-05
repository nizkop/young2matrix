from typing import List

from source.pure_chemical_functions.calculate_ms_quantum_number import calculate_ms_quantum_number
from source.pure_chemical_functions.calculate_spin_quantum_numbers import calculate_spin_quantum_numbers
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

    def to_text(self) -> str:
        return super().to_text()

    def solve(self):
        pass

    def get_spatial_choices(self):
        pass

    def calulate_all_overlap_integrals(self):
        pass

    def calculate_all_hamilton_integrals(self):
        pass

    def get_spin_choices(self):
        """
        Gesamtspin S = { |s1 - s_2 - ... - s_i| , |s1 - s2 - ... - si| +1, ... , (s1 + ... + si) }
        M_S = { -max(S), -max(S)+1, ..., 0, ..., max(S) }
        """
        spins = calculate_spin_quantum_numbers(number_of_particles=self.permutation_group)
        for spin in spins:
            ms_values = calculate_ms_quantum_number(total_spin=spin)
        return ms_values


if __name__ == '__main__':
    s = chemical_standard_tableau([(1,2)])
    # s.print()
    s.set_up_function()

    print(
        s.get_spin_choices()
    )

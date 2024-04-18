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
        self.help: function_combination = None #function_combination()
        self.spatial_parts: List[spatial_part] = []
        self.spin_parts: List[spin_part] = []

    def print(self) -> None:
        super().print()

    def to_text(self) -> str:
        return super().to_text()

    def solve(self):
        pass

    def get_spatial_choices(self):
        """
        total angular momentum L = { |l1-l2-...-li | , ..., (l1+...+li) }
        ML = { -L, ..., L} = ml1 + ... + mli

        angular momentum of a particle l = 0 (s orbital), 1 (p orbital, 2 (d orbital), ...
        ml = alignment of the individual orbital = { -l , ..., l }
        """
        print("we dont want to choose the orbitals yet")
        if self.function is None:#spatial part needs function as a general behavior pattern
            self.set_up_function()
        self.spatial_parts.append(spatial_part(behavior=self.function))


    def calulate_all_overlap_integrals(self):
        pass

    def calculate_all_hamilton_integrals(self):
        pass

    def get_spin_choices(self):
        """
        finding all combinations of spin quantum numbers for this specific tableau
        """
        if self.number_of_rows > 2:
            # only 2 different spin functions = more antisymmetric than 2 impossible
            return
        if self.function is None:#spin need function as a general behavior pattern
            self.set_up_function()
        spins = calculate_spin_quantum_numbers(number_of_particles=self.permutation_group)
        for spin in spins:
            # get total number of non-alpha spins:
            anti = 0
            alpha_beta = {"alpha": [], "beta": []}
            for r in range(len(self.numbers_in_row)):
                if r % 2 == 1:
                    for i in self.numbers_in_row[r]:
                        alpha_beta["beta"].append(i)
                    anti += len(self.numbers_in_row[r])
                else:
                    for i in self.numbers_in_row[r]:
                        alpha_beta["alpha"].append(i)

            # only pick s, ms combination, if value of S is fitting (first line alpha, second beta, ...)_
            if spin == anti * -0.5 + 0.5 * (self.permutation_group - anti):
                ms_values = calculate_ms_quantum_number(total_spin=spin)
                for q in ms_values:
                    self.spin_parts.append( spin_part(permutation_group=self.permutation_group, total_spin=spin, ms=q, choices_for_spin=alpha_beta,behavior=self.function) )
        # normalizing:











if __name__ == '__main__':
    s = chemical_standard_tableau([(1,2,3)])
    s.print()
    # s.set_up_function()

    s.get_spin_choices()
    for t in s.spin_parts:
        t.print()
        print(t.to_tex())
    # s.function.print()
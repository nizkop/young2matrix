import copy
from fractions import Fraction
from typing import List

from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind
from source.function_parts.text_kinds import text_kinds
from source.pure_chemical_functions.calculate_ms_quantum_number import calculate_ms_quantum_number
from source.pure_chemical_functions.calculate_spin_quantum_numbers import calculate_spin_quantum_numbers
from source.function_parts.spatial_part import spatial_part
from source.function_parts.spin_part import spin_part
from source.standard_tableau import standard_tableau



class chemical_standard_tableau(standard_tableau):

    def __init__(self,numbers_in_row:List[tuple]):
        super().__init__(numbers_in_row=numbers_in_row)
        self.spatial_parts: List[spatial_part] = []
        self.spin_parts: List[spin_part] = []
        self.overlap = []

    def print(self) -> None:
        super().print()

    def to_text(self) -> str:
        return super().to_text()

    def solve(self):
        pass

    def get_spatial_choices(self) -> None:
        """
        total angular momentum L = { |l1-l2-...-li | , ..., (l1+...+li) }
        ML = { -L, ..., L} = ml1 + ... + mli

        angular momentum of a particle l = 0 (s orbital), 1 (p orbital, 2 (d orbital), ...
        ml = alignment of the individual orbital = { -l , ..., l }
        """
        # print("we dont want to choose the orbitals yet")
        if self.function is None:#spatial part needs function as a general behavior pattern
            self.set_up_function()
        if max([len(i) for i in self.numbers_in_row]) > 2:
            # no spin tableaus with more than 2 rows -> spatial tableaus have to be conjoint to the spin tableaus -> 2 columns max.
            # self.print()
            # print("number of columns to high:", "number of columns:", self.number_of_columns, "number of rows:", self.number_of_rows,
            #       "get number in columns:", self.get_numbers_in_columns(), "numbers in each row:", self.numbers_in_row)
            return
        if len(self.spatial_parts) == 0:
            self.spatial_parts.append(spatial_part(behavior=self.function))


    def calulate_all_overlap_integrals(self, kind: spin_vs_spatial_kind=spin_vs_spatial_kind.GENERAL) -> None:
        """
        determine overlap of all integral combinations and saving the results in self.overlap
        :param kind: choice of spin or spatial function type
        """
        if kind == spin_vs_spatial_kind.GENERAL:
            self.calulate_all_overlap_integrals(kind=spin_vs_spatial_kind.SPATIAL)
            self.calulate_all_overlap_integrals(kind=spin_vs_spatial_kind.SPIN)
            return
        if kind == spin_vs_spatial_kind.SPIN:
            if any(entry.get("kind") == spin_vs_spatial_kind.SPIN for entry in self.overlap):
                return # stop repetition
            self.get_spin_choices()  # just to be sure
            tableau_functions = self.spin_parts
        else:
            if any(entry.get("kind") == spin_vs_spatial_kind.SPATIAL for entry in self.overlap):
                return # no repetition
            self.get_spatial_choices()  # just to be sure
            tableau_functions = self.spatial_parts
        if len(tableau_functions) == 0:
            if (not (self.number_of_rows > 2 and kind == spin_vs_spatial_kind.SPIN) and
                not (len(self.get_numbers_in_columns()) > 2 and kind == spin_vs_spatial_kind.SPATIAL)):
                    raise Exception("calulate_all_overlap_integrals impossible because of no parts")
            return
        for i in range(len(tableau_functions)):
            for j in range(i, len(tableau_functions)):
                g = calculate_overlap_integral_between_functions(tableau_functions[i].function, tableau_functions[j].function)
                if kind == spin_vs_spatial_kind.SPIN:
                    info = {"bra": tableau_functions[i].get_shortend_form(text_kinds.TEX),
                            "ket": tableau_functions[j].get_shortend_form(text_kinds.TEX), "kind": kind, "result": g}
                else:
                    info = {"bra": tableau_functions[i].function.to_tex(), "ket": tableau_functions[j].function.to_tex(),
                            "kind": kind, "result": g}
                if info not in self.overlap:
                    self.overlap.append(info)
        return

    def get_spin_choices(self):
        """
        finding all combinations of spin quantum numbers for this specific tableau
        """
        if self.number_of_rows > 2:
            # only 2 different spin functions = more antisymmetric than 2 impossible
            # print("number of rows to high")
            return
        if self.function is None:#spin need function as a general behavior pattern
            self.set_up_function()
        if len(self.spin_parts) > 0:
            return
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

            # only pick s, ms combination, if value of S is fitting (first line alpha, second beta, ...):
            if spin == anti * -Fraction(1,2) + Fraction(1,2) * (self.permutation_group - anti):
                ms_values = calculate_ms_quantum_number(total_spin=spin)
                for ms in ms_values:
                    if ms == spin: #anti * -Fraction(1,2) + Fraction(1,2) * (self.permutation_group - anti)
                        self.spin_parts.append( spin_part(permutation_group=self.permutation_group, total_spin=spin,
                                                          ms=ms, choices_for_spin=alpha_beta,behavior=self.function) )
                    else:
                        modified_alpha_beta = copy.deepcopy(alpha_beta)
                        diff = spin - ms
                        for number_wrong_spins_in_default in range(int(diff)):
                            if len(modified_alpha_beta["alpha"]) == 0:
                                # impossible to build fitting start order of spin functions
                                continue
                            if ms >= 0:
                                modified_alpha_beta["beta"].append(max( modified_alpha_beta["alpha"]))
                                modified_alpha_beta["alpha"].remove(max(modified_alpha_beta["alpha"]))
                            else:
                                modified_alpha_beta["beta"].append(min(modified_alpha_beta["alpha"]))
                                modified_alpha_beta["alpha"].remove(min(modified_alpha_beta["alpha"]))
                        self.spin_parts.append(spin_part(permutation_group=self.permutation_group, total_spin=spin, ms=ms,
                                          choices_for_spin=modified_alpha_beta, behavior=self.function))


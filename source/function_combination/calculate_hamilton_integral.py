from typing import List

from source.function_combination.shorten_total_function_of_hamilton_integrals import shorten_total_function_of_hamilton_integrals
from source.chemical_standard_tableau import chemical_standard_tableau
from source.function_combination.calculate_hamilton_integral_between_functions import \
    calculate_hamilton_integral_between_functions
from source.function_parts.hamilton_integral import hamilton_integral
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind


def calculate_hamilton_integral(tableau_a: chemical_standard_tableau, tableau_b: chemical_standard_tableau, kind :spin_vs_spatial_kind) -> List[hamilton_integral]:
    if tableau_a.number_of_rows != tableau_b.number_of_rows and tableau_a.get_number_of_columns() != tableau_b.get_number_of_columns():
        return []# always gives 0

    results = []
    if kind == spin_vs_spatial_kind.SPATIAL:
        for bra in tableau_a.spatial_parts:
            for ket in tableau_b.spatial_parts:
                for h in calculate_hamilton_integral_between_functions(bra.function, ket.function):
                    norm = bra.function.get_normalization_factor()['fraction'] * ket.function.get_normalization_factor()['fraction']
                    h.factor *= norm
                    results.append( h )
    else:
        for bra in tableau_a.spin_parts:
            for ket in tableau_b.spin_parts:
                for h in calculate_hamilton_integral_between_functions(bra.function, ket.function):
                    norm = bra.function.get_normalization_factor()['fraction'] * ket.function.get_normalization_factor()['fraction']
                    h.factor *= norm
                    results.append( h )

    return shorten_total_function_of_hamilton_integrals(results)





# if __name__ == '__main__':

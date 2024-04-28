from typing import List

from source.chemical_standard_tableau import chemical_standard_tableau
from source.function_combination.calculate_hamilton_integral_between_functions import \
    calculate_hamilton_integral_between_functions
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind


def calculate_hamilton_integral(tableau_a: chemical_standard_tableau, tableau_b: chemical_standard_tableau, kind :spin_vs_spatial_kind) -> List[dict]:

    results = []
    if kind == spin_vs_spatial_kind.SPATIAL:
        for bra in tableau_a.spatial_parts:
            for ket in tableau_b.spatial_parts:
                results.append( calculate_hamilton_integral_between_functions(bra.function, ket.function) )
    else:
        for bra in tableau_a.spin_parts:
            for ket in tableau_b.spin_parts:
                results.append( calculate_hamilton_integral_between_functions(bra.function, ket.function) )

    return results





# if __name__ == '__main__':

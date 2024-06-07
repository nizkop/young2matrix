from typing import List

from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_combination.shorten_total_function_of_hamilton_integrals import shorten_total_function_of_hamilton_integrals
from source.ChemicalStandardTableau import ChemicalStandardTableau
from source.function_combination.calculate_hamilton_integral_between_functions import \
    calculate_hamilton_integral_between_functions
from source.function_parts.HamiltonIntegral import HamiltonIntegral
from source.function_parts.SpinVsSpatialKind import SpinVsSpatialKind


# noinspection PyTypeChecker
def calculate_hamilton_integral(tableau_a:ChemicalStandardTableau, tableau_b:ChemicalStandardTableau,
                                kind:SpinVsSpatialKind) -> List[HamiltonIntegral]:
    """
    calculate all hamilton integrals between different tableaus
    :param kind:
    :param tableau_a: bra terms
    :param tableau_b: ket terms
    :return: combined non-vanishing hamilton integrals
    """
    if (tableau_a.number_of_rows != tableau_b.number_of_rows and
            tableau_a.get_number_of_columns() != tableau_b.get_number_of_columns()):
        return []# always gives 0

    results = []
    if kind == SpinVsSpatialKind.SPATIAL:
        for bra in tableau_a.spatial_parts:
            for ket in tableau_b.spatial_parts:
                for h in calculate_hamilton_integral_between_functions(bra.function, ket.function):
                    norm = bra.function.get_normalization_factor()['fraction'] * ket.function.get_normalization_factor()['fraction']
                    h.factor *= norm
                    results.append( h )
    else:
        for bra in tableau_a.spin_parts:
            for ket in tableau_b.spin_parts:
                # noinspection PyTypeChecker
                for h in calculate_overlap_integral_between_functions(bra.function, ket.function):
                    norm = bra.function.get_normalization_factor()['fraction'] * ket.function.get_normalization_factor()['fraction']
                    h.factor *= norm
                    results.append( h )

    return shorten_total_function_of_hamilton_integrals(results)




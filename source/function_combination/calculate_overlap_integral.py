from typing import List

from source.chemical_standard_tableau import chemical_standard_tableau
from source.function_combination.calculate_overlap_integral_basisfunction import \
    calculate_overlap_integral_basisfunction
from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind
from source.function_parts.text_kinds import text_kinds


def calculate_overlap_integral(tableau_a: chemical_standard_tableau, tableau_b: chemical_standard_tableau, kind :spin_vs_spatial_kind) -> List[dict]:
    if tableau_a.permutation_group != tableau_b.permutation_group:
        raise Exception("function_combination error: The tableaus dont fit.")

    info = {"bra": tableau_a.function.to_tex(), "ket": tableau_b.function.to_tex(), "kind": kind}
    empty_function = function(product_term(Sign("+"), ()) ,normalizable=False)

    # check if identical form
    if tableau_a.number_of_rows != tableau_b.number_of_rows or tableau_a.number_of_columns != tableau_b.number_of_columns:
        # basis function of young tableaux from different young diagrams are automatically diagonal
        empty_function.parts[0].factor = 0
        empty_function.parts = [empty_function.parts[0]]
        info["result"] = empty_function
        return [info]
    # same young diagram (form):

    # test if same standard tableau:
    if tableau_a.numbers_in_row == tableau_b.numbers_in_row:
        empty_function.parts[0].factor = 1
        empty_function.parts[0].ordered_functions = ()
        empty_function.parts = [empty_function.parts[0]]
        info["result"] = empty_function
        return [info]

    results = []
    info = {"bra_tableau": tableau_a.to_tex(), "ket_tableau": tableau_b.to_tex(), "kind": kind}
    if kind == spin_vs_spatial_kind.SPIN:
        # multiple results
        for sp in range(len(tableau_a.spin_parts)):
           spin_choice = tableau_a.spin_parts[sp]
           for sp2 in range(sp, len(tableau_b.spin_parts)):
               spin_choice_2 = tableau_b.spin_parts[sp2]
               g = calculate_overlap_integral_between_functions(spin_choice.function,
                                                                     spin_choice_2.function)
               info["bra"] = spin_choice.get_shortend_form(kind=text_kinds.TEX)
               info["ket"] = spin_choice_2.get_shortend_form(kind=text_kinds.TEX)
               info["result"] = g
               results.append(info)
    else:
        if kind == spin_vs_spatial_kind.GENERAL:
            g = calculate_overlap_integral_basisfunction(tableau_a, tableau_b)
            info["bra"] = tableau_a.function.to_tex()
            info["ket"] = tableau_b.function.to_tex()
        elif kind == spin_vs_spatial_kind.SPATIAL:
            if len(tableau_a.spatial_parts) > 0 and len(tableau_b.spatial_parts) > 0:
                # assumption that only 1 part per tableau
                g = calculate_overlap_integral_between_functions(tableau_a.spatial_parts[0].function,
                                                                      tableau_b.spatial_parts[0].function)
                info["bra"] = tableau_a.spatial_parts[0].function
                info["ket"] = tableau_b.spatial_parts[0].function
            else:
                empty_function.parts[0].factor = 0
                empty_function.parts = [empty_function.parts[0]]
                g = empty_function

        info["result"] = g
        results.append(info)
    return results



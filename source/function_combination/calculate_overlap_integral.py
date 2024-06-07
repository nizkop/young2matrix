from typing import List

from source.ChemicalStandardTableau import ChemicalStandardTableau
from source.function_combination.calculate_overlap_integral_basisfunction import \
    calculate_overlap_integral_basisfunction
from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.ProductTerm import ProductTerm
from source.function_parts.Sign import Sign
from source.function_parts.SpinVsSpatialKind import SpinVsSpatialKind
from source.function_parts.TextKinds import TextKinds


def calculate_overlap_integral(tableau_a: ChemicalStandardTableau, tableau_b: ChemicalStandardTableau,
                               kind: SpinVsSpatialKind) -> List[dict]:
    """
    calculating the overlap between all functions/combinations of two standard tableaus
    -> combination of identical tableaus and different/identical standard tableaus - and entirely different tableaus
    :param kind: type of function (spatial vs. spin)
    :param tableau_a: bra terms
    :param tableau_b: ket terms
    :return: list of remaining overlap integrals
    """
    if tableau_a.permutation_group != tableau_b.permutation_group:
        raise Exception("function_combination error: The tableaus dont fit.")

    info = {"bra": tableau_a.function.to_tex(), "ket": tableau_b.function.to_tex(), "kind": kind}
    empty_function = FunctionDependency(ProductTerm(Sign("+"), ()), normalizable=False)

    # check if identical form
    if tableau_a.number_of_rows != tableau_b.number_of_rows or tableau_a.numbers_in_columns != tableau_b.numbers_in_columns:
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
    if kind == SpinVsSpatialKind.SPIN:
        # multiple results
        for sp in range(len(tableau_a.spin_parts)):
           spin_choice = tableau_a.spin_parts[sp]
           for sp2 in range(sp, len(tableau_b.spin_parts)):
               spin_choice_2 = tableau_b.spin_parts[sp2]
               g = calculate_overlap_integral_between_functions(spin_choice.function,
                                                                     spin_choice_2.function)
               info["bra"] = spin_choice.get_shortend_form(kind=TextKinds.TEX)
               info["ket"] = spin_choice_2.get_shortend_form(kind=TextKinds.TEX)
               info["result"] = g
               results.append(info)
    else:
        if kind == SpinVsSpatialKind.GENERAL:
            g = calculate_overlap_integral_basisfunction(tableau_a, tableau_b)
            info["bra"] = tableau_a.function.to_tex()
            info["ket"] = tableau_b.function.to_tex()
        elif kind == SpinVsSpatialKind.SPATIAL:
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
        else:
            raise Exception("not implemented!")

        info["result"] = g
        results.append(info)
    return results



from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.ProductTerm import ProductTerm
from source.function_parts.Sign import Sign
from source.StandardTableau import StandardTableau


def calculate_overlap_integral_basisfunction(tableau_a: StandardTableau, tableau_b: StandardTableau) -> FunctionDependency:
    """
    calculating the overlap between the basis function = general behavior, not spin/spatial integrals
    :param tableau_a: bra terms
    :param tableau_b: ket terms
    :return: overlap
    """
    if tableau_a.permutation_group != tableau_b.permutation_group:
        raise Exception("function_combination error: The tableaus dont fit.")

    empty_function = FunctionDependency(ProductTerm(Sign("+"), ()), normalizable=False)
    # check if identical form
    if tableau_a.number_of_rows != tableau_b.number_of_rows or tableau_a.numbers_in_columns != tableau_b.numbers_in_columns:
        # basis function of young tableaux from different young diagrams are automatically diagonal
        empty_function.parts[0].factor = 0
        empty_function.parts = [empty_function.parts[0]]

    # test if same standard tableau:
    elif tableau_a.numbers_in_row == tableau_b.numbers_in_row:
        empty_function.parts[0].factor = 1
        empty_function.parts[0].ordered_functions = ()
        empty_function.parts = [empty_function.parts[0]]

    else:
        empty_function = calculate_overlap_integral_between_functions(function_a=tableau_a.function, function_b=tableau_b.function)
    return empty_function

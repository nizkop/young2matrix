from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from source.standard_tableau import standard_tableau


def calculate_overlap_integral_basisfunction(tableau_a: standard_tableau, tableau_b: standard_tableau) -> function:
    if tableau_a.permutation_group != tableau_b.permutation_group:
        raise Exception("function_combination error: The tableaus dont fit.")

    info = {"bra": tableau_a.function.to_tex(), "ket": tableau_b.function.to_tex()}
    empty_function = function(product_term(Sign("+"), ()) ,normalizable=False)
    # check if identical form
    if tableau_a.number_of_rows != tableau_b.number_of_rows or tableau_a.number_of_columns != tableau_b.number_of_columns:
        # basis function of young tableaux from different young diagrams are automatically diagonal
        empty_function.parts[0].factor = 0
        empty_function.parts = [empty_function.parts[0]]
    # same young diagram (form):

    # test if same standard tableau:
    elif tableau_a.numbers_in_row == tableau_b.numbers_in_row:
        empty_function.parts[0].factor = 1
        empty_function.parts[0].ordered_functions = ()
        empty_function.parts = [empty_function.parts[0]]

    else:
        empty_function = calculate_overlap_integral_between_functions(function_a=tableau_a.function, function_b=tableau_b.function)
    return empty_function
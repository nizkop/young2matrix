
import sympy as sp

from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.get_normalization_factor_as_fraction import get_normalization_factor_as_fraction
from source.function_parts.ProductTerm import ProductTerm
from source.function_parts.Sign import Sign


def calculate_overlap_integral_between_functions(function_a:FunctionDependency, function_b:FunctionDependency) -> FunctionDependency:
    """
    calculating overlap between all parts of a function a and a function b
    :param function_a: bra terms
    :param function_b: ket terms
    :return: overlap
    """
    empty_function = FunctionDependency(ProductTerm(Sign("+"), ()), normalizable=False)

    if function_a == function_b:
        empty_function.parts[0].factor = 1
        empty_function.parts[0].ordered_functions = ()
        empty_function.parts = [empty_function.parts[0]]
    else:
        factor_of_non_cancelled_terms = 0
        norm = sp.sqrt(function_a.get_normalization_factor()["1/sqrt"]) * sp.sqrt \
            (function_b.get_normalization_factor()["1/sqrt"])
        total_eq = ""
        left_eq = ""
        no_of_terms = 0
        for i in function_a.parts:
            for j in function_b.parts:
                no_of_terms += 1
                p, eq_braket = i.integrational_multiply(j)
                total_eq +=" +  "+ eq_braket
                if p.factor != 0:
                    left_eq += p.to_text()
                if p.sign == Sign.PLUS:
                    factor_of_non_cancelled_terms += abs(p.factor)
                else:
                    factor_of_non_cancelled_terms -= abs(p.factor)
        empty_function.parts[0].factor = get_normalization_factor_as_fraction(factor_of_non_cancelled_terms, norm)
    if empty_function.parts[0].factor < 0:
        empty_function.parts[0].sign = Sign.MINUS
        empty_function.parts[0].factor = abs( empty_function.parts[0].factor )
    return empty_function



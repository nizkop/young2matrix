
from fractions import Fraction
import sympy as sp

from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign



def calculate_overlap_integral_between_functions(function_a:function, function_b:function) -> function:
    empty_function = function(product_term(Sign("+"), ()) ,normalizable=False)

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
                # if p.factor != 0:
                #     empty_function.parts.append(p)
        try:
            empty_function.parts[0].factor = Fraction(factor_of_non_cancelled_terms, norm)
        except:
            # only exception where factor is not an int (because of the square root)
            empty_function.parts[0].factor = sp.sqrt \
                (Fraction(factor_of_non_cancelled_terms * factor_of_non_cancelled_terms, norm *norm))
        # print(total_eq, "\n\n= ", left_eq, "\nnumber of terms:", no_of_terms, "\n")
    if empty_function.parts[0].factor < 0:
        empty_function.parts[0].sign = Sign.MINUS
        empty_function.parts[0].factor = abs( empty_function.parts[0].factor )
    # empty_function.print()
    return empty_function


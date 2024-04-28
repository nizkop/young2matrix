import copy

from source.function_parts.function import function
from source.function_parts.hamilton_integral import hamilton_integral
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign


def calculate_overlap_integral_between_functions(function_a:function, function_b:function) -> function:
    empty_function = function(product_term(Sign("+"), ()) ,normalizable=False)

    if function_a == function_b:
        return []
    else:
        # todo norm!? , sign , factor
        non_vanishing_integrals = []
        for i in function_a.parts:
            for j in function_b.parts:
                h = hamilton_integral(copy.deepcopy(i), copy.deepcopy(j))
                non_vanishing_integrals.append(h)

                # sp_functions_a = i.get_list_of_parts()
                # sp_functions_b = j.get_list_of_parts()
                #
                # for func in sp_functions_a+sp_functions_b:
                #     if not (func in sp_functions_a and func in sp_functions_b):
                #         count += 1
                # # TODO: Anzahl vertauschungen dürfen nicht mehr als 2 sein, count schon!
                # if count <= 2: # todo, was wenn count = 1
                #     bra.append(i)
                #     ket.append(j)
                #     factor = i.factor * j.factor

    return [result for result in non_vanishing_integrals if result.factor != 0]
    # return empty_function_bra, empty_function_ket



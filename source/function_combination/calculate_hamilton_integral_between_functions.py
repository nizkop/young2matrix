import copy
from typing import List

from source.function_parts.function import function
from source.function_parts.hamilton_integral import hamilton_integral


def calculate_hamilton_integral_between_functions(function_a:function, function_b:function) -> List[hamilton_integral]:
    if function_a == function_b:
        return []
    else:
        # todo norm!? , sign , factor
        non_vanishing_integrals = []
        for i in function_a.parts:
            for j in function_b.parts:
                h = hamilton_integral(copy.deepcopy(i), copy.deepcopy(j))
                non_vanishing_integrals.append(h)

    return [result for result in non_vanishing_integrals if result.factor != 0]



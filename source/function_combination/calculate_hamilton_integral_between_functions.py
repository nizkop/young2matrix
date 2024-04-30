import copy
from typing import List

from source.function_parts.function import function
from source.function_parts.hamilton_integral import hamilton_integral


def calculate_hamilton_integral_between_functions(function_a:function, function_b:function) -> List[hamilton_integral]:
    non_vanishing_integrals = []
    if function_a == function_b:
        h = calculate_hamilton_integral_between_functions(function_a,function_b)

        # for part in range(len(function_a.parts)):
        #     h = hamilton_integral(copy.deepcopy(function_a.parts[part]), copy.deepcopy(function_b.parts[part]))
        non_vanishing_integrals.append(h)
    else:
        # todo norm!? , sign , factor
        for i in function_a.parts:
            for j in function_b.parts:
                h = hamilton_integral(copy.deepcopy(i), copy.deepcopy(j))
                non_vanishing_integrals.append(h)

    return [result for result in non_vanishing_integrals if result.factor != 0]



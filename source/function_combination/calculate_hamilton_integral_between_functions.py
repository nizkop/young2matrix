import copy
from typing import List

from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.hamilton_integral import hamilton_integral


def calculate_hamilton_integral_between_functions(function_a:function, function_b:function) -> List[hamilton_integral]:
    non_vanishing_integrals = []
    if function_a == function_b:
        h = calculate_overlap_integral_between_functions(function_a,function_b)
        non_vanishing_integrals.append(h)
    else:
        for i in function_a.parts:
            for j in function_b.parts:
                h = hamilton_integral(copy.deepcopy(i), copy.deepcopy(j))
                non_vanishing_integrals.append(h)

    return non_vanishing_integrals # [result for result in non_vanishing_integrals if result.factor != 0]



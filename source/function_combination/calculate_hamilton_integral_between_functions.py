import copy
from typing import List

from source.function_parts.function import function
from source.function_parts.hamilton_integral import hamilton_integral


def calculate_hamilton_integral_between_functions(function_a:function, function_b:function) -> List[hamilton_integral]:
        non_vanishing_integrals = []
        for i in range(len(function_a.parts)):
            part_a = function_a.parts[i]
            for j in range(0, len(function_b.parts)):
                part_b = function_b.parts[j]
                h = hamilton_integral(copy.deepcopy(part_a), copy.deepcopy(part_b))
                non_vanishing_integrals.append(h)

        return [result for result in non_vanishing_integrals if result.factor != 0]



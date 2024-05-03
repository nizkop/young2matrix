import copy
from typing import List

from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.hamilton_integral import hamilton_integral


def calculate_hamilton_integral_between_functions(function_a:function, function_b:function) -> List[hamilton_integral]:
        non_vanishing_integrals = []
        for i in range(len(function_a.parts)):
            part_a = function_a.parts[i]
            for j in range(i, len(function_b.parts)):
                part_b = function_b.parts[j]
                h = hamilton_integral(copy.deepcopy(part_a), copy.deepcopy(part_b))
                non_vanishing_integrals.append(h)

        # print("calculate_hamilton_integral_between_functions", len(non_vanishing_integrals), "->", len([result for result in non_vanishing_integrals if result.factor != 0]),
        #       "mit:", len([h for h in non_vanishing_integrals if "".join(sorted(h.get_shortened_symbol())) == "abcd"]))
        return [result for result in non_vanishing_integrals if result.factor != 0]



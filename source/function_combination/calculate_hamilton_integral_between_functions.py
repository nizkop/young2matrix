import copy
from typing import List

from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.HamiltonIntegral import HamiltonIntegral


def calculate_hamilton_integral_between_functions(function_a:FunctionDependency, function_b:FunctionDependency) -> List[HamiltonIntegral]:
        """
        calculating the hamilton integral between two (spatial) functions
        :param function_a: bra terms
        :param function_b: ket terms
        :return: list of non-vanishing hamilton integrals (without regard to identical values/integrals, that may cancel each other)
        """
        non_vanishing_integrals = []
        for i in range(len(function_a.parts)):
            part_a = function_a.parts[i]
            for j in range(0, len(function_b.parts)):
                part_b = function_b.parts[j]
                h = HamiltonIntegral(copy.deepcopy(part_a), copy.deepcopy(part_b))
                non_vanishing_integrals.append(h)

        return [result for result in non_vanishing_integrals if result.factor != 0]



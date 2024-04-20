from fractions import Fraction

from source.function_combination import function_combination
from source.standard_tableau import standard_tableau



trials = [
    {"input1": [(1, 2,), (3, 4,)], "input2": [(1, 2,), (3, 4,)], "expected": 1, "error_message": "S4 [2^2] overlap itself"},
    {"input1": [(1, 2, ), (3, 4,)], "input2": [(1, 3,), (2, 4,)],  "expected": -Fraction(1,4), "error_message": "S4 [2^2]"  },
    # {"input1": [(1, 3,), (2, 4,)], "input2": [(1, 2,), (3, 4,)], "expected": -Fraction(1,4), "error_message": "S4 [2^2]"},
    {"input1": [(1, 2,), (3, 4,)], "input2": [(1, 2, 3), (4,)], "expected": 0, "error_message": "S4 [2^2] vs. [3 1]"},

    {"input1": [(1, 4,), (2,), (3,)], "input2": [(1, 3,), (2,), (4,)], "expected": Fraction(-1,6), "error_message": "S4 [21^2] "},
    # {"input": , "expected": [], "error_message": ""},
]



general_error = "error in overlap calculation"
for trial in trials:
    t1 = standard_tableau(trial["input1"])
    t1.set_up_function()
    t2 = standard_tableau(trial["input2"])
    t2.set_up_function()

    f = function_combination(t1, t2)
    product = f.calculate_overlap_integral()
    if len(product.parts) != 1:
        raise Exception(f"{general_error} - {trial['error_message']}: wrong number of output terms")
    f_reverse = function_combination(t2, t1)
    product_revers = f_reverse.calculate_overlap_integral()
    if product.parts[0].factor != product_revers.parts[0].factor or len(product.parts[0].ordered_functions) != 0 or len(product_revers.parts[0].ordered_functions) != 0:
        raise Exception(f"{general_error} - {trial['error_message']}: multiplication not commutative")
    if product.parts[0].factor != trial["expected"]:
        wrong = trial["expected"] / product.parts[0].factor
        print(trial['error_message'], "wrong by: ", wrong)
        # raise Exception(f"{general_error} - {trial['error_message']}: {product.parts[0].factor} vs. {trial['expected']}")


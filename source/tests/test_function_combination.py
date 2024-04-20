from fractions import Fraction

from source.function_combination import function_combination
from source.standard_tableau import standard_tableau


###  spatial tableaus  ###

trials = [
    {"input1": [(1, 2,), (3, 4,)], "input2": [(1, 2,), (3, 4,)], "expected": 1, "error_message": "S4 [2^2] overlap itself"},
    {"input1": [(1, 2, ), (3, 4,)], "input2": [(1, 3,), (2, 4,)], "expected": -Fraction(1,4), "error_message": "S4 [2^2]"  },
    {"input1": [(1, 2,), (3, 4,)], "input2": [(1, 2, 3), (4,)], "expected": 0, "error_message": "S4 [2^2] vs. [3 1]"},

    {"input1": [(1, 4,), (2,), (3,)], "input2": [(1, 3,), (2,), (4,)], "expected": Fraction(-1,6), "error_message": "S4 [21^2] "},
    {"input1": [(1, 4,), (2,), (3,)], "input2": [(1, 2,), (3,), (4,)], "expected": Fraction(-1, 6), "error_message": "S4 [21^2] "},
    {"input1": [(1, 3,), (2,), (4,)], "input2": [(1, 2,), (3,), (4,)], "expected": Fraction(-1, 6), "error_message": "S4 [21^2] "},
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
        raise Exception(f"{general_error} - {trial['error_message']}: {product.parts[0].factor} vs. {trial['expected']}")




###  spin tableaus  ###

trials = [
    # combination of tableaus each having only one choice of m_s:
    {"tableau1": [(1, 2,), (3, 4,)], "spin1": ["α", "α", "β", "β"],
     "tableau2": [(1, 3,), (2, 4,)], "spin2": ["α", "β", "α", "β"],
     "expected": Fraction(1,2), "error_message": "S4 [2^2]"},

    # different combinations between 2 standard tableaus of the same young tableau:
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "α", "α", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "α", "β"],
     "expected": 0, "error_message": "S4 [2^2] different m_s"},
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "α", "β", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "α", "β"],
     "expected": Fraction(1,2), "error_message": "S4 [2^2] same m_s"},
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "β", "β", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "α", "β"],
     "expected": 0, "error_message": "S4 [2^2]"},

    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "α", "α", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "α", "α"],
     "expected": Fraction(1, 2), "error_message": "S4 [2^2] different m_s"},
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "α", "β", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "α", "α"],
     "expected": 0, "error_message": "S4 [2^2] same m_s"},
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "β", "β", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "α", "α"],
     "expected": 0, "error_message": "S4 [2^2]"},

    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "α", "α", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "β", "β"],
     "expected": 0, "error_message": "S4 [2^2] different m_s"},
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "α", "β", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "β", "β"],
     "expected": 0, "error_message": "S4 [2^2] same m_s"},
    {"tableau1": [(1, 2, 3,), (4,)], "spin1": ["α", "β", "β", "β"],
     "tableau2": [(1, 3, 4,), (2,)], "spin2": ["α", "β", "β", "β"],
     "expected": Fraction(1, 2), "error_message": "S4 [2^2]"},

]

general_error = "error in spin overlap"
for trial in trials:
    # set up (with spins):
    t1 = standard_tableau(trial["tableau1"])
    t1.set_up_function()
    t1.function.set_spin_functions(trial["spin1"])

    t2 = standard_tableau(trial["tableau2"])
    t2.set_up_function()
    t2.function.set_spin_functions(trial["spin2"])


    # calculating overlap:
    f = function_combination(t1, t2)
    product = f.calculate_overlap_integral()
    if len(product.parts) != 1:
        raise Exception(f"{general_error} - {trial['error_message']}: wrong number of output terms")
    if product.parts[0].factor != trial["expected"] and round(trial["expected"]/product.parts[0].factor, 4) != 1:
        wrong = trial["expected"] / product.parts[0].factor
        # t1.function.print(), t2.function.print()
        # print(trial['error_message'], product.parts[0].factor , "instead of", trial["expected"], "-> wrong by: ", wrong)
        raise Exception(f"{general_error} - {trial['error_message']}: {product.parts[0].factor} vs. {trial['expected']}")
    f_reverse = function_combination(t2, t1)
    product_revers = f_reverse.calculate_overlap_integral()
    if product.parts[0].factor != product_revers.parts[0].factor or len(product.parts[0].ordered_functions) != 0 or len(
            product_revers.parts[0].ordered_functions) != 0:
        raise Exception(f"{general_error} - {trial['error_message']}: multiplication not commutative")



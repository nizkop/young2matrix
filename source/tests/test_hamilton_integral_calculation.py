from source.chemical_standard_tableau import chemical_standard_tableau
from source.function_combination.calculate_hamilton_integral import calculate_hamilton_integral
from source.function_combination.calculate_hamilton_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind



### hamilton with functions ###
trials = [
    {"input1": (1,2,), "input2": (1,2,), "expected_bra": [], "expected_ket": []},
    {"input1": (2,1), "input2": (1, 2,), "expected_bra": ["a2", "b1"], "expected_ket": ["a1", "b2"]},
    {"input1": (1,2,3), "input2": (3,2,1), "expected_bra": ["a1", "c3"], "expected_ket": ["c1", "a3"]},# proposal example

]


general_error = "testing single product integration including hamilton operator"
for trial in trials:


    f1 = function(product_term(Sign("+"), trial["input1"]))
    f2 = function(product_term(Sign("+"), trial["input2"]))

    f1.print(), f2.print()

    results = calculate_overlap_integral_between_functions(f1, f2)

    if len(results) != 1:
        raise Exception("thie test is only able to test one product")

    for r in results:
        print(r.to_text())
        calculated_bra = r.bra.get_list_of_parts()
        calculated_ket = r.ket.get_list_of_parts()

        if len(calculated_bra) != len(trial["expected_bra"]) or len(calculated_ket) != len(trial["expected_ket"]):
            raise Exception(f"{general_error}: dimensions dont fit")

        for b in calculated_bra:
            b = b.replace("{","").replace("}","").replace("_","")
            if b not in trial["expected_bra"]:
                raise Exception(f"{general_error}: wrong bra function ({b})")
        for k in calculated_ket:
            k = k.replace("{","").replace("}","").replace("_","")
            if k not in trial["expected_ket"]:
                raise Exception(f"{general_error}: wrong ket function ({k})")




















###  whole tableaus   ###

# trials = [
#     # {"input1": [(1, 2,), (3, 4,)], "input2": [(1, 2,), (3, 4,)], "expected": 1, "error_message": "S4 [2^2] overlap itself"},
#     {"input1": [(1, 2,), (3, )], "input2": [(1, 3,), (2,)], "expected": None, "error_message": "S4 [2^2]"  },
#
# ]
#
#
# general_error = "error in overlap calculation (tableaus)"
# for trial in trials:
#     t1 = chemical_standard_tableau(trial["input1"])
#     t1.set_up_function()
#     t1.get_spatial_choices()
#     t2 = chemical_standard_tableau(numbers_in_row=trial["input2"])
#     t2.set_up_function()
#     t2.get_spatial_choices()
#
#     t1.print(), t2.print()
#
#     t1.function.print(), t2.function.print()
#
#     product = calculate_hamilton_integral(t1, t2, kind=spin_vs_spatial_kind.SPATIAL)[0]["result"]
#
#
#     print(product)
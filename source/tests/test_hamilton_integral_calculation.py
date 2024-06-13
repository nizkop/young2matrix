from source.ChemicalStandardTableau import ChemicalStandardTableau
from source.function_combination.calculate_hamilton_integral import calculate_hamilton_integral
from source.function_combination.calculate_hamilton_integral_between_functions import \
    calculate_hamilton_integral_between_functions
from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.ProductTerm import ProductTerm
from source.function_parts.Sign import Sign
from source.function_parts.SpinVsSpatialKind import SpinVsSpatialKind



###   test functions of hamilton integrals   ###
trials = [
    {"input1": (1,2,), "input2": (1,2,), "expected_bra": ["a1", "b2"], "expected_ket": ["a1", "b2"]},
    {"input1": (2,1), "input2": (1, 2,), "expected_bra": ["a2", "b1"], "expected_ket": ["a1", "b2"]},
    {"input1": (1,2,3), "input2": (3,2,1), "expected_bra": ["a1", "c3"], "expected_ket": ["c1", "a3"]},# proposal example
    {"input1": (1, 2, 3), "input2": (1, 2, 3), "expected_bra": ["a1", "b2", "c3"], "expected_ket": ["a1", "b2", "c3"]},
]

general_error = "testing single product integration including hamilton operator"
for trial in trials:
    f1 = FunctionDependency(ProductTerm(Sign("+"), trial["input1"]))
    f2 = FunctionDependency(ProductTerm(Sign("+"), trial["input2"]))
    results = calculate_hamilton_integral_between_functions(f1, f2)

    assert len(results) == 1, "this test is only able to test one product"

    for r in results:
        calculated_bra = r.bra.get_list_of_parts()
        calculated_ket = r.ket.get_list_of_parts()

        assert len(calculated_bra) == len(trial["expected_bra"]) and len(calculated_ket) == len(trial["expected_ket"]), \
            f"{general_error}: dimensions dont fit"

        for b in calculated_bra:
            b = b.replace("{","").replace("}","").replace("_","")
            assert b in trial["expected_bra"], f"{general_error}: wrong bra function ({b})"
        for k in calculated_ket:
            k = k.replace("{","").replace("}","").replace("_","")
            assert k in trial["expected_ket"], f"{general_error}: wrong ket function ({k})"



###  test whole tableaus   ###

trials = [
    {"input1": [(1,),(2,),(3,),(4,)], "input2": [(1,),(2,), (3,),(4,)], "error_message": "1^4 sym",
        "expected": ["+ 1 (abcd)", "- 1/2 (ab)", "- 1/2 (ac)", "- 1/2 (ad)", "- 1/2(bc)", "- 1/2 (bd)", "- 1/2 (cd)"]},
        # <- difference from prior (manual) calculation (= no -- combinations, all integrals added)

    {"input1": [(1,4,),(2,),(3,)], "input2": [(1,4,),(2,),(3,)], "error_message": "[31] symmetric 14",
        "expected": ["+ 1 (abcd)", "- 1/2 (ab)", "- 1/2 (ac)", "+ 1 (ad)", "- 1 (bc)", "- 1/2 (bd)", "- 1/2 (cd)"]},
    {"input1": [(1,3,),(2,),(4,)], "input2": [(1,3,),(2,),(4,)], "error_message": "[31] symmetric 13",
        "expected": ["+ 1 (abcd)", "- 1/2 (ab)", "+ 1 (ac)", "- 1/2 (ad)", "- 1/2 (bc)", "- 1 (bd)", "- 1/2 (cd)"]},
    {"input1": [(1,2,),(3,),(4,)], "input2": [(1,2,),(3,),(4,)], "error_message": "[31] symmetric 12",
        "expected": ["+ 1 (abcd)", "+ 1 (ab)", "- 1/2 (ac)", "- 1/2 (ad)", "- 1/2 (bc)", "- 1/2 (bd)", "- 1 (cd)"]},

    {"input1": [(1,4,),(2,),(3,)], "input2": [(1,3,),(2,),(4,)],"error_message": "[31] 14-13",
        "expected": ["- 1/6 (abcd)", "- 1/6 (ac)", "- 1/6 (ad)", "+ 1/6 (bc)", "+ 1/6 (bd)", "+ 1/3 (cd)"]},
    {"input1": [(1,4,),(2,),(3,)], "input2": [(1,2,),(3,),(4,)], "error_message": "[31] 14-12",
        "expected": ["- 1/6 (abcd)", "- 1/6 (ab)", "- 1/6 (ad)", "+ 1/6 (bc)", "+ 1/3 (bd)", "+ 1/6 (cd)"]},
    {"input1": [(1,3,),(2,),(4,)], "input2": [(1,2),(3,),(4,)], "error_message": "[31] 13-12",
        "expected": ["- 1/6 (abcd)", "- 1/6 (ab)", "- 1/6 (ac)", "+ 1/3 (bc)", "+ 1/6 (bd)", "+ 1/6 (cd)"]},

    {"input1": [(1, 3), (2, 4)], "input2": [(1, 2), (3, 4)],
        "expected": ["- 1/4 (abcd)", "- 1/4 (ab)", "- 1/4 (ac)", "+ 1/2 (ad)", "+ 1/2 (bc)", "- 1/4 (bd)", "- 1/4 (cd)"],
        "error_message": "2^2 combination"},
    {"input1": [(1, 2), (3, 4)], "input2": [(1, 2), (3, 4)],
        "expected": ["+ 1 (abcd)", "+ 1 (ab)", "- 1/2 (ac)", "- 1/2 (ad)", "- 1/2 (bc)", "- 1/2 (bd)", "+ 1 (cd)"],
        "error_message": "2^2 one tableau"},
    {"input1": [(1, 3), (2, 4)], "input2": [(1, 3), (2, 4)],
        "expected": ["+ 1 (abcd)", "- 1/2 (ab)", "+ 1 (ac)", "- 1/2 (ad)", "- 1/2 (bc)", "+ 1 (bd)", "- 1/2 (cd)"],
        "error_message": "2^2 one tableau"}
]

general_error = "error in hamilton integral calculation (tableaus)"
for trial in trials:
    t1 = ChemicalStandardTableau(trial["input1"])
    t1.set_up_function()
    t1.get_spatial_choices()
    t2 = ChemicalStandardTableau(numbers_in_row=trial["input2"])
    t2.set_up_function()
    t2.get_spatial_choices()

    product = calculate_hamilton_integral(t1, t2, kind=SpinVsSpatialKind.SPATIAL)

    assert len(product) == len(trial["expected"]), \
        f"{general_error}: unfitting number of terms for {trial['error_message']}"

    for x in product:
        checked = False
        for y in trial["expected"]:
            if "("+''.join(sorted(x.get_shortened_symbol()))+")" in y:
                assert f"{x.sign.value} {x.factor}" in y, \
                    f"{general_error} - wrong factor: {x.sign.value} {x.factor} vs. {y} for {trial['error_message']}"
                checked = True
                break
        unexpected = f"{x.sign.value} {x.factor} ({''.join(sorted(x.get_shortened_symbol()))})"#not used/useful in case of successfull test
        assert checked, f"{general_error}: {unexpected} not expected for {trial['error_message']}"

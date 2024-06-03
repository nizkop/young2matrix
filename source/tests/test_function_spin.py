from source.function_parts.sign import Sign
from source.standard_tableau import standard_tableau

general_error = "error in build spin functions"

trials = [
    # weissbluth examples:
    {"input": [(1,2,3)], "spin_input": ["α", "α", "α"], "expected_sqrt": 1,
            "expected": [{"value": ['α1', 'α2', 'α3'], "sign": Sign.PLUS}], "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1,2,3)], "spin_input": ["α", "α", "β"], "expected_sqrt": 3,
            "expected": [{"value": ['α1', 'α2', 'β3'], "sign": Sign.PLUS}, {"value": ['α3', 'α2', 'β1'], "sign": Sign.PLUS}, {"value": ['α1', 'α3', 'β2'], "sign": Sign.PLUS}],
            "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1, 2, 3)], "spin_input": ["β", "β", "α"], "expected_sqrt": 3,
            "expected": [{"value": ['β1', 'β2', 'α3'], "sign": Sign.PLUS}, {"value": ['α1', 'β2', 'β3'], "sign": Sign.PLUS}, {"value": ['β1', 'α2', 'β3'], "sign": Sign.PLUS}],
            "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1, 2, 3)], "spin_input": ["β", "β", "β"],
     "expected": [{"value": ['β1', 'β2', 'β3'], "sign": Sign.PLUS}],
            "expected_sqrt": 1, "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1,2),(3,)], "spin_input": ["α", "β", "β"],"expected_sqrt": 2,
            "expected": [{"value": ['α1', 'β2', 'β3'], "sign": Sign.PLUS}, {"value": ['α3', 'β2', 'β1'], "sign": Sign.MINUS}], "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1, 2), (3,)], "spin_input": ["α", "α", "β"], "expected_sqrt": 2,
            "expected": [{"value": ['α1', 'α2', 'β3'], "sign": Sign.PLUS}, {"value": ['α3', 'α2', 'β1'], "sign": Sign.MINUS}],
            "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1,3),(2,)], "spin_input": ["α", "β", "α"], "expected_sqrt": 2,
            "expected": [{"value": ['α1', 'β2', 'α3'], "sign": Sign.PLUS}, {"value": ['β1','α2','α3'], "sign": Sign.MINUS}],
            "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1, 3), (2,)], "spin_input": ["α", "β", "β"],
     "expected": [{"value": ['α1', 'β2', 'β3'], "sign": Sign.PLUS},{"value":  ['β1', 'α2', 'β3'], "sign": Sign.MINUS}],
     "expected_sqrt": 2, "error_message": "anti- & symmetrizing wrong"},


    # own manual calculations:
    {"input": [(1, 2), (3,4)], "spin_input": ["α", "α", "β", "β"], "expected_sqrt": 4,
     "expected": [{"value": ['α1', 'α2', 'β3', 'β4'], "sign": Sign.PLUS},
                  {"value": ['β1', 'α2', 'α3', 'β4'], "sign": Sign.MINUS},
                  {"value": ['α1', 'β2', 'β3', 'α4'], "sign": Sign.MINUS},
                  {"value": ['β1', 'β2', 'α3', 'α4'], "sign": Sign.PLUS},
                  ],
     "error_message": "S4 [2^2] anti- & symmetrizing wrong"},
    {"input": [(1, 3), (2, 4)], "spin_input": ["α","β", "α", "β"], "expected_sqrt": 4,
     "expected": [{"value": ['α1', 'β2', 'α3', 'β4'], "sign": Sign.PLUS},
                  {"value": ['β1', 'α2', 'α3', 'β4'], "sign": Sign.MINUS},
                  {"value": ['α1', 'β2', 'β3', 'α4'], "sign": Sign.MINUS},
                  {"value": ['β1', 'α2', 'β3', 'α4'], "sign": Sign.PLUS},
                  ],
     "error_message": "S4 [2^2] anti- & symmetrizing wrong"},
    # {"input": [], "spin_input": ["α", "β", "β"], "expected": "+ ", "error_message": ""},
]



for i in trials:
    s = standard_tableau(i["input"])
    s.set_up_function()
    s.function.set_spin_functions(i["spin_input"])

    expected = ["".join(sorted(x)) for x in [y["value"] for y in i["expected"]]]

    calculated_part = ""
    for calculated in s.function.parts:
        calculated_part = "".join(sorted(calculated.get_list_of_parts())).replace("{","").replace("}","").replace("_","")
        try:
            index = expected.index(calculated_part)
            if i["expected"][index]["sign"] != calculated.sign:
                raise Exception("wrong sign")
        except ValueError: #... not in list
             raise Exception(general_error + " - " + i["error_message"] + ": " + str(calculated_part) + " to much (unexpected result)")

    if len(expected) != len(s.function.parts):
        raise Exception(general_error+" - "+i["error_message"]+": "+ str(calculated_part) + " missing")

    # comparison of the square roots (underneath the fraction bar):
    if s.function.get_normalization_factor()["1/sqrt"] != i["expected_sqrt"]:
        raise Exception(f"{general_error}: wrong normalization factor for \"{i['error_message']}\"")




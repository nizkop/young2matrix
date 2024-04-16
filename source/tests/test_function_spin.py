from source.standard_tableau import standard_tableau

general_error = "error in build spin functions"

trials = [
    {"input": [(1,2,3)], "spin_input": ["α", "α", "α"],
            "expected": [['α1', 'α2', 'α3']], "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1,2,3)], "spin_input": ["α", "α", "β"],
            "expected": [['α1', 'α2', 'β3'], ['α3', 'α2', 'β1'],['α1', 'α3', 'β2']],
            "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1, 2, 3)], "spin_input": ["β", "β", "α"],
            "expected": [['β1', 'β2', 'α3'], ['α1', 'β2', 'β3'], ['β1', 'α2', 'β3']],
            "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1, 2, 3)], "spin_input": ["β", "β", "β"], "expected": [['β1', 'β2', 'β3']],
            "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1,2),(3,)], "spin_input": ["α", "β", "β"],
            "expected": [['α1', 'β2', 'β3'], ['α3', 'β2', 'β1']], "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1, 2), (3,)], "spin_input": ["α", "α", "β"], "expected": [['α1', 'α2', 'β3'], ['α3', 'α2', 'β1']],
            "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1,3),(2,)],  "spin_input": ["α", "β", "α"],
            "expected": [['α1', 'β2', 'α3'], ['β1','α2','α3']], "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1, 3), (2,)], "spin_input": ["α", "β", "β"], "expected": [['α1', 'β2', 'β3'], ['β1', 'α2', 'β3']],
     "error_message": "anti- & symmetrizing wrong"},
    # {"input": [], "spin_input": ["α", "β", "β"], "expected": "+ ", "error_message": ""},
]



for i in trials:
    expected = i["expected"]
    s = standard_tableau(i["input"])
    s.set_up_function()

    for part in s.function.parts:
        part.lowercase_letters = i["spin_input"]
    s.function.aggregate_terms()

    expected = ["".join(sorted(x)) for x in i["expected"]]
    calculated = ["".join(sorted(x.get_list_of_parts())) for x in s.function.parts]

    for calculated_part in calculated:
        if calculated_part not in expected:
            raise Exception(general_error+" - "+i["error_message"]+": "+ str(calculated_part) + " missing")
    for expected_part in expected:
        if expected_part not in calculated:
            raise Exception(general_error + " - "+ i["error_message"]+": "+ str(expected_part)+ " to much")


